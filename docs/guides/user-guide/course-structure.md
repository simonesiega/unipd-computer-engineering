# Course Structure

[← Documentation](../README.md) · [Creating a course](../getting-started/creating-a-course.md) · [Writing notes](writing-notes.md) · [Metadata](metadata.md)

This guide defines how course files are organized. All course-specific sources and assets are kept together under the course’s degree-year directory, with one `main.tex` entry point.

## Standard layout

Courses use the layout below. The [course generator](../getting-started/creating-a-course.md) creates `main.tex`, `README.md`, `sections/`, and `assets/`; add `references.bib` if a bibliography is needed.

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

Keep shared typography and layout in the class or components. Course-local notation, glossary entries, listing-language definitions, and diagram parameters may live in the preamble or an included source. Reuse existing interfaces; see the [course compatibility contract](../development/architecture.md#course-compatibility-contract) for extension boundaries.

## Organizing source files

Preserve each course's teaching organization: topics, numbered lectures, laboratories, or a mixture. The repository fixes the entry point and metadata, not a universal chapter sequence or lecture-numbering scheme.

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

Keep editable originals when useful: SVG or Draw.io diagrams, CSV data, notebooks, and other subject-specific files may accompany the notes. Not every stored format can be included directly by LuaLaTeX. Use supported image formats or course-local TikZ sources in the document; document any conversion steps and verify them in the network-disabled Docker environment.

Follow [Sources and attribution](writing-notes.md#sources-and-attribution) for asset provenance and [Licensing and attribution](../../../CONTRIBUTING.md#licensing-and-attribution) for redistribution rights.

## Generated files

[Review the output](../getting-started/building-documents.md#review-the-output) owns generated-file locations, PDF fixtures, and what may be committed. [Generated README content](../development/build-system.md#generated-readme-content) explains marker ownership and the distinction between local contents and published downloads. For hosted review copies, see [CI artifacts](../development/tool-test-and-ci.md#pull-requests-and-main).

Continue with [Writing notes](writing-notes.md) for content conventions or [Building documents](../getting-started/building-documents.md) for build and validation commands.
