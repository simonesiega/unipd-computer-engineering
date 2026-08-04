# Build System

[← Documentation](../README.md) · [Architecture](architecture.md) · [Building documents](../getting-started/building-documents.md) · [Validation, Tests, and CI](tool-test-and-ci.md)

`latex/tools/build.py` discovers LaTeX documents, selects targets, compiles them in isolated output directories, refreshes generated README content, and verifies tracked generated fixtures. `latex/tools/package_notes.py` has the separate responsibility of turning complete course build outputs into release assets.

## Document discovery and output

The build system searches:

```text
1/
2/
3/
latex/components/
latex/integration/
```

Every discovered `main.tex` is an independent document. A target may be a document directory or its `main.tex`. Output mirrors the source path:

```text
1/course-name/main.tex
└── .build/1/course-name/main.pdf

latex/components/code/example/main.tex
└── .build/latex/components/code/example/main.pdf

latex/integration/english/main.tex
└── .build/latex/integration/english/main.pdf
```

Each output directory is removed and recreated before compilation. Course PDFs remain in `.build/` and are never copied into course directories. Normal component and integration builds continue to update their tracked example PDF beside `main.tex`.

## Selection modes

Exactly one selection mode is required:

| Mode | Selection |
|---|---|
| Explicit targets | One or more directories or `main.tex` files |
| `--all` | Every course, component example, and integration project |
| `--changed-from REVISION` | Documents affected by a Git diff from `REVISION` to `HEAD` |
| `--changed-file-list FILE` | Documents affected by repository-relative paths listed in a file |

`--changed-to` changes the end revision used with `--changed-from`; its default is `HEAD`. `--changed-file-list` is used in CI because changed paths are collected outside the TeX container. No affected document is a successful no-op.

## Affected-document mapping

| Changed path | Selected documents |
|---|---|
| File inside `1/<course>/`, `2/<course>/`, or `3/<course>/` | That course |
| File inside a component `example/` | That component example |
| File inside `latex/integration/<example>/` | That integration example |
| `compose.yaml` or the CI/release build workflows | Every document |
| `latex/unipd-notes.cls` | Every document |
| Component `.sty` file | Every document |
| Bundled `.otf` or `.ttf` font | Every document |
| `latex/tools/build.py` | Every document |
| Unrelated documentation or policy file | None |

Push publication does not use this reduced selection: it always passes `--all` so the release is a complete archive.

## Compilation

Each document is compiled from its source directory with:

```text
latexmk
-lualatex
-halt-on-error
-interaction=nonstopmode
-file-line-error
-outdir=<mirrored .build directory>
main.tex
```

The environment prepends `latex/` to `TEXINPUTS`, fixes `SOURCE_DATE_EPOCH`, enables `FORCE_SOURCE_DATE`, and sets UTC. These reduce variable output but do not make unrelated TeX installations byte-identical. Canonical CI and release builds therefore use the pinned `texlive` service in `compose.yaml`. Documents store publication dates explicitly rather than use `\today`.

After compilation, `main.pdf`, `main.toc`, logs, and other temporary files remain in `.build/<document>/`. The PDF is the one to inspect locally for a course. Do not copy or stage it under `1/`, `2/`, or `3/`.

## Generated README content

For courses and integration projects, the tool parses `main.toc` into a localized Markdown table of contents between:

```html
<!-- GENERATED:START -->
<!-- GENERATED:END -->
```

Course README blocks link to the deterministic asset in the rolling `notes-latest` release, for example:

```text
https://github.com/simonesiega/unipd-computer-engineering/
releases/download/notes-latest/1-calculus-1.pdf
```

Integration README blocks continue to link to their tracked local `main.pdf`. Component examples do not receive generated README content. Existing content outside the markers is preserved.

With `--no-compile`, README generation reuses `main.pdf` and `main.toc` from `.build/`; non-course documents may fall back to local generated files. If required output is unavailable, the command fails before changing the README. Use `--no-readme` when intentionally compiling or reusing only a PDF.

## Generated-state verification

`--check-generated` compiles into `.build/` without publishing tracked files. It checks:

- generated course and integration README content;
- tracked component-example and integration PDFs byte for byte.

It deliberately does not compare a course PDF with `<year>/<course>/main.pdf`, because that file must not be tracked or expected. Git-aware repository validation independently rejects any generated course PDF forced into the index.

`--check-generated` cannot be combined with `--no-compile` or `--no-readme`.

## Processing options

| Option | Behavior |
|---|---|
| `--no-compile` | Reuse existing PDF and `.toc` data; fail safely when required output is missing |
| `--no-readme` | Compile without creating or updating generated README content |
| `--keep-going` | Process every selected document and report all failures afterward |
| `--clean` | Remove the repository-level `.build/` directory after success |
| `--check-generated` | Verify tracked generated fixtures and README sections without replacing them |

Without `--keep-going`, the first error stops processing. With it, all failures are collected and returned through a non-zero status.

## Release packaging

After a successful complete build, package course outputs with stable injected metadata:

```bash
python3 latex/tools/package_notes.py \
  --source-commit <40-character-sha> \
  --release-timestamp <iso-8601-timestamp> \
  --release-title "Latest compiled notes"
```

The tool:

1. removes and recreates `.build/release/`;
2. discovers direct `<year>/<course>/main.tex` sources;
3. requires each matching `.build/<year>/<course>/main.pdf`;
4. validates year and lowercase kebab-case identity;
5. derives `<year>-<course-slug>.pdf` without spaces or path traversal;
6. rejects duplicate names rather than overwrite them;
7. copies PDF bytes without changing canonical build output;
8. sorts courses by degree year, course name, and asset filename;
9. writes `manifest.json`, `RELEASE_NOTES.md`, and `SHA256SUMS.txt`.

The manifest records course metadata where available, source directory, size, SHA-256, source commit, and injected release timestamp. Supplying the commit timestamp makes repeated packaging of the same source deterministic. An empty source archive succeeds with an empty manifest and explanatory release index. A course source with no compiled PDF fails clearly.

Release staging is ignored and tool-owned. Workflows publish exactly those staged files; they do not duplicate naming, manifest, or checksum logic in shell.

See [Docker builds](../getting-started/docker.md), [Building documents](../getting-started/building-documents.md), and [Validation, Tests, and CI](tool-test-and-ci.md).
