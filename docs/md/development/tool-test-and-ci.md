# Validation, Tests, and CI

[← Documentation](../README.md) · [Architecture](architecture.md) · [Build system](build-system.md) · [Building documents](../getting-started/building-documents.md)

The repository uses three complementary validation layers: direct repository checks, pre-commit hooks, and the `LaTeX CI` GitHub Actions workflow. Compilation and generated-file verification remain responsibilities of the build system. A separate `Course changelogs` workflow publishes a weekly recap of per-course Git histories.

## Local validation

Run the repository-specific validator from the repository root.

Linux or macOS:

```bash
python3 latex/tools/check_repository.py
```

Windows PowerShell:

```powershell
py latex/tools/check_repository.py
```

`check_repository.py` has no command-line options; it always validates the complete repository.

To reproduce the complete CI quality job, install the pinned CI dependency and run every pre-commit hook:

Linux or macOS:

```bash
python3 -m pip install -r .github/requirements-ci.txt
pre-commit run --all-files --show-diff-on-failure
```

Windows PowerShell:

```powershell
py -m pip install -r .github/requirements-ci.txt
pre-commit run --all-files --show-diff-on-failure
```

Here, pip's `-r` option installs from the requirements file, `--all-files` checks the complete repository instead of only changed files, and `--show-diff-on-failure` prints modifications made by a failing hook. The CI requirements currently pin `pre-commit` to version `4.3.0`.

## Python tool tests

Tests for the repository’s Python tools are organized by responsibility under `latex/tools/test/`:

| Test file | Tool covered | Behavior covered |
|---|---|---|
| `test_course_creation.py` | `create_course.py` | Slug generation, academic years, generated layout and metadata, duplicate detection, and argument-domain validation |
| `test_build_selection.py` | `build.py` | Document discovery, affected-document selection, and localized integration README generation |
| `test_changelog_generation.py` | `generate_changelog.py` | History parsing, per-course file changes, renames, dates, commits, and empty-directory placeholders |
| `test_repository_validation.py` | `check_repository.py` | Course entry-point structure, complete integration-project files, and LaTeX source-hygiene errors |

Run the complete test suite from the repository root.

Linux or macOS:

```bash
python3 -m unittest discover -s latex/tools/test -p 'test_*.py'
```

Windows PowerShell:

```powershell
py -m unittest discover -s latex/tools/test -p 'test_*.py'
```

`discover` enables test discovery, `-s latex/tools/test` selects its starting directory, and `-p 'test_*.py'` selects test filenames.

Run one focused test file by passing its path directly. Replace the filename with any of the other test files listed above when needed.

Linux or macOS:

```bash
python3 latex/tools/test/test_course_creation.py
```

Windows PowerShell:

```powershell
py latex/tools/test/test_course_creation.py
```

The tests use only the Python standard library. Temporary repositories are created for file-system tests and removed automatically; the working repository is not modified.

## Pre-commit checks

The pre-commit configuration requires version `3.7.0` or newer and runs these general checks:

| Check | Purpose |
|---|---|
| Added large files | Reject files larger than 10 MiB |
| Case conflicts | Detect filenames that conflict on case-insensitive filesystems |
| Merge conflicts | Detect unresolved conflict markers |
| YAML | Validate YAML syntax |
| End of file | Ensure text files end with a newline |
| Line endings | Normalize text files to LF |
| Trailing whitespace | Remove trailing spaces |

Font, PDF, and PNG files are excluded from text-only fixes where appropriate.

The local `course-tool-tests` hook runs the complete `latex/tools/test/` suite when a Python tool, tool test, or the pre-commit configuration changes. The `latex-repository-check` hook runs `latex/tools/check_repository.py` for changes under the course directories, `latex/`, workflow files, or the pre-commit configuration. Both hooks receive no individual filenames; the test hook runs the complete tool suite, and the repository hook validates the repository as a whole.

## Repository-specific checks

`check_repository.py` validates:

| Area | Checks |
|---|---|
| Courses | Entry points are direct `<year>/<course>/main.tex` files under `1/`, `2/`, or `3/` |
| Course documents | `main.tex` declares a document class and contains a complete document environment |
| Components | Each component contains `<component>.sty` and `example/` |
| Component examples | Each `example/` contains exactly `main.tex` and `main.pdf` |
| Integration examples | Each directory under `latex/integration/` contains exactly `main.tex` and `main.pdf` |
| LaTeX sources | `.tex`, `.sty`, `.cls`, and `.bib` files are valid UTF-8 |
| Source hygiene | No tabs, trailing whitespace, or unresolved merge-conflict markers |

