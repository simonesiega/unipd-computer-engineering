"""Test mapping changed repository paths to affected LaTeX documents."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build import (
    TocEntry,
    affected_documents,
    discover_documents,
    document_language,
    process_document,
    render_generated_markdown,
)


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
            integration = self.create_document(root, "latex/integration/english")

            self.assertEqual(
                discover_documents(root), sorted([course, example, integration])
            )

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

    def test_generated_readme_uses_document_language(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            document = Path(temporary_directory) / "main.tex"
            document.write_text(
                "\\documentclass[bibliography,english]{unipd-notes}\n",
                encoding="utf-8",
            )
            entries = [TocEntry("chapter", "Introduction", "1")]

            language = document_language(document)
            markdown = render_generated_markdown(entries, language)

            self.assertEqual(language, "english")
            self.assertIn("[Open the compiled PDF](main.pdf)", markdown)
            self.assertIn("## Table of contents", markdown)
            self.assertIn("Introduction — p. 1", markdown)

            italian = render_generated_markdown(entries, "italian")
            self.assertIn("[Apri il PDF compilato](main.pdf)", italian)
            self.assertIn("## Indice dei contenuti", italian)
            self.assertIn("Introduction — p. 1", italian)

            self.assertIn(
                "- No numbered entries.",
                render_generated_markdown([], "english"),
            )
            self.assertIn(
                "- Nessuna voce numerata.",
                render_generated_markdown([], "italian"),
            )

    def test_integration_build_generates_localized_readme(self) -> None:
        cases = (
            ("english", "Open the compiled PDF", "Table of contents", "Introduction"),
            (
                "italian",
                "Apri il PDF compilato",
                "Indice dei contenuti",
                "Introduzione",
            ),
        )
        for language, pdf_label, contents_label, chapter in cases:
            with tempfile.TemporaryDirectory() as tmp, self.subTest(language=language):
                root = Path(tmp)
                document = self.create_document(root, f"latex/integration/{language}")
                document.write_text(
                    f"\\documentclass[{language}]{{unipd-notes}}\n",
                    encoding="utf-8",
                )
                (document.parent / "main.pdf").write_bytes(b"pdf")
                toc = root / f".build/latex/integration/{language}/main.toc"
                toc.parent.mkdir(parents=True)
                toc.write_text(
                    f"\\contentsline {{chapter}}"
                    f"{{\\numberline {{1}}{chapter}}}{{1}}{{chapter.1}}%\n",
                    encoding="utf-8",
                )

                process_document(
                    root,
                    document,
                    compile_enabled=False,
                    readme_enabled=True,
                    check_generated=False,
                )

                readme = (document.parent / "README.md").read_text(encoding="utf-8")
                self.assertIn(f"[{pdf_label}](main.pdf)", readme)
                self.assertIn(f"## {contents_label}", readme)
                self.assertIn(f"{chapter} — p. 1", readme)

    def test_integration_change_selects_its_document(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            integration = self.create_document(root, "latex/integration/english")

            affected = affected_documents(
                root, [Path("latex/integration/english/main.tex")]
            )

            self.assertEqual(affected, [integration])


if __name__ == "__main__":
    unittest.main()
