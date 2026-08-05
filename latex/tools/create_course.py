#!/usr/bin/env python3
"""Create a course directory with the repository's standard files and metadata."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

DEGREE_START_YEAR = 2026
VALID_YEARS = (1, 2, 3)
VALID_SEMESTERS = (1, 2)
VALID_LANGUAGES = ("italian", "english")
SCAFFOLD_LABELS = {
    "italian": {
        "document_type": "Appunti delle lezioni",
        "introduction": "Introduzione",
        "placeholder": "Aggiungere qui i contenuti del corso.",
        "readme_placeholder": (
            "I contenuti generati del corso appariranno qui dopo la prima build."
        ),
    },
    "english": {
        "document_type": "Lecture notes",
        "introduction": "Introduction",
        "placeholder": "Add the course content here.",
        "readme_placeholder": (
            "The generated course contents will appear here after the first build."
        ),
    },
}


@dataclass(frozen=True)
class Course:
    year: int
    name: str
    short_name: str
    professor: str
    semester: int
    document_date: str
    language: str


def repository_root() -> Path:
    """Return the repository root."""
    return Path(__file__).resolve().parents[2]


def non_empty(value: str) -> str:
    """Return a trimmed command-line value, rejecting blank strings."""
    value = value.strip()
    if not value:
        raise argparse.ArgumentTypeError("value must not be empty")
    return value


def kebab_case(value: str) -> str:
    """Convert a human-readable course name to an ASCII kebab-case slug."""
    # Remove accents before replacing non-alphanumeric runs with hyphens.
    normalized = unicodedata.normalize("NFKD", value.casefold())
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    if not slug:
        raise ValueError(
            "Course name does not contain characters usable in a directory name"
        )
    return slug


def academic_year(degree_year: int) -> str:
    """Return the academic year associated with a degree year in this archive."""
    start = DEGREE_START_YEAR + degree_year - 1
    return f"{start}--{start + 1}"


def canonical_build_command(course_directory: Path) -> str:
    """Return the canonical Docker command for building a course."""
    return (
        "docker compose run --rm texlive python3 latex/tools/build.py "
        f"{course_directory.as_posix()}"
    )


def escape_latex(value: str) -> str:
    """Escape user-provided text for use in a LaTeX metadata value."""
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "#": r"\#",
        "%": r"\%",
        "_": r"\_",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(character, character) for character in value)


def render_main(course: Course) -> str:
    """Render the initial main.tex for a course."""
    labels = SCAFFOLD_LABELS[course.language]
    return f"""\\documentclass[{course.language}]{{unipd-notes}}

\\unipdsetup{{
  course = {{{escape_latex(course.name)}}},
  short-course = {{{escape_latex(course.short_name)}}},
  professor = {{{escape_latex(course.professor)}}},
  academic-year = {{{academic_year(course.year)}}},
  degree-year = {{{course.year}}},
  semester = {{{course.semester}}},
  document-type = {{{labels["document_type"]}}},
  author = {{Your Name}},
  date = {{{escape_latex(course.document_date)}}},
  version = {{0.1.0}}
}}

\\begin{{document}}
\\makecoursefrontmatter
\\makecoursemainmatter

\\chapter{{{labels["introduction"]}}}

{labels["placeholder"]}

\\end{{document}}
"""


def render_readme(course: Course) -> str:
    """Render the localized initial course README."""
    placeholder = SCAFFOLD_LABELS[course.language]["readme_placeholder"]
    return f"""# {course.name}

<!-- GENERATED:START -->
{placeholder}
<!-- GENERATED:END -->
"""


def duplicate_directory(root: Path, slug: str) -> Path | None:
    """Find an existing course directory with the same slug in any degree year."""
    for year in VALID_YEARS:
        year_directory = root / str(year)
        if not year_directory.is_dir():
            continue
        for path in year_directory.iterdir():
            if path.is_dir() and path.name.casefold() == slug.casefold():
                return path
    return None


def create_course(root: Path, course: Course) -> Path:
    """Create a validated course skeleton and return its directory."""
    if course.year not in VALID_YEARS:
        raise ValueError(f"Year must be one of: {', '.join(map(str, VALID_YEARS))}")
    if course.semester not in VALID_SEMESTERS:
        raise ValueError(
            f"Semester must be one of: {', '.join(map(str, VALID_SEMESTERS))}"
        )
    if course.language not in VALID_LANGUAGES:
        raise ValueError(f"Language must be one of: {', '.join(VALID_LANGUAGES)}")

    slug = kebab_case(course.name)
    duplicate = duplicate_directory(root, slug)
    if duplicate is not None:
        raise FileExistsError(
            f"Course directory already exists: {duplicate.relative_to(root)}"
        )

    course_directory = root / str(course.year) / slug
    if course_directory.exists():
        raise FileExistsError(
            f"Path already exists: {course_directory.relative_to(root)}"
        )

    course_directory.parent.mkdir(exist_ok=True)
    course_directory.mkdir()
    try:
        for directory_name in ("sections", "assets"):
            scaffold_directory = course_directory / directory_name
            scaffold_directory.mkdir()
            (scaffold_directory / ".gitkeep").write_text("", encoding="utf-8")
        (course_directory / "main.tex").write_text(
            render_main(course), encoding="utf-8", newline="\n"
        )
        (course_directory / "README.md").write_text(
            render_readme(course), encoding="utf-8", newline="\n"
        )
    except OSError:
        # Never leave a partially generated course in the repository.
        shutil.rmtree(course_directory, ignore_errors=True)
        raise

    return course_directory


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--year", type=int, choices=VALID_YEARS, required=True, help="Degree year"
    )
    parser.add_argument(
        "--course", type=non_empty, required=True, help="Official course name"
    )
    parser.add_argument(
        "--short-course", type=non_empty, required=True, help="Short course name"
    )
    parser.add_argument(
        "--professor", type=non_empty, required=True, help="Professor name"
    )
    parser.add_argument(
        "--semester",
        type=int,
        choices=VALID_SEMESTERS,
        required=True,
        help="Teaching semester",
    )
    parser.add_argument(
        "--date",
        type=non_empty,
        required=True,
        help="Explicit document publication date",
    )
    parser.add_argument(
        "--language",
        choices=VALID_LANGUAGES,
        required=True,
        help="Document language",
    )
    return parser.parse_args()


def main() -> int:
    """Create a course from command-line arguments."""
    arguments = parse_arguments()
    course = Course(
        year=arguments.year,
        name=arguments.course,
        short_name=arguments.short_course,
        professor=arguments.professor,
        semester=arguments.semester,
        document_date=arguments.date,
        language=arguments.language,
    )
    root = repository_root()
    course_directory = create_course(root, course)
    relative = course_directory.relative_to(root)
    print(f"Created course: {relative}")
    print(f"Academic year: {academic_year(course.year)}")
    print(f"Next step: {canonical_build_command(relative)}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
