"""Test public-site staging and rendered links without MkDocs or network access."""

from __future__ import annotations

import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_docs


class DocumentationSiteTests(unittest.TestCase):
    @staticmethod
    def write(root: Path, name: str, content: str = "# Page\n") -> Path:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def public_repository(self, root: Path) -> None:
        for name in build_docs.ROOT_DOCUMENTS:
            self.write(root, name)
        self.write(
            root,
            "mkdocs.yml",
            "site_name: Test\nsite_url: https://example.com/project/\n",
        )
        self.write(root, "docs/guides/README.md")
        self.write(root, "docs/assets/logo.png", "image")
        self.write(root, "docs/assets/site.css", "body {}\n")
        self.write(root, ".agents/skills/example/SKILL.md")
        self.write(root, "latex/README.md")
        self.write(root, "latex/LATEX.md")
        self.write(root, "latex/tools/TOOLS.md")
        self.write(root, "latex/tools/test/TESTS.md")
        self.write(root, "latex/components/README.md")
        self.write(root, "latex/components/COMPONENTS.md")
        self.write(root, "latex/fonts/README.md")
        self.write(root, "latex/fonts/FONTS.md")
        self.write(root, "latex/fonts/FONT-LICENSE.md")
        self.write(root, "latex/integration/english/README.md")
        self.write(root, "latex/integration/italian/README.md")
        self.write(root, ".github/PULL_REQUEST_TEMPLATE.md", "## Summary\n")
        self.write(root, "CHANGELOG/1/example.md")
        self.write(root, "CHANGELOG/BASELINE", "a" * 40)
        self.write(root, "CHANGELOG/2/.gitkeep", "")
        self.write(root, "1/example/README.md", "# Example course\n")
        self.write(
            root, "1/example/main.tex", "\\unipdsetup{course = {Example course}}\n"
        )

    def test_stage_excludes_private_state_sources_fonts_and_pdfs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            for name in (
                ".context/private.md",
                ".build/private.md",
                ".env",
                "latex/fonts/example.otf",
                "1/example/main.pdf",
            ):
                self.write(root, name, "private")
            build_docs.stage_documents(root, stage)
            self.assertTrue((stage / "1/example/README.md").is_file())
            self.assertTrue((stage / "LICENSE.md").is_file())
            self.assertTrue((stage / "docs/assets/logo.png").is_file())
            self.assertTrue((stage / "courses.md").is_file())
            self.assertTrue((stage / "3/README.md").is_file())
            for name in (
                ".context/private.md",
                ".build/private.md",
                ".env",
                "latex/fonts/example.otf",
                "1/example/main.pdf",
            ):
                self.assertFalse((stage / name).exists(), name)

    def test_latex_structure_tools_and_test_catalogues_are_public_pages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            documents = {
                "latex/README.md": "# LaTeX overview\n\n[Structure](LATEX.md)\n",
                "latex/LATEX.md": "# LaTeX structure\n\n[Tools](tools/TOOLS.md)\n",
                "latex/components/COMPONENTS.md": (
                    "# Components\n\n[Fonts](../fonts/FONTS.md)\n"
                ),
                "latex/fonts/FONTS.md": (
                    "# Fonts\n\n[Components](../components/COMPONENTS.md)\n"
                ),
                "latex/tools/TOOLS.md": "# Tools\n\n[Tests](test/TESTS.md)\n",
                "latex/tools/test/TESTS.md": (
                    "# Tests\n\n[Source](test_build_selection.py)\n"
                ),
            }
            for name, content in documents.items():
                self.write(root, name, content)
            self.write(
                root,
                "docs/README.md",
                "# Documentation\n" + "".join(
                    f"[Reference](../{name})\n" for name in documents
                ),
            )
            self.write(root, "latex/tools/test/test_build_selection.py")
            self.write(root, "latex/tools/private.md")
            build_docs.stage_documents(root, stage)
            index = (stage / "docs/README.md").read_text(encoding="utf-8")
            for name, content in documents.items():
                self.assertTrue((stage / name).is_file(), name)
                self.assertIn(f"(../{name})", index)
                self.assertEqual((root / name).read_text(encoding="utf-8"), content)
                if name != "latex/tools/test/TESTS.md":
                    self.assertEqual((stage / name).read_text(encoding="utf-8"), content)
            self.assertIn(
                f"{build_docs.REPOSITORY_URL}/blob/main/latex/tools/test/test_build_selection.py",
                (stage / "latex/tools/test/TESTS.md").read_text(encoding="utf-8"),
            )
            self.assertFalse((stage / "latex/tools/private.md").exists())
            self.assertFalse((stage / "latex/tools/test/test_build_selection.py").exists())

    def test_nested_private_directories_are_not_published(self) -> None:
        for name in (
            "docs/.context/private.md",
            "docs/assets/.build/private.md",
            ".agents/skills/.venv/private.md",
            "CHANGELOG/.context/private.md",
        ):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "repo"
                stage = Path(directory) / "stage"
                self.public_repository(root)
                self.write(root, name, "private")
                build_docs.stage_documents(root, stage)
                self.assertFalse((stage / build_docs.site_path(Path(name))).exists())

    def test_long_fences_preserve_nested_examples_and_resume_prose(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            build_docs.stage_documents(root, stage)
            for marker in ("`", "~"):
                with self.subTest(marker=marker):
                    example = (
                        f"{marker * 4}markdown\n"
                        f"{marker * 3}text\n[Literal](absent.md)\n"
                        f"{marker * 3}\n[Still literal](absent.md)\n"
                        f"{marker * 4}not-a-closing-fence\n"
                        f"[Also literal](absent.md)\n{marker * 5}\n"
                    )
                    content = example + "[License](LICENSE)\n"
                    self.assertEqual(
                        build_docs.rewrite_document(
                            root, stage, Path("README.md"), content
                        ),
                        example + "[License](LICENSE.md)\n",
                    )

    def test_links_resolve_to_staged_pages_or_github_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            self.write(root, "latex/components/code/example/main.tex")
            self.write(
                root,
                "README.md",
                (
                    "# Home\n[Guides](docs/guides/)\n[Year](1/)\n"
                    "[Course](1/example/)\n[License](LICENSE)\n"
                    "[Source](latex/components/code/example/main.tex)\n"
                    '<a href="LICENSE-MIT">MIT</a>\n'
                    '<img src="docs/assets/logo.png">\n'
                    "[Remote](https://example.com/file.pdf)\n"
                    "```markdown\n[Literal](not-a-real-file.md)\n```\n"
                ),
            )
            build_docs.stage_documents(root, stage)
            content = (stage / "README.md").read_text(encoding="utf-8")
            self.assertIn("(docs/guides/README.md)", content)
            self.assertIn("(1/README.md)", content)
            self.assertIn("(1/example/README.md)", content)
            self.assertIn("(LICENSE.md)", content)
            self.assertIn("/blob/main/latex/components/code/example/main.tex", content)
            self.assertIn('href="LICENSE-MIT.html"', content)
            self.assertIn('src="docs/assets/logo.png"', content)
            self.assertIn("[Literal](not-a-real-file.md)", content)
            self.assertIn("(https://example.com/file.pdf)", content)
            self.assertEqual(
                (root / "README.md").read_text(encoding="utf-8").count("[Literal]"), 1
            )

    def release_catalogue(self, root: Path) -> str:
        newest = f"{build_docs.REPOSITORY_URL}/releases/download/week-02/1-example.pdf"
        older = (
            f"{build_docs.REPOSITORY_URL}/releases/download/notes-latest/1-example.pdf"
        )
        self.write(
            root,
            "RELEASES.md",
            f"# Releases\n\n[Newest]({newest})\n[Older rolling]({older})\n",
        )
        return newest

    def test_reader_routes_and_unpublished_courses(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            build_docs.stage_documents(root, stage)
            reader = (stage / "example/README.md").read_text(encoding="utf-8")
            self.assertIn("# Example course", reader)
            self.assertIn("No PDF has been published", reader)
            self.assertIn("(../1/example/README.md)", reader)
            self.assertNotIn("<iframe", reader)
            self.assertIn(
                "(example/README.md)",
                (stage / "courses.md").read_text(encoding="utf-8"),
            )

    def test_readers_cover_all_years_and_escape_course_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            for year in (2, 3):
                self.write(root, f"{year}/course-{year}/README.md")
                self.write(
                    root,
                    f"{year}/course-{year}/main.tex",
                    '\\unipdsetup{course = {A <course> & "notes"}}\n',
                )
            build_docs.stage_documents(root, stage)
            for year in (2, 3):
                reader = (stage / f"course-{year}/README.md").read_text(
                    encoding="utf-8"
                )
                self.assertIn("A &lt;course&gt; &amp; &quot;notes&quot;", reader)
                self.assertIn(f"(../{year}/course-{year}/README.md)", reader)
                index = (stage / str(year) / "README.md").read_text(encoding="utf-8")
                self.assertIn(f"(../course-{year}/README.md)", index)

    def test_latest_pdf_follows_catalogue_order_not_rolling_tag_preference(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            newest = self.release_catalogue(root)
            pdfs = build_docs.published_pdfs(root)
            self.assertEqual(pdfs[(1, "example")].download_url, newest)
            self.assertEqual(pdfs[(1, "example")].filename, "1-example.pdf")

    def test_reader_without_downloads_links_to_release_but_does_not_embed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            newest = self.release_catalogue(root)
            with patch.object(build_docs, "urlopen") as request:
                build_docs.stage_documents(root, stage)
            request.assert_not_called()
            reader = (stage / "example/README.md").read_text(encoding="utf-8")
            self.assertIn(newest, reader)
            self.assertIn("--with-pdfs", reader)
            self.assertNotIn("<iframe", reader)
            self.assertFalse((stage / "pdfs").exists())

    def test_online_reader_embeds_an_unchanged_same_origin_release_copy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            self.release_catalogue(root)
            payload = b"%PDF-1.7\nreleased PDF bytes\n%%EOF\n"
            with patch.object(
                build_docs, "urlopen", return_value=io.BytesIO(payload)
            ) as request:
                build_docs.stage_documents(root, stage, with_pdfs=True)
            self.assertEqual((stage / "pdfs/1-example.pdf").read_bytes(), payload)
            reader = (stage / "example/README.md").read_text(encoding="utf-8")
            self.assertIn('<iframe class="course-pdf"', reader)
            self.assertIn('src="../pdfs/1-example.pdf?v=', reader)
            self.assertIn('download="1-example.pdf"', reader)
            self.assertIn('target="_blank" rel="noopener"', reader)
            self.assertIn("week-02", reader)
            self.assertEqual(request.call_count, 1)
            self.assertFalse((root / "1/example/main.pdf").exists())

    def test_reader_route_collisions_fail_without_overwriting_guides(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            self.write(root, "2/docs/main.tex", "\\unipdsetup{course = {Docs}}\n")
            self.write(root, "2/docs/README.md")
            with self.assertRaisesRegex(ValueError, "reader route"):
                build_docs.stage_documents(root, stage)
            self.assertTrue((stage / "docs/guides/README.md").is_file())

    def test_year_index_routes_cannot_be_used_by_course_readers(self) -> None:
        for year in build_docs.YEARS:
            with self.subTest(year=year), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "repo"
                stage = Path(directory) / "stage"
                self.public_repository(root)
                source_year = "2" if year == "1" else "1"
                self.write(root, f"{source_year}/{year}/README.md")
                self.write(root, f"{source_year}/{year}/main.tex")
                with self.assertRaisesRegex(ValueError, "reader route"):
                    build_docs.stage_documents(root, stage)

    def test_catalogue_rejects_untrusted_or_malformed_pdf_urls(self) -> None:
        for target in (
            "https://example.com/1-example.pdf",
            f"{build_docs.REPOSITORY_URL}/blob/main/1-example.pdf",
            f"{build_docs.REPOSITORY_URL}/releases/download/week-02/1-example.pdf?token=secret",
            f"{build_docs.REPOSITORY_URL}/releases/download/../1-example.pdf",
        ):
            with (
                self.subTest(target=target),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                self.write(root, "RELEASES.md", f"[PDF]({target})\n")
                with self.assertRaisesRegex(ValueError, "published PDF URL"):
                    build_docs.published_pdfs(root)

    def test_pdf_download_errors_and_non_pdf_responses_are_not_hidden(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.release_catalogue(root)
            pdf = build_docs.published_pdfs(root)[(1, "example")]
            destination = root / "output/1-example.pdf"
            with (
                patch.object(
                    build_docs,
                    "urlopen",
                    return_value=io.BytesIO(b"<html>error</html>"),
                ),
                self.assertRaisesRegex(ValueError, "PDF header"),
            ):
                build_docs.download_pdf(pdf, destination)
            self.assertFalse(destination.exists())
            with (
                patch.object(build_docs, "urlopen", side_effect=URLError("offline")),
                self.assertRaises(URLError),
            ):
                build_docs.download_pdf(pdf, destination)

    def test_complete_pdf_downloads_keep_exact_bytes_and_leave_no_temporary_file(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.release_catalogue(root)
            pdf = build_docs.published_pdfs(root)[(1, "example")]
            payload = b"%PDF-1.7\n" + b"0" * 4096 + b"\n%%EOF\n \t\r\n"
            response = io.BytesIO(payload)
            destination = root / "output/1-example.pdf"
            with (
                patch.object(
                    response,
                    "headers",
                    {"Content-Length": str(len(payload))},
                    create=True,
                ),
                patch.object(build_docs, "urlopen", return_value=response),
            ):
                build_docs.download_pdf(pdf, destination)
            self.assertEqual(destination.read_bytes(), payload)
            self.assertEqual(list(destination.parent.iterdir()), [destination])

    def test_incomplete_pdf_downloads_preserve_existing_copies(self) -> None:
        payload = b"%PDF-1.7\nreleased PDF bytes\n%%EOF\n"
        for status, data, length in (
            (206, payload, len(payload)),
            (200, payload, len(payload) + 10),
            (200, payload.removesuffix(b"%%EOF\n"), None),
        ):
            with (
                self.subTest(status=status, length=length),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                self.release_catalogue(root)
                pdf = build_docs.published_pdfs(root)[(1, "example")]
                destination = self.write(root, "output/1-example.pdf", "previous")
                response = io.BytesIO(data)
                headers = {} if length is None else {"Content-Length": str(length)}
                with (
                    patch.object(response, "status", status, create=True),
                    patch.object(response, "headers", headers, create=True),
                    patch.object(build_docs, "urlopen", return_value=response),
                    self.assertRaises(ValueError),
                ):
                    build_docs.download_pdf(pdf, destination)
                self.assertEqual(destination.read_bytes(), b"previous")
                self.assertEqual(list(destination.parent.iterdir()), [destination])

    def test_interrupted_pdf_copy_cleans_up_partial_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.release_catalogue(root)
            pdf = build_docs.published_pdfs(root)[(1, "example")]
            destination = root / "output/1-example.pdf"
            with (
                patch.object(build_docs, "urlopen", return_value=io.BytesIO(b"%PDF-")),
                patch.object(
                    build_docs.shutil, "copyfileobj", side_effect=OSError("interrupted")
                ),
                self.assertRaises(OSError),
            ):
                build_docs.download_pdf(pdf, destination)
            self.assertEqual(list(destination.parent.iterdir()), [])

    def test_rendered_validation_allows_only_named_release_pdf_copies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            self.write(
                site,
                "index.html",
                '<iframe src="pdfs/1-example.pdf?v=abc#view=FitH" title="PDF"></iframe>',
            )
            self.write(site, "pdfs/1-example.pdf", "%PDF-1.7\n%%EOF\n")
            self.assertEqual(build_docs.validate_site(site), [])
            self.write(site, "private.pdf", "%PDF-1.7\n%%EOF\n")
            self.assertTrue(
                any(
                    "Unexpected site file" in error
                    for error in build_docs.validate_site(site)
                )
            )

    def test_cli_enables_pdf_downloads_only_when_requested(self) -> None:
        for arguments, enabled in (([], False), (["--with-pdfs"], True)):
            with (
                patch.object(sys, "argv", ["build_docs.py", *arguments]),
                patch.object(build_docs, "build_site") as build,
            ):
                self.assertEqual(build_docs.main(), 0)
                self.assertEqual(build.call_args.kwargs["with_pdfs"], enabled)

    def test_public_aliases_keep_original_source_relative_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            self.write(
                root,
                "README.md",
                "# Home\n[Template](.github/PULL_REQUEST_TEMPLATE.md)\n[Skill](.agents/skills/example/SKILL.md)\n",
            )
            self.write(
                root, ".github/PULL_REQUEST_TEMPLATE.md", "[Home](../README.md)\n"
            )
            self.write(
                root, ".agents/skills/example/SKILL.md", "[Home](../../../README.md)\n"
            )
            build_docs.stage_documents(root, stage)
            home = (stage / "README.md").read_text(encoding="utf-8")
            self.assertIn("(PULL_REQUEST_TEMPLATE.md)", home)
            self.assertIn("(agents/skills/example/SKILL.md)", home)
            self.assertEqual(
                (stage / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8"),
                "[Home](README.md)\n",
            )
            self.assertFalse((stage / ".github").exists())
            self.assertFalse((stage / ".agents").exists())
            self.assertEqual(
                (root / ".github/PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8"),
                "[Home](../README.md)\n",
            )

    def test_unpublished_local_builds_are_not_linked_as_site_assets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            self.write(root, "README.md", "# Home\n[Private](.context/private.md)\n")
            self.write(root, ".context/private.md", "secret")
            with self.assertRaisesRegex(ValueError, "Private documentation link"):
                build_docs.stage_documents(root, stage)

    def test_unexpected_assets_and_missing_links_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            bad = self.write(root, "docs/assets/secrets.txt", "secret")
            with self.assertRaisesRegex(ValueError, "Unexpected documentation file"):
                build_docs.stage_documents(root, stage)
            bad.unlink()
            self.write(root, "README.md", "# Home\n[Missing](absent.md)\n")
            with self.assertRaisesRegex(ValueError, "Missing documentation target"):
                build_docs.stage_documents(root, stage)

    def test_course_index_discovers_years_and_escapes_names(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(
                root, "2/another/main.tex", "\\unipdsetup{course = {A [course]}}\n"
            )
            self.write(root, "2/another/README.md")
            content = build_docs.course_index(root)
            self.assertIn("2027–2028", content)
            self.assertIn(r"[A \[course\]](another/README.md)", content)
            self.assertIn("[Contents and sources](2/another/README.md)", content)
            self.assertIn("No course sources yet.", content)
            self.assertNotIn("covered", content)

    def test_private_and_traversing_public_inputs_are_rejected(self) -> None:
        for name in (".context/private.md", "docs/.venv/private.md", "../outside.md"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "repo"
                source = self.write(root, name, "private")
                with self.assertRaisesRegex(ValueError, "Private or unsafe"):
                    build_docs.public_file(root, source)

    def test_symlinked_parent_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            self.public_repository(root)
            source = root / "docs/guides/README.md"
            original = Path.is_symlink
            with (
                patch.object(
                    Path,
                    "is_symlink",
                    lambda path: path == root / "docs" or original(path),
                ),
                self.assertRaisesRegex(ValueError, "symlink"),
            ):
                build_docs.public_file(root, source)

    def test_missing_public_file_and_symlinked_tree_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "Missing public documentation"):
                build_docs.public_file(root, root / "missing.md")
            with (
                patch.object(Path, "is_symlink", lambda path: path == root / "docs"),
                self.assertRaisesRegex(ValueError, "symlink"),
            ):
                build_docs.tree_files(root, root / "docs")

    def test_link_traversal_outside_repository_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            stage = Path(directory) / "stage"
            self.public_repository(root)
            self.write(root, "README.md", "# Home\n[Outside](../outside.md)\n")
            self.write(Path(directory), "outside.md")
            with self.assertRaisesRegex(ValueError, "outside the repository"):
                build_docs.stage_documents(root, stage)

    def test_built_links_queries_images_and_anchors_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            self.write(
                site,
                "index.html",
                '<a href="guide.html?view=1#topic">Guide</a><img src="logo.png"><a href="https://example.com">Remote</a>',
            )
            self.write(
                site,
                "guide.html",
                '<h2 id="topic">Topic</h2><a href="index.html">Home</a>',
            )
            self.write(site, "logo.png", "image")
            self.assertEqual(build_docs.validate_site(site), [])

    def test_project_site_root_urls_resolve_without_escaping_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            self.write(
                site,
                "index.html",
                '<link rel="canonical" href="https://example.com/project/index.html"><h1 id="home">Home</h1>',
            )
            self.write(site, "404.html", '<a href="/project/index.html#home">Home</a>')
            self.assertEqual(build_docs.validate_site(site), [])
            self.assertEqual(build_docs.validate_site(site, "/project/"), [])
            self.write(
                site,
                "404.html",
                '<a href="https://example.com/project/index.html#home">Home</a>'
                '<a href="//example.com/project/index.html#home">Home</a>'
                '<a href="https://example.com/another-project/">External project</a>'
                '<a href="https://elsewhere.test/project/missing.html">External</a>',
            )
            self.assertEqual(build_docs.validate_site(site), [])
            for target, diagnostic in (
                ("https://example.com/project/missing.html", "Missing site target"),
                ("https://example.com/project/index.html#absent", "Missing site anchor"),
                ("//example.com/project/missing.html", "Missing site target"),
            ):
                with self.subTest(target=target):
                    self.write(site, "404.html", f'<a href="{target}">Broken</a>')
                    self.assertTrue(
                        any(diagnostic in error for error in build_docs.validate_site(site))
                    )
            self.write(
                site, "404.html", '<a href="/elsewhere/index.html">Wrong site</a>'
            )
            self.assertTrue(
                any(
                    "outside the site" in error
                    for error in build_docs.validate_site(site, "/project/")
                )
            )

    def test_built_missing_targets_anchors_and_traversal_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            self.write(
                site,
                "index.html",
                '<a href="missing.html">Missing</a><a href="#absent">Anchor</a><img src="../outside.png">',
            )
            errors = build_docs.validate_site(site)
            self.assertEqual(len(errors), 3)
            self.assertTrue(any("Missing site target" in error for error in errors))
            self.assertTrue(any("Missing site anchor" in error for error in errors))
            self.assertTrue(any("outside the site" in error for error in errors))

    def test_missing_build_and_unexpected_public_files_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            self.assertTrue(build_docs.validate_site(site))
            self.write(site, "index.html", "<h1>Home</h1>")
            self.write(site, "private.tex", "source")
            self.assertTrue(
                any(
                    "Unexpected site file" in error
                    for error in build_docs.validate_site(site)
                )
            )

    def test_rendered_symlinks_are_rejected_without_reading_them(self) -> None:
        original_read = Path.read_text
        for name in ("", "index.html", "linked.html"):
            with (
                self.subTest(name=name),
                tempfile.TemporaryDirectory() as directory,
            ):
                site = Path(directory).resolve()
                self.write(site, "index.html", "<h1>Home</h1>")
                linked = self.write(site, name, "private") if name else site

                def guarded_read(
                    path: Path, encoding: str = "utf-8", rejected: Path = linked
                ) -> str:
                    self.assertNotEqual(path, rejected, "Read a rejected symlink")
                    return original_read(path, encoding=encoding)

                with (
                    patch.object(
                        Path, "is_symlink", lambda path, rejected=linked: path == rejected
                    ),
                    patch.object(Path, "read_text", guarded_read),
                ):
                    errors = build_docs.validate_site(site)
                self.assertTrue(any("Unexpected site file" in error for error in errors))

    def test_build_uses_strict_mkdocs_and_validates_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.public_repository(root)
            self.write(root, "mkdocs.yml", "site_name: Test\n")
            self.write(root, ".build/docs-site/index.html", "<h1>Home</h1>")
            with patch.object(build_docs.subprocess, "run") as run:
                build_docs.build_site(root)
            self.assertIn("--strict", run.call_args.args[0])
            self.assertTrue(run.call_args.kwargs["check"])
            self.assertIn("UNIPD_DOCS_DIR", run.call_args.kwargs["env"])
            self.assertNotEqual(
                run.call_args.kwargs["env"]["UNIPD_DOCS_DIR"], str(root)
            )

    def test_build_failures_and_symlinked_output_are_not_hidden(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.public_repository(root)
            with (
                patch.object(
                    build_docs.subprocess,
                    "run",
                    side_effect=subprocess.CalledProcessError(1, "mkdocs"),
                ),
                self.assertRaises(subprocess.CalledProcessError),
            ):
                build_docs.build_site(root)
            with (
                patch.object(build_docs.subprocess, "run"),
                self.assertRaisesRegex(ValueError, "Missing site homepage"),
            ):
                build_docs.build_site(root)
            original = Path.is_symlink
            with (
                patch.object(
                    Path,
                    "is_symlink",
                    lambda path: path == root / ".build" or original(path),
                ),
                self.assertRaisesRegex(ValueError, "symlink"),
            ):
                build_docs.build_site(root)

    def test_site_dependency_pins_match_the_precommit_hook(self) -> None:
        root = Path(__file__).resolve().parents[3]
        requirements = (
            (root / ".github/requirements-docs.txt")
            .read_text(encoding="utf-8")
            .splitlines()
        )
        config = (root / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        for requirement in requirements:
            if requirement and not requirement.startswith("#"):
                self.assertIn(requirement, config)

    def test_github_urls_quote_spaces_and_directory_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "fonts/Source Sans 3/font.otf")
            self.assertIn(
                "/blob/main/fonts/Source%20Sans%203/font.otf",
                build_docs.github_target(root, root / "fonts/Source Sans 3/font.otf"),
            )
            self.assertIn(
                "/tree/main/fonts", build_docs.github_target(root, root / "fonts")
            )
            self.assertEqual(
                build_docs.html_path(Path("1/example/README.md")),
                Path("1/example/index.html"),
            )


if __name__ == "__main__":
    unittest.main()
