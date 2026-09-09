# `unipd-notes` Document Class

[← Documentation](../README.md) · [Metadata](../user-guide/metadata.md) · [Components](../../../latex/components/README.md) · [Fonts](../../../latex/fonts/README.md)

The `unipd-notes` class is the shared foundation for every course document. It defines the base document model, loads the repository's LaTeX components, and exposes the supported document-level interfaces.

## Basic usage

Load the class directly:

```latex
\documentclass[italian]{unipd-notes}
```

Use `english` for courses taught in English:

```latex
\documentclass[english]{unipd-notes}
```

Repository courses must declare exactly one supported language option.

The build system adds `latex/` to the LaTeX search path, so course sources should not reference the class through a relative path.

LuaLaTeX is required.

## Class options

### Language

Supported language options are:

```text
italian
english
```

The selected language configures shared localization across Babel, `siunitx`, theorem and algorithm labels, cross-references, glossary and contents headings, cover fields, revision history, and other component output.

Italian remains the class-level fallback for compatibility with non-course examples, but repository courses must select a language explicitly.

### Bibliography

Enable bibliography support with:

```latex
\documentclass[italian,bibliography]{unipd-notes}
```

Then register and print the bibliography normally:

```latex
\addbibresource{references.bib}

\begin{document}

% Course content

\printcoursebibliography
\end{document}
```

Bibliography builds require Biber, which `latexmk` invokes automatically.

Other class options are forwarded to the underlying `scrreprt` class.

## Base document

The class is based on KOMA-Script's `scrreprt` with these defaults:

| Setting | Value |
|---|---|
| Font size | `11pt` |
| Paper | `a4paper` |
| Layout | `oneside` |
| Chapter opening | `open=any` |
| Heading size | `headings=normal` |

Shared page and heading behavior should remain centralized in the class and its components.

## Loaded components

The class loads the shared components below:

| Area | Components |
|---|---|
| Document information and presentation | `metadata`, `typography`, `page-style`, `navigation` |
| General content | `lists`, `mathematics`, `figures-tables`, `diagrams` |
| Educational material | `environments`, `code`, `algorithms` |
| Document organization | `document-structure`, `cover`, `table-of-contents` |
| Supporting material | `references`, `glossary`, `front-back-matter` |

Course documents should use the public interfaces exposed by these components rather than loading component `.sty` files directly.

See the [component reference](../../../latex/components/README.md) for component-specific APIs and examples.

## Document lifecycle

The class provides shared interfaces for the main document phases:

| Interface | Purpose |
|---|---|
| `\makecoursefrontmatter` | Create the cover and Roman-numbered table of contents |
| `coursepreface` | Add an optional preface |
| `revisionhistory` and `\revision` | Add an optional revision-history table |
| `\makecoursemainmatter` | Switch to Arabic numbering and begin the main document |
| `\printcourselists` | Print selected document lists |
| `\courseappendices` | Start the appendix sequence |

`\printcourselists` accepts any combination of:

```text
figures
tables
algorithms
listings
```

For example:

```latex
\printcourselists[figures,listings]
```

The [`front-back-matter`](../../../latex/components/front-back-matter/example/main.tex) example shows the complete lifecycle in context.

## Minimal course document

```latex
\documentclass[english]{unipd-notes}

\unipdsetup{
  course = {Official Course Name},
  author = {Ada Lovelace},
  academic-year = {2026--2027},
  degree-year = {1},
  semester = {1},
  document-type = {Lecture notes},
  date = {28 September 2026},
  version = {0.1.0}
}

\begin{document}

\makecoursefrontmatter
\makecoursemainmatter

\chapter{Introduction}

Course content.

\end{document}
```

For the complete `\unipdsetup` field reference, see [Metadata](../user-guide/metadata.md).

For note-writing conventions, see [Writing notes](../user-guide/writing-notes.md).

## Extending the class

Shared behavior should be added to the component that owns that responsibility.

Create a new component only when the feature has a distinct concern that does not fit an existing package.

Changes to the class or shared components affect every course and example, so they require a complete canonical build and generated-state verification.

Do not use or redefine internal class path commands from course documents.
