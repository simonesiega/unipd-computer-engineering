"""Generate README exam coverage and release tables from GitHub Releases."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from package_notes import course_metadata

START_MARKER = "<!-- RELEASE-CATALOG:START -->"
END_MARKER = "<!-- RELEASE-CATALOG:END -->"
PDF_ASSET = re.compile(r"^([123])-([a-z0-9]+(?:-[a-z0-9]+)*)\.pdf$")
YEARS = (1, 2, 3)
YEAR_LABELS = {1: "First year", 2: "Second year", 3: "Third year"}


@dataclass(frozen=True)
class ReleasedPdf:
    """One course PDF attached to a published release."""

    year: int
    slug: str
    filename: str
    download_url: str


@dataclass(frozen=True)
class PublishedRelease:
    """Release metadata needed by the generated README catalogue."""

    tag: str
    title: str
    url: str
    published_at: str
    immutable: bool
    pdfs: tuple[ReleasedPdf, ...]


def repository_root() -> Path:
    """Return the repository root."""
    return Path(__file__).resolve().parents[2]


def _markdown(value: str) -> str:
    """Escape text for a Markdown table cell."""
    return " ".join(value.replace("|", r"\|").splitlines())


def _release_records(data: Any) -> list[dict[str, Any]]:
    """Flatten normal or gh --paginate --slurp release JSON."""
    if not isinstance(data, list):
        raise TypeError("Release data must be a JSON array")
    records: list[dict[str, Any]] = []
    for item in data:
        if isinstance(item, list):
            records.extend(record for record in item if isinstance(record, dict))
        elif isinstance(item, dict):
            records.append(item)
    return records


def parse_releases(data: Any) -> list[PublishedRelease]:
    """Parse published GitHub releases in newest-first order."""
    releases: list[PublishedRelease] = []
    for record in _release_records(data):
        if record.get("draft") or not record.get("published_at"):
            continue
        pdfs: list[ReleasedPdf] = []
        assets = record.get("assets", [])
        if not isinstance(assets, list):
            raise TypeError("Release assets must be a JSON array")
        for asset in assets:
            if not isinstance(asset, dict):
                continue
            filename = str(asset.get("name", ""))
            match = PDF_ASSET.fullmatch(filename)
            if match is None:
                continue
            pdfs.append(
                ReleasedPdf(
                    year=int(match.group(1)),
                    slug=match.group(2),
                    filename=filename,
                    download_url=str(asset.get("browser_download_url", "")),
                )
            )
        pdfs.sort(key=lambda pdf: (pdf.year, pdf.slug, pdf.filename))
        tag = str(record.get("tag_name", ""))
        timestamp = (
            record.get("updated_at") if tag == "notes-latest" else None
        ) or record["published_at"]
        releases.append(
            PublishedRelease(
                tag=tag,
                title=str(record.get("name") or tag),
                url=str(record.get("html_url", "")),
                published_at=str(timestamp),
                immutable=tag != "notes-latest" and not record.get("prerelease"),
                pdfs=tuple(pdfs),
            )
        )
    return sorted(
        releases,
        key=lambda release: (release.published_at, release.tag),
        reverse=True,
    )


def course_name(root: Path, year: int, slug: str) -> str:
    """Return canonical course metadata or a readable historical fallback."""
    main_file = root / str(year) / slug / "main.tex"
    if main_file.is_file():
        name = course_metadata(main_file).get("course", "").strip()
        if name:
            return name
    return slug.replace("-", " ").title()


def covered_courses(
    releases: list[PublishedRelease],
) -> dict[tuple[int, str], ReleasedPdf]:
    """Return unique courses from immutable snapshots, linked to their newest asset."""
    covered: dict[tuple[int, str], ReleasedPdf] = {}
    for release in releases:
        if not release.immutable:
            continue
        for pdf in release.pdfs:
            covered.setdefault((pdf.year, pdf.slug), pdf)
    return covered


def render_catalog(root: Path, releases: list[PublishedRelease]) -> str:
    """Render the three generated README tables."""
    covered = covered_courses(releases)
    counts = {year: sum(key[0] == year for key in covered) for year in YEARS}
    lines = [
        START_MARKER,
        "| Degree year | Exams covered |",
        "|---|---:|",
    ]
    lines.extend(
        f"| {YEAR_LABELS[year]} | {counts[year]} |" for year in YEARS
    )
    lines.extend(
        (
            f"| **Total** | **{sum(counts.values())}** |",
            "",
            "Current covered exams:",
            "",
            "| Year | Exam | Course archive | Compiled notes |",
            "|---:|---|---|---|",
        )
    )
    if not covered:
        lines.append("| — | _No exams covered yet_ | — | — |")
    else:
        for (year, slug), pdf in sorted(
            covered.items(),
            key=lambda item: (item[0][0], course_name(root, *item[0]).casefold()),
        ):
            source = root / str(year) / slug
            archive = f"[`{year}/{slug}`]({year}/{slug}/)" if source.is_dir() else "—"
            compiled = (
                f"[{pdf.filename}]({pdf.download_url})"
                if pdf.download_url
                else f"`{pdf.filename}`"
            )
            lines.append(
                f"| {year} | {_markdown(course_name(root, year, slug))} | "
                f"{archive} | {compiled} |"
            )

    lines.extend(
        (
            "",
            "## Releases",
            "",
            "| Release | Date | Title | PDFs |",
            "|---|---|---|---|",
        )
    )
    if not releases:
        lines.append("| — | — | _No releases published yet_ | — |")
    else:
        for release in releases:
            release_link = (
                f"[`{release.tag}`]({release.url})" if release.url else f"`{release.tag}`"
            )
            pdf_links = "<br>".join(
                f"[{pdf.filename}]({pdf.download_url})"
                if pdf.download_url
                else f"`{pdf.filename}`"
                for pdf in release.pdfs
            ) or "—"
            lines.append(
                f"| {release_link} | {release.published_at[:10]} | "
                f"{_markdown(release.title)} | {pdf_links} |"
            )
    lines.append(END_MARKER)
    return "\n".join(lines)


def update_readme(readme: Path, generated: str) -> bool:
    """Replace the generated catalogue and return whether content changed."""
    content = readme.read_text(encoding="utf-8")
    if content.count(START_MARKER) != 1 or content.count(END_MARKER) != 1:
        raise ValueError(f"Expected exactly one release catalogue marker pair in {readme}")
    start = content.index(START_MARKER)
    end = content.index(END_MARKER, start) + len(END_MARKER)
    updated = content[:start] + generated + content[end:]
    if updated == content:
        return False
    temporary = readme.with_suffix(".md.tmp")
    try:
        temporary.write_text(updated, encoding="utf-8", newline="\n")
        os.replace(temporary, readme)
    finally:
        temporary.unlink(missing_ok=True)
    return True


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--releases-json", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    """Update README from prepared GitHub release JSON."""
    arguments = parse_arguments()
    root = repository_root()
    data = json.loads(arguments.releases_json.read_text(encoding="utf-8"))
    releases = parse_releases(data)
    changed = update_readme(root / "README.md", render_catalog(root, releases))
    print(
        f"{'Updated' if changed else 'Verified'} README release catalogue from "
        f"{len(releases)} published release(s)."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
