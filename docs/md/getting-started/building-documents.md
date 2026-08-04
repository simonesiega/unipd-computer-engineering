# Building Documents

[← Documentation](../README.md) · [Installation](installation.md) · [Docker builds](docker.md)

This guide covers local compilation, generated files, and checks before contributing. Run commands from the repository root after following [Installation](installation.md).

## Build documents

Use the canonical Docker Compose environment. It matches CI and release builds across platforms.

| Task | Command |
|---|---|
| Build one course | `docker compose run --rm texlive python3 latex/tools/build.py 1/course-name` |
| Build one component example | `docker compose run --rm texlive python3 latex/tools/build.py latex/components/diagrams/example` |
| Build an integration example | `docker compose run --rm texlive python3 latex/tools/build.py latex/integration/english` |
| Build multiple targets | `docker compose run --rm texlive python3 latex/tools/build.py 1/course-a 1/course-b` |
| Build all documents | `docker compose run --rm texlive python3 latex/tools/build.py --all --keep-going` |

Replace example paths as needed. Every output is available under `.build/<document>/main.pdf`. A course build does not create or update `<year>/<course>/main.pdf`; generated course PDFs are ignored and must not be committed. It does refresh the generated course README section with a link to the rolling release. Component and integration examples keep their tracked PDFs beside their sources.

Do not manually edit content between:

```html
<!-- GENERATED:START -->
<!-- GENERATED:END -->
```

A native TeX installation may be used for quick previews by replacing the Docker prefix with `python3` on Linux/macOS or `py` on Windows. Release and CI output always uses the pinned Docker image.

## Build changed documents

Build only documents affected since another revision:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py --changed-from origin/main --keep-going
```

Course-local changes select that course. Component-example and integration changes select their document. Shared LaTeX, fonts, the canonical environment, build workflow, or build tool select every document. Documentation-only changes generally select none. Push publication intentionally ignores this optimization and builds the complete archive.

## Validate changes

Run repository and Git-index checks:

| Platform | Command |
|---|---|
| Linux or macOS | `python3 latex/tools/check_repository.py` |
| Windows PowerShell | `py latex/tools/check_repository.py` |

The validator checks source/layout conventions, Markdown links, and whether a generated course PDF was accidentally tracked.

Verify all tracked generated fixtures and README sections in the canonical environment:

```bash
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py --all --keep-going --check-generated
```

`--check-generated` compiles under `.build/`. It compares tracked component/integration PDFs and generated README content, but correctly does not expect a committed course PDF. Always inspect affected course PDFs from `.build/` visually. Pull-request reviewers can instead use the temporary `latex-pdfs-<commit-sha>` GitHub Actions artifact, retained for approximately 14 days.

If a generated course PDF was forced into Git, remove it only from the index:

```bash
git rm --cached -- <year>/<course>/main.pdf
```

Do not rewrite history for normal contribution cleanup.

## Complete build command reference

Exactly one selection mode is required: explicit `TARGET` values, `--all`, `--changed-from`, or `--changed-file-list`.

| Argument or option | Value | Purpose |
|---|---|---|
| `TARGET` | Directory or `main.tex` path | Build one or more explicitly listed documents |
| `--all` | None | Discover and build every document |
| `--changed-from` | Git revision | Build documents affected from that revision to `HEAD` |
| `--changed-to` | Git revision | Change the end revision used with `--changed-from` |
| `--changed-file-list` | File path | Read repository-relative changed paths from a file |
| `--no-compile` | None | Reuse existing PDF and `.toc` data, normally from `.build/` |
| `--no-readme` | None | Do not update generated README content |
| `--clean` | None | Remove `.build/` after success |
| `--keep-going` | None | Process all selected targets and report failures together |
| `--check-generated` | None | Compare tracked generated fixtures and README content |
| `-h`, `--help` | None | Print the command reference |

`--check-generated` cannot be combined with `--no-compile` or `--no-readme`. `--changed-to` applies only to `--changed-from`.

Display built-in help with:

```bash
docker compose run --rm texlive python3 latex/tools/build.py --help
```

Release packaging and publication are maintainer/CI responsibilities described in [Validation, Tests, and CI](../development/tool-test-and-ci.md). Contributors do not stage `.build/release/` or generated course PDFs.
