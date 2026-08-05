# `unipd-notes` Document Class

[← Documentation](../README.md) · [Metadata](../user-guide/metadata.md) · [Components](../../../latex/components/README.md) · [Fonts](../../../latex/fonts/README.md)

The `unipd-notes` class provides the shared foundation for every course document. It configures the base page model, exposes the bibliography option, and loads the repository's LaTeX components.

## Basic usage

Course documents should load the class directly:

```latex
\documentclass[italian]{unipd-notes}
```

Use `english` instead when the course is taught in English. Repository course validation requires exactly one supported language option.

The repository build tool adds `latex/` to the LaTeX search path, so course files should not use a relative path to the class.

LuaLaTeX is required. Compilation with another TeX engine stops with an error.

## Class options

### Language

Select the language of every course explicitly:

```latex
\documentclass[italian]{unipd-notes}
\documentclass[english]{unipd-notes}
```

Italian remains the class-level default for compatibility with non-course examples and older external documents, but repository courses must never rely on that fallback. The language option configures Babel, `siunitx`, theorem and algorithm names, cross-references, glossary and contents headings, cover fields, revision history, and other shared labels. Course prose and user-supplied metadata must use the same language.

### Bibliography

Enable bibliography support with:

```latex
\documentclass[bibliography]{unipd-notes}
```

The option enables the bibliography features provided by the references component. Register the bibliography file in the preamble and print it at the appropriate position in the document:

```latex
\documentclass[bibliography]{unipd-notes}
\addbibresource{references.bib}

\begin{document}
% Course content

\printcoursebibliography
\end{document}
```

Bibliography builds require Biber, which `latexmk` runs automatically. Courses without a bibliography should omit the option.

The language and bibliography options may be combined, for example `\documentclass[english,bibliography]{unipd-notes}`. Other class options are forwarded to the underlying `scrreprt` class. Avoid overriding the shared defaults unless the change is necessary and consistent with the rest of the archive.

## Base document

The class is based on KOMA-Script's `scrreprt` with these defaults:

| Setting | Value |
|---|---|
| Font size | `11pt` |
| Paper | `a4paper` |
| Layout | `oneside` |
| Chapter opening | `open=any` |
| Heading size | `headings=normal` |

Course documents should rely on these shared settings rather than redefining page dimensions, heading styles, or document layout locally.

## Loaded components

The class loads the following components, grouped here by responsibility:

| Area | Components |
|---|---|
| Document information and presentation | `metadata`, `typography`, `page-style`, `navigation` |
| General content | `lists`, `mathematics`, `figures-tables`, `diagrams` |
| Educational material | `environments`, `code`, `algorithms` |
| Document organization | `document-structure`, `cover`, `table-of-contents` |
| Supporting material | `references`, `glossary`, `front-back-matter` |

Course documents should use the interfaces exposed by these components instead of loading their `.sty` files directly.

See the [component reference](../../../latex/components/README.md) for responsibilities, examples, and extension rules.

## Document lifecycle

Use the shared lifecycle commands instead of manipulating page numbering directly:

| Interface | Purpose |
|---|---|
| `\makecoursefrontmatter` | Create the cover and Roman-numbered table of contents. |
| `coursepreface` | Add an optional preface to the table of contents. |
| `revisionhistory` and `\revision` | Add an optional, page-breakable revision table. |
| `\makecoursemainmatter` | Start Arabic page numbering at 1 before the first chapter. |
| `\printcourselists` | Print localized document lists. The optional selection accepts `figures`, `tables`, `algorithms`, and `listings`; omitting it prints all four. |
| `\courseappendices` | Start the appendix sequence. |

Use `\printcourselists[figures,listings]`, for example, when a course has no tables or algorithms. Omit the command entirely when the document has no listable material.

The focused [`front-back-matter`](../../../latex/components/front-back-matter/example/main.tex) example demonstrates the complete order. Bibliographies and glossaries use their own component interfaces and may be printed where the document structure requires them.

## Typical document

```latex
\documentclass[english]{unipd-notes}

\unipdsetup{
  course = {Official Course Name},
  author = {Ada Lovelace},
  academic-year = {2026--2027},
  degree-year = {1},
  semester = {1},
  document-type = {Lecture notes},
  date = {3 August 2026},
  version = {0.1.0}
}

\begin{document}
\makecoursefrontmatter
\makecoursemainmatter

\chapter{Introduction}

Course content.

\end{document}
```

`\makecoursefrontmatter` creates the cover and table of contents while preserving Roman page numbering, so a preface or revision history can follow it. Call `\makecoursemainmatter` immediately before the first chapter to clear the page, switch to Arabic numbering, and start the main text at page 1.

See [Metadata](../user-guide/metadata.md) for every `\unipdsetup` field and [Writing notes](../user-guide/writing-notes.md) for authoring conventions.

## Extending the class

Add shared behavior to the component responsible for that concern. Create a new component only when the feature has a distinct responsibility and cannot reasonably belong to an existing one.

Preserve component load order and compatibility across every course and example. Changes to the class or a component package affect all documents and require a full [canonical Docker build](../getting-started/docker.md) and generated-file check.

Do not use or redefine the class's internal path commands in course documents.
