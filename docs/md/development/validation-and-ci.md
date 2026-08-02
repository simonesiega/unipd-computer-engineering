# Validation and CI

[← Documentation](../README.md) · [Architecture](architecture.md) · [Build system](build-system.md) · [Building documents](../getting-started/building-documents.md)

The repository uses three complementary validation layers: direct repository checks, pre-commit hooks, and the `LaTeX CI` GitHub Actions workflow. Compilation and generated-file verification remain responsibilities of the build system.

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

The CI requirements currently pin `pre-commit` to version `4.3.0`.

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

The local `latex-repository-check` hook runs `latex/tools/check_repository.py` for changes under the course directories, `latex/`, workflow files, or the pre-commit configuration. It receives no individual filenames and validates the repository as a whole.

## Repository-specific checks

`check_repository.py` validates:

| Area | Checks |
|---|---|
| Courses | Entry points are direct `<year>/<course>/main.tex` files under `1/`, `2/`, or `3/` |
| Course documents | `main.tex` declares a document class and contains a complete document environment |
| Components | Each component contains `<component>.sty` and `example/` |
| Component examples | Each `example/` contains exactly `main.tex` and `main.pdf` |
| LaTeX sources | `.tex`, `.sty`, `.cls`, and `.bib` files are valid UTF-8 |
| Source hygiene | No tabs, trailing whitespace, or unresolved merge-conflict markers |

The validator ignores `.git/` and `.build/`. Empty degree-year directories are not required because Git does not preserve empty directories.

## Workflow triggers

`.github/workflows/ci.yml` defines the `LaTeX CI` workflow. It runs on:

| Event | Scope |
|---|---|
| Pull request | The proposed pull-request changes |
| Push to `main` | Changes introduced by the push |
| Manual dispatch | A complete build |

The workflow has read-only repository permissions. Checkout credentials are not persisted.

Only one run for the same workflow and Git reference remains active. A newer run cancels an older in-progress run for that reference.

## Quality job

The `Quality` job:

1. runs on Ubuntu 24.04;
2. checks out the repository;
3. installs Python 3.13;
4. installs dependencies from `.github/requirements-ci.txt`;
5. runs `pre-commit run --all-files --show-diff-on-failure`.

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

## Generated-file verification

The current workflow compiles affected documents but does not compare the resulting files with the committed `main.pdf` and generated course README sections.

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
