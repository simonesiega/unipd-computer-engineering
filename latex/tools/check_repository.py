#!/usr/bin/env python3
"""Validate the repository's LaTeX sources and document layouts."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

from latex_source import strip_comments

YEARS = ("1", "2", "3")
SOURCE_SUFFIXES = (".tex", ".sty", ".cls", ".bib")
COMPONENTS_DIRECTORY = "latex/components"
INTEGRATION_DIRECTORY = "latex/integration"
INTEGRATION_EXAMPLES = ("english", "italian")
CONFLICT_MARKER = re.compile(r"^(?:<{7}|={7}|>{7})(?: |$)", re.MULTILINE)
COURSE_DIRECTORY_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COURSE_CLASS = re.compile(
    r"\\documentclass\s*\[([^]]*)\]\s*\{unipd-notes\}"
)
COURSE_SETUP = re.compile(r"\\unipdsetup\s*\{(.*?)\}\s*\\begin\{document\}", re.DOTALL)
METADATA_VALUE = re.compile(r"(?m)^\s*([a-z-]+)\s*=\s*\{([^{}]*)\}\s*,?\s*$")
ACADEMIC_YEAR = re.compile(r"^(\d{4})--(\d{4})$")
SUPPORTED_LANGUAGES = {"italian", "english"}
DEGREE_COHORT_START_YEAR = 2026
PLACEHOLDER_AUTHORS = {"author", "nome cognome", "todo", "tbd", "your name"}
README_START_MARKER = "<!-- GENERATED:START -->"
README_END_MARKER = "<!-- GENERATED:END -->"
MARKDOWN_LINK = re.compile(r"!?\[[^]]*\]\((?:<([^>]+)>|([^\s)]+))")
MARKDOWN_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
MARKDOWN_ANCHOR_PUNCTUATION = re.compile(r"[^\w\- ]", re.UNICODE)


def repository_root() -> Path:
    """Return the repository root."""
    return Path(__file__).resolve().parents[2]


def validate_source(path: Path, root: Path) -> list[str]:
    """Validate a LaTeX source for encoding and source-hygiene errors."""
    relative = path.relative_to(root)
    source_bytes = path.read_bytes()
    try:
        content = source_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        return [f"{relative}: is not valid UTF-8 ({error})"]

    errors: list[str] = []
    if b"\r" in source_bytes:
        errors.append(f"{relative}: must use LF line endings")
    if content and not content.endswith("\n"):
        errors.append(f"{relative}: must end with a newline")
    if CONFLICT_MARKER.search(content):
        errors.append(f"{relative}: contains an unresolved merge-conflict marker")
    if "\t" in content:
        errors.append(f"{relative}: contains tab characters; use spaces")
    for number, line in enumerate(content.splitlines(), start=1):
        if line.rstrip() != line:
            errors.append(f"{relative}:{number}: trailing whitespace")
    return errors


def markdown_anchors(content: str) -> set[str]:
    """Return GitHub-style anchors for ATX headings outside fenced code blocks."""
    anchors: set[str] = set()
    occurrences: dict[str, int] = {}
    in_fence = False
    fence_marker = ""
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
            continue
        if in_fence:
            continue
        match = MARKDOWN_HEADING.match(line)
        if match is None:
            continue
        heading = re.sub(r"<[^>]+>", "", match.group(1)).casefold()
        base = MARKDOWN_ANCHOR_PUNCTUATION.sub("", heading).replace(" ", "-")
        count = occurrences.get(base, 0)
        occurrences[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def validate_markdown_links(path: Path, root: Path) -> list[str]:
    """Report missing repository-relative Markdown targets and heading anchors."""
    content = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for match in MARKDOWN_LINK.finditer(content):
        target = unquote(match.group(1) or match.group(2))
        parsed = urlparse(target)
        if parsed.scheme or parsed.netloc:
            continue
        destination = (path.parent / (parsed.path or path.name)).resolve()
        line = content.count("\n", 0, match.start()) + 1
        relative = path.relative_to(root)
        if not destination.exists():
            errors.append(f"{relative}:{line}: broken Markdown link: {target}")
            continue
        if parsed.fragment and destination.is_file() and destination.suffix == ".md":
            destination_content = destination.read_text(encoding="utf-8")
            if parsed.fragment.casefold() not in markdown_anchors(destination_content):
                errors.append(
                    f"{relative}:{line}: broken Markdown anchor: {target}"
                )
    return errors


def validate_tracked_course_pdfs(root: Path) -> list[str]:
    """Reject generated course PDFs recorded in the Git index."""
    result = subprocess.run(
        ("git", "ls-files", "-z", "--", *YEARS),
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        details = result.stderr.decode("utf-8", errors="replace").strip()
        return [f"Unable to inspect tracked files with Git: {details}"]

    tracked = sorted(
        Path(value.decode("utf-8", errors="surrogateescape"))
        for value in result.stdout.split(b"\0")
        if value
    )
    errors: list[str] = []
    for path in tracked:
        if (
            len(path.parts) >= 3
            and path.parts[0] in YEARS
            and path.parts[-1] == "main.pdf"
        ):
            relative = path.as_posix()
            errors.append(
                f"{relative}: generated course PDF is tracked. Compiled course PDFs "
                "must not be committed; build the PDF locally or download it from "
                "the notes-latest release. Remove it from the index with: "
                f"git rm --cached -- {relative}"
            )
    return errors


def validate_course(main_file: Path, root: Path) -> list[str]:
    """Validate a course entry point and its document structure."""
    relative = main_file.relative_to(root)
    errors: list[str] = []
    if len(relative.parts) != 3 or relative.parts[0] not in YEARS:
        errors.append(
            f"{relative}: course entry points must be located at <year>/<course>/main.tex"
        )
        return errors

    if COURSE_DIRECTORY_NAME.fullmatch(relative.parts[1]) is None:
        errors.append(
            f"{relative}: course directory names must use lowercase kebab-case"
        )

    content = strip_comments(
        main_file.read_text(encoding="utf-8", errors="replace")
    )
    class_matches = COURSE_CLASS.findall(content)
    if len(class_matches) != 1:
        errors.append(
            f"{relative}: must contain exactly one \\documentclass declaration "
            "using unipd-notes with an italian or english option"
        )
    else:
        options = {
            option.strip() for option in class_matches[0].split(",") if option.strip()
        }
        languages = options & SUPPORTED_LANGUAGES
        if len(languages) != 1:
            errors.append(
                f"{relative}: must select exactly one supported language: "
                "italian or english"
            )

    if "\\begin{document}" not in content or "\\end{document}" not in content:
        errors.append(f"{relative}: must contain a complete document environment")

    setup_match = COURSE_SETUP.search(content)
    metadata: dict[str, str] = {}
    if setup_match is None:
        errors.append(f"{relative}: must declare \\unipdsetup before the document")
    else:
        metadata = {
            key: value.strip()
            for key, value in METADATA_VALUE.findall(setup_match.group(1))
        }
        for key in (
            "course",
            "author",
            "academic-year",
            "degree-year",
            "semester",
            "date",
            "version",
        ):
            if key not in metadata:
                errors.append(f"{relative}: \\unipdsetup must define {key}")

        if "course" in metadata and not metadata["course"]:
            errors.append(f"{relative}: course metadata must not be empty")
        if "author" in metadata:
            author = metadata["author"]
            if not author or author.casefold() in PLACEHOLDER_AUTHORS:
                errors.append(
                    f"{relative}: author metadata must be non-empty and not a placeholder"
                )
        expected_degree_year = relative.parts[0]
        if (
            "degree-year" in metadata
            and metadata["degree-year"] != expected_degree_year
        ):
            errors.append(
                f"{relative}: degree-year must match directory year "
                f"{expected_degree_year}"
            )
        if "semester" in metadata and metadata["semester"] not in {"1", "2"}:
            errors.append(f"{relative}: semester must be 1 or 2")
        if "academic-year" in metadata:
            academic_match = ACADEMIC_YEAR.fullmatch(metadata["academic-year"])
            degree_year = int(expected_degree_year)
            expected_start = DEGREE_COHORT_START_YEAR + degree_year - 1
            if (
                academic_match is None
                or int(academic_match.group(1)) != expected_start
                or int(academic_match.group(2)) != expected_start + 1
            ):
                errors.append(
                    f"{relative}: academic-year must be "
                    f"{expected_start}--{expected_start + 1} for degree year "
                    f"{expected_degree_year}"
                )
        if "version" in metadata and not metadata["version"]:
            errors.append(f"{relative}: version metadata must not be empty")

    readme = main_file.with_name("README.md")
    if not readme.is_file():
        errors.append(f"{readme.relative_to(root)}: missing required course README")
    else:
        readme_content = readme.read_text(encoding="utf-8", errors="replace")
        start_count = readme_content.count(README_START_MARKER)
        end_count = readme_content.count(README_END_MARKER)
        if (
            start_count != 1
            or end_count != 1
            or readme_content.index(README_START_MARKER)
            > readme_content.index(README_END_MARKER)
        ):
            errors.append(
                f"{readme.relative_to(root)}: must contain exactly one ordered pair "
                "of generated README markers"
            )
    return errors


def validate_components(root: Path) -> list[str]:
    """Validate component packages and their required examples."""
    components_directory = root / COMPONENTS_DIRECTORY
    errors: list[str] = []
    if not components_directory.is_dir():
        return [f"{COMPONENTS_DIRECTORY}/: missing components directory"]

    for component in sorted(
        path for path in components_directory.iterdir() if path.is_dir()
    ):
        relative = component.relative_to(root)
        if COURSE_DIRECTORY_NAME.fullmatch(component.name) is None:
            errors.append(
                f"{relative}: component directory names must use lowercase kebab-case"
            )
        package = component / f"{component.name}.sty"
        example = component / "example"
        required_paths = {package, example}

        if not package.is_file():
            errors.append(f"{relative}: missing {component.name}.sty")
        if not example.is_dir():
            errors.append(f"{relative}: missing example/ directory")
        else:
            expected_example_files = {example / "main.tex", example / "main.pdf"}
            for expected in sorted(expected_example_files):
                if not expected.is_file():
                    errors.append(
                        f"{expected.relative_to(root)}: missing required file"
                    )
            for path in sorted(example.iterdir()):
                if path not in expected_example_files:
                    errors.append(
                        f"{path.relative_to(root)}: unexpected component example entry"
                    )

        for path in sorted(component.iterdir()):
            if path not in required_paths:
                errors.append(f"{path.relative_to(root)}: unexpected component entry")
    return errors


def validate_integration_examples(root: Path) -> list[str]:
    """Validate complete integration projects and their generated files."""
    integration_directory = root / INTEGRATION_DIRECTORY
    if not integration_directory.is_dir():
        return [f"{INTEGRATION_DIRECTORY}/: missing integration directory"]

    errors: list[str] = []
    expected_examples = {
        integration_directory / language for language in INTEGRATION_EXAMPLES
    }
    for example in sorted(expected_examples):
        relative = example.relative_to(root)
        if not example.is_dir():
            errors.append(f"{relative}/: missing integration example")
            continue
        main_file = example / "main.tex"
        expected_files = {main_file, example / "main.pdf", example / "README.md"}
        for expected in sorted(expected_files):
            if not expected.is_file():
                errors.append(f"{expected.relative_to(root)}: missing required file")
        if main_file.is_file():
            source = main_file.read_text(encoding="utf-8", errors="replace")
            language = example.name
            class_pattern = rf"\\documentclass\[[^]]*\b{language}\b[^]]*\]"
            if re.search(class_pattern, source) is None:
                errors.append(
                    f"{main_file.relative_to(root)}: must select the {language} class option"
                )
        for path in sorted(example.iterdir()):
            if path not in expected_files:
                errors.append(f"{path.relative_to(root)}: unexpected integration entry")

    for path in sorted(integration_directory.iterdir()):
        if path not in expected_examples:
            errors.append(f"{path.relative_to(root)}: unexpected integration entry")
    return errors


def main() -> int:
    """Validate repository LaTeX sources and directory layouts."""
    root = repository_root()
    errors: list[str] = []

    errors.extend(validate_tracked_course_pdfs(root))

    for year in YEARS:
        year_directory = root / year
        # Git does not preserve empty directories. A year directory becomes
        # mandatory only when the repository contains at least one course in it.
        if not year_directory.exists():
            continue
        if not year_directory.is_dir():
            errors.append(f"{year}: expected a course-year directory")
            continue
        course_directories = sorted(
            path for path in year_directory.iterdir() if path.is_dir()
        )
        for course_directory in course_directories:
            main_file = course_directory / "main.tex"
            if not main_file.is_file():
                errors.append(
                    f"{course_directory.relative_to(root)}: course directory is missing main.tex"
                )
                continue
            errors.extend(validate_course(main_file, root))

        expected_main_files = {
            directory / "main.tex" for directory in course_directories
        }
        for main_file in sorted(year_directory.rglob("main.tex")):
            if main_file not in expected_main_files:
                errors.extend(validate_course(main_file, root))

    errors.extend(validate_components(root))
    errors.extend(validate_integration_examples(root))

    source_files = sorted(
        path
        for path in root.rglob("*")
        if ".git" not in path.parts
        and ".build" not in path.parts
        and path.is_file()
        and path.suffix.lower() in SOURCE_SUFFIXES
    )
    for path in source_files:
        errors.extend(validate_source(path, root))

    markdown_files = sorted(
        path
        for path in root.rglob("*.md")
        if ".git" not in path.parts
        and ".build" not in path.parts
        and path.is_file()
    )
    for path in markdown_files:
        errors.extend(validate_markdown_links(path, root))

    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    course_count = sum(1 for year in YEARS for _ in (root / year).glob("*/main.tex"))
    print(
        f"Validated {len(source_files)} LaTeX source files and {course_count} courses."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
