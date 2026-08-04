"""Test deterministic packaging of compiled course-note releases."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from package_notes import (
    CHECKSUMS_NAME,
    MANIFEST_NAME,
    RELEASE_NOTES_NAME,
    asset_filename,
    course_identity,
    package_release,
    sha256_file,
    slugify,
)


class NotesPackagingTests(unittest.TestCase):
    SOURCE_COMMIT = "a" * 40
    TIMESTAMP = "2026-08-04T12:00:00+00:00"

    @staticmethod
    def create_course(
        root: Path, year: int, slug: str, name: str, pdf: bytes | None = b"pdf"
    ) -> Path:
        course = root / str(year) / slug
        course.mkdir(parents=True)
        main = course / "main.tex"
        main.write_text(
            "\\documentclass{unipd-notes}\n"
            "\\unipdsetup{\n"
            f"  course = {{{name}}},\n"
            f"  degree-year = {{{year}}}\n"
            "}\n"
            "\\begin{document}\\end{document}\n",
            encoding="utf-8",
        )
        if pdf is not None:
            built = root / ".build" / str(year) / slug / "main.pdf"
            built.parent.mkdir(parents=True)
            built.write_bytes(pdf)
        return main

    def test_slug_and_asset_names_are_url_safe_and_stable(self) -> None:
        self.assertEqual(slugify("Probabilità e Statistica"), "probabilita-e-statistica")
        self.assertEqual(asset_filename(1, "calculus-1"), "1-calculus-1.pdf")
        with self.assertRaisesRegex(ValueError, "kebab-case"):
            asset_filename(1, "Invalid Course")
        with self.assertRaisesRegex(ValueError, "degree year"):
            asset_filename(4, "course")

    def test_manifest_checksums_and_ordering_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.create_course(root, 2, "zoology", "Zoology", b"second")
            self.create_course(root, 1, "linear-algebra", "Linear Algebra", b"first-b")
            self.create_course(root, 1, "calculus-1", "Calculus 1", b"first-a")
            output = root / ".build" / "release"

            assets = package_release(
                root,
                output,
                self.SOURCE_COMMIT,
                self.TIMESTAMP,
                "Snapshot",
                "Test description.",
            )
            first_contents = {
                path.name: path.read_bytes() for path in sorted(output.iterdir())
            }
            package_release(
                root,
                output,
                self.SOURCE_COMMIT,
                self.TIMESTAMP,
                "Snapshot",
                "Test description.",
            )
            second_contents = {
                path.name: path.read_bytes() for path in sorted(output.iterdir())
            }

            self.assertEqual(first_contents, second_contents)
            self.assertEqual(
                [asset.asset_filename for asset in assets],
                ["1-calculus-1.pdf", "1-linear-algebra.pdf", "2-zoology.pdf"],
            )
            manifest = json.loads((output / MANIFEST_NAME).read_text(encoding="utf-8"))
            self.assertEqual(manifest["source_commit"], self.SOURCE_COMMIT)
            self.assertEqual(manifest["release_timestamp"], self.TIMESTAMP)
            self.assertEqual(
                [course["course_name"] for course in manifest["courses"]],
                ["Calculus 1", "Linear Algebra", "Zoology"],
            )
            first_course = manifest["courses"][0]
            self.assertEqual(first_course["degree_year"], 1)
            self.assertEqual(first_course["course_slug"], "calculus-1")
            self.assertEqual(first_course["source_directory"], "1/calculus-1")
            self.assertEqual(first_course["file_size"], len(b"first-a"))
            self.assertEqual(
                first_course["sha256"], sha256_file(output / "1-calculus-1.pdf")
            )
            checksums = (output / CHECKSUMS_NAME).read_text(
                encoding="utf-8"
            ).splitlines()
            self.assertEqual(checksums, sorted(checksums, key=lambda line: line[66:]))
            for filename in (
                "1-calculus-1.pdf",
                "1-linear-algebra.pdf",
                "2-zoology.pdf",
                MANIFEST_NAME,
                RELEASE_NOTES_NAME,
            ):
                expected = f"{sha256_file(output / filename)}  {filename}"
                self.assertIn(expected, checksums)
            release_notes = (output / RELEASE_NOTES_NAME).read_text(encoding="utf-8")
            self.assertIn("# Snapshot", release_notes)
            self.assertIn("Test description.", release_notes)
            self.assertIn(self.SOURCE_COMMIT, release_notes)
            self.assertLess(
                release_notes.index("1-calculus-1.pdf"),
                release_notes.index("2-zoology.pdf"),
            )

    def test_missing_compiled_pdf_fails_without_partial_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.create_course(root, 1, "missing", "Missing", None)
            output = root / ".build" / "release"
            output.mkdir(parents=True)
            (output / "stale.pdf").write_bytes(b"stale")

            with self.assertRaisesRegex(FileNotFoundError, "Missing compiled course PDFs"):
                package_release(
                    root, output, self.SOURCE_COMMIT, self.TIMESTAMP
                )

            self.assertEqual(list(output.iterdir()), [])

    def test_invalid_course_paths_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            nested = root / "1" / "course" / "nested" / "main.tex"
            nested.parent.mkdir(parents=True)
            nested.write_text("source\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "expected <year>/<course>/main.tex"):
                course_identity(root, nested)
            with self.assertRaisesRegex(ValueError, "Invalid course path"):
                package_release(
                    root,
                    root / ".build" / "release",
                    self.SOURCE_COMMIT,
                    self.TIMESTAMP,
                )

    def test_duplicate_asset_names_are_rejected_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.create_course(root, 1, "course-a", "Course A")
            self.create_course(root, 1, "course-b", "Course B")
            output = root / ".build" / "release"

            with patch("package_notes.asset_filename", return_value="1-collision.pdf"):
                with self.assertRaisesRegex(ValueError, "Duplicate release asset name"):
                    package_release(
                        root, output, self.SOURCE_COMMIT, self.TIMESTAMP
                    )

            self.assertFalse((output / "1-collision.pdf").exists())

    def test_output_outside_owned_release_staging_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            unsafe = root / "release"
            unsafe.mkdir()
            marker = unsafe / "keep.txt"
            marker.write_text("keep\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "refusing to clean"):
                package_release(
                    root, unsafe, self.SOURCE_COMMIT, self.TIMESTAMP
                )

            self.assertTrue(marker.is_file())

    def test_empty_course_archive_generates_metadata_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            output = root / ".build" / "release"

            assets = package_release(
                root, output, self.SOURCE_COMMIT, self.TIMESTAMP
            )

            self.assertEqual(assets, [])
            manifest = json.loads((output / MANIFEST_NAME).read_text(encoding="utf-8"))
            self.assertEqual(manifest["courses"], [])
            self.assertIn(
                "No course PDFs are available",
                (output / RELEASE_NOTES_NAME).read_text(encoding="utf-8"),
            )
            self.assertTrue((output / CHECKSUMS_NAME).is_file())


if __name__ == "__main__":
    unittest.main()
