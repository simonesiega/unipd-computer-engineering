# Repository Architecture

[← Documentation](../README.md) · [Course structure](../user-guide/course-structure.md) · [Document class](../reference/unipd-notes-class.md) · [Build system](build-system.md) · [Validation and CI](validation-and-ci.md)

The repository combines course-specific archives with one shared LaTeX system and a small set of Python tools. Course sources and assets remain separated, while common presentation, compilation, validation, and automation are centralized.

## System overview

```text
Course sources ──────────────┐
Component examples ──────────┤
                             ├─> build.py ─> .build/<document>/
Shared class and components ─┤                    │
Bundled fonts ───────────────┘                    ├─> main.pdf
                                                  └─> main.toc
                                                        │
                         course directory <─────────────┤
                         main.pdf + generated README ───┘
```

Repository validation runs separately from compilation. Pre-commit executes structural and source checks, while GitHub Actions coordinates quality checks and affected-document builds.

## Repository layers

| Layer | Location | Responsibility |
|---|---|---|
| Course archives | `1/`, `2/`, `3/` | Course-specific sources, assets, references, compiled PDFs, and generated README contents |
| Shared typesetting | `latex/unipd-notes.cls` | Common document defaults and component loading |
| LaTeX components | `latex/components/` | Focused packages with isolated examples |
| Fonts | `latex/fonts/` | Bundled typefaces, configuration, and licenses |
| Build and validation | `latex/tools/` | Document discovery, compilation, generated files, and repository checks |
| Documentation | `docs/md/` | User, reference, and development guides |
| Automation | `.github/`, `.pre-commit-config.yaml` | Continuous integration, dependency updates, and local quality checks |

Root-level files define project policies, licenses, contribution rules, and the public entry point.

## Document model

Every course entry point is located at:

```text
<year>/<course-name>/main.tex
```

The build system also treats each `latex/components/<component>/example/main.tex` as an independent document.

All documents use the shared `unipd-notes` class. The class loads the component stack, and the components provide metadata, typography, mathematics, educational environments, figures, code, navigation, references, and document structure.

Course files may depend on the shared LaTeX system. Shared components must not depend on a particular course.

## Build flow

For each selected document, the build tool:

1. resolves its `main.tex`;
2. creates a mirrored output directory under `.build/`;
3. compiles with `latexmk` and LuaLaTeX;
4. makes the repository's `latex/` directory available through `TEXINPUTS`;
5. reads the generated table of contents;
6. publishes `main.pdf` beside the source;
7. updates the generated section of a course `README.md`.

Component examples publish their PDF but do not receive generated README contents.

The `--check-generated` mode compares newly built outputs with committed files without replacing them. Detailed commands and selection modes are documented in [Build system](build-system.md).

## Change boundaries

| Change | Expected impact |
|---|---|
| File inside one course | That course |
| File inside one component example | That example |
| Shared class or component package | Every document |
| Bundled font | Every document |
| Build tool | Every document |
| Documentation or policy only | No LaTeX document |

New shared paths must be added to the affected-document mapping so that changes to them trigger a complete build.

## Validation and automation

`check_repository.py` validates the required course and component layouts and checks LaTeX sources for UTF-8, unresolved conflict markers, tabs, and trailing whitespace.

Pre-commit combines that repository-specific validation with general file checks. In GitHub Actions, the quality job runs first; the build job runs only after it succeeds.

The CI workflow performs a complete build for an initial or manual run. For ordinary pushes and pull requests, it collects changed paths and compiles only the affected documents. PDFs produced under `.build/` are uploaded as workflow artifacts, and failed LaTeX logs are retained temporarily.

See [Validation and CI](validation-and-ci.md) for workflow behavior and [Building documents](../getting-started/building-documents.md) for the contributor-facing commands.
