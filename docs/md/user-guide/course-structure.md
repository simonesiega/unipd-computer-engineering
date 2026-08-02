# Course Structure

[← Documentation](../README.md) · [Creating a course](../getting-started/creating-a-course.md) · [Writing notes](writing-notes.md) · [Metadata](metadata.md)

This guide defines how course files are organized. All course-specific sources and assets are kept together under the course’s degree-year directory, with one `main.tex` entry point.

## Standard layout

To generate this structure automatically, follow the [Creating a course](../getting-started/creating-a-course.md) guide, which explains how to use `create_course.py` and configure the required course metadata.

```text
<year>/<course-name>/
├── main.tex              # required source entry point
├── main.pdf              # generated and committed
├── README.md             # contains a generated contents section
├── sections/             # optional course content
├── assets/               # optional images, diagrams, and data
└── references.bib        # optional bibliography
```

`<year>` must be `1`, `2`, or `3`, and `<course-name>` must use lowercase kebab-case. Course directories must be direct children of their degree-year directory.

## File responsibilities

| Path | Responsibility |
|---|---|
| `main.tex` | Loads the document class, defines metadata, and establishes document order. |
| `sections/` | Contains substantial chapters or sections included by `main.tex`. |
| `assets/` | Stores course-specific images, diagrams, data, and supporting files. |
| `references.bib` | Stores bibliography entries when the course uses external references. |
| `main.pdf` | Published output produced by the build tool. |
| `README.md` | Provides course information and an automatically generated contents section. |

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

Use descriptive filenames and keep each asset close to the course that uses it. Create subdirectories under `assets/` only when they improve navigation.

Document the source and license of third-party material. Prefer original diagrams and figures whenever possible.

## Generated files

Builds place temporary files under the repository-level `.build/` directory and publish the final `main.pdf` inside the course directory.

The build tool creates or updates the generated section of `README.md` from the compiled table of contents. Do not edit content between:

```html
<!-- GENERATED:START -->
<!-- GENERATED:END -->
```

Manual course information may be written outside those markers.

Do not commit temporary LaTeX files such as `.aux`, `.log`, `.out`, or `.toc`. When source changes affect the document, commit the updated `main.pdf` and generated README section with the same change.

Continue with [Writing notes](writing-notes.md) for content conventions or [Building documents](../getting-started/building-documents.md) for build and validation commands.
