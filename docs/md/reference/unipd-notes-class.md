# `unipd-notes` Document Class

[← Documentation](../README.md) · [Metadata](../user-guide/metadata.md) · [Components](../../../latex/components/README.md) · [Fonts](../../../latex/fonts/README.md)

The `unipd-notes` class provides the shared foundation for every course document. It configures the base page model, exposes the bibliography option, and loads the repository's LaTeX components.

## Basic usage

Course documents should load the class directly:

```latex
\documentclass{unipd-notes}
```

The repository build tool adds `latex/` to the LaTeX search path, so course files should not use a relative path to the class.

LuaLaTeX is required. Compilation with another TeX engine stops with an error.

## Class option

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

Other class options are forwarded to the underlying `scrreprt` class. Avoid overriding the shared defaults unless the change is necessary and consistent with the rest of the archive.

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

## Typical document

```latex
\documentclass{unipd-notes}

\unipdsetup{
  course = {Official Course Name},
  author = {Your Name},
  academic-year = {2026--2027},
  degree-year = {1},
  semester = {1},
  document-type = {Appunti delle lezioni},
  version = {0.1.0}
}

\begin{document}
\makecoursecover
\makecoursetableofcontents

\chapter{Introduction}

Course content.

\end{document}
```

See [Metadata](../user-guide/metadata.md) for every `\unipdsetup` field and [Writing notes](../user-guide/writing-notes.md) for authoring conventions.

## Extending the class

Add shared behavior to the component responsible for that concern. Create a new component only when the feature has a distinct responsibility and cannot reasonably belong to an existing one.

Preserve component load order and compatibility across every course and example. Changes to the class or a component package affect all documents and require a full build.

Do not use or redefine the class's internal path commands in course documents.
