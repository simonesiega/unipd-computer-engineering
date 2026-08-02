# Repository Architecture

[← Documentation](../README.md) · [Course structure](../user-guide/course-structure.md) · [Document class](../reference/unipd-notes-class.md) · [Build system](build-system.md) · [Validation, Tests, and CI](tool-test-and-ci.md)

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
| Course creation, build, validation, and changelogs | `latex/tools/` | Course scaffolding, document discovery, compilation, generated files, repository checks, and per-course Git histories |
| Documentation | `docs/md/` | User, reference, and development guides |
| Automation | `.github/`, `.pre-commit-config.yaml` | Continuous integration, scheduled changelog generation, dependency updates, and local quality checks |

Root-level files define project policies, licenses, contribution rules, and the public entry point. `CHANGELOG/` mirrors the three degree-year directories and contains one generated Markdown history per course. Tracked `.gitkeep` placeholders preserve `1/`, `2/`, `3/`, `CHANGELOG/`, and each changelog year directory before they contain course material.

## Document model

Every course entry point is located at:

```text
<year>/<course-name>/main.tex
```

The build system also treats each `latex/components/<component>/example/main.tex` as an independent document.

All documents use the shared `unipd-notes` class. The class loads the component stack, and the components provide metadata, typography, mathematics, educational environments, figures, code, navigation, references, and document structure.

Course files may depend on the shared LaTeX system. Shared components must not depend on a particular course.

## Course creation

`create_course.py` creates the standard course layout from validated command-line metadata. It derives an ASCII kebab-case directory name, prevents duplicate course directories across degree years, and maps degree years `1` through `3` to the archive's `2026--2029` academic-year sequence. The generated course contains an initial `main.tex`, `README.md`, and empty `sections/` and `assets/` directories.

The contributor-facing command and options are documented in [Creating a course](../getting-started/creating-a-course.md). Python unit tests live under `latex/tools/test/`, with separate files covering course creation, build selection, changelog generation, and repository validation. Test commands and coverage are documented in [Validation, Tests, and CI](tool-test-and-ci.md).

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

A separate weekly workflow runs `generate_changelog.py` with complete Git history. Every Sunday at 00:00 UTC, it rebuilds each `CHANGELOG/<year>/<course>.md` from commits affecting that course and creates one recap commit when generated files changed. It can also be started manually.

See [Validation, Tests, and CI](tool-test-and-ci.md) for workflow behavior and [Building documents](../getting-started/building-documents.md) for the contributor-facing commands.
