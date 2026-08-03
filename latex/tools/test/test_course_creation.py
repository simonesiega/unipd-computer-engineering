"""Test course metadata, naming, and skeleton creation."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from create_course import Course, academic_year, create_course, kebab_case


class CourseCreationTests(unittest.TestCase):
    def test_kebab_case_normalizes_names(self) -> None:
        self.assertEqual(kebab_case("  Analisi Matematica 1  "), "analisi-matematica-1")
        self.assertEqual(
            kebab_case("Probabilità e Statistica"), "probabilita-e-statistica"
        )

    def test_academic_year_follows_degree_year(self) -> None:
        self.assertEqual(academic_year(1), "2026--2027")
        self.assertEqual(academic_year(2), "2027--2028")
        self.assertEqual(academic_year(3), "2028--2029")

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
            )

            directory = create_course(root, course)

            self.assertEqual(directory, root / "1" / "analisi-matematica-1")
            self.assertTrue((directory / "main.tex").is_file())
            self.assertTrue((directory / "README.md").is_file())
            self.assertTrue((directory / "sections").is_dir())
            self.assertTrue((directory / "assets").is_dir())
            main = (directory / "main.tex").read_text(encoding="utf-8")
            readme = (directory / "README.md").read_text(encoding="utf-8")
            self.assertIn(r"\documentclass[italian]{unipd-notes}", main)
            self.assertIn("academic-year = {2026--2027}", main)
            self.assertIn("degree-year = {1}", main)
            self.assertIn("date = {3 agosto 2026}", main)
            self.assertNotIn(r"\today", main)
            self.assertIn("document-type = {Appunti delle lezioni}", main)
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
            )

            directory = create_course(root, course)
            main = (directory / "main.tex").read_text(encoding="utf-8")
            readme = (directory / "README.md").read_text(encoding="utf-8")

            self.assertIn(r"\documentclass[english]{unipd-notes}", main)
            self.assertIn("document-type = {Lecture notes}", main)
            self.assertIn(r"\chapter{Introduction}", main)
            self.assertIn("Add the course content here.", main)
            self.assertIn("generated course contents", readme)

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
        self.assertIn("argument --date: value must not be empty", result.stderr)

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
                        "--date",
                        "3 August 2026",
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
