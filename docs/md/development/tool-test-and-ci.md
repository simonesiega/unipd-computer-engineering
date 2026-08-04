# Validation, Tests, and CI

[← Documentation](../README.md) · [Architecture](architecture.md) · [Build system](build-system.md) · [Building documents](../getting-started/building-documents.md)

The repository uses repository-specific validation, pre-commit hooks, Python unit tests, canonical Docker builds, pull-request artifacts, and GitHub Release publication. A separate `Course changelogs` workflow continues to generate weekly source histories.

## Local quality checks

Run the repository validator from the root:

```bash
python3 latex/tools/check_repository.py
```

On Windows PowerShell, use `py` instead of `python3`. The validator has no options and always checks the complete repository.

Reproduce the quality jobs with:

```bash
python3 -m pip install -r .github/requirements-ci.txt
pre-commit run --all-files --show-diff-on-failure
```

Pre-commit pins its hooks and tool dependencies. Dependabot monitors CI requirements, hooks, actions, and the canonical Docker image.

## Python tool tests

Tests use standard-library `unittest`, temporary directories and repositories, deterministic input, and no network access.

| Test file | Main responsibility |
|---|---|
| `test_course_creation.py` | Course slug, metadata, scaffold, duplicate, and argument validation |
| `test_build_selection.py` | Discovery, affected paths, TOC/README behavior, generated state, and rolling-release course links |
| `test_notes_packaging.py` | Asset/slug naming, collisions, manifests, checksums, ordering, missing PDFs, invalid paths, and empty archives |
| `test_release_catalog.py` | Release parsing, immutable-snapshot coverage, deduplication, ordering, README tables, and empty release history |
| `test_gitignore.py` | Specific course `main.pdf` ignore rules without globally ignoring PDFs |
| `test_changelog_generation.py` | Complete Git history, per-course changes, renames, dates, and placeholders |
| `test_repository_validation.py` | Layouts, Markdown links, source hygiene, and tracked generated-course-PDF rejection |

Run all tests:

```bash
python3 -m unittest discover -s latex/tools/test -p 'test_*.py'
```

Run one file directly, for example:

```bash
python3 latex/tools/test/test_notes_packaging.py
```

CI invokes `latex/tools/run_tool_tests.py`, which adds Coverage.py branch reporting and enforces the repository's 60% minimum.

## Pre-commit and repository validation

Pre-commit runs added-file-size, case-conflict, merge-conflict, YAML, final-newline, line-ending, trailing-whitespace, Actionlint, Ruff, mypy, tool tests/coverage, repository structure, and Markdown-link checks. Binary font, PDF, and image files remain excluded from text fixers where appropriate.

`check_repository.py` validates:

| Area | Checks |
|---|---|
| Courses | Direct `<year>/<course>/main.tex`, lowercase kebab-case, class declaration, and complete document environment |
| Tracked course outputs | No indexed `1/**/main.pdf`, `2/**/main.pdf`, or `3/**/main.pdf` |
| Components | Matching package plus `example/main.tex` and tracked `example/main.pdf` only |
| Integration examples | Localized `main.tex`, tracked `main.pdf`, and generated `README.md` only |
| Sources | UTF-8 `.tex`, `.sty`, `.cls`, and `.bib`; no tabs, trailing whitespace, or conflict markers |
| Documentation | Existing repository-relative Markdown link targets |

The generated-course-PDF rule queries `git ls-files`, not the local filesystem. Ignored local `.build/` output therefore does not fail validation, while a PDF forced into the index does. Its diagnostic names the file, explains local/release access, and gives `git rm --cached -- <path>` removal guidance.

## Workflow separation and security

`.github/workflows/ci.yml` handles pull requests and optional manual validation. `.github/workflows/publish-notes.yml` handles pushes to `main` and manually requested immutable snapshots. Actions are pinned to full commit SHAs. Pull-request jobs and all build/package jobs use `contents: read`; only the final trusted publisher job receives `contents: write`. The workflows do not use `pull_request_target`, expose repository secrets to pull-request code, or require custom secrets. GitHub CLI publication uses `GH_TOKEN: ${{ github.token }}`.

Concurrency cancels superseded validation on the same pull-request reference. Release runs are serialized and are not cancelled mid-publication. Before moving `notes-latest`, an older queued push run checks whether its commit is still current `main` and exits without rolling the release backward.

## Pull requests

The quality job runs every pre-commit hook. The build job checks out complete history, obtains the pull-request base, writes changed paths to `.build/changed-files.txt`, and lets `build.py` select affected documents. If a usable base is unavailable or the workflow is dispatched manually, it builds all documents.

The canonical command is either:

```bash
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py \
    --changed-file-list .build/changed-files.txt \
    --keep-going \
    --check-generated
```

or the complete fallback:

```bash
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py --all --keep-going --check-generated
```

Successful `.build/**/main.pdf` files are uploaded as `latex-pdfs-<commit-sha>`, without extra compression, for approximately 14 days. Reviewers download this temporary artifact from the workflow run; it is not a permanent publication. When compilation fails, `.log` and `.blg` files are uploaded as `latex-logs-<commit-sha>` for 7 days when available. A quality failure has no LaTeX logs because compilation never starts. Pull requests never create or modify a GitHub Release.

