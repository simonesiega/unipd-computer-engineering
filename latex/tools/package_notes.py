#!/usr/bin/env python3
"""Package compiled course PDFs and deterministic release metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from create_course import kebab_case as slugify

YEARS = ("1", "2", "3")
COURSE_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SOURCE_COMMIT = re.compile(r"^[0-9a-fA-F]{40}$")
DEFAULT_TITLE = "Latest compiled notes"
RELEASE_DIRECTORY = Path(".build/release")
MANIFEST_NAME = "manifest.json"
CHECKSUMS_NAME = "SHA256SUMS.txt"
RELEASE_NOTES_NAME = "RELEASE_NOTES.md"


@dataclass(frozen=True)
class CourseBuild:
    """A canonical course and its compiled PDF before release staging."""

    degree_year: int
    course_name: str
    course_slug: str
    source_directory: str
    built_pdf: Path
    asset_filename: str


@dataclass(frozen=True)
class CourseAsset:
    """Metadata for one packaged course PDF."""

    degree_year: int
    course_name: str
    course_slug: str
    source_directory: str
    asset_filename: str
    file_size: int
    sha256: str
    source_commit: str
    release_timestamp: str


def repository_root() -> Path:
    """Return the repository root."""
    return Path(__file__).resolve().parents[2]


def asset_filename(degree_year: int, course_slug: str) -> str:
    """Return the deterministic release filename for a course."""
    if str(degree_year) not in YEARS:
        raise ValueError(f"Invalid degree year: {degree_year}")
    if COURSE_SLUG.fullmatch(course_slug) is None:
        raise ValueError(
            f"Invalid course slug {course_slug!r}; expected lowercase kebab-case"
        )
    return f"{degree_year}-{slugify(course_slug)}.pdf"


def sha256_file(path: Path) -> str:
    """Return the hexadecimal SHA-256 digest of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _braced_group(text: str, opening: int) -> tuple[str, int]:
    """Return one balanced braced group and the position after it."""
    if opening >= len(text) or text[opening] != "{":
        raise ValueError("Expected an opening brace")
    depth = 0
    start = opening + 1
    position = start
    while position < len(text):
        escaped = position > 0 and text[position - 1] == "\\"
        if text[position] == "{" and not escaped:
            depth += 1
        elif text[position] == "}" and not escaped:
            if depth == 0:
                return text[start:position], position + 1
            depth -= 1
        position += 1
    raise ValueError("Unclosed metadata group")


def _split_metadata(setup: str) -> dict[str, str]:
    """Parse top-level key-value entries from a unipdsetup group."""
    entries: list[str] = []
    depth = 0
    start = 0
    for position, character in enumerate(setup):
        escaped = position > 0 and setup[position - 1] == "\\"
        if character == "{" and not escaped:
            depth += 1
        elif character == "}" and not escaped:
            depth -= 1
        elif character == "," and depth == 0:
            entries.append(setup[start:position])
            start = position + 1
    entries.append(setup[start:])

    metadata: dict[str, str] = {}
    for entry in entries:
        if "=" not in entry:
            continue
        key, value = entry.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("{"):
            try:
                value, _ = _braced_group(value, 0)
            except ValueError:
                continue
        metadata[key] = value.strip()
    return metadata


def course_metadata(main_file: Path) -> dict[str, str]:
    """Read available canonical course metadata from main.tex."""
    source = main_file.read_text(encoding="utf-8")
    marker = "\\unipdsetup"
    position = source.find(marker)
    if position < 0:
        return {}
    opening = source.find("{", position + len(marker))
    if opening < 0:
        return {}
    try:
        setup, _ = _braced_group(source, opening)
    except ValueError:
        return {}
    return _split_metadata(setup)


def course_identity(root: Path, main_file: Path) -> tuple[int, str, str]:
    """Validate a course source path and return year, slug, and source path."""
    root = root.resolve()
    resolved = main_file.resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError as error:
        raise ValueError(f"Course source escapes the repository: {main_file}") from error
    if (
        len(relative.parts) != 3
        or relative.parts[0] not in YEARS
        or relative.parts[2] != "main.tex"
    ):
        raise ValueError(
            f"Invalid course path {relative.as_posix()}; expected <year>/<course>/main.tex"
        )
    slug = relative.parts[1]
    if COURSE_SLUG.fullmatch(slug) is None:
        raise ValueError(
            f"Invalid course path {relative.as_posix()}; "
            "course names must use lowercase kebab-case"
        )
    return int(relative.parts[0]), slug, relative.parent.as_posix()


