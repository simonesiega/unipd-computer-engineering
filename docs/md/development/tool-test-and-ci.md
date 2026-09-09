# Validation, Tests, and CI

[← Documentation](../README.md) · [Architecture](architecture.md) · [Build system](build-system.md) · [Building documents](../getting-started/building-documents.md)

This guide covers repository validation, Python tool tests, pre-commit checks, GitHub Actions behavior, review artifacts, and release publication.

Build-tool behavior such as document discovery, selection, compilation, generated README handling, and packaging belongs in [Build system](build-system.md).

## Local quality checks

Run the repository validator from the repository root:

```bash
python3 latex/tools/check_repository.py
```

On Windows PowerShell, use `py` instead of `python3`.

To reproduce the repository quality checks:

```bash
python3 -m pip install -r .github/requirements-ci.txt
pre-commit run --all-files --show-diff-on-failure
```

Pre-commit pins its hooks and tool dependencies. Dependabot monitors CI requirements, hooks, GitHub Actions, and the canonical Docker image.

## Python tool tests

Repository tools use standard-library `unittest`, deterministic inputs, temporary directories and repositories, and no network access.

| Test file | Main responsibility |
|---|---|
| `test_course_creation.py` | Course creation, metadata, duplicate handling, cleanup, and CLI validation |
| `test_build_selection.py` | Document discovery, affected paths, generated README behavior, and build selection |
| `test_notes_packaging.py` | Release asset naming, metadata, manifests, checksums, ordering, and packaging failures |
| `test_release_catalog.py` | Published-release parsing, exam coverage, deduplication, and generated release tables |
| `test_gitignore.py` | Course-PDF ignore rules without globally ignoring PDF files |
| `test_changelog_generation.py` | Per-course history generation, renames, dates, and placeholders |
| `test_repository_validation.py` | Repository structure, source hygiene, Markdown links, metadata, and generated-output rules |

Run the complete test suite with:

```bash
python3 -m unittest discover -s latex/tools/test -p 'test_*.py'
```

CI uses `latex/tools/run_tool_tests.py` to add branch coverage and enforce the repository's minimum coverage threshold.

## Repository validation

`check_repository.py` validates repository-wide structural rules that should remain true regardless of which document is currently being edited.

| Area | Main checks |
|---|---|
| Courses | Direct course layout, kebab-case names, supported language/class, required metadata, cohort-consistent academic year, and generated README markers |
| Course outputs | No tracked `1/**/main.pdf`, `2/**/main.pdf`, or `3/**/main.pdf` |
| Components | Expected package and isolated tracked example structure |
| Integration examples | Expected source, generated README, and tracked example PDF structure |
| Sources | UTF-8, LF line endings, final newlines, and no tabs, trailing whitespace, or merge-conflict markers |
| Documentation | Existing repository-relative targets and valid GitHub-style heading anchors |

The tracked-course-PDF rule checks the Git index rather than local `.build/` output, so normal local compilation does not fail validation.

## Pre-commit

The pre-commit pipeline combines generic repository hygiene with project-specific checks.

It includes:

- added-file-size, case-conflict, and merge-conflict checks;
- YAML, newline, line-ending, and trailing-whitespace checks;
- Actionlint for GitHub Actions;
- Ruff and mypy for Python tooling;
- Python tool tests and coverage;
- repository structure validation;
- Markdown link and anchor validation.

Binary fonts, PDFs, and images are excluded from text-only fixers where appropriate.

## CI workflows

The repository separates validation from publication:

| Workflow | Responsibility |
|---|---|
| `ci.yml` | Pull requests, pushes to `main`, and optional manual validation |
| `publish-notes.yml` | Manually requested rolling releases and immutable snapshots |
| `Course changelogs` | Weekly generated per-course source histories |

Validation jobs use read-only repository permissions. In `publish-notes.yml`, only the trusted publication stage receives write access. The separate `Course changelogs` workflow has write access only to publish its generated recap.

