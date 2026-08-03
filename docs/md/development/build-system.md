# Build System

[← Documentation](../README.md) · [Architecture](architecture.md) · [Building documents](../getting-started/building-documents.md) · [Validation, Tests, and CI](tool-test-and-ci.md)

The repository build system is implemented by `latex/tools/build.py`. It discovers LaTeX documents, selects the required targets, compiles them in isolated output directories, publishes generated files, and detects stale committed outputs.

## Document discovery

The build system searches these document roots:

```text
1/
2/
3/
latex/components/
latex/integration/
```

Every discovered `main.tex` is treated as an independent document. A user-supplied target may be either a document directory or its `main.tex` file.

Build output mirrors the document path under `.build/`:

```text
1/course-name/main.tex
└── .build/1/course-name/

latex/components/code/example/main.tex
└── .build/latex/components/code/example/

latex/integration/english/main.tex
└── .build/latex/integration/english/
```

The output directory for a document is removed and recreated before compilation.

## Selection modes

Exactly one selection mode is required:

| Mode | Selection |
|---|---|
| Explicit targets | One or more directories or `main.tex` files |
| `--all` | Every discovered course and component example |
| `--changed-from REVISION` | Documents affected by a Git diff from `REVISION` to `HEAD` |
| `--changed-file-list FILE` | Documents affected by repository-relative paths listed in a file |

`--changed-to` changes the end revision used with `--changed-from`; its default is `HEAD`.

`--changed-file-list` exists for CI, where changed paths are collected outside the TeX container. When no changed path affects a LaTeX document, the script exits successfully without compiling anything.

## Affected-document mapping

Changed paths are mapped conservatively:

| Changed path | Selected documents |
|---|---|
| File inside `1/<course>/`, `2/<course>/`, or `3/<course>/` | That course |
| File inside a component's `example/` directory | That component example |
| File inside `latex/integration/<example>/` | That integration example |
| `latex/unipd-notes.cls` | Every document |
| Component `.sty` file | Every document |
| Bundled `.otf` or `.ttf` font | Every document |
| `latex/tools/build.py` | Every document |
| Unrelated documentation or policy file | None |

A shared-system change returns the complete document set immediately because every document may depend on it.

## Compilation

Each document is compiled from its own source directory with:

```text
latexmk
-lualatex
-halt-on-error
-interaction=nonstopmode
-file-line-error
-outdir=<mirrored .build directory>
main.tex
```

`latexmk` must be available on `PATH`.

The build environment:

- prepends the repository's `latex/` directory to `TEXINPUTS`;
- fixes `SOURCE_DATE_EPOCH`;
- enables `FORCE_SOURCE_DATE`;
- sets the timezone to UTC.

These values reduce environment-dependent differences between local and CI builds. Because they also fix TeX's clock, documents must store their publication date explicitly in `main.tex` rather than use `\today`.

After a successful compilation, `main.pdf` and `main.toc` remain under `.build/`. In a normal build, the PDF is copied atomically beside the source `main.tex`.

## Generated course README

For course documents, the script parses `main.toc` and converts table-of-contents entries for parts, chapters, sections, subsections, and subsubsections into Markdown. Generated headings and links use the `italian` or `english` language selected by the document class.

The generated block contains a link to `main.pdf` and the document contents with page numbers. It is inserted between:

```html
<!-- GENERATED:START -->
<!-- GENERATED:END -->
```

When a course README does not exist, the script creates one using the course directory name as its heading. Existing content outside the markers is preserved.

Component and integration examples do not receive generated README content.

## Generated-file verification

With `--check-generated`, compilation still occurs under `.build/`, but committed files are not replaced. The script compares:

- the newly built PDF with the committed `main.pdf`;
- the expected generated README content with the committed course `README.md`.

The build fails when either file is missing or stale.

`--check-generated` cannot be combined with `--no-compile` or `--no-readme`.

## Processing options

| Option | Behavior |
|---|---|
| `--no-compile` | Reuse an existing PDF and available `.toc` data |
| `--no-readme` | Compile without creating or updating course README files |
| `--keep-going` | Process every selected document and report all failures afterward |
| `--clean` | Remove the repository-level `.build/` directory after a successful run |
| `--check-generated` | Verify committed PDFs and generated README sections |

Without `--keep-going`, the first build error stops execution. With it, failures are collected, printed with their document paths, and returned through a non-zero exit status.

See [Building documents](../getting-started/building-documents.md) for contributor-facing commands and [Validation, Tests, and CI](tool-test-and-ci.md) for automation behavior.
