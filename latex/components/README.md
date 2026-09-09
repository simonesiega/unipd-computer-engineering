# LaTeX Components

[← Documentation](../../docs/README.md) · [`unipd-notes` class](../../docs/md/reference/unipd-notes-class.md) · [Docker builds](../../docs/md/getting-started/docker.md)

This directory contains the reusable LaTeX components loaded by [`unipd-notes.cls`](../unipd-notes.cls).

Each component owns one focused responsibility and exposes a small public interface shared by course documents and integration examples.

## Component structure

Every component follows the same layout:

```text
component-name/
├── component-name.sty
└── example/
    ├── main.tex
    └── main.pdf
```

| File | Responsibility |
|---|---|
| `component-name.sty` | Reusable LaTeX implementation |
| `example/main.tex` | Isolated example of the component's public behavior |
| `example/main.pdf` | Canonically compiled visual fixture |

No additional files or subdirectories belong inside a component directory.

## Component catalogue

| Component | Responsibility |
|---|---|
| [`algorithms`](algorithms/) | Localized pseudocode, algorithm numbering, captions, labels, input/output declarations, and presentation |
| [`code`](code/) | Source listings and terminal sessions with syntax highlighting, numbering, captions, labels, and monospace typography |
| [`cover`](cover/) | Course-note cover generated from shared document metadata |
| [`diagrams`](diagrams/) | Shared TikZ and CircuitikZ styles for technical diagrams |
| [`document-structure`](document-structure/) | Chapter and section hierarchy, numbering, unnumbered structure, and appendices |
| [`environments`](environments/) | Definitions, theorems, proofs, examples, remarks, warnings, exercises, and solutions |
| [`figures-tables`](figures-tables/) | Figures, tables, captions, source notes, float behavior, and table typography |
| [`front-back-matter`](front-back-matter/) | Preface, revision history, document lists, and front/main-matter transitions |
| [`glossary`](glossary/) | Course terminology and acronyms |
| [`lists`](lists/) | Bulleted, numbered, descriptive, nested, and procedural lists |
| [`mathematics`](mathematics/) | Mathematical fonts, symbols, operators, equation behavior, and common helpers |
| [`metadata`](metadata/) | Course/document configuration, shared translations, and language-dependent defaults |
| [`navigation`](navigation/) | PDF hyperlinks, URLs, bookmarks, and link behavior |
| [`page-style`](page-style/) | Page geometry, margins, headers, footers, and page numbers |
| [`references`](references/) | Cross-references, labels, reference formatting, and optional bibliography support |
| [`table-of-contents`](table-of-contents/) | Main contents page and front-matter contents presentation |
| [`typography`](typography/) | Fonts, colors, text hierarchy, paragraph behavior, spacing, and general typography |

For class-level loading, supported options, and document lifecycle interfaces, see the [`unipd-notes` class reference](../../docs/md/reference/unipd-notes-class.md).

## Responsibility boundaries

Components should remain independent in purpose and reuse existing shared interfaces instead of duplicating them.

Important ownership rules:

- `metadata` owns document information, translations, and language-dependent shared labels;
- `typography` owns fonts, colors, text hierarchy, and general typographic primitives;
- `page-style` owns page geometry, headers, footers, and page-number presentation;
- `figures-tables` owns shared figure and table infrastructure;
- `references` owns cross-reference names and formatting;
- `diagrams` builds on figure infrastructure for TikZ and CircuitikZ diagrams;
- course-specific behavior does not belong in shared components.

Language-dependent text must use the repository translation interfaces rather than hard-coded Italian or English labels.

A component may depend on another component when the dependency follows these ownership boundaries. Dependencies should remain explicit and one-directional.

## Component requirements

Every component must:

1. use the standard directory structure;
2. contain one `.sty` package named after its directory;
3. provide an isolated, compilable `example/main.tex`;
4. keep its corresponding `example/main.pdf` up to date;
5. own one clear responsibility;
6. expose a small and stable public interface;
7. reuse existing shared fonts, colors, counters, spacing, and helpers;
8. avoid unrelated global changes;
9. follow repository naming and formatting conventions;
10. compile cleanly with LuaLaTeX.

Avoid relying on undocumented internals of third-party LaTeX packages when a public interface is available.

## Examples as visual fixtures

Each `example/main.tex` serves both as documentation and as an isolated visual test.

A good example should:

- demonstrate the important public behavior of the component;
- use realistic Computer Engineering content;
- remain focused on the component being tested;
- include labels, captions, numbering, or references when relevant;
- compile through the normal repository build system.

The corresponding `example/main.pdf` is tracked and must be regenerated whenever the component or its example changes.

The integration projects under [`latex/integration/`](../integration/) provide broader end-to-end verification across multiple components and both supported languages.

## Adding or changing a component

When modifying the component system:

1. identify the component that owns the behavior;
2. update its `.sty` implementation and isolated example;
3. register a new component in [`unipd-notes.cls`](../unipd-notes.cls) at the correct dependency position when necessary;
4. update this catalogue if responsibilities or available components change;
5. rebuild the affected component example;
6. run both integration examples when shared behavior may affect them;
7. review the regenerated PDFs visually;
8. run the repository generated-state checks before committing.

For canonical build commands and generated-file verification, see [Building documents](../../docs/md/getting-started/building-documents.md).

Shared tools, general documentation, assets, and build scripts belong elsewhere in the repository rather than inside a component directory.