def discover_courses(root: Path) -> list[Path]:
    """Discover course entry points and reject invalid nested entry points."""
    courses: list[Path] = []
    for year in YEARS:
        year_directory = root / year
        if not year_directory.exists():
            continue
        for main_file in sorted(
            year_directory.rglob("main.tex"),
            key=lambda path: path.relative_to(root).as_posix(),
        ):
            course_identity(root, main_file)
            courses.append(main_file.resolve())
    return courses


def _course_name(main_file: Path, fallback_slug: str) -> str:
    """Return a readable canonical course name when metadata is available."""
    name = course_metadata(main_file).get("course", "").strip()
    return name or fallback_slug.replace("-", " ").title()


def _manifest(
    assets: list[CourseAsset], source_commit: str, release_timestamp: str
) -> dict[str, object]:
    """Return the machine-readable release manifest."""
    return {
        "schema_version": 1,
        "source_commit": source_commit,
        "release_timestamp": release_timestamp,
        "courses": [asdict(asset) for asset in assets],
    }


def _markdown_cell(value: str) -> str:
    """Escape untrusted metadata for one Markdown table cell."""
    return " ".join(value.replace("|", r"\|").splitlines())


def render_release_notes(
    assets: list[CourseAsset],
    title: str,
    source_commit: str,
    release_timestamp: str,
    description: str = "",
) -> str:
    """Render a stable human-readable index of packaged notes."""
    lines = [f"# {title}", ""]
    if description.strip():
        lines.extend((description.strip(), ""))
    lines.extend(
        (
            f"Source commit: `{source_commit}`",
            "",
            f"Release timestamp: `{release_timestamp}`",
            "",
            "Compiled PDFs are generated distributions of the corresponding "
            "CC BY-SA 4.0 course sources.",
            "",
            "## Available notes",
            "",
        )
    )
    if not assets:
        lines.extend(("_No course PDFs are available in this archive._", ""))
        return "\n".join(lines)

    lines.extend(
        (
            "| Degree year | Course | PDF | SHA-256 |",
            "|---:|---|---|---|",
        )
    )
    for asset in assets:
        lines.append(
            f"| {asset.degree_year} | {_markdown_cell(asset.course_name)} | "
            f"`{asset.asset_filename}` | `{asset.sha256}` |"
        )
    lines.append("")
    return "\n".join(lines)


def _validate_release_metadata(
    source_commit: str, release_timestamp: str, title: str
) -> None:
    """Validate metadata shared by every staged release asset."""
    if SOURCE_COMMIT.fullmatch(source_commit) is None:
        raise ValueError("Source commit must be a 40-character hexadecimal Git SHA")
    if not release_timestamp.strip():
        raise ValueError("Release timestamp must not be empty")
    if not title.strip():
        raise ValueError("Release title must not be empty")


def _prepare_release_directory(root: Path, output_directory: Path) -> Path:
    """Validate, clean, and recreate the tool-owned staging directory."""
    output_directory = Path(os.path.abspath(output_directory))
    expected_output = root / RELEASE_DIRECTORY
    if output_directory != expected_output:
        raise ValueError(
            f"Release output must be {expected_output}; refusing to clean "
            f"{output_directory}"
        )
    if expected_output.parent.is_symlink() or output_directory.is_symlink():
        raise ValueError("Release staging must not be a symbolic link")
    if output_directory.exists():
        shutil.rmtree(output_directory)
    output_directory.mkdir(parents=True)
    return output_directory


def _discover_course_builds(root: Path) -> list[CourseBuild]:
    """Return validated course builds in deterministic release order."""
    builds: list[CourseBuild] = []
    seen_names: dict[str, str] = {}
    missing: list[str] = []
    for main_file in discover_courses(root):
        year, slug, source_directory = course_identity(root, main_file)
        filename = asset_filename(year, slug)
        previous = seen_names.get(filename.casefold())
        if previous is not None:
            raise ValueError(
                f"Duplicate release asset name {filename!r} for "
                f"{previous} and {source_directory}"
            )
        seen_names[filename.casefold()] = source_directory

        built_pdf = root / ".build" / source_directory / "main.pdf"
        if not built_pdf.is_file():
            missing.append(f"{source_directory}: expected {built_pdf.relative_to(root)}")
            continue
        builds.append(
            CourseBuild(
                degree_year=year,
                course_name=_course_name(main_file, slug),
                course_slug=slug,
                source_directory=source_directory,
                built_pdf=built_pdf,
                asset_filename=filename,
            )
        )

    if missing:
        details = "\n  - ".join(missing)
        raise FileNotFoundError(f"Missing compiled course PDFs:\n  - {details}")
    return sorted(
        builds,
        key=lambda build: (
            build.degree_year,
            build.course_name.casefold(),
            build.asset_filename,
        ),
    )


