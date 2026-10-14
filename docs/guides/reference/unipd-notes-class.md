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

Bibliography builds require Biber, which `latexmk` invokes automatically. Without the `bibliography` option, `\printcoursebibliography` does nothing; citation commands from BibLaTeX are not loaded.

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

The class loads the shared packages in the dependency order recorded in [`unipd-notes.cls`](../../../latex/unipd-notes.cls). Use their public interfaces rather than loading `.sty` files directly. [COMPONENTS.md](../../../latex/components/COMPONENTS.md#component-catalogue) owns the API catalogue; the [component router](../../../latex/components/README.md#component-catalogue) links isolated examples.

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

Without an option list, `\printcourselists` prints all four lists. The [`front-back-matter`](../../../latex/components/front-back-matter/example/main.tex) example shows these phases in context.

## Minimal course document

Use [Creating a course](../getting-started/creating-a-course.md) for a complete localized scaffold. [Metadata: course setup](../user-guide/metadata.md#course-setup) owns the illustrative `\unipdsetup` block and field reference; place that setup before the document environment.

For a complete composed example rather than another template here, inspect the [English integration source](../../../latex/integration/english/main.tex) or [Italian integration source](../../../latex/integration/italian/main.tex). [Writing notes](../user-guide/writing-notes.md) owns content conventions.

## Numbering and contents

Headings are numbered through `\subsubsection` (`secnumdepth=3`); the contents page includes through `\subsection` by default (`tocdepth=2`). Set a literal `\setcounter{tocdepth}{N}` in the preamble if a course needs a different contents depth. The generated README respects that explicit setting too.

Equations and numbered educational environments use chapter-based numbering. Each numbered environment has its own counter: theorem and definition numbers do not share a sequence. The `proof` environment is unnumbered.

## Extending the class

Follow [Component development](../../../latex/components/COMPONENTS.md#adding-or-changing-a-component) for ownership, dependency ordering, examples, and validation. Do not use or redefine internal class path commands from course documents.
