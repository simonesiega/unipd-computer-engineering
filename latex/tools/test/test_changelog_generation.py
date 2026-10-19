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
    build_course_histories,
    markdown_code,
    parse_history,
    read_baseline,
    read_history,
    render_changelog,
    reset_baseline,
    write_changelogs,
)


class ChangelogGenerationTests(unittest.TestCase):
    def test_real_git_history_preserves_quoted_paths_and_control_characters(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            environment = {
                **os.environ,
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_AUTHOR_DATE": "2026-08-01T09:00:00Z",
                "GIT_COMMITTER_DATE": "2026-08-01T09:00:00Z",
            }

            def git(*arguments: str, data: bytes | None = None) -> bytes:
                return subprocess.run(
                    ("git", *arguments), cwd=root, env=environment, input=data,
                    capture_output=True, check=True,
                ).stdout

            git("init", "--quiet")
            git("config", "user.name", "Test Author")
            git("config", "user.email", "test@example.com")
            # Populate only the index: these Git paths need not be valid host filenames.
            git("config", "core.protectNTFS", "false")
            blob = git("hash-object", "-w", "--stdin", data=b"source\n").decode().strip()
            paths = (
                "1/course/continuità.tex", "1/course/figure 1.tex",
                '1/course/quoted"input.tex', "1/course/tab\tinput.tex",
                "1/course/line\ninput.tex", "1/course/carriage\rinput.tex",
                "1/course/record\x1einput.tex", "1/course/field\x1finput.tex",
            )
            git(
                "update-index", "-z", "--index-info",
                data="".join(f"100644 {blob}\t{path}\0" for path in paths).encode(),
            )
            subject = "Add inputs with \x1e and \x1f separators"
            git("commit", "--quiet", "--message", subject)

            history = read_history(root)

            self.assertEqual(len(history), 1)
            self.assertEqual(history[0].subject, subject)
            self.assertEqual(
                {change.paths for change in history[0].changes},
                {(path,) for path in paths},
            )
            histories = build_course_histories(history)
            self.assertEqual(set(histories), {("1", "course")})
            self.assertEqual(len(histories[("1", "course")][0].changes), len(paths))
            rendered = render_changelog(("1", "course"), histories[("1", "course")], None)
            for control in ("\t", "\r", "\x1e", "\x1f"):
                self.assertNotIn(control, rendered)
            self.assertIn(r"`line\ninput.tex`", rendered)

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

    def test_history_can_start_after_a_baseline_commit(self) -> None:
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
            baseline = subprocess.run(
                ("git", "rev-parse", "HEAD"),
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            ).stdout.strip()
            main_file.write_text("second\n", encoding="utf-8", newline="\n")
            self._commit(root, "Revise course", "2026-08-02T09:00:00Z")

            history = read_history(root, baseline)

            self.assertEqual([commit.subject for commit in history], ["Revise course"])

    def test_reset_baseline_records_head_and_can_be_read(self) -> None:
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
            tracked = root / "tracked.txt"
            tracked.write_text("content\n", encoding="utf-8", newline="\n")
            self._commit(root, "Initial commit", "2026-08-01T09:00:00Z")
            expected = subprocess.run(
                ("git", "rev-parse", "HEAD"),
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            ).stdout.strip()

            baseline = reset_baseline(root)

            self.assertEqual(baseline, expected)
            self.assertEqual(read_baseline(root), expected)
            self.assertEqual(
                (root / "CHANGELOG" / "BASELINE").read_text(encoding="utf-8"),
                expected + "\n",
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
        with (
            patch("generate_changelog.run_git", return_value="true\n") as git,
            self.assertRaisesRegex(ValueError, "shallow repository"),
        ):
            read_history(root)

        git.assert_called_once_with(
            root, "rev-parse", "--is-shallow-repository"
        )

    def test_history_is_split_by_course_and_includes_every_changed_file(self) -> None:
        newest_sha = "b" * 40
        oldest_sha = "a" * 40
        output = (
            f"\0{newest_sha}\0"
            "2026-08-02T10:00:00Z\0Revise limits\0\n"
            "M\x001/analisi-matematica-1/main.tex\0"
            "A\x001/analisi-matematica-1/sections/limits.tex\0"
            "M\x002/fisica-1/main.tex\0"
            f"\0{oldest_sha}\0"
            "2026-08-01T09:00:00+02:00\0Create course\0\n"
            "A\x001/analisi-matematica-1/main.tex\0"
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

    def test_renames_and_copies_are_recorded_in_both_course_histories(self) -> None:
        sha = "c" * 40
        for status, label in (("R100", "Renamed"), ("C100", "Copied")):
            with self.subTest(status=status):
                output = (
                    f"\0{sha}\0"
                    "2026-08-02T10:00:00Z\0Move course\0\n"
                    f"{status}\x001/old-course/main.tex\x002/new-course/main.tex\0"
                )
                histories = build_course_histories(parse_history(output))

                self.assertEqual(set(histories), {("1", "old-course"), ("2", "new-course")})
                for course, old, new in (
                    (("1", "old-course"), "main.tex", "2/new-course/main.tex"),
                    (("2", "new-course"), "1/old-course/main.tex", "main.tex"),
                ):
                    self.assertIn(
                        f"**{label}** `{old}` → `{new}`",
                        render_changelog(course, histories[course], None),
                    )

    def test_placeholders_follow_directory_contents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            course = root / "1" / "example"
            course.mkdir(parents=True)
            write_changelogs(root, {}, None)
            histories = build_course_histories(parse_history(
                f"\0{'a' * 40}\0"
                "2026-08-01T09:00:00Z\0Create course\0\n"
                "A\x001/example/main.tex\0"
            ))

            for _ in range(2):
                write_changelogs(root, histories, None)
                self.assertFalse((root / "1" / ".gitkeep").exists())
                self.assertFalse((root / "CHANGELOG" / ".gitkeep").exists())
                self.assertFalse((root / "CHANGELOG" / "1" / ".gitkeep").exists())
                self.assertTrue((root / "CHANGELOG" / "1" / "example.md").is_file())
                self.assertTrue((root / "CHANGELOG" / "2" / ".gitkeep").is_file())

            write_changelogs(root, {}, None)
            self.assertTrue((root / "CHANGELOG" / "1" / ".gitkeep").is_file())
            self.assertFalse((root / "CHANGELOG" / "1" / "example.md").exists())

    def test_history_parser_rejects_truncated_or_malformed_records(self) -> None:
        header = f"\0{'a' * 40}\0" + "2026-08-01T09:00:00Z\0Subject\0"
        for output in (
            header.removesuffix("\0"),
            "not-a-header\0",
            "\0short-sha\0date\0subject\0",
            header + "\nA\0",
            header + "\nR100\x001/old/main.tex\0",
            header + "\ninvalid\x001/course/main.tex\0",
        ):
            with self.subTest(output=output), self.assertRaises(ValueError):
                parse_history(output)
        self.assertEqual(parse_history(""), [])
        self.assertEqual(parse_history(header)[0].changes, ())

    def test_changelog_inline_code_preserves_backticks_and_control_characters(self) -> None:
        self.assertEqual(markdown_code("main.tex"), "`main.tex`")
        self.assertEqual(markdown_code("`input``.tex"), "``` `input``.tex ```")
        self.assertEqual(
            markdown_code("line\ninput\t\r\x1e\x1f.tex"),
            r"`line\ninput\t\r\x1e\x1f.tex`",
        )

    def test_required_empty_directories_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)

            write_changelogs(root, {}, None)

            for year in ("1", "2", "3"):
                self.assertTrue((root / year / ".gitkeep").is_file())
                self.assertTrue((root / "CHANGELOG" / year / ".gitkeep").is_file())
            self.assertFalse((root / "CHANGELOG" / ".gitkeep").exists())


if __name__ == "__main__":
    unittest.main()
