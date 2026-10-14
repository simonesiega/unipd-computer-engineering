# LaTeX Directory Structure

[← LaTeX overview](README.md) · [Documentation](../docs/README.md) · [Tool index](tools/TOOLS.md) · [Test catalogue](tools/test/TESTS.md)

The `latex/` directory holds the shared document class, reusable typesetting packages, bundled fonts, integration examples, and Python tooling. Course sources live separately under the repository's `1/`, `2/`, and `3/` directories.

This page describes the directory structure only. Use the linked indexes for component interfaces, font details, tool behavior, and individual tests.

## Directory overview

```text
latex/
├── README.md
├── LATEX.md
├── unipd-notes.cls
├── components/
│   ├── README.md
│   ├── COMPONENTS.md
│   └── <component>/        # package and isolated example
├── fonts/
│   ├── README.md
│   ├── FONTS.md
│   ├── FONT-LICENSE.md
│   ├── IBM Plex Mono/
│   ├── Libertinus/
│   └── Source Sans 3/
├── integration/
│   ├── english/
│   └── italian/
└── tools/
    ├── TOOLS.md
    ├── *.py
    └── test/
        ├── TESTS.md
        └── test_*.py
```

| Path | Description |
|---|---|
| [`unipd-notes.cls`](unipd-notes.cls) | Shared entry-point class that loads and coordinates the typesetting components. |
| [`components/`](components/README.md) | Reusable packages, each paired with an isolated source/PDF example. |
| [`fonts/`](fonts/README.md) | Bundled OpenType font families and their documentation. |
| [`integration/`](integration/) | Complete English and Italian example documents that combine shared components. |
| [`tools/`](tools/TOOLS.md) | Python build, generation, validation, packaging, and website tools. |

## Components

Each directory below is one component. [COMPONENTS.md](components/COMPONENTS.md#component-structure) owns its internal package/example layout and API reference; the [component router](components/README.md#component-catalogue) links example sources.

| Directory | Description |
|---|---|
| [`algorithms/`](components/algorithms/) | Localized pseudocode and algorithm presentation. |
| [`code/`](components/code/) | Source-code listings and terminal output. |
| [`cover/`](components/cover/) | Course cover layout. |
| [`diagrams/`](components/diagrams/) | Shared TikZ and CircuitikZ diagram styles. |
| [`document-structure/`](components/document-structure/) | Heading hierarchy, numbering, and appendices. |
| [`environments/`](components/environments/) | Academic blocks such as definitions, proofs, examples, and exercises. |
| [`figures-tables/`](components/figures-tables/) | Figures, tables, captions, and source attribution. |
| [`front-back-matter/`](components/front-back-matter/) | Prefaces, revision history, document lists, and front/main-matter transitions. |
| [`glossary/`](components/glossary/) | Terms, acronyms, and glossary output. |
| [`lists/`](components/lists/) | Standard lists and procedural steps. |
| [`mathematics/`](components/mathematics/) | Mathematical fonts, notation, operators, and quantities. |
| [`metadata/`](components/metadata/) | Course information, shared labels, and translations. |
| [`navigation/`](components/navigation/) | Hyperlinks, bookmarks, and PDF metadata. |
| [`page-style/`](components/page-style/) | Page geometry, running headers, footers, and page numbers. |
| [`references/`](components/references/) | Cross-references and optional bibliography support. |
| [`table-of-contents/`](components/table-of-contents/) | Course contents-page presentation. |
| [`typography/`](components/typography/) | Text fonts, colors, spacing, and emphasis. |

## Fonts

Font-family directories contain the OpenType files used by shared components. [FONTS.md](fonts/FONTS.md#font-catalogue) owns the individual-file catalogue and mappings; [FONT-LICENSE.md](fonts/FONT-LICENSE.md) owns attribution and license text.

| Directory | Description |
|---|---|
| [`IBM Plex Mono/`](fonts/IBM%20Plex%20Mono/) | Monospaced faces for code, commands, and technical identifiers. |
| [`Libertinus/`](fonts/Libertinus/) | Serif text faces and the mathematics font. |
| [`Source Sans 3/`](fonts/Source%20Sans%203/) | Sans-serif faces for headings and structural text. |

## Integration examples

Both language directories contain `main.tex`, a tracked `main.pdf` fixture, and a README with a generated contents section.

| Directory | Description |
|---|---|
| [`integration/english/`](integration/english/README.md) | Combined-component example using the English class option. |
| [`integration/italian/`](integration/italian/README.md) | Combined-component example using the Italian class option. |

## Tools and tests

| Directory | Description |
|---|---|
| [`tools/`](tools/TOOLS.md) | Production Python modules and command-line tools, described file by file in `TOOLS.md`. |
| [`tools/test/`](tools/test/TESTS.md) | Standard-library unit tests, described individually and grouped by source file in `TESTS.md`. |

Local `__pycache__/` directories are interpreter caches, not part of the source layout. Temporary compilation output belongs under the repository-root `.build/` directory, outside `latex/`.
