"""Generate one complete Git changelog for every course archive."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from urllib.parse import quote

YEARS = ("1", "2", "3")
CHANGELOG_DIRECTORY = "CHANGELOG"
RECORD_SEPARATOR = "\x1e"
FIELD_SEPARATOR = "\x1f"


@dataclass(frozen=True)
class FileChange:
    """A file status and its one or two associated repository paths."""

    status: str
    paths: tuple[str, ...]


@dataclass(frozen=True)
class Commit:
    """The course-related data from one Git commit."""

    sha: str
    committed_on: date
    subject: str
    changes: tuple[FileChange, ...]


@dataclass(frozen=True)
class CourseCommit:
    """The subset of one commit that belongs to a particular course."""

    commit: Commit
    changes: tuple[FileChange, ...]


def repository_root() -> Path:
    """Return the repository root."""
    return Path(__file__).resolve().parents[2]


def run_git(root: Path, *arguments: str) -> str:
    """Run Git in *root* and return UTF-8 output."""
    result = subprocess.run(
        ("git", "-c", "core.quotepath=false", *arguments),
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def parse_history(output: str) -> list[Commit]:
    """Parse the record-separated output produced by :func:`read_history`."""
    commits: list[Commit] = []
    for record in output.split(RECORD_SEPARATOR):
        record = record.lstrip("\n")
        if not record:
            continue

        header, separator, body = record.partition("\n")
        if not separator:
            body = ""
        fields = header.split(FIELD_SEPARATOR, maxsplit=2)
        if len(fields) != 3:
            raise ValueError("Could not parse Git changelog commit metadata")
        sha, committed_at, subject = fields

        changes: list[FileChange] = []
        for line in body.splitlines():
            if not line.strip():
                continue
            parts = line.split("\t")
            status = parts[0]
            expected_paths = 2 if status[:1] in {"R", "C"} else 1
            if len(parts) != expected_paths + 1:
                raise ValueError(f"Could not parse Git name-status line: {line!r}")
            changes.append(FileChange(status, tuple(parts[1:])))

        timestamp = datetime.fromisoformat(committed_at.replace("Z", "+00:00"))
        commits.append(Commit(sha, timestamp.date(), subject, tuple(changes)))
    return commits


def ensure_complete_history(root: Path) -> None:
    """Reject repositories whose available Git history is incomplete."""
    shallow = run_git(root, "rev-parse", "--is-shallow-repository").strip()
    if shallow == "true":
        raise ValueError(
            "Cannot generate changelogs from a shallow repository; "
            "fetch complete history with 'git fetch --unshallow' first"
        )
    if shallow != "false":
        raise ValueError(f"Unexpected Git shallow-repository status: {shallow!r}")


def read_history(root: Path) -> list[Commit]:
    """Read every commit that changed a degree-year archive."""
    ensure_complete_history(root)
    output = run_git(
        root,
        "log",
        f"--format={RECORD_SEPARATOR}%H{FIELD_SEPARATOR}%cI{FIELD_SEPARATOR}%s",
        "--name-status",
        "--find-renames",
        "HEAD",
        "--",
        *YEARS,
    )
    return parse_history(output)


def course_for_path(path: str) -> tuple[str, str] | None:
    """Return ``(year, course)`` for a path inside a course directory."""
    parts = PurePosixPath(path).parts
    if len(parts) < 3 or parts[0] not in YEARS:
        return None
    return parts[0], parts[1]


def build_course_histories(
    commits: list[Commit],
) -> dict[tuple[str, str], list[CourseCommit]]:
    """Split repository history into newest-first per-course histories."""
    histories: dict[tuple[str, str], list[CourseCommit]] = {}
    for commit in commits:
        course_changes: dict[tuple[str, str], list[FileChange]] = {}
        for change in commit.changes:
            courses = {
                course
                for path in change.paths
                if (course := course_for_path(path)) is not None
            }
            for course in courses:
                course_changes.setdefault(course, []).append(change)
        for course, changes in course_changes.items():
            histories.setdefault(course, []).append(
                CourseCommit(commit, tuple(changes))
            )
    return histories


def markdown_code(value: str) -> str:
    """Wrap a short value in Markdown inline-code delimiters."""
    delimiter = "``" if "`" in value else "`"
    return f"{delimiter}{value}{delimiter}"


def display_path(path: str, course: tuple[str, str]) -> str:
    """Return a path relative to *course* whenever it belongs to that course."""
    prefix = f"{course[0]}/{course[1]}/"
    return path.removeprefix(prefix)


def render_change(change: FileChange, course: tuple[str, str]) -> str:
    """Render one name-status record as a Markdown list item."""
    kind = change.status[:1]
    labels = {
        "A": "Added",
        "M": "Modified",
        "D": "Deleted",
        "T": "Type changed",
        "U": "Unmerged",
        "X": "Changed",
        "B": "Changed",
    }
    if kind in {"R", "C"}:
        action = "Renamed" if kind == "R" else "Copied"
        old_path, new_path = change.paths
        return (
            f"- **{action}** {markdown_code(display_path(old_path, course))} "
            f"→ {markdown_code(display_path(new_path, course))}"
        )

    action = labels.get(kind, "Changed")
    return f"- **{action}** {markdown_code(display_path(change.paths[0], course))}"


def render_changelog(
    course: tuple[str, str],
    history: list[CourseCommit],
    repository_url: str | None,
) -> str:
    """Render a course's complete history as Markdown."""
    year, slug = course
    lines = [
        "<!-- Generated by latex/tools/generate_changelog.py; do not edit. -->",
        "",
        f"# Changelog: {slug}",
        "",
        f"Committed changes for {markdown_code(f'{year}/{slug}')} and every file below it.",
        "",
        "Newest changes appear first.",
    ]
    current_date: date | None = None
    base_url = repository_url.rstrip("/") if repository_url else None

    for course_commit in history:
        commit = course_commit.commit
        if commit.committed_on != current_date:
            current_date = commit.committed_on
            lines.extend(
                [
                    "",
                    f"## {current_date.day}/{current_date.month}/{current_date.year}",
                ]
            )

        short_sha = commit.sha[:7]
        commit_label = markdown_code(short_sha)
        if base_url:
            commit_label = f"[{commit_label}]({base_url}/commit/{quote(commit.sha)})"
        subject = commit.subject.replace("\\", "\\\\").replace("`", "\\`")
        lines.extend(["", f"### {commit_label} — {subject}", ""])
        lines.extend(render_change(change, course) for change in course_commit.changes)

    return "\n".join(lines) + "\n"


