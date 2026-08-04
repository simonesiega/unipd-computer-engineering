"""Test repository ignore rules for generated course PDFs."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


class GitignoreTests(unittest.TestCase):
    def test_only_generated_course_main_pdfs_are_ignored(self) -> None:
        repository_root = Path(__file__).resolve().parents[3]
        rules = (repository_root / ".gitignore").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / ".gitignore").write_text(rules, encoding="utf-8")
            subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
            paths = (
                "1/calculus/main.pdf",
                "2/algorithms/main.pdf",
                "3/networks/main.pdf",
                "1/calculus/reference.pdf",
                "latex/components/code/example/main.pdf",
            )
            for relative in paths:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"pdf")

            ignored = subprocess.run(
                ("git", "check-ignore", *paths),
                cwd=root,
                check=False,
                stdout=subprocess.PIPE,
                text=True,
            ).stdout.splitlines()

            self.assertEqual(ignored, list(paths[:3]))


if __name__ == "__main__":
    unittest.main()
