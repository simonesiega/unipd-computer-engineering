# LaTeX Components

This directory contains the modular components used by the [`unipd-notes`](../unipd-notes.cls) document class.

Each component has one specific responsibility and always follows the same structure:

```text
component-name/
├── component-name.sty
└── example/
    ├── main.tex
    └── main.pdf
```

The files have the following roles:

- `component-name.sty` contains the reusable LaTeX implementation.
- `example/main.tex` demonstrates the component in isolation.
- `example/main.pdf` is the compiled example produced with LuaLaTeX.

No additional files belong inside a component directory.

## Components

| Component | Purpose | Package | Example source | Example PDF |
|---|---|---|---|---|
| **Algorithms** | Localized pseudocode, algorithm numbering, line numbering, input and output declarations, captions, labels, and presentation. | [`algorithms.sty`](algorithms/algorithms.sty) | [`main.tex`](algorithms/example/main.tex) | [`main.pdf`](algorithms/example/main.pdf) |
| **Code** | Source-code listings and terminal sessions with syntax highlighting, line numbering, captions, labels, and consistent monospace typography. | [`code.sty`](code/code.sty) | [`main.tex`](code/example/main.tex) | [`main.pdf`](code/example/main.pdf) |
| **Cover** | Course-note cover generated from the shared academic and document metadata. | [`cover.sty`](cover/cover.sty) | [`main.tex`](cover/example/main.tex) | [`main.pdf`](cover/example/main.pdf) |
| **Diagrams** | Reusable TikZ and CircuitikZ styles for graphs, automata, circuits, flowcharts, software architecture, and UML diagrams. | [`diagrams.sty`](diagrams/diagrams.sty) | [`main.tex`](diagrams/example/main.tex) | [`main.pdf`](diagrams/example/main.pdf) |
| **Document structure** | Chapter and section hierarchy, numbering, unnumbered structural sections, and appendix management. | [`document-structure.sty`](document-structure/document-structure.sty) | [`main.tex`](document-structure/example/main.tex) | [`main.pdf`](document-structure/example/main.pdf) |
| **Environments** | Definitions, theorems, proofs, propositions, lemmas, corollaries, examples, remarks, warnings, exercises, and solutions. | [`environments.sty`](environments/environments.sty) | [`main.tex`](environments/example/main.tex) | [`main.pdf`](environments/example/main.pdf) |
| **Figures and tables** | Figure and table structure, external images, captions, source notes, labels, reference integration, float behavior, and table typography. | [`figures-tables.sty`](figures-tables/figures-tables.sty) | [`main.tex`](figures-tables/example/main.tex) | [`main.pdf`](figures-tables/example/main.pdf) |
| **Front and back matter** | Preface, revision history, document lists, appendix and bibliography placement, and closing sections. | [`front-back-matter.sty`](front-back-matter/front-back-matter.sty) | [`main.tex`](front-back-matter/example/main.tex) | [`main.pdf`](front-back-matter/example/main.pdf) |
| **Glossary** | Course terminology and acronyms with consistent definitions, grouping, and presentation. | [`glossary.sty`](glossary/glossary.sty) | [`main.tex`](glossary/example/main.tex) | [`main.pdf`](glossary/example/main.pdf) |
| **Lists** | Bulleted, numbered, descriptive, nested, and procedural lists with consistent spacing and indentation. | [`lists.sty`](lists/lists.sty) | [`main.tex`](lists/example/main.tex) | [`main.pdf`](lists/example/main.pdf) |
| **Mathematics** | Mathematical fonts, symbols, operators, equation behavior, and helpers for vectors, matrices, sets, and probability. | [`mathematics.sty`](mathematics/mathematics.sty) | [`main.tex`](mathematics/example/main.tex) | [`main.pdf`](mathematics/example/main.pdf) |
| **Metadata** | Central configuration of course and document information, language-dependent defaults, and shared translations. | [`metadata.sty`](metadata/metadata.sty) | [`main.tex`](metadata/example/main.tex) | [`main.pdf`](metadata/example/main.pdf) |
| **Navigation** | PDF hyperlinks, URLs, bookmarks, link appearance, and navigation behavior. | [`navigation.sty`](navigation/navigation.sty) | [`main.tex`](navigation/example/main.tex) | [`main.pdf`](navigation/example/main.pdf) |
| **Page style** | A4 page geometry, margins, running headers, footers, and page-number presentation. | [`page-style.sty`](page-style/page-style.sty) | [`main.tex`](page-style/example/main.tex) | [`main.pdf`](page-style/example/main.pdf) |
| **References** | Intelligent cross-references, labels, reference formatting, and optional bibliography management. | [`references.sty`](references/references.sty) | [`main.tex`](references/example/main.tex) | [`main.pdf`](references/example/main.pdf) |
| **Table of contents** | Main table of contents, linked entries, front-matter pagination, and transition to Arabic page numbering. | [`table-of-contents.sty`](table-of-contents/table-of-contents.sty) | [`main.tex`](table-of-contents/example/main.tex) | [`main.pdf`](table-of-contents/example/main.pdf) |
| **Typography** | Document fonts, shared colors, typographic hierarchy, paragraph behavior, vertical rhythm, and general text rules. | [`typography.sty`](typography/typography.sty) | [`main.tex`](typography/example/main.tex) | [`main.pdf`](typography/example/main.pdf) |

