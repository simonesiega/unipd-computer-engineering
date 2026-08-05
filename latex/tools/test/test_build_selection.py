"""Test mapping changed repository paths to affected LaTeX documents."""

from __future__ import annotations

import argparse
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build as build_module
from build import (
    TocEntry,
    affected_documents,
    course_release_pdf_target,
    discover_documents,
    document_language,
    generated_file_error,
    parse_toc,
    process_document,
    process_documents,
    render_generated_markdown,
    resolve_document,
    validate_arguments,
)


class BuildSelectionTests(unittest.TestCase):
    @staticmethod
    def create_document(root: Path, relative: str) -> Path:
        document = root / relative / "main.tex"
        document.parent.mkdir(parents=True)
        document.write_text("\\begin{document}\\end{document}\n", encoding="utf-8")
        return document.resolve()

    @staticmethod
    def arguments(**overrides: object) -> argparse.Namespace:
        values: dict[str, object] = {
            "targets": ["1/course"],
            "all": False,
            "changed_from": None,
            "changed_to": "HEAD",
            "changed_file_list": None,
            "no_compile": False,
            "no_readme": False,
            "clean": False,
            "keep_going": False,
            "check_generated": False,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def test_build_argument_validation_rejects_conflicting_modes(self) -> None:
        invalid_arguments = (
            self.arguments(no_compile=True, check_generated=True),
            self.arguments(no_readme=True, check_generated=True),
            self.arguments(targets=[], all=False),
            self.arguments(all=True),
        )
        invalid_arguments[-1].targets = ["1/course"]
        for arguments in invalid_arguments:
            with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                validate_arguments(arguments)

    def test_keep_going_collects_partial_build_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first = self.create_document(root, "1/first")
            second = self.create_document(root, "1/second")
            arguments = self.arguments(keep_going=True)

            with patch.object(
                build_module,
                "process_document",
                side_effect=[OSError("broken output"), None],
            ):
                failures = process_documents(root, [first, second], arguments)

            self.assertEqual(len(failures), 1)
            self.assertEqual(failures[0][0], Path("1/first/main.tex"))
            self.assertIn("broken output", str(failures[0][1]))

    def test_build_main_cleans_outputs_after_success(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            document = self.create_document(root, "1/course")
            build_directory = root / ".build"
            build_directory.mkdir()
            arguments = self.arguments(clean=True)
            with (
                patch.object(build_module, "parse_arguments", return_value=arguments),
                patch.object(build_module, "repository_root", return_value=root),
                patch.object(
                    build_module, "select_documents", return_value=[document]
                ),
                patch.object(
                    build_module, "process_documents", return_value=[]
                ),
            ):
                self.assertEqual(build_module.main(), 0)

            self.assertFalse(build_directory.exists())

    def test_build_main_reports_failures_and_empty_selection(self) -> None:
        arguments = self.arguments()
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            document = self.create_document(root, "1/course")
            with (
                patch.object(build_module, "parse_arguments", return_value=arguments),
                patch.object(build_module, "repository_root", return_value=root),
                patch.object(
                    build_module, "select_documents", return_value=[document]
                ),
                patch.object(
                    build_module,
                    "process_documents",
                    return_value=[(Path("1/course/main.tex"), OSError("failed"))],
                ),
                patch.object(build_module, "report_failures") as report,
            ):
                self.assertEqual(build_module.main(), 1)
                report.assert_called_once()

            with (
                patch.object(build_module, "parse_arguments", return_value=arguments),
                patch.object(build_module, "repository_root", return_value=root),
                patch.object(build_module, "select_documents", return_value=[]),
                self.assertRaisesRegex(RuntimeError, "No main.tex"),
            ):
                build_module.main()

    def test_changed_file_selection_can_be_a_valid_no_op(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            changed = root / "changed.txt"
            changed.write_text("README.md\n", encoding="utf-8")
            arguments = self.arguments(
                targets=[], changed_file_list=str(changed)
            )

            self.assertIsNone(build_module.select_documents(root, arguments))

    def test_document_discovery_finds_courses_and_component_examples(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = self.create_document(root, "1/course")
            example = self.create_document(root, "latex/components/code/example")
            integration = self.create_document(root, "latex/integration/english")

            self.assertEqual(
                discover_documents(root), sorted([course, example, integration])
            )

    def test_explicit_document_must_remain_inside_repository(self) -> None:
        with (
            tempfile.TemporaryDirectory() as repository_directory,
            tempfile.TemporaryDirectory() as external_directory,
        ):
            root = Path(repository_directory)
            external = self.create_document(Path(external_directory), "document")

            with self.assertRaisesRegex(ValueError, "inside the repository"):
                resolve_document(root, str(external))

    def test_course_change_selects_only_that_course(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            selected = self.create_document(root, "1/selected")
            self.create_document(root, "2/unaffected")

            affected = affected_documents(root, [Path("1/selected/sections/topic.tex")])

            self.assertEqual(affected, [selected])

    def test_shared_changes_select_every_document(self) -> None:
        shared_paths = (
            Path("compose.yaml"),
            Path(".github/workflows/ci.yml"),
            Path(".github/workflows/publish-notes.yml"),
            Path("latex/tools/build.py"),
            Path("latex/tools/latex_source.py"),
            Path("latex/unipd-notes.cls"),
            Path("latex/components/code/code.sty"),
            Path("latex/fonts/Example/font.otf"),
        )
        for changed_path in shared_paths:
            with self.subTest(path=changed_path), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                course = self.create_document(root, "1/course")
                component = self.create_document(
                    root, "latex/components/code/example"
                )
                integration = self.create_document(root, "latex/integration/english")

                affected = affected_documents(root, [changed_path])

                self.assertEqual(
                    affected, sorted([course, component, integration])
                )

    def test_component_change_selects_only_its_example(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            component = self.create_document(root, "latex/components/code/example")
            self.create_document(root, "latex/components/lists/example")

            affected = affected_documents(
                root, [Path("latex/components/code/example/main.tex")]
            )

            self.assertEqual(affected, [component])

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

    def test_document_language_ignores_commented_class_declarations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            document = Path(temporary_directory) / "main.tex"
            document.write_text(
                "% \\documentclass[english]{unipd-notes}\n"
                "\\documentclass[italian]{unipd-notes}\n",
                encoding="utf-8",
            )

            self.assertEqual(document_language(document), "italian")

    def test_toc_parser_handles_nested_formatting_and_ignores_unknown_levels(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            toc = Path(temporary_directory) / "main.toc"
            toc.write_text(
                "\\contentsline {chapter}{\\numberline {1}"
                "A \\textbf{formatted} \\& escaped title}{7}{chapter.1}%\n"
                "\\contentsline {paragraph}{Ignored}{8}{paragraph.1}%\n",
                encoding="utf-8",
            )

            self.assertEqual(
                parse_toc(toc),
                [TocEntry("chapter", "1 A formatted & escaped title", "7")],
            )

    def test_generated_file_comparison_detects_missing_and_stale_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            generated = root / "generated.pdf"
            committed = root / "committed.pdf"
            generated.write_bytes(b"current")

            missing_error = generated_file_error(generated, committed)
            self.assertIsNotNone(missing_error)
            assert missing_error is not None
            self.assertIn("not tracked", missing_error)
            committed.write_bytes(b"stale")
            stale_error = generated_file_error(generated, committed)
            self.assertIsNotNone(stale_error)
            assert stale_error is not None
            self.assertIn("stale", stale_error)
            committed.write_bytes(b"current")
            self.assertIsNone(generated_file_error(generated, committed))

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

    def test_no_compile_preserves_readme_when_toc_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            document = self.create_document(root, "1/course")
            built_pdf = root / ".build/1/course/main.pdf"
            built_pdf.parent.mkdir(parents=True)
            built_pdf.write_bytes(b"pdf")
            readme = document.parent / "README.md"
            original = (
                "# Course\n\n<!-- GENERATED:START -->\n"
                "Existing index\n<!-- GENERATED:END -->\n"
            )
            readme.write_text(original, encoding="utf-8")

            with self.assertRaisesRegex(FileNotFoundError, "Table of contents"):
                process_document(
                    root,
                    document,
                    compile_enabled=False,
                    readme_enabled=True,
                    check_generated=False,
                )

            self.assertEqual(readme.read_text(encoding="utf-8"), original)

    def test_course_readme_links_to_rolling_release_asset(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            document = self.create_document(root, "2/algorithms-and-data-structures")
            built = root / ".build/2/algorithms-and-data-structures"
            built.mkdir(parents=True)
            (built / "main.pdf").write_bytes(b"pdf")
            (built / "main.toc").write_text(
                "\\contentsline {chapter}{Introduction}{1}{chapter.1}%\n",
                encoding="utf-8",
            )

            process_document(
                root,
                document,
                compile_enabled=False,
                readme_enabled=True,
                check_generated=False,
            )

            target = course_release_pdf_target(root, document)
            self.assertEqual(
                target,
                "https://github.com/simonesiega/unipd-computer-engineering/"
                "releases/download/notes-latest/"
                "2-algorithms-and-data-structures.pdf",
            )
            readme = (document.parent / "README.md").read_text(encoding="utf-8")
            self.assertIn(f"]({target})", readme)
            self.assertFalse((document.parent / "main.pdf").exists())

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
