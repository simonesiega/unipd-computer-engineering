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

Here, pip's `-r` option installs the pinned pre-commit runner, `--all-files` checks the complete repository instead of only changed files, and `--show-diff-on-failure` prints modifications made by a failing hook. `.pre-commit-config.yaml` pins Coverage.py, Ruff, and mypy inside their hook environments, so local and hosted checks use the same versions without duplicating those pins in the CI requirements. Dependabot monitors the CI requirement, pre-commit hooks, GitHub Actions, and Docker Compose image.

## Python tool tests

Tests for the repository’s Python tools are organized by responsibility under `latex/tools/test/`:

| Test file | Tool covered | Behavior covered |
|---|---|---|
| `test_course_creation.py` | `create_course.py` | Slug generation, metadata escaping, academic years, generated layout and metadata, duplicate detection, and argument-domain validation |
| `test_build_selection.py` | `build.py` | Document discovery, every affected-path category, TOC parsing, generated-output comparison, localized integration README generation, and missing-TOC safety |
| `test_changelog_generation.py` | `generate_changelog.py` | Complete-history enforcement, history parsing, per-course file changes, renames, dates, commits, and empty-directory placeholders |
| `test_repository_validation.py` | `check_repository.py` | Course, component, and integration layouts; Markdown links; and LaTeX source-hygiene errors |

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

The test cases use only the Python standard library. CI invokes them through `latex/tools/run_tool_tests.py`, which uses Coverage.py to report statement and branch coverage and enforces a 60% repository-wide minimum. Temporary repositories are created for file-system tests and removed automatically; the working repository is not modified.

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
| Actionlint | Validate GitHub Actions syntax and expressions |
| Ruff | Lint Python tools and tests |
| mypy | Type-check Python tools and tests |
| Tool tests and coverage | Run unit tests with statement and branch coverage reporting |
| Markdown links | Reject missing repository-relative documentation targets |

Font, PDF, and PNG files are excluded from text-only fixes where appropriate.

The local `course-tool-tests` hook runs the complete `latex/tools/test/` suite with coverage when a Python tool, tool test, or the pre-commit configuration changes. Separate hooks run Ruff and mypy for Python files, while Actionlint validates workflow files. The `latex-repository-check` hook runs `latex/tools/check_repository.py` for course, LaTeX, documentation, workflow, Markdown, or pre-commit changes. Hooks that validate repository-wide relationships receive no individual filenames.

## Repository-specific checks

`check_repository.py` validates:

| Area | Checks |
|---|---|
| Courses | Entry points are direct `<year>/<course>/main.tex` files under `1/`, `2/`, or `3/`, with lowercase kebab-case course names |
| Course documents | `main.tex` declares a document class and contains a complete document environment |
| Components | Each component contains `<component>.sty` and `example/` |
| Component examples | Each `example/` contains exactly `main.tex` and `main.pdf` |
| Integration examples | Each directory under `latex/integration/` contains exactly `main.tex`, `main.pdf`, and a localized `README.md` |
| LaTeX sources | `.tex`, `.sty`, `.cls`, and `.bib` files are valid UTF-8 |
| Source hygiene | No tabs, trailing whitespace, or unresolved merge-conflict markers |
| Markdown links | Repository-relative link targets exist |

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

The pre-commit configuration also runs the complete Python tool test suite with coverage, Ruff, mypy, Actionlint, Markdown link validation, and repository-specific structural checks.

Its timeout is 10 minutes.

The build job depends on `Quality`. When quality validation fails, compilation is skipped.

## Build job

`Compile affected documents` runs on Ubuntu 24.04 with a 45-minute timeout.

The job checks out the complete Git history and determines the comparison base. If the event has no usable base commit, it safely falls back to a complete build. Otherwise, it writes changed repository paths to:

```text
.build/changed-files.txt
```

It explicitly pulls and then runs the `texlive` service from the repository's [`compose.yaml`](../../../compose.yaml). The service pins its TeX Live image by digest, uses the fixed `/workspace` path and `linux/amd64` platform, and has no runtime network access. It is also the canonical local PDF build environment.

For an initial push or a manual workflow run:

```bash
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py --all --keep-going --check-generated
```

For an ordinary pull request or push:

```bash
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py \
    --changed-file-list .build/changed-files.txt \
    --keep-going \
    --check-generated
```

The mapping from changed paths to documents is implemented by `build.py` and documented in [Build system](build-system.md). Both modes use `--check-generated`, so CI fails when a selected document's committed PDF or generated README section is missing or stale.

## Artifacts

After a successful build step, the workflow attempts to upload:

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

The generator checks `git rev-parse --is-shallow-repository` before reading commits and refuses to run when the local history is shallow. Fetch the complete history with `git fetch --unshallow` before generating changelogs.

Generated changelogs must not be edited by hand; the weekly workflow replaces their contents.

## Generated-file verification

The workflow uses `--check-generated` to compare compiled outputs with the committed `main.pdf` and generated course or integration README sections. It checks every document for an initial or manual run and the affected documents for ordinary pushes and pull requests.

Run the same check locally in the canonical environment before contributing:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py --all --keep-going --check-generated
```

The comparison is byte for byte. `SOURCE_DATE_EPOCH` removes time-dependent variation but cannot make different LuaLaTeX or package versions identical, so a native TeX installation is not suitable for final generated-file verification.

A successful normal build may update generated files in the working tree. Commit those updates with the source changes they represent.

## Diagnosing failures

For a `Quality` failure, open the failing pre-commit step and run the reported hook locally. Some hooks modify files automatically; review and commit those changes before pushing again.

For a compilation failure, open the failed document in the job log and download the `latex-logs-<commit-sha>` artifact when available. Reproduce the affected build through the `texlive` Compose service, fix the first meaningful LaTeX error, and rebuild the document.

After pushing a correction, GitHub starts a new workflow run. To retry an unchanged run, open it under the repository's **Actions** tab and use **Re-run jobs**.