The workflows do not use `pull_request_target`, do not expose repository secrets to pull-request code, and do not require custom publication secrets.

## Pull requests and `main`

For pull requests and pushes to `main`, CI runs the complete quality pipeline and builds affected documents when possible.

Successful PDFs are uploaded as temporary review artifacts:

```text
latex-pdfs-<commit-sha>
```

They are retained for approximately 14 days and are intended only for review.

When compilation fails, available LaTeX logs are uploaded separately as:

```text
latex-logs-<commit-sha>
```

Neither pull requests nor normal pushes to `main` publish or modify a GitHub Release.

If CI cannot determine a reliable comparison base, it falls back to validating the complete document set.

## Release publication

Release publication is always manual and uses the complete validated archive. A maintainer starts it from **Actions → Publish compiled notes → Run workflow** on the intended `main` commit.

Two publication modes are supported:

| Mode | Purpose |
|---|---|
| `rolling` | Refresh the moving `notes-latest` release with the current complete archive |
| `snapshot` | Publish an immutable, maintainer-approved semester archive |

Both modes run the complete quality checks, build every document, package course assets, verify generated metadata and checksums, and only then publish the staged release assets.

### Rolling release

The rolling release uses:

```text
tag:   notes-latest
title: Latest compiled notes
```

It represents the latest successfully published complete archive from `main`. The workflow rejects a rolling run unless its source is still the current `main` commit.

Publication is staged as a draft while assets are replaced so a partial update is not presented as successful. Matching assets are replaced, stale assets are removed, and the `notes-latest` tag is moved to the source/build commit before publication. Re-running the same source is idempotent.

If publication fails, inspect the draft release and workflow output before retrying.

### Immutable snapshots

Select `snapshot` and provide:

- a unique `release_tag`, such as `2026-2027-semester-1`;
- a non-empty `release_title`;
- optionally, a repository-relative `release_description_file` that identifies a committed Markdown file.

Use the [release description questionnaire](../release/example.md) as the starting point. Replace every placeholder and remove sections that do not apply. The workflow rejects absolute paths, paths outside the repository, missing files, unsafe tags, the reserved `notes-latest` tag, and any tag or release that already exists.

Published snapshots are never moved or overwritten. If an upload fails, its draft remains non-public; inspect it and explicitly delete only that failed draft and tag before retrying the same snapshot identifier. Never delete a published snapshot merely to replace its contents.

Publishing a snapshot explicitly approves every included course PDF as covered. The rolling `notes-latest` release does not establish exam coverage by itself.

## Release catalogue

After successful publication, `update_release_catalog.py` reads published GitHub Releases and refreshes the generated release catalogue in the root README.

The generated section is bounded by:

```html
<!-- RELEASE-CATALOG:START -->
<!-- RELEASE-CATALOG:END -->
```

Draft releases are ignored. Immutable snapshots establish covered exams, while the rolling release is listed without contributing to coverage.

The catalogue update is limited to the generated README section and is committed automatically with `[skip ci]` when its contents change. The rolling tag remains attached to the source/build commit rather than moving to this later catalogue-only commit.

The weekly `Course changelogs` workflow separately regenerates protected files under `CHANGELOG/` from complete Git history and commits them only when their generated content changes.

## Failure diagnosis

| Failure | First place to look |
|---|---|
| Quality check | The failing pre-commit hook and any automatic fixes |
| Python test | The reported test file and assertion |
| Repository validation | The named path and violated structural rule |
| Compilation | The first meaningful LaTeX error and uploaded log artifact |
| Packaging | Missing course build output, invalid asset name, collision, manifest, or checksum error |
| Rolling publication | Draft release state, asset replacement, tag update, and final publish step |
| Snapshot publication | Existing tag/release, invalid release input, or failed draft |

For build-tool internals, see [Build system](build-system.md). For local build commands, see [Building documents](../getting-started/building-documents.md).
