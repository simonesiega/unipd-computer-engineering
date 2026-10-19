"""Generate one complete Git changelog for every course archive."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from urllib.parse import quote

YEARS = ("1", "2", "3")
CHANGELOG_DIRECTORY = "CHANGELOG"
BASELINE_FILENAME = "BASELINE"
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")


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
        ("git", *arguments),
        cwd=root,
        check=True,
        capture_output=True,
    )
    return result.stdout.decode("utf-8", errors="surrogateescape")


def parse_history(output: str) -> list[Commit]:
    """Parse NUL-delimited headers and unquoted name-status records from Git."""
    if output and not output.endswith("\0"):
        raise ValueError("Git changelog output must be NUL-terminated")
    fields = output.split("\0")
    commits: list[Commit] = []
    cursor = 0
    while cursor < len(fields) - 1:
        # An empty token marks each header; Git paths cannot contain NULs.
        if fields[cursor] or len(fields) - cursor < 5:
            raise ValueError("Could not parse Git changelog commit metadata")
        sha, committed_at, subject = fields[cursor + 1:cursor + 4]
        if COMMIT_SHA.fullmatch(sha) is None:
            raise ValueError("Could not parse Git changelog commit metadata")
        cursor += 4

        changes: list[FileChange] = []
        while cursor < len(fields) - 1 and fields[cursor]:
            status = fields[cursor].removeprefix("\n")
            expected_paths = 2 if status[:1] in {"R", "C"} else 1
            paths = fields[cursor + 1:cursor + 1 + expected_paths]
            if (
                re.fullmatch(r"[ACDMRTUXB][0-9]*", status) is None
                or len(paths) != expected_paths
                or not all(paths)
            ):
                raise ValueError(f"Could not parse Git name-status record: {status!r}")
            changes.append(FileChange(status, tuple(paths)))
            cursor += 1 + expected_paths

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


def baseline_path(root: Path) -> Path:
    """Return the tracked changelog-baseline path."""
    return root / CHANGELOG_DIRECTORY / BASELINE_FILENAME


def read_baseline(root: Path) -> str | None:
    """Read and validate the optional changelog baseline commit."""
    path = baseline_path(root)
    if not path.exists():
        return None
    baseline = path.read_text(encoding="utf-8").strip()
    if COMMIT_SHA.fullmatch(baseline) is None:
        raise ValueError(f"Invalid changelog baseline in {path}: {baseline!r}")
    try:
        run_git(root, "cat-file", "-e", f"{baseline}^{{commit}}")
        run_git(root, "merge-base", "--is-ancestor", baseline, "HEAD")
    except subprocess.CalledProcessError as error:
        raise ValueError(
            f"Changelog baseline is not an ancestor of HEAD: {baseline}"
        ) from error
    return baseline


def reset_baseline(root: Path) -> str:
    """Set the changelog baseline to HEAD and return its full commit ID."""
    ensure_complete_history(root)
    baseline = run_git(root, "rev-parse", "HEAD").strip()
    if COMMIT_SHA.fullmatch(baseline) is None:
        raise ValueError(f"Git returned an invalid HEAD commit ID: {baseline!r}")
    (root / CHANGELOG_DIRECTORY).mkdir(parents=True, exist_ok=True)
    baseline_path(root).write_text(baseline + "\n", encoding="utf-8", newline="\n")
    return baseline


def read_history(root: Path, baseline: str | None = None) -> list[Commit]:
    """Read degree-year commits, optionally only those after *baseline*."""
    ensure_complete_history(root)
    revision = f"{baseline}..HEAD" if baseline else "HEAD"
    output = run_git(
        root,
        "log",
        "--format=%x00%H%x00%cI%x00%s",
        "--name-status",
        "-z",
        "--find-renames",
        revision,
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


def visible_text(value: str) -> str:
    """Display control characters as escapes rather than Markdown line breaks."""
    return "".join(
        character if character.isprintable() else repr(character)[1:-1]
        for character in value
    )


def markdown_code(value: str) -> str:
    """Wrap a short value with safe Markdown inline-code delimiters."""
    value = visible_text(value)
    delimiter = "`" * (max((len(run) for run in re.findall(r"`+", value)), default=0) + 1)
    padding = " " if value.startswith("`") or value.endswith("`") else ""
    return f"{delimiter}{padding}{value}{padding}{delimiter}"


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
        subject = visible_text(commit.subject).replace("\\", "\\\\").replace("`", "\\`")
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
    """Keep a tracked placeholder only when the directory is otherwise empty."""
    path.mkdir(parents=True, exist_ok=True)
    keep_file = path / ".gitkeep"
    if any(entry != keep_file for entry in path.iterdir()):
        keep_file.unlink(missing_ok=True)
    elif not keep_file.exists():
        keep_file.write_text("", encoding="utf-8", newline="\n")


def write_changelogs(
    root: Path,
    histories: dict[tuple[str, str], list[CourseCommit]],
    repository_url: str | None,
) -> None:
    """Synchronize generated files and all required placeholder directories."""
    changelog_root = root / CHANGELOG_DIRECTORY
    changelog_root.mkdir(parents=True, exist_ok=True)
    for year in YEARS:
        ensure_preserved_directory(root / year)
        year_directory = changelog_root / year
        year_directory.mkdir(parents=True, exist_ok=True)

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

    for year in YEARS:
        ensure_preserved_directory(changelog_root / year)
    ensure_preserved_directory(changelog_root)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository-url",
        help="Base URL used for commit links (defaults to the origin remote)",
    )
    parser.add_argument(
        "--reset-baseline",
        action="store_true",
        help="start future changelogs after the current HEAD commit",
    )
    return parser.parse_args()


def main() -> int:
    """Generate all course changelogs from the current branch history."""
    arguments = parse_arguments()
    root = repository_root()
    repository_url = arguments.repository_url or discover_repository_url(root)
    baseline = reset_baseline(root) if arguments.reset_baseline else read_baseline(root)
    histories = build_course_histories(read_history(root, baseline))
    write_changelogs(root, histories, repository_url)
    suffix = f" after baseline {baseline[:7]}" if baseline else ""
    print(f"Generated {len(histories)} course changelog(s){suffix}.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
