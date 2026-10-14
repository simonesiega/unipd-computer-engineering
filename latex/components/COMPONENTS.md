# Component Reference and Development

[← Component router](README.md) · [Document class](../../docs/guides/reference/unipd-notes-class.md) · [Font reference](../fonts/FONTS.md)

This reference owns the shared packages' public-interface catalogue, dependency boundaries, and development requirements. For package directories and example sources, use the [component router](README.md#component-catalogue).

## Component structure

Every component follows this exact layout:

```text
component-name/
├── component-name.sty
└── example/
    ├── main.tex
    └── main.pdf
```

| File | Responsibility |
|---|---|
| `component-name.sty` | Reusable implementation named after its directory. |
| `example/main.tex` | Isolated demonstration of public behavior. |
| `example/main.pdf` | Canonically compiled, tracked visual fixture. |

Component names use lowercase ASCII kebab-case. No unrelated files or directories belong inside a component directory. The wider source tree is documented in [LATEX.md](../LATEX.md).

## Component catalogue

Courses load the [document class](../../docs/guides/reference/unipd-notes-class.md), not individual component packages. The class controls dependency order. Consult the [isolated examples](README.md#component-catalogue) for complete syntax.

| Component | Public interfaces or facilities |
|---|---|
| `algorithms` | `algorithm`, `\KwInput`, `\KwOutput`, `\For`, `\While`, `\If`, `\Return`; localized `algorithm2e` pseudocode. |
| `code` | `unipdcode`, `unipdterminal`, and shared `listings` styles. |
| `cover` | `\makecoursecover`, using the document's metadata. |
| `diagrams` | `unipd/...` TikZ and CircuitikZ styles for graphs, automata, flowcharts, architecture, UML, and circuits. |
| `document-structure` | Heading hierarchy, numbering, and `\courseappendices`. |
| `environments` | Definitions, results, proofs, examples, remarks, warnings, exercises, and solutions. |
| `figures-tables` | Figures, tables, captions, `L`/`C` columns, `\figuresource`, and `\tablesource`. |
| `front-back-matter` | `coursepreface`, `revisionhistory`, `\revision`, `\printcourselists`, and front/main-matter transitions. |
| `glossary` | `\newcourseterm`, `\newcourseacronym`, `\gls`, and `\printcourseglossary`, without an external indexing step. |
| `lists` | Standard lists and `steps`. |
| `mathematics` | Math fonts, operators, delimiters, `\vect`, `\mat`, number sets, and `siunitx` quantities. |
| `metadata` | `\unipdsetup`, `\unipdmetadata`, `\unipdifmetadata`, `\unipdheadcourse`, and `\unipdtranslate`; field details belong in [Metadata](../../docs/guides/user-guide/metadata.md). |
| `navigation` | `\href`, `\url`, PDF bookmarks, and PDF metadata. |
| `page-style` | Geometry, running headers, footers, and page numbers. |
| `references` | `\cref`, `\Cref`, optional BibLaTeX support, and `\printcoursebibliography`. |
| `table-of-contents` | `\makecoursetableofcontents` and Roman-numbered contents. |
| `typography` | Text fonts, shared colors, paragraph spacing, and emphasis. |

The class reference owns [document-level lifecycle commands](../../docs/guides/reference/unipd-notes-class.md#document-lifecycle); [Writing notes](../../docs/guides/user-guide/writing-notes.md) owns their pedagogical use.

## Responsibility boundaries

Extend the existing owner rather than creating duplicate commands or cross-cutting global patches. In particular:

- `metadata` owns translations and shared language-dependent labels;
- `typography` owns text fonts and general typographic primitives, while `page-style` owns geometry and running page elements;
- `figures-tables` owns float/caption infrastructure; `diagrams` builds on it;
- `references` owns cross-reference names and formatting;
- course-specific content must not become a dependency of a shared package.

Dependencies must be explicit, one-directional, and compatible with the class's loading order. Use translation interfaces for language-dependent text rather than hard-coded Italian or English labels.

## Component requirements

Public commands and environments should be semantic, focused, documented, and backward-compatible where practical. Reuse shared fonts, colors, counters, lengths, translations, and existing packages. Prefer upstream public interfaces over undocumented internals, and preserve LuaLaTeX compatibility.

The [course compatibility contract](../../docs/guides/development/architecture.md#course-compatibility-contract) defines what belongs in shared infrastructure versus a course-local extension.

## Examples as visual fixtures

An example should demonstrate the package's important public behavior with focused Computer Engineering material. Include labels, captions, numbering, references, localization, or long-line cases when relevant to the feature; do not turn it into an unrelated showcase.

`example/main.pdf` is tool-owned and must be regenerated when its sources or package change. The [English and Italian integration documents](../LATEX.md#integration-examples) exercise interactions across components. [Building documents](../../docs/guides/getting-started/building-documents.md#review-the-output) owns fixture replacement and PDF-review instructions.

## Adding or changing a component

1. Identify the owner and inspect its package, example, callers, and dependency order in [`unipd-notes.cls`](../unipd-notes.cls).
2. Update the implementation and isolated example together, respecting the requirements above.
3. For a genuinely new responsibility, add the standard component layout, register the package in the class, and update this catalogue, the [example router](README.md#component-catalogue), and [directory reference](../LATEX.md#components).
4. Follow [Building documents](../../docs/guides/getting-started/building-documents.md) for compilation, visual review, and generated-state checks. The [affected-document rules](../../docs/guides/development/build-system.md#target-selection) determine the required scope.

Font changes additionally follow [Changing the font system](../fonts/FONTS.md#changing-the-font-system). General documentation, tools, and course assets do not belong inside an individual component directory.
