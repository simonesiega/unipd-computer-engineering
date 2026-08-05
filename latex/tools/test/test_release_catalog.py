"""Test README catalogues generated from published GitHub Releases."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from update_release_catalog import (
    END_MARKER,
    START_MARKER,
    covered_courses,
    parse_releases,
    render_catalog,
    update_readme,
)


class ReleaseCatalogTests(unittest.TestCase):
    @staticmethod
    def release(
        tag: str,
        published_at: str,
        assets: list[str],
        *,
        draft: bool = False,
    ) -> dict[str, object]:
        return {
            "tag_name": tag,
            "name": f"Release {tag}",
            "html_url": f"https://example.test/releases/{tag}",
            "published_at": published_at,
            "draft": draft,
            "assets": [
                {
                    "name": name,
                    "browser_download_url": f"https://example.test/{tag}/{name}",
                }
                for name in assets
            ],
        }

    def test_parser_handles_slurped_pages_and_ignores_drafts_and_non_course_assets(self) -> None:
        data = [
            [
                self.release(
                    "2026-2027-semester-1",
                    "2027-02-01T10:00:00Z",
                    ["1-calculus-1.pdf", "manifest.json"],
                )
            ],
            [
                self.release(
                    "draft-snapshot",
                    "2027-03-01T10:00:00Z",
                    ["1-hidden.pdf"],
                    draft=True,
                )
            ],
        ]

        releases = parse_releases(data)

        self.assertEqual([release.tag for release in releases], ["2026-2027-semester-1"])
        self.assertEqual([pdf.filename for pdf in releases[0].pdfs], ["1-calculus-1.pdf"])

    def test_parser_rejects_non_array_release_and_asset_data(self) -> None:
        with self.assertRaisesRegex(TypeError, "Release data"):
            parse_releases({})

        invalid_assets = self.release(
            "snapshot",
            "2027-01-01T10:00:00Z",
            [],
        )
        invalid_assets["assets"] = {}
        with self.assertRaisesRegex(TypeError, "Release assets"):
            parse_releases([invalid_assets])

    def test_only_immutable_snapshots_cover_exams_and_duplicates_are_removed(self) -> None:
        releases = parse_releases(
            [
                self.release(
                    "notes-latest",
                    "2027-03-01T10:00:00Z",
                    ["1-in-progress.pdf"],
                ),
                self.release(
                    "2026-2027-semester-2",
                    "2027-02-01T10:00:00Z",
                    ["1-calculus-1.pdf", "2-algorithms.pdf"],
                ),
                self.release(
                    "2026-2027-semester-1",
                    "2027-01-01T10:00:00Z",
                    ["1-calculus-1.pdf"],
                ),
            ]
        )

        covered = covered_courses(releases)

        self.assertEqual(set(covered), {(1, "calculus-1"), (2, "algorithms")})
        self.assertEqual(covered[(1, "calculus-1")].download_url, "https://example.test/2026-2027-semester-2/1-calculus-1.pdf")

    def test_catalog_contains_counts_courses_and_every_published_release(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "1" / "calculus-1"
            course.mkdir(parents=True)
            (course / "main.tex").write_text(
                "\\unipdsetup{course = {Analisi Matematica 1}}\n",
                encoding="utf-8",
            )
            releases = parse_releases(
                [
                    self.release(
                        "notes-latest",
                        "2027-02-02T10:00:00Z",
                        ["1-calculus-1.pdf", "1-in-progress.pdf"],
                    ),
                    self.release(
                        "2026-2027-semester-1",
                        "2027-02-01T10:00:00Z",
                        ["1-calculus-1.pdf"],
                    ),
                ]
            )

            catalog = render_catalog(root, releases)

            self.assertIn("| First year | 1 |", catalog)
            self.assertIn("| **Total** | **1** |", catalog)
            self.assertIn("Analisi Matematica 1", catalog)
            self.assertNotIn("In Progress |", catalog)
            self.assertIn("`notes-latest`", catalog)
            self.assertIn("`2026-2027-semester-1`", catalog)
            releases_table = catalog[catalog.index("## Releases") :]
            self.assertLess(
                releases_table.index("notes-latest"),
                releases_table.index("2026-2027-semester-1"),
            )

    def test_empty_catalog_and_atomic_readme_update(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            readme = root / "README.md"
            readme.write_text(
                f"Before\n{START_MARKER}\nold\n{END_MARKER}\nAfter\n",
                encoding="utf-8",
            )
            catalog = render_catalog(root, [])

            self.assertTrue(update_readme(readme, catalog))
            content = readme.read_text(encoding="utf-8")
            self.assertIn("No exams covered yet", content)
            self.assertIn("No releases published yet", content)
            self.assertTrue(content.startswith("Before\n"))
            self.assertTrue(content.endswith("\nAfter\n"))
            self.assertFalse(update_readme(readme, catalog))


if __name__ == "__main__":
    unittest.main()