def normalize_repository_url(remote: str) -> str | None:
    """Convert a common Git remote syntax to an HTTPS repository URL."""
    remote = remote.strip()
    if not remote:
        return None
    if remote.startswith("git@") and ":" in remote:
        host_and_path = remote[4:]
        host, path = host_and_path.split(":", maxsplit=1)
        remote = f"https://{host}/{path}"
    elif remote.startswith("ssh://git@"):
        remote = "https://" + remote[len("ssh://git@") :].replace(":", "/", 1)
    if remote.startswith(("https://", "http://")):
        return remote.removesuffix(".git").rstrip("/")
    return None


def discover_repository_url(root: Path) -> str | None:
    """Return the normalized origin URL when the repository has one."""
    try:
        remote = run_git(root, "config", "--get", "remote.origin.url")
    except subprocess.CalledProcessError:
        return None
    return normalize_repository_url(remote)


def ensure_preserved_directory(path: Path) -> None:
    """Create a directory and its tracked empty-directory placeholder."""
    path.mkdir(parents=True, exist_ok=True)
    keep_file = path / ".gitkeep"
    if not keep_file.exists():
        keep_file.write_text("", encoding="utf-8", newline="\n")


def write_changelogs(
    root: Path,
    histories: dict[tuple[str, str], list[CourseCommit]],
    repository_url: str | None,
) -> None:
    """Synchronize generated files and all required placeholder directories."""
    changelog_root = root / CHANGELOG_DIRECTORY
    ensure_preserved_directory(changelog_root)
    for year in YEARS:
        ensure_preserved_directory(root / year)
        year_directory = changelog_root / year
        ensure_preserved_directory(year_directory)

        expected = {
            year_directory / f"{slug}.md"
            for history_year, slug in histories
            if history_year == year
        }
        for stale_file in year_directory.glob("*.md"):
            if stale_file not in expected:
                stale_file.unlink()

    for course, history in sorted(histories.items()):
        year, slug = course
        output = changelog_root / year / f"{slug}.md"
        output.write_text(
            render_changelog(course, history, repository_url),
            encoding="utf-8",
            newline="\n",
        )


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository-url",
        help="Base URL used for commit links (defaults to the origin remote)",
    )
    return parser.parse_args()


def main() -> int:
    """Generate all course changelogs from the current branch history."""
    arguments = parse_arguments()
    root = repository_root()
    repository_url = arguments.repository_url or discover_repository_url(root)
    histories = build_course_histories(read_history(root))
    write_changelogs(root, histories, repository_url)
    print(f"Generated {len(histories)} course changelog(s).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