The validator ignores `.git/` and `.build/`. Empty directory structure is preserved through tracked `.gitkeep` placeholders, but their presence is not required by the validator.

## Workflow triggers

`.github/workflows/ci.yml` defines the `LaTeX CI` workflow. It runs on:

| Event | Scope |
|---|---|
| Pull request | The proposed pull-request changes |
| Push to `main` | Changes introduced by the push |
| Manual dispatch | A complete build |

The workflow has read-only repository permissions. Checkout credentials are not persisted.

Only one run for the same workflow and Git reference remains active. A newer run cancels an older in-progress run for that reference.

`.github/workflows/changelog.yml` runs every Sunday at 00:00 UTC and on manual dispatch. Scheduled runs use the default branch. The workflow has write access only to repository contents, checks out complete history, generates course changelogs, and creates one recap commit only when generated files changed. Ordinary pushes do not run this workflow, so several commits made during the week are consolidated into one changelog update. If the default branch changes while the workflow is running, it fetches and resets to the latest version, regenerates the changelogs, and retries the commit and push, for up to three attempts.

## Quality job

The `Quality` job:

1. runs on Ubuntu 24.04;
2. checks out the repository;
3. installs Python 3.13;
4. installs dependencies from `.github/requirements-ci.txt`;
5. runs `pre-commit run --all-files --show-diff-on-failure`.

Because the pre-commit configuration includes the `course-tool-tests` hook, this job also runs the complete Python tool test suite.

Its timeout is 10 minutes.

The build job depends on `Quality`. When quality validation fails, compilation is skipped.

## Build job

`Compile affected documents` runs on Ubuntu 24.04 with a 45-minute timeout.

The job checks out the complete Git history, determines the comparison base, and writes changed repository paths to:

```text
.build/changed-files.txt
```

It then runs inside a pinned TeX Live container.

For an initial push or a manual workflow run:

```bash
python3 latex/tools/build.py --all --keep-going
```

For an ordinary pull request or push:

```bash
python3 latex/tools/build.py \
  --changed-file-list .build/changed-files.txt \
  --keep-going
```

The mapping from changed paths to documents is implemented by `build.py` and documented in [Build system](build-system.md).

## Artifacts

After the build step, the workflow attempts to upload:

```text
.build/**/main.pdf
```

The artifact is named `latex-pdfs-<commit-sha>`, retained for 14 days, and uploaded without additional compression.

When compilation fails, the workflow instead attempts to upload:

```text
.build/**/*.log
.build/**/*.blg
```

The failure artifact is named `latex-logs-<commit-sha>` and retained for 7 days.

A quality-job failure does not produce LaTeX logs because the build job never starts.

## Generated course changelogs

`generate_changelog.py` reads commits affecting `1/`, `2/`, and `3/`. For each course it writes:

```text
CHANGELOG/<year>/<course>.md
```

Each generated file groups changes by commit date and records the linked commit, its message, and every added, modified, deleted, copied, or renamed course file. Histories are rebuilt from Git rather than appended, so they remain deterministic and retain deleted-course history. Renames between courses appear in both histories.

The generator also creates tracked `.gitkeep` placeholders for the source years, `CHANGELOG/`, and its three year directories. This is necessary because Git does not store empty directories. Run it locally with:

```bash
python3 latex/tools/generate_changelog.py
```

Generated changelogs must not be edited by hand; the weekly workflow replaces their contents.

## Generated-file verification

The current workflow compiles affected documents but does not compare the resulting files with the committed `main.pdf` and generated course or integration README sections.

Run this check locally before contributing:

Linux or macOS:

```bash
python3 latex/tools/build.py --all --keep-going --check-generated
```

Windows PowerShell:

```powershell
py latex/tools/build.py --all --keep-going --check-generated
```

A successful normal build may update generated files in the working tree. Commit those updates with the source changes they represent.

## Diagnosing failures

For a `Quality` failure, open the failing pre-commit step and run the reported hook locally. Some hooks modify files automatically; review and commit those changes before pushing again.

For a compilation failure, open the failed document in the job log and download the `latex-logs-<commit-sha>` artifact when available. Reproduce the affected build locally, fix the first meaningful LaTeX error, and rebuild the document.

After pushing a correction, GitHub starts a new workflow run. To retry an unchanged run, open it under the repository's **Actions** tab and use **Re-run jobs**.
