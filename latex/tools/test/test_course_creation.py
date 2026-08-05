"""Test course metadata, naming, and skeleton creation."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import create_course as create_course_module
from create_course import (
    Course,
    academic_year,
    canonical_build_command,
    create_course,
    escape_latex,
    iso_date,
    kebab_case,
    localized_date,
)


class CourseCreationTests(unittest.TestCase):
    def test_kebab_case_normalizes_names(self) -> None:
        self.assertEqual(kebab_case("  Analisi Matematica 1  "), "analisi-matematica-1")
        self.assertEqual(
            kebab_case("Probabilità e Statistica"), "probabilita-e-statistica"
        )

    def test_latex_metadata_characters_are_escaped(self) -> None:
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
        for character, escaped in replacements.items():
            with self.subTest(character=character):
                self.assertEqual(escape_latex(character), escaped)
        self.assertEqual(escape_latex("Probabilità"), "Probabilità")

    def test_iso_dates_are_validated_and_localized(self) -> None:
        self.assertEqual(iso_date("2026-09-28"), "2026-09-28")
        self.assertEqual(localized_date("2026-09-28", "italian"), "28 settembre 2026")
        self.assertEqual(localized_date("2026-09-28", "english"), "28 September 2026")
        for invalid in ("tomorrow", "TODO", "2026-02-30", "28 September 2026"):
            with self.subTest(value=invalid), self.assertRaises(
                argparse.ArgumentTypeError
            ):
                iso_date(invalid)

    def test_academic_year_follows_degree_year(self) -> None:
        self.assertEqual(academic_year(1), "2026--2027")
        self.assertEqual(academic_year(2), "2027--2028")
        self.assertEqual(academic_year(3), "2028--2029")

    def test_next_build_command_uses_the_canonical_environment(self) -> None:
        self.assertEqual(
            canonical_build_command(Path("1/analisi-matematica-1")),
            "docker compose run --rm texlive python3 latex/tools/build.py "
            "1/analisi-matematica-1",
        )

    def test_standard_layout_and_metadata_are_created(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = Course(
                1,
                "Analisi Matematica 1",
                "Analisi 1",
                "Name",
                1,
                "3 agosto 2026",
                "italian",
                "Ada Lovelace",
            )

            directory = create_course(root, course)

            self.assertEqual(directory, root / "1" / "analisi-matematica-1")
            self.assertTrue((directory / "main.tex").is_file())
            self.assertTrue((directory / "README.md").is_file())
            self.assertTrue((directory / "sections").is_dir())
            self.assertTrue((directory / "sections" / ".gitkeep").is_file())
            self.assertTrue((directory / "assets").is_dir())
            self.assertTrue((directory / "assets" / ".gitkeep").is_file())
            main = (directory / "main.tex").read_text(encoding="utf-8")
            readme = (directory / "README.md").read_text(encoding="utf-8")
            self.assertIn(r"\documentclass[italian]{unipd-notes}", main)
            self.assertIn("academic-year = {2026--2027}", main)
            self.assertIn("degree-year = {1}", main)
            self.assertIn("author = {Ada Lovelace}", main)
            self.assertIn("date = {3 agosto 2026}", main)
            self.assertNotIn(r"\today", main)
            self.assertIn("document-type = {Appunti delle lezioni}", main)
            self.assertIn(r"\makecoursefrontmatter", main)
            self.assertIn(r"\makecoursemainmatter", main)
            self.assertIn(r"\chapter{Introduzione}", main)
            self.assertIn("Aggiungere qui i contenuti del corso.", main)
            self.assertIn("contenuti generati del corso", readme)

    def test_english_course_scaffold_is_localized(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = Course(
                1,
                "Computer Architecture",
                "Architecture",
                "Name",
                1,
                "3 August 2026",
                "english",
                "Grace Hopper",
            )

            directory = create_course(root, course)
            main = (directory / "main.tex").read_text(encoding="utf-8")
            readme = (directory / "README.md").read_text(encoding="utf-8")

            self.assertIn(r"\documentclass[english]{unipd-notes}", main)
            self.assertIn("author = {Grace Hopper}", main)
            self.assertIn("document-type = {Lecture notes}", main)
            self.assertIn(r"\chapter{Introduction}", main)
            self.assertIn("Add the course content here.", main)
            self.assertIn("generated course contents", readme)

    def test_partial_course_is_removed_when_scaffolding_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = Course(
                1,
                "Operating Systems",
                "Systems",
                "Name",
                1,
                "3 August 2026",
                "english",
                "Ada Lovelace",
            )
            original_write_text = Path.write_text

            def fail_on_readme(
                path: Path,
                data: str,
                encoding: str | None = None,
                errors: str | None = None,
                newline: str | None = None,
            ) -> int:
                if path.name == "README.md":
                    raise OSError("simulated write failure")
                return original_write_text(
                    path,
                    data,
                    encoding=encoding,
                    errors=errors,
                    newline=newline,
                )

            with (
                patch.object(Path, "write_text", fail_on_readme),
                self.assertRaisesRegex(OSError, "simulated write failure"),
            ):
                create_course(root, course)

            self.assertFalse((root / "1" / "operating-systems").exists())

    def test_cli_main_creates_course_with_explicit_author(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            arguments = [
                "create_course.py",
                "--year", "1",
                "--course", "Operating Systems",
                "--short-course", "Systems",
                "--professor", "Name",
                "--semester", "1",
                "--author", "Ada Lovelace",
                "--date", "2026-08-03",
                "--language", "english",
            ]
            with (
                patch.object(sys, "argv", arguments),
                patch.object(
                    create_course_module, "repository_root", return_value=root
                ),
                patch("builtins.print"),
            ):
                self.assertEqual(create_course_module.main(), 0)

            source = (root / "1" / "operating-systems" / "main.tex").read_text(
                encoding="utf-8"
            )
            self.assertIn("author = {Ada Lovelace}", source)
            self.assertIn("date = {3 August 2026}", source)

    def test_duplicate_slug_is_rejected_across_years(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            create_course(
                root,
                Course(
                    1,
                    "Analisi Matematica 1",
                    "Analisi 1",
                    "Name",
                    1,
                    "3 agosto 2026",
                    "italian",
                    "Ada Lovelace",
                ),
            )

            with self.assertRaises(FileExistsError):
                create_course(
                    root,
                    Course(
                        2,
                        "Analisi Matematica 1",
                        "Analisi 1",
                        "Name",
                        1,
                        "3 agosto 2026",
                        "italian",
                        "Ada Lovelace",
                    ),
                )

    def test_invalid_course_values_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with self.assertRaises(ValueError):
                create_course(
                    root,
                    Course(
                        4,
                        "Course",
                        "Course",
                        "Name",
                        1,
                        "3 agosto 2026",
                        "italian",
                        "Ada Lovelace",
                    ),
                )
            with self.assertRaises(ValueError):
                create_course(
                    root,
                    Course(
                        1,
                        "Course",
                        "Course",
                        "Name",
                        3,
                        "3 agosto 2026",
                        "italian",
                        "Ada Lovelace",
                    ),
                )
            with self.assertRaises(ValueError):
                create_course(
                    root,
                    Course(
                        1,
                        "Course",
                        "Course",
                        "Name",
                        1,
                        "3 agosto 2026",
                        "german",
                        "Ada Lovelace",
                    ),
                )

        result = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve().parents[1] / "create_course.py"),
                "--year",
                "1",
                "--course",
                "Course",
                "--short-course",
                "Course",
                "--professor",
                "Name",
                "--semester",
                "1",
                "--author",
                "Ada Lovelace",
                "--date",
                " ",
                "--language",
                "italian",
            ],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("argument --date: date must use ISO YYYY-MM-DD format", result.stderr)

        for invalid_language in ("", "german"):
            with self.subTest(language=invalid_language):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(Path(__file__).resolve().parents[1] / "create_course.py"),
                        "--year",
                        "1",
                        "--course",
                        "Course",
                        "--short-course",
                        "Course",
                        "--professor",
                        "Name",
                        "--semester",
                        "1",
                        "--author",
                        "Ada Lovelace",
                        "--date",
                        "2026-08-03",
                        "--language",
                        invalid_language,
                    ],
                    capture_output=True,
                    check=False,
                    text=True,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("argument --language: invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