def _stage_course_asset(
    build: CourseBuild,
    output_directory: Path,
    source_commit: str,
    release_timestamp: str,
) -> CourseAsset:
    """Copy one compiled PDF and return its release metadata."""
    destination = output_directory / build.asset_filename
    shutil.copyfile(build.built_pdf, destination)
    return CourseAsset(
        degree_year=build.degree_year,
        course_name=build.course_name,
        course_slug=build.course_slug,
        source_directory=build.source_directory,
        asset_filename=build.asset_filename,
        file_size=destination.stat().st_size,
        sha256=sha256_file(destination),
        source_commit=source_commit,
        release_timestamp=release_timestamp,
    )


def _write_release_metadata(
    output_directory: Path,
    assets: list[CourseAsset],
    source_commit: str,
    release_timestamp: str,
    title: str,
    description: str,
) -> None:
    """Write the manifest and human-readable release index."""
    manifest = json.dumps(
        _manifest(assets, source_commit, release_timestamp),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
    (output_directory / MANIFEST_NAME).write_text(
        manifest + "\n", encoding="utf-8", newline="\n"
    )
    notes = render_release_notes(
        assets, title, source_commit, release_timestamp, description
    )
    (output_directory / RELEASE_NOTES_NAME).write_text(
        notes, encoding="utf-8", newline="\n"
    )


def _write_checksums(output_directory: Path) -> None:
    """Write sorted SHA-256 records for every other staged asset."""
    checksum_files = sorted(
        (
            path
            for path in output_directory.iterdir()
            if path.is_file() and path.name != CHECKSUMS_NAME
        ),
        key=lambda path: path.name,
    )
    lines = [f"{sha256_file(path)}  {path.name}" for path in checksum_files]
    (output_directory / CHECKSUMS_NAME).write_text(
        "\n".join(lines) + ("\n" if lines else ""),
        encoding="utf-8",
        newline="\n",
    )


def package_release(
    root: Path,
    output_directory: Path,
    source_commit: str,
    release_timestamp: str,
    title: str = DEFAULT_TITLE,
    description: str = "",
) -> list[CourseAsset]:
    """Create a clean release directory from compiled course outputs."""
    root = root.resolve()
    source_commit = source_commit.lower()
    title = title.strip()
    _validate_release_metadata(source_commit, release_timestamp, title)
    output_directory = _prepare_release_directory(root, output_directory)
    assets = [
        _stage_course_asset(build, output_directory, source_commit, release_timestamp)
        for build in _discover_course_builds(root)
    ]
    _write_release_metadata(
        output_directory,
        assets,
        source_commit,
        release_timestamp,
        title,
        description,
    )
    _write_checksums(output_directory)
    return assets


def _git(root: Path, *arguments: str) -> str:
    """Run Git and return stripped standard output."""
    result = subprocess.run(
        ("git", *arguments),
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repository_root())
    parser.add_argument("--source-commit", help="Source Git commit SHA")
    parser.add_argument("--release-timestamp", help="Stable ISO-8601 timestamp")
    parser.add_argument("--release-title", default=DEFAULT_TITLE)
    parser.add_argument("--description-file", type=Path)
    return parser.parse_args()


def main() -> int:
    """Build release assets from command-line options."""
    arguments = parse_arguments()
    root = arguments.root.resolve()
    output = root / RELEASE_DIRECTORY
    source_commit = arguments.source_commit or _git(root, "rev-parse", "HEAD")
    release_timestamp = arguments.release_timestamp or _git(
        root, "show", "-s", "--format=%cI", source_commit
    )
    description = ""
    if arguments.description_file:
        description_path = arguments.description_file
        if not description_path.is_absolute():
            description_path = root / description_path
        description = description_path.read_text(encoding="utf-8")

    assets = package_release(
        root,
        output,
        source_commit,
        release_timestamp,
        arguments.release_title,
        description,
    )
    print(f"Packaged {len(assets)} course PDF(s) in {output.relative_to(root)}.")
    for asset in assets:
        print(f"  - {asset.asset_filename} ({asset.sha256})")
    print(f"  - {MANIFEST_NAME}")
    print(f"  - {CHECKSUMS_NAME}")
    print(f"  - {RELEASE_NOTES_NAME}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