## Loading

The components are loaded centrally by [`unipd-notes.cls`](../unipd-notes.cls) in dependency order.

A document enables the complete system with:

```latex
\documentclass[italian]{unipd-notes}
\documentclass[english]{unipd-notes}
```

Course documents should normally load the class rather than importing individual component packages directly. The language option localizes all shared component labels.

LuaLaTeX is required to compile the class and every component example.

## Building the examples

From the repository root, compile all documents and regenerate their published PDFs with:

```bash
python3 latex/tools/build.py --all
```

To compile a single component example, pass its directory to the same tool:

```bash
python3 latex/tools/build.py latex/components/diagrams/example
```

The comprehensive [`english`](../integration/english/) and [`italian`](../integration/italian/) integration examples verify localization across components, including statements, algorithms, listings, document lists, quantities, cross-references, and appendices.

## Component responsibilities

Each component has one specific responsibility and should not duplicate functionality provided by another component.

Shared definitions such as fonts and colors belong to `typography`, document information and translated labels belong to `metadata`, and page layout belongs to `page-style`. Components must retrieve language-dependent text with `\unipdtranslate` rather than hard-code Italian or English labels.

`figures-tables` manages figures and tables, including floats, captions, numbering, labels, reference integration, and source notes. `diagrams` provides TikZ and CircuitikZ styles for technical diagrams, which continue to use the standard figure infrastructure from `figures-tables`.

Therefore, `diagrams` depends on `figures-tables`, while `figures-tables` can be used independently.

## Component requirements

Every component must:

1. use the exact directory structure documented above;
2. contain one `.sty` package named after its directory;
3. contain an isolated and compilable `example/main.tex`;
4. contain the corresponding `example/main.pdf`;
5. have one clear responsibility;
6. expose a small and stable public interface;
7. reuse existing fonts, colors, counters, spacing, and helpers;
8. avoid unrelated global changes;
9. follow the naming and formatting conventions already used by the repository;
10. compile with LuaLaTeX without errors, undefined references, duplicate destinations, or avoidable overfull boxes.

## Examples

Each `example/main.tex` is both documentation and a visual test.

An example should:

- demonstrate the component's important public features;
- use realistic Computer Engineering content in its selected language;
- remain focused on that component;
- use the shared document style where appropriate;
- include numbering, labels, captions, or references when relevant;
- compile independently through the repository's normal build system.

The corresponding `example/main.pdf` must be regenerated whenever the example source or component implementation changes.

## Adding or changing a component

When adding a component or changing an existing one:

1. inspect the current component conventions;
2. create or update the `.sty` package;
3. create or update `example/main.tex`;
4. register the component in [`unipd-notes.cls`](../unipd-notes.cls) at the correct dependency position;
5. update this README when the component catalogue or responsibility boundaries change;
6. compile the component example;
7. compile the complete demonstration document;
8. regenerate the affected `main.pdf` files;
9. review the PDFs visually before committing.

Do not add extra files or subdirectories to a component folder. Shared tools, documentation, assets, and build scripts belong elsewhere in the repository.
