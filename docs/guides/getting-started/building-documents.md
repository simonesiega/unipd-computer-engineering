# Building Documents

[← Documentation](../README.md) · [Installation](installation.md) · [Docker builds](docker.md) · [Build system](../development/build-system.md)

This guide covers the normal workflow for compiling notes, reviewing generated PDFs, and validating changes before opening a Pull Request.

Run commands from the repository root after completing [Installation](installation.md).

## Daily shortcuts

The root [`Makefile`](../../../Makefile) provides short wrappers for common tasks:

| Task | Command |
|---|---|
| Build one course | `make build COURSE=1/analisi-matematica-1` |
| Build every document | `make all` |
| Run repository checks | `make check` |
| Build the documentation site | `make docs` (install the [site dependencies](../development/documentation-site.md#build-and-review-locally) first) |
| Remove `.build/` | `make clean` |
| List available shortcuts | `make help` |

These commands are convenience wrappers. The website uses host Python (`make docs PYTHON=python` overrides the launcher); LaTeX commands use Docker. The Docker commands below remain the canonical interface and should be used when you need advanced options or do not have GNU Make installed.

## Build a document

Use the pinned Docker environment used by CI and release builds:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py 1/analisi-matematica-1
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

For example, `1/analisi-matematica-1/main.tex` produces `.build/1/analisi-matematica-1/main.pdf`.

Open the PDF and check the changed passages and neighboring pages after every meaningful content or layout change. Compilation alone does not catch clipped diagrams, awkward page breaks, or incorrect content.

Generated course `main.pdf` files under `1/`, `2/`, or `3/` must not be committed.

Component and integration examples have tracked PDFs beside their sources. A normal build replaces these fixtures; `--check-generated` compares them without replacing them.

## Generated README sections

See [Generated README content](../development/build-system.md#generated-readme-content) for marker ownership, localization, and contents generation. That reference also explains which README text remains manually editable.

## Build only changed documents

To compile documents affected by changes since `origin/main`:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py \
    --changed-from origin/main \
    --keep-going
```

This selects committed differences, not uncommitted edits. Read the [selection rules](../development/build-system.md#target-selection), including revision availability and shared-change scope; use explicit targets or `--all` while editing uncommitted work.

## Validate your changes

Run [Local quality checks](../development/tool-test-and-ci.md#local-quality-checks) for every change. Documentation-only edits additionally follow the [site-build and browser-review workflow](../development/documentation-site.md#build-and-review-locally), but need no LaTeX compilation or PDF review unless rendered documents are affected.

For LaTeX sources or document-build changes, verify generated state in the canonical environment:

```bash
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py \
    --all \
    --keep-going \
    --check-generated
```

Review the resulting PDFs as described above; a successful comparison is not a visual review. The [generated-state reference](../development/build-system.md#generated-state-verification) explains comparison semantics. For Python tests, use [TESTS.md](../../../latex/tools/test/TESTS.md#running-tests); for CI artifacts, use [Validation, tests, and CI](../development/tool-test-and-ci.md#pull-requests-and-main).

## If a course PDF was accidentally tracked

Remove it from Git without deleting your local file:

```bash
git rm --cached -- <year>/<course>/main.pdf
```

Do not rewrite repository history for normal contribution cleanup.

## Useful build options

The [selection modes](../development/build-system.md#target-selection) and [build options](../development/build-system.md#build-options) are maintained in the build-system reference. The tool also provides `--help`.

Release packaging and publication are maintainer responsibilities. Contributors should not stage `.build/release/` or generated course PDFs.
