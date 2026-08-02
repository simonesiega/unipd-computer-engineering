"""Test mapping changed repository paths to affected LaTeX documents."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build import affected_documents, discover_documents


class BuildSelectionTests(unittest.TestCase):
    @staticmethod
    def create_document(root: Path, relative: str) -> Path:
        document = root / relative / "main.tex"
        document.parent.mkdir(parents=True)
        document.write_text("\\begin{document}\\end{document}\n", encoding="utf-8")
        return document.resolve()

    def test_document_discovery_finds_courses_and_component_examples(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = self.create_document(root, "1/course")
            example = self.create_document(root, "latex/components/code/example")

            self.assertEqual(discover_documents(root), sorted([course, example]))

    def test_course_change_selects_only_that_course(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            selected = self.create_document(root, "1/selected")
            self.create_document(root, "2/unaffected")

            affected = affected_documents(root, [Path("1/selected/sections/topic.tex")])

            self.assertEqual(affected, [selected])

    def test_shared_build_change_selects_every_document(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first = self.create_document(root, "1/first")
            second = self.create_document(root, "2/second")

            affected = affected_documents(root, [Path("latex/tools/build.py")])

            self.assertEqual(affected, sorted([first, second]))

    def test_unrelated_change_selects_no_documents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.create_document(root, "1/course")

            self.assertEqual(affected_documents(root, [Path("README.md")]), [])


if __name__ == "__main__":
    unittest.main()
