# Course Structure

[← Documentation](../README.md) · [Creating a course](../getting-started/creating-a-course.md) · [Writing notes](writing-notes.md) · [Metadata](metadata.md)

This guide defines how course files are organized. All course-specific sources and assets are kept together under the course’s degree-year directory, with one `main.tex` entry point.

## Standard layout

To generate this structure automatically, follow the [Creating a course](../getting-started/creating-a-course.md) guide, which explains how to use `create_course.py` and configure the required course metadata.

```text
<year>/<course-name>/
├── main.tex              # required source entry point
├── README.md             # contains a generated contents section
├── sections/             # optional course content
│   └── .gitkeep          # preserves the initially empty directory
├── assets/               # optional images, diagrams, and data
│   └── .gitkeep          # preserves the initially empty directory
└── references.bib        # optional bibliography
```

`<year>` must be `1`, `2`, or `3`, and `<course-name>` must use lowercase kebab-case. Course directories must be direct children of their degree-year directory. The course creation tool adds empty `.gitkeep` files so that Git retains `sections/` and `assets/` before they contain course files.

## File responsibilities

| Path | Responsibility |
|---|---|
| `main.tex` | Loads the document class, defines metadata, and establishes document order. |
| `sections/` | Contains substantial chapters or sections included by `main.tex`. |
| `assets/` | Stores course-specific images, diagrams, data, and supporting files. |
| `references.bib` | Stores bibliography entries when the course uses external references. |
| `.build/<year>/<course-name>/main.pdf` | Ignored local/CI output produced by the build tool; not a course source file. |
| `README.md` | Provides course information, a rolling-release PDF link, and an automatically generated contents section. |

Keep shared LaTeX behavior outside course directories. Reusable commands, environments, typography, and layout belong in the shared class or components.

## Organizing source files

Keep short documents in `main.tex`. Move substantial content into `sections/` as the course grows:

```text
sections/
├── 01-introduction.tex
├── 02-main-topic.tex
└── 03-exercises.tex
```

Include the files from `main.tex` in reading order:

```latex
\input{sections/01-introduction}
\input{sections/02-main-topic}
\input{sections/03-exercises}
```

Use lowercase kebab-case, descriptive names, and two-digit numeric prefixes when file order matters. Do not create another `main.tex` inside a course.

## Assets

Use descriptive filenames and store each asset within the course that uses it. Create subdirectories under `assets/` only when they make the directory easier to navigate.

Assets may use any format appropriate for the course, including SVG images, JPEG files, CSV datasets, Jupyter notebooks, Draw.io diagrams, and domain-specific data files.

Document the source and license of all third-party material. Whenever possible, prefer original diagrams, figures, and datasets.

## Generated files

Builds place compilation files and the final course PDF under the repository-level `.build/<year>/<course-name>/` directory. The PDF stays there for local review. Pull requests expose it through a temporary CI artifact, while successful complete `main` builds publish a renamed copy through the rolling GitHub Release.

The build tool creates or updates the generated section of `README.md` from the compiled table of contents and links to the stable rolling-release asset. Do not edit content between:

```html
<!-- GENERATED:START -->
<!-- GENERATED:END -->
```

Manual course information may be written outside those markers.

Do not commit temporary LaTeX files such as `.aux`, `.log`, `.out`, or `.toc`, and do not commit `<year>/<course>/main.pdf`. When source changes affect the document, rebuild in the [canonical Docker environment](../getting-started/docker.md), visually review `.build/<year>/<course>/main.pdf`, and commit only source-owned files plus generated README content. If a course PDF was accidentally tracked, remove it with `git rm --cached -- <year>/<course>/main.pdf`; normal contributions must not rewrite Git history.

Continue with [Writing notes](writing-notes.md) for content conventions or [Building documents](../getting-started/building-documents.md) for build and validation commands.
