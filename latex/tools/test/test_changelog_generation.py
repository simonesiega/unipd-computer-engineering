"""Test Git history parsing and per-course changelog generation."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from generate_changelog import (
    FIELD_SEPARATOR,
    RECORD_SEPARATOR,
    build_course_histories,
    parse_history,
    read_history,
    render_changelog,
    write_changelogs,
)


class ChangelogGenerationTests(unittest.TestCase):
    def test_real_git_history_is_read_newest_first(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
            subprocess.run(
                ("git", "config", "user.name", "Test Author"),
                cwd=root,
                check=True,
            )
            subprocess.run(
                ("git", "config", "user.email", "test@example.com"),
                cwd=root,
                check=True,
            )
            subprocess.run(
                ("git", "config", "core.autocrlf", "false"),
                cwd=root,
                check=True,
            )
            course = root / "1" / "analisi-matematica-1"
            course.mkdir(parents=True)
            main_file = course / "main.tex"
            main_file.write_text("first\n", encoding="utf-8", newline="\n")
            self._commit(root, "Create course", "2026-08-01T09:00:00Z")
            main_file.write_text("second\n", encoding="utf-8", newline="\n")
            self._commit(root, "Revise course", "2026-08-02T09:00:00Z")

            history = read_history(root)

            self.assertEqual(
                [commit.subject for commit in history],
                ["Revise course", "Create course"],
            )
            self.assertEqual(history[0].changes[0].status, "M")
            self.assertEqual(
                history[0].changes[0].paths,
                ("1/analisi-matematica-1/main.tex",),
            )

    @staticmethod
    def _commit(root: Path, subject: str, timestamp: str) -> None:
        subprocess.run(("git", "add", "."), cwd=root, check=True)
        environment = os.environ.copy()
        environment["GIT_AUTHOR_DATE"] = timestamp
        environment["GIT_COMMITTER_DATE"] = timestamp
        subprocess.run(
            ("git", "commit", "--quiet", "--message", subject),
            cwd=root,
            env=environment,
            check=True,
        )

    def test_shallow_repository_is_rejected_before_reading_history(self) -> None:
        root = Path("repository")
        with patch("generate_changelog.run_git", return_value="true\n") as git:
            with self.assertRaisesRegex(ValueError, "shallow repository"):
                read_history(root)

        git.assert_called_once_with(
            root, "rev-parse", "--is-shallow-repository"
        )

    def test_history_is_split_by_course_and_includes_every_changed_file(self) -> None:
        newest_sha = "b" * 40
        oldest_sha = "a" * 40
        output = (
            f"{RECORD_SEPARATOR}{newest_sha}{FIELD_SEPARATOR}"
            f"2026-08-02T10:00:00Z{FIELD_SEPARATOR}Revise limits\n\n"
            "M\t1/analisi-matematica-1/main.tex\n"
            "A\t1/analisi-matematica-1/sections/limits.tex\n"
            "M\t2/fisica-1/main.tex\n"
            f"{RECORD_SEPARATOR}{oldest_sha}{FIELD_SEPARATOR}"
            f"2026-08-01T09:00:00+02:00{FIELD_SEPARATOR}Create course\n\n"
            "A\t1/analisi-matematica-1/main.tex\n"
        )

        histories = build_course_histories(parse_history(output))

        self.assertEqual(
            set(histories),
            {("1", "analisi-matematica-1"), ("2", "fisica-1")},
        )
        analysis_history = histories[("1", "analisi-matematica-1")]
        self.assertEqual(len(analysis_history), 2)
        self.assertEqual(len(analysis_history[0].changes), 2)

        rendered = render_changelog(
            ("1", "analisi-matematica-1"),
            analysis_history,
            "https://github.com/example/notes",
        )
        self.assertIn("## 2/8/2026", rendered)
        self.assertIn("## 1/8/2026", rendered)
        self.assertIn(f"/commit/{newest_sha}", rendered)
        self.assertIn("**Modified** `main.tex`", rendered)
        self.assertIn("**Added** `sections/limits.tex`", rendered)

    def test_rename_is_recorded_in_both_course_histories(self) -> None:
        sha = "c" * 40
        output = (
            f"{RECORD_SEPARATOR}{sha}{FIELD_SEPARATOR}"
            f"2026-08-02T10:00:00Z{FIELD_SEPARATOR}Move course\n\n"
            "R100\t1/old-course/main.tex\t2/new-course/main.tex\n"
        )

        histories = build_course_histories(parse_history(output))

        self.assertIn(("1", "old-course"), histories)
        self.assertIn(("2", "new-course"), histories)

    def test_required_empty_directories_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)

            write_changelogs(root, {}, None)

            for year in ("1", "2", "3"):
                self.assertTrue((root / year / ".gitkeep").is_file())
                self.assertTrue((root / "CHANGELOG" / year / ".gitkeep").is_file())
            self.assertTrue((root / "CHANGELOG" / ".gitkeep").is_file())


if __name__ == "__main__":
    unittest.main()
