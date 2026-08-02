"""Test course layout and LaTeX source validation errors."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check_repository import validate_course, validate_source


class RepositoryValidationTests(unittest.TestCase):
    def test_valid_course_entry_point_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            main = root / "1" / "course" / "main.tex"
            main.parent.mkdir(parents=True)
            main.write_text(
                "\\documentclass{unipd-notes}\n\\begin{document}\n\\end{document}\n",
                encoding="utf-8",
            )

            self.assertEqual(validate_course(main, root), [])

    def test_invalid_course_location_and_incomplete_document_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            nested = root / "1" / "course" / "nested" / "main.tex"
            nested.parent.mkdir(parents=True)
            nested.write_text("content\n", encoding="utf-8")
            invalid = root / "2" / "course" / "main.tex"
            invalid.parent.mkdir(parents=True)
            invalid.write_text("content\n", encoding="utf-8")

            self.assertTrue(validate_course(nested, root))
            errors = validate_course(invalid, root)
            self.assertTrue(any("document class" in error for error in errors))
            self.assertTrue(any("document environment" in error for error in errors))

    def test_source_hygiene_errors_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.tex"
            source.write_text("<<<<<<< HEAD\n\tcontent  \n", encoding="utf-8")

            errors = validate_source(source, root)

            self.assertTrue(any("merge-conflict" in error for error in errors))
            self.assertTrue(any("tab characters" in error for error in errors))
            self.assertTrue(any("trailing whitespace" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