## Pushes to main and rolling release

Every push to `main` runs all quality checks and the complete canonical build, regardless of changed-file selection:

```bash
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py --all --keep-going --check-generated
```

The workflow injects the source SHA and its commit timestamp into `package_notes.py`, validates JSON, verifies every line in `SHA256SUMS.txt`, and transfers the clean `.build/release/` directory to the write-scoped publisher job. Build failure logs remain temporary and separate from permanent assets.

The publisher creates or updates the rolling release:

- tag: `notes-latest`;
- title: `Latest compiled notes`;
- stable URL: <https://github.com/simonesiega/unipd-computer-engineering/releases/tag/notes-latest>;
- source: the successfully packaged current `main` commit;
- assets: every staged PDF plus `manifest.json`, `SHA256SUMS.txt`, and `RELEASE_NOTES.md`.

The release is set to draft while assets are replaced. Uploads use clobber semantics, stale assets are deleted, the tag is force-moved to the source commit, and the release is made public only after every step succeeds. A failure leaves a draft rather than a falsely successful partial release. Repeating the same commit is idempotent: filenames and metadata remain stable and assets are replaced rather than duplicated. Deleted or renamed courses disappear because assets not present in staging are removed.

## Immutable manual snapshots

Run **Publish compiled notes** manually and provide:

- `release_tag`, such as `2026-2027-semester-1`;
- `release_title`;
- optional `release_description_file`, a repository-relative path to a committed Markdown file.

Copy the [snapshot description questionnaire](../release/example.md), answer each prompt, replace every bracketed placeholder, and remove sections that do not apply before publishing. The file input supports paragraphs, lists, links, and other structured release notes that GitHub's single-line `workflow_dispatch` fields cannot represent directly. The workflow validates that the path is relative, remains inside the checked-out repository, and identifies an existing file before copying it into release staging.

Preflight rejects unsafe identifiers, the reserved `notes-latest` tag, blank titles, and any existing matching tag or release. The workflow then performs the same quality checks, complete build, packaging, metadata validation, and checksums as the rolling release. It creates a new draft at the dispatch source commit, uploads assets, and publishes it. Generated release notes and `manifest.json` include the source SHA. Existing snapshots are never edited, moved, or overwritten.

Publishing an immutable snapshot explicitly marks every PDF in that snapshot as maintainer-approved and covered. Do not publish a snapshot containing incomplete or unreviewed notes. Rolling `notes-latest` assets never establish covered status by themselves.

If a snapshot upload fails, its draft intentionally remains non-public so partial assets are not presented as complete. Inspect it and the job output; if retrying the same requested tag is appropriate, the maintainer must explicitly delete only that failed draft and tag first. Never replace an already published snapshot.

## Asset contract

Course asset names are:

```text
<degree-year>-<canonical-course-directory-slug>.pdf
```

Examples include `1-calculus-1.pdf`, `1-linear-algebra.pdf`, and `2-algorithms-and-data-structures.pdf`. Names are lowercase kebab-case, shell/URL safe, deterministic across operating systems, and independent of temporary build paths. Collisions and invalid paths fail packaging.

`manifest.json` contains sorted course records with degree year, course name when available from `\unipdsetup`, course slug, source directory, asset filename, byte size, SHA-256, source SHA, and release timestamp. `SHA256SUMS.txt` covers every PDF, the manifest, and `RELEASE_NOTES.md`. The Markdown file provides the human-readable sorted index and licensing statement.

## Diagnosing failures

- **Quality:** run the reported pre-commit hook locally and inspect automatic fixes.
- **Compilation:** find the first meaningful LaTeX error and download the failure-log artifact.
- **Packaging:** confirm every source course has `.build/<year>/<course>/main.pdf`; inspect invalid paths, duplicate output names, JSON, and checksum output.
- **Rolling publication:** inspect the draft, stale-asset deletion, tag update, and final API call. A rerun is safe after correcting the cause.
- **Snapshot publication:** an existing tag/release is a deliberate hard failure; do not bypass it or overwrite a published snapshot.
- **Accidentally tracked course PDF:** run `git rm --cached -- <year>/<course>/main.pdf`; keep any desired local build under `.build/` and do not rewrite history.

## Generated README release catalogue

After publishing, the write-scoped job downloads all published release metadata with the GitHub API and runs `update_release_catalog.py`. Drafts are ignored. The tool deduplicates course asset names across immutable snapshots, counts covered exams by degree year, links each covered course to its newest immutable asset, and lists every published release with all matching course PDFs. It atomically replaces only the content between `<!-- RELEASE-CATALOG:START -->` and `<!-- RELEASE-CATALOG:END -->` in the root README.

When the catalogue changes, the workflow commits `README.md` as `github-actions[bot]` with `[skip ci]` and retries up to three times if `main` advances. The workflow token does not start another publication run for that bot commit. It therefore moves `notes-latest` to the catalogue commit after a successful push; course sources are unchanged, while the immutable semester tag remains attached to the build source commit.

The weekly `Course changelogs` workflow remains separate. It reads complete history, regenerates protected `CHANGELOG/<year>/<course>.md` files, and creates one recap commit only when content changes.
