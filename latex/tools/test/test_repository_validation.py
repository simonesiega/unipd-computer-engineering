"""Test course layout and LaTeX source validation errors."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check_repository import (
    validate_components,
    validate_course,
    validate_integration_examples,
    validate_markdown_links,
    validate_source,
    validate_tracked_course_pdfs,
)


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

    def test_source_only_course_has_no_tracked_pdf_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
            main = root / "1" / "source-only" / "main.tex"
            main.parent.mkdir(parents=True)
            main.write_text(
                "\\documentclass{unipd-notes}\n"
                "\\begin{document}\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(("git", "add", "1/source-only/main.tex"), cwd=root, check=True)

            self.assertEqual(validate_course(main, root), [])
            self.assertEqual(validate_tracked_course_pdfs(root), [])

    def test_tracked_generated_course_pdf_is_rejected_with_removal_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
            pdf = root / "2" / "algorithms" / "main.pdf"
            pdf.parent.mkdir(parents=True)
            pdf.write_bytes(b"pdf")
            subprocess.run(
                ("git", "add", "-f", "2/algorithms/main.pdf"), cwd=root, check=True
            )

            errors = validate_tracked_course_pdfs(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("2/algorithms/main.pdf", errors[0])
            self.assertIn("must not be committed", errors[0])
            self.assertIn("build the PDF locally", errors[0])
            self.assertIn("notes-latest release", errors[0])
            self.assertIn(
                "git rm --cached -- 2/algorithms/main.pdf", errors[0]
            )

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

            uppercase = root / "3" / "Invalid Course" / "main.tex"
            uppercase.parent.mkdir(parents=True)
            uppercase.write_text(
                "\\documentclass{unipd-notes}\n"
                "\\begin{document}\n\\end{document}\n",
                encoding="utf-8",
            )
            errors = validate_course(uppercase, root)
            self.assertTrue(any("lowercase kebab-case" in error for error in errors))

    def test_component_validation_requires_exact_package_and_example_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            component = root / "latex" / "components" / "code"
            example = component / "example"
            example.mkdir(parents=True)
            (component / "code.sty").write_text("package\n", encoding="utf-8")
            (example / "main.tex").write_text("source\n", encoding="utf-8")
            (example / "main.pdf").write_bytes(b"pdf")

            self.assertEqual(validate_components(root), [])

            invalid_component = root / "latex" / "components" / "Invalid Component"
            invalid_example = invalid_component / "example"
            invalid_example.mkdir(parents=True)
            (invalid_component / "Invalid Component.sty").write_text(
                "package\n", encoding="utf-8"
            )
            (invalid_example / "main.tex").write_text("source\n", encoding="utf-8")
            (invalid_example / "main.pdf").write_bytes(b"pdf")
            errors = validate_components(root)
            self.assertTrue(any("lowercase kebab-case" in error for error in errors))

            (example / "main.log").write_text("temporary\n", encoding="utf-8")
            errors = validate_components(root)
            self.assertTrue(any("unexpected component example" in error for error in errors))

    def test_integration_projects_require_source_pdf_and_readme(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            integration = root / "latex" / "integration"
            english = integration / "english"
            english.mkdir(parents=True)
            (english / "main.tex").write_text(
                "\\documentclass[english]{unipd-notes}\n", encoding="utf-8"
            )

            errors = validate_integration_examples(root)
            self.assertTrue(any("missing required file" in error for error in errors))
            self.assertTrue(
                any("missing integration example" in error for error in errors)
            )

            (english / "main.pdf").write_bytes(b"pdf")
            (english / "README.md").write_text("# English\n", encoding="utf-8")
            italian = integration / "italian"
            italian.mkdir()
            (italian / "main.tex").write_text(
                "\\documentclass[italian]{unipd-notes}\n", encoding="utf-8"
            )
            (italian / "main.pdf").write_bytes(b"pdf")
            (italian / "README.md").write_text("# Italiano\n", encoding="utf-8")
            self.assertEqual(validate_integration_examples(root), [])

            (english / "main.log").write_text("log\n", encoding="utf-8")
            errors = validate_integration_examples(root)
            self.assertTrue(
                any("unexpected integration entry" in error for error in errors)
            )

    def test_markdown_link_validation_reports_missing_local_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            docs = root / "docs"
            docs.mkdir()
            (docs / "target.md").write_text("# Target\n", encoding="utf-8")
            page = docs / "page.md"
            page.write_text(
                "[Valid](target.md#section)\n"
                "[External](https://example.com)\n"
                "[Missing](missing.md)\n",
                encoding="utf-8",
            )

            errors = validate_markdown_links(page, root)

            self.assertEqual(len(errors), 1)
            self.assertIn("page.md:3", errors[0])
            self.assertIn("missing.md", errors[0])

    def test_source_hygiene_errors_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.tex"
            source.write_bytes(b"<<<<<<< HEAD\r\n\tcontent  ")

            errors = validate_source(source, root)

            self.assertTrue(any("LF line endings" in error for error in errors))
            self.assertTrue(any("end with a newline" in error for error in errors))
            self.assertTrue(any("merge-conflict" in error for error in errors))
            self.assertTrue(any("tab characters" in error for error in errors))
            self.assertTrue(any("trailing whitespace" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
