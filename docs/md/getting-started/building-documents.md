# Building Documents

[← Documentation](../README.md) · [Installation](installation.md) · [Docker builds](docker.md) · [Build system](../development/build-system.md)

This guide covers the normal workflow for compiling notes, reviewing generated PDFs, and validating changes before opening a Pull Request.

Run commands from the repository root after completing [Installation](installation.md).

## Daily shortcuts

The root [`Makefile`](../../../Makefile) provides short wrappers for common tasks:

| Task | Command |
|---|---|
| Build one course | `make build COURSE=1/calculus-1` |
| Build every document | `make all` |
| Run repository checks | `make check` |
| Remove `.build/` | `make clean` |
| List available shortcuts | `make help` |

These commands are convenience wrappers. The Docker commands below remain the canonical interface and should be used when you need advanced options or do not have GNU Make installed.

## Build a document

Use the pinned Docker environment so local output matches CI and release builds:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py 1/course-name
```

The same command works for other document types:

```bash
# Component example
docker compose run --rm texlive \
  python3 latex/tools/build.py latex/components/diagrams/example

# Integration example
docker compose run --rm texlive \
  python3 latex/tools/build.py latex/integration/english
```

Build multiple documents by listing multiple targets, or build everything with:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py --all --keep-going
```

## Review the output

Build output is written under `.build/` using the same path as the source document.

For a course:

```text
1/course-name/main.tex
└── .build/1/course-name/main.pdf
```

Review `.build/<year>/<course>/main.pdf` after every meaningful content or layout change.

Generated course `main.pdf` files under `1/`, `2/`, or `3/` must not be committed.

Component and integration examples may keep tracked PDFs beside their sources because they act as repository fixtures.

## Generated README sections

Course and integration builds may update generated README content between:

```html
<!-- GENERATED:START -->
<!-- GENERATED:END -->
```

Do not edit content inside these markers manually.

Manual course information may be written outside the generated section.

## Build only changed documents

To compile documents affected by changes since `origin/main`:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py \
    --changed-from origin/main \
    --keep-going
```

Course-local changes normally select that course. Shared LaTeX, fonts, the canonical build environment, or build-tool changes may select every document.

For the complete selection rules, see [Build system](../development/build-system.md).

## Validate your changes

Run the repository validator:

| Platform | Command |
|---|---|
| Linux or macOS | `python3 latex/tools/check_repository.py` |
| Windows PowerShell | `py latex/tools/check_repository.py` |

Then verify generated tracked state in the canonical environment:

```bash
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py \
    --all \
    --keep-going \
    --check-generated
```

This checks generated README sections and tracked component/integration fixtures. Course PDFs remain under `.build/` and should be reviewed visually.

For the complete repository quality pipeline, tests, CI behavior, and Pull Request artifacts, see [Validation, tests, and CI](../development/tool-test-and-ci.md).

## If a course PDF was accidentally tracked

Remove it from Git without deleting your local file:

```bash
git rm --cached -- <year>/<course>/main.pdf
```

Do not rewrite repository history for normal contribution cleanup.

## Useful build options

| Option | Use it when |
|---|---|
| `--all` | You want to build every document |
| `--changed-from REVISION` | You want to build only affected documents |
| `--keep-going` | You want all selected documents processed even if one fails |
| `--no-readme` | You want to compile without updating generated README content |
| `--clean` | You want `.build/` removed after a successful run |
| `--check-generated` | You want to verify tracked generated state |

For the full command reference and tool behavior, see [Build system](../development/build-system.md).

Display built-in help with:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py --help
```

Release packaging and publication are maintainer responsibilities. Contributors should not stage `.build/release/` or generated course PDFs.
