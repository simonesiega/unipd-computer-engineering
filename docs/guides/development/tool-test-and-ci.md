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

Create and activate the validation environment described in [Installation](../getting-started/installation.md), then run:

```bash
pre-commit run --all-files --show-diff-on-failure
git diff --check
```

Pre-commit pins its hooks and tool dependencies. Its first run needs network access to create the hook environments. Some hooks fix files; inspect those changes and rerun the command. `--all-files` checks Git-tracked files, not new untracked files. The repository validator independently scans new source and Markdown files.

Dependabot monitors CI requirements, hooks, GitHub Actions, and the Docker image. CI uses Python 3.13; repository tools support Python 3.10+.

## Python tool tests

[TESTS.md](../../../latex/tools/test/TESTS.md) owns the file-by-file test catalogue, isolation contract, commands for all/focused tests, and coverage threshold. Its [Running tests](../../../latex/tools/test/TESTS.md#running-tests) section also explains the pinned coverage hook. This guide owns how those checks participate in local validation and CI.

## Repository validation

`check_repository.py` validates repository-wide structural rules that should remain true regardless of which document is currently being edited.

| Area | Main checks |
|---|---|
| Courses | Direct course layout, kebab-case names, supported language/class, required metadata, optional `course-code`/`channel` formats, cohort-consistent academic year, and generated README markers |
| Course outputs | No tracked `1/**/main.pdf`, `2/**/main.pdf`, or `3/**/main.pdf` |
| Components | Expected package and isolated tracked example structure |
| Integration examples | Both language directories, source language option, required README/PDF files, and no unexpected entries |
| LaTeX and bibliography sources | UTF-8, LF line endings, final newlines, and no tabs, trailing whitespace, or merge-conflict markers |
| Documentation | Existing repository-relative targets and valid GitHub-style heading anchors |

The tracked-course-PDF rule checks the Git index rather than local `.build/` output, so normal local compilation does not fail validation.

Source and Markdown scans include new, unstaged repository files but prune local-only trees: `.git`, `.build`, `.context`, `.venv`, `venv`, Python/tool caches, `htmlcov`, notebook checkpoints, and editor directories. Installing dependencies in a local virtual environment therefore does not make third-party files subject to repository source and link checks.

## Pre-commit

The pre-commit pipeline combines generic repository hygiene with project-specific checks.

It includes:

- added-file-size, case-conflict, and merge-conflict checks;
- YAML, newline, line-ending, and trailing-whitespace checks;
- Actionlint for GitHub Actions;
- Ruff and mypy for Python tooling;
- Python tool tests and coverage;
- repository structure validation;
- Markdown link and anchor validation;
- a strict documentation-site build and rendered-link check.

Binary fonts, PDFs, and images are excluded from text-only fixers where appropriate.

## CI workflows

The repository separates validation from publication:

| Workflow | Responsibility |
|---|---|
| `ci.yml` | Pull requests, pushes to `main`, and optional manual validation |
| `publish-notes.yml` | Manually requested rolling releases and immutable snapshots |
| `Course changelogs` | Weekly generated per-course source histories |
| `documentation.yml` | Strict site builds, review artifacts, and trusted `main` deployments to GitHub Pages |

Validation jobs have read-only repository permissions. In `publish-notes.yml`, only the `publish` job receives `contents: write`; its responsibilities include release assets, tags, and catalogue commits. The separate `Course changelogs` workflow also has `contents: write` to commit its generated recap.

The workflows do not use `pull_request_target`, do not expose repository secrets to pull-request code, and do not require custom publication secrets. [Documentation site](documentation-site.md#enable-github-pages) owns Pages permissions, setup, and post-publication refresh.

## Pull requests and `main`

For pull requests and pushes to `main`, CI runs the complete quality pipeline and builds affected documents when possible.

Successful PDFs are uploaded as temporary review artifacts:

```text
latex-pdfs-<commit-sha>
```

They are retained for 14 days and are intended only for review. Documentation-only changes may select no documents and produce no PDF artifact.

When compilation fails, available LaTeX logs are uploaded separately as:

```text
latex-logs-<commit-sha>
```

Log artifacts are retained for 7 days. A failed build step does not upload the normal PDF artifact, even if some documents compiled.

Neither pull requests nor normal pushes to `main` publish or modify a GitHub Release.

If CI cannot determine a reliable comparison base, it falls back to validating the complete document set.

## Release publication

Release publication is manual and uses the complete archive. A maintainer starts it from **Actions → Publish compiled notes → Run workflow** and selects the intended source ref.

For rolling publication, this must resolve to the latest `main` commit. For snapshots, project practice is to select the reviewed `main` revision, but the workflow does not enforce `main`: it publishes the dispatched ref. Check that ref before starting the run.

Two publication modes are supported:

| Mode | Purpose |
|---|---|
| `rolling` | Refresh the moving `notes-latest` release with the current complete archive |
| `snapshot` | Publish an immutable, maintainer-approved archive |

Both modes run the complete quality checks, build every document with `--check-generated`, package course assets, check that the manifest parses and the release notes are non-empty, and verify checksums before publication. Stale README sections or tracked example PDFs must be regenerated and committed beforehand; publication does not repair them.

These automated checks do not review academic correctness or PDF layout. Complete those reviews before dispatching a snapshot.

### Rolling release

The rolling release uses:

```text
tag:   notes-latest
title: Latest compiled notes
```

It represents the latest successfully published complete archive from `main`. The workflow checks the source against the current `main` commit in preflight and again immediately before mutating a release or tag. If `main` advances during compilation, publication stops without modifying the release; dispatch a new run from the latest commit.

Publication is staged as a draft while assets are replaced so a partial update is not presented as successful. Matching assets are replaced, stale assets are removed, and the `notes-latest` tag is moved to the source/build commit before publication. Re-running the same source is idempotent while it remains the current `main` commit.

If publication fails, inspect the draft release and workflow output before retrying.

### Immutable snapshots

Select `snapshot` and provide:

- a unique `release_tag`, such as `2026-2027-semester-1`;
- a non-empty `release_title`;
- optionally, a repository-relative `release_description_file` that identifies a committed Markdown file.

Use the [release description template](../release/example.md) as the starting point. Replace every placeholder and remove sections that do not apply. Commit the completed description before dispatching. The workflow checks that the path is repository-relative, resolves inside the repository, and names an existing UTF-8 file; it does not enforce a `.md` extension or detect leftover placeholders.

Snapshot tags must start with an ASCII letter or digit and contain only letters, digits, dots, underscores, or hyphens. The workflow rejects the reserved `notes-latest` tag and any existing tag or release.

Snapshots are immutable by project policy: this workflow refuses to reuse an existing snapshot tag or release. It does not enable GitHub's separate immutable-release setting. Never move a published snapshot tag or replace its assets.

If an upload fails, its draft remains non-public; inspect it and explicitly delete only that failed draft and tag before retrying the same snapshot identifier. Never delete a published snapshot merely to replace its contents.

Publishing a snapshot explicitly approves every included course PDF as covered. Packaging includes every course in the archive, including scaffolds and unfinished notes; the release description does not filter this set. Use rolling publication until every included course is sufficiently complete and reviewed. The rolling `notes-latest` release does not establish exam coverage by itself.

## Release catalogue

After successful publication, `update_release_catalog.py` reads published GitHub Releases and refreshes the generated catalogue in the root README and the complete [release archive](../../../RELEASES.md). The README shows at most the five newest published releases in the same table format as the archive; when fewer exist, it shows all of them. Both listings include published rolling releases, while drafts are excluded.

The generated section is bounded by:

```html
<!-- RELEASE-CATALOG:START -->
<!-- RELEASE-CATALOG:END -->
```

The catalogue treats published, non-prerelease releases other than `notes-latest` as snapshots for coverage; it does not inspect GitHub's immutable-release setting or academic review evidence. Creating such a release is therefore a maintainer approval decision, not a status inferred from prose in its description. The rolling release and prereleases do not contribute to coverage. `RELEASES.md` is wholly tool-owned and must not be edited manually. The updater changes only the generated README section and `RELEASES.md`; the publication workflow commits them together with `[skip ci]` when either changes. The rolling tag remains attached to the source/build commit rather than moving to this later catalogue-only commit.

## Course changelogs

The `Course changelogs` workflow runs on Sundays at 00:00 UTC or on manual dispatch. It regenerates protected files under `CHANGELOG/` from complete Git history and preserves degree-year placeholders. It commits only when generated files or placeholders change. When `CHANGELOG/BASELINE` exists, only course commits after that recorded commit are included.

A maintainer can intentionally start a fresh changelog period with:

```bash
python3 latex/tools/generate_changelog.py --reset-baseline
```

The command records the current `HEAD`, removes earlier generated course changelogs, and preserves the year placeholders. Future workflow runs then report only course changes committed after that baseline. The baseline and generated changelogs are tool-owned and must not be edited manually.

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
