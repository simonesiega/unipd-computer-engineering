# Build System

[← Documentation](../README.md) · [Architecture](architecture.md) · [Building documents](../getting-started/building-documents.md) · [Validation, tests, and CI](tool-test-and-ci.md)

`latex/tools/build.py` is the repository's document build entry point. It discovers LaTeX documents, selects targets, compiles them into isolated output directories, updates generated README content, and verifies tracked generated fixtures.

`latex/tools/package_notes.py` owns the separate packaging step that turns complete course build outputs into release-ready assets.

## Document discovery

The build system discovers independent `main.tex` entry points under:

```text
1/
2/
3/
latex/components/
latex/integration/
```

Each discovered `main.tex` is treated as one buildable document.

Build output mirrors the source path under `.build/`:

```text
1/course-name/main.tex
└── .build/1/course-name/main.pdf

latex/components/code/example/main.tex
└── .build/latex/components/code/example/main.pdf

latex/integration/english/main.tex
└── .build/latex/integration/english/main.pdf
```

Course PDFs remain under `.build/` and are never copied into course directories.

Tracked component and integration example PDFs are maintained separately as generated fixtures.

## Target selection

Exactly one selection mode is required:

| Mode | Selection |
|---|---|
| Explicit target | One or more document directories or `main.tex` files |
| `--all` | Every course, component example, and integration project |
| `--changed-from REVISION` | Documents affected by changes from `REVISION` to `HEAD` |
| `--changed-file-list FILE` | Documents affected by repository-relative paths listed in a file |

`--changed-to` may be used with `--changed-from` to change the end revision from its default of `HEAD`.

Changed-file selection is intentionally conservative:

| Changed area | Build impact |
|---|---|
| File inside one course | That course |
| File inside one component example | That example |
| File inside one integration example | That integration project |
| Shared class, component package, font, build environment, or build tooling | Every document |
| Unrelated documentation or policy | No LaTeX document |

Complete archive publication uses `--all`; reduced selection is only an optimization for development and validation.

## Compilation

Each selected document is compiled with `latexmk` and LuaLaTeX in a mirrored `.build/` directory.

The effective compilation uses:

```text
latexmk
-lualatex
-halt-on-error
-interaction=nonstopmode
-file-line-error
-outdir=<mirrored .build directory>
main.tex
```

The environment adds `latex/` to `TEXINPUTS`, fixes the source-date environment, and uses UTC to reduce avoidable output differences.

Canonical builds use the pinned `texlive` service defined in `compose.yaml`.

After compilation, the generated PDF, table of contents, logs, and auxiliary files remain under:

```text
.build/<document>/
```

For course work, `.build/<year>/<course>/main.pdf` is the PDF to review locally.

## Generated README content

For courses and integration projects, `build.py` reads the compiled `main.toc` and generates a localized Markdown contents section between:

```html
<!-- GENERATED:START -->
<!-- GENERATED:END -->
```

Content outside those markers is preserved.

Course README sections link to the stable asset published through the rolling `notes-latest` release. Integration projects may link to their tracked local PDF. Component examples do not receive generated README content.

Do not edit generated sections manually.

## Generated-state verification

`--check-generated` verifies that tracked generated content matches what the current sources produce.

It checks:

- generated course and integration README sections;
- tracked component-example PDFs;
- tracked integration PDFs.

Course PDFs are deliberately excluded from tracked-PDF comparison because normal course output belongs only under `.build/`.

Repository validation separately rejects generated course PDFs that are forced into Git.

## Build options

| Option | Behavior |
|---|---|
| `--no-compile` | Reuse existing PDF and `.toc` output when available |
| `--no-readme` | Compile without updating generated README content |
| `--keep-going` | Continue through all selected documents and report failures afterward |
| `--clean` | Remove the repository-level `.build/` directory after success |
| `--check-generated` | Verify generated tracked state without replacing it |

`--check-generated` cannot be combined with `--no-compile` or `--no-readme`.

Without `--keep-going`, processing stops at the first failure.

## Release packaging

After a complete build, `latex/tools/package_notes.py` converts course PDFs into deterministic release assets under `.build/release/`. Invoke it with release metadata supplied by the publishing workflow:

```bash
python3 latex/tools/package_notes.py \
  --source-commit <40-character-sha> \
  --release-timestamp <iso-8601-timestamp-with-utc-offset> \
  --release-title "Latest compiled notes"
```

The source commit must be a full SHA. The release timestamp must include a UTC offset, for example `2026-08-04T12:00:00+00:00` or its equivalent `Z` form. Publishing uses the source commit timestamp so repeated packaging of the same source remains deterministic.

The packaging step:

- discovers direct course entry points under `1/`, `2/`, and `3/`;
- requires the matching compiled PDF under `.build/`;
- derives stable asset names such as `1-calculus-1.pdf`;
- rejects invalid paths and naming collisions;
- copies the built PDF bytes without modifying them;
- reads canonical course metadata from `\unipdsetup`;
- creates a sorted manifest and release index;
- generates SHA-256 checksums;
- succeeds with an empty manifest and explanatory release index when the course archive is empty.

A discovered course with no matching compiled PDF, malformed canonical metadata, or invalid release metadata causes packaging to fail.

The release staging directory contains:

```text
.build/release/
├── <year>-<course-slug>.pdf
├── manifest.json
├── SHA256SUMS.txt
└── RELEASE_NOTES.md
```

Packaging owns asset naming, metadata generation, checksums, and release staging. GitHub workflows publish these outputs but should not duplicate that logic.

For publication behavior, workflow permissions, CI artifacts, and rolling or snapshot releases, see [Validation, tests, and CI](tool-test-and-ci.md).

For local commands and normal student workflows, see [Building documents](../getting-started/building-documents.md) and [Docker builds](../getting-started/docker.md).
