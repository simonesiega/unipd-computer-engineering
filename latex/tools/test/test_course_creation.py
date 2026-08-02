"""Test course metadata, naming, and skeleton creation."""

from __future__ import annotations

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
            course = Course(1, "Analisi Matematica 1", "Analisi 1", "Name", 1)

            directory = create_course(root, course)

            self.assertEqual(directory, root / "1" / "analisi-matematica-1")
            self.assertTrue((directory / "main.tex").is_file())
            self.assertTrue((directory / "README.md").is_file())
            self.assertTrue((directory / "sections").is_dir())
            self.assertTrue((directory / "assets").is_dir())
            main = (directory / "main.tex").read_text(encoding="utf-8")
            self.assertIn("academic-year = {2026--2027}", main)
            self.assertIn("degree-year = {1}", main)

    def test_duplicate_slug_is_rejected_across_years(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            create_course(
                root, Course(1, "Analisi Matematica 1", "Analisi 1", "Name", 1)
            )

            with self.assertRaises(FileExistsError):
                create_course(
                    root, Course(2, "Analisi Matematica 1", "Analisi 1", "Name", 1)
                )

    def test_invalid_year_and_semester_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with self.assertRaises(ValueError):
                create_course(root, Course(4, "Course", "Course", "Name", 1))
            with self.assertRaises(ValueError):
                create_course(root, Course(1, "Course", "Course", "Name", 3))


if __name__ == "__main__":
    unittest.main()
