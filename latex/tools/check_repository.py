#!/usr/bin/env python3
"""Validate the repository's LaTeX sources and course directory layout."""

from __future__ import annotations

import re
import sys
from pathlib import Path

YEARS = ("1", "2", "3")
SOURCE_SUFFIXES = (".tex", ".sty", ".cls", ".bib")
COMPONENTS_DIRECTORY = "latex/components"
CONFLICT_MARKER = re.compile(r"^(?:<{7}|={7}|>{7})(?: |$)", re.MULTILINE)


def repository_root() -> Path:
    # Return the root directory of the repository, which is two levels above this script's location.
    return Path(__file__).resolve().parents[2]


def validate_source(path: Path, root: Path) -> list[str]:
    # Validate a LaTeX source file for common issues such as merge conflict markers, tab characters, and trailing whitespace.
    relative = path.relative_to(root)
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        return [f"{relative}: is not valid UTF-8 ({error})"]

    errors: list[str] = []
    if CONFLICT_MARKER.search(content):
        errors.append(f"{relative}: contains an unresolved merge-conflict marker")
    if "\t" in content:
        errors.append(f"{relative}: contains tab characters; use spaces")
    for number, line in enumerate(content.splitlines(), start=1):
        if line.rstrip() != line:
            errors.append(f"{relative}:{number}: trailing whitespace")
    return errors


def validate_course(main_file: Path, root: Path) -> list[str]:
    # Validate a course's main.tex file to ensure it is located in the correct directory structure and contains the necessary LaTeX document structure.
    relative = main_file.relative_to(root)
    errors: list[str] = []
    if len(relative.parts) != 3 or relative.parts[0] not in YEARS:
        errors.append(
            f"{relative}: course entry points must be located at <year>/<course>/main.tex"
        )
        return errors

    content = main_file.read_text(encoding="utf-8")
    if "\\documentclass" not in content:
        errors.append(f"{relative}: does not declare a document class")
    if "\\begin{document}" not in content or "\\end{document}" not in content:
        errors.append(f"{relative}: must contain a complete document environment")
    return errors


def validate_components(root: Path) -> list[str]:
    # Validate the components directory to ensure each component has the required .sty file and example directory with main.tex and main.pdf.
    components_directory = root / COMPONENTS_DIRECTORY
    errors: list[str] = []
    if not components_directory.is_dir():
        return [f"{COMPONENTS_DIRECTORY}/: missing components directory"]

    for component in sorted(path for path in components_directory.iterdir() if path.is_dir()):
        relative = component.relative_to(root)
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
                    errors.append(f"{expected.relative_to(root)}: missing required file")
            for path in sorted(example.iterdir()):
                if path not in expected_example_files:
                    errors.append(f"{path.relative_to(root)}: unexpected component example entry")

        for path in sorted(component.iterdir()):
            if path not in required_paths:
                errors.append(f"{path.relative_to(root)}: unexpected component entry")
    return errors


def main() -> int:
    # Validate the repository's LaTeX sources and course directory layout, returning an exit code indicating success or failure.
    root = repository_root()
    errors: list[str] = []

    # Validate course directories for each year, checking for the presence of main.tex and validating its content.
    for year in YEARS:
        year_directory = root / year
        # Git does not preserve empty directories. A year directory becomes
        # mandatory only when the repository contains at least one course in it.
        if not year_directory.exists():
            continue
        if not year_directory.is_dir():
            errors.append(f"{year}: expected a course-year directory")
            continue
        course_directories = sorted(path for path in year_directory.iterdir() if path.is_dir())
        for course_directory in course_directories:
            main_file = course_directory / "main.tex"
            if not main_file.is_file():
                errors.append(
                    f"{course_directory.relative_to(root)}: course directory is missing main.tex"
                )
                continue
            errors.extend(validate_course(main_file, root))

        expected_main_files = {directory / "main.tex" for directory in course_directories}
        for main_file in sorted(year_directory.rglob("main.tex")):
            if main_file not in expected_main_files:
                errors.extend(validate_course(main_file, root))

    errors.extend(validate_components(root))

    # Validate all LaTeX source files in the repository, excluding .git and .build directories, for common issues.
    for path in root.rglob("*"):
        if ".git" in path.parts or ".build" in path.parts:
            continue
        if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES:
            errors.extend(validate_source(path, root))

    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    course_count = sum(1 for year in YEARS for _ in (root / year).glob("*/main.tex"))
    source_count = sum(
        1
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SOURCE_SUFFIXES
        and ".build" not in path.parts
        and ".git" not in path.parts
    )
    print(f"Validated {source_count} LaTeX source files and {course_count} courses.")
    return 0


if __name__ == "__main__":
    # Run the main function and handle exceptions, exiting with an appropriate status code.
    sys.exit(main())
