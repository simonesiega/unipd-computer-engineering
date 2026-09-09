# Repository Architecture

[← Documentation](../README.md) · [Course structure](../user-guide/course-structure.md) · [Document class](../reference/unipd-notes-class.md) · [Build system](build-system.md) · [Validation, tests, and CI](tool-test-and-ci.md)

The repository separates course-owned material from shared typesetting, tooling, generated output, documentation, and automation. Course sources remain reproducible in Git, while compiled course PDFs are treated as build and release artifacts.

## System overview

```text
Course archives
1/   2/   3/
 │    │    │
 └────┴────┴───┐
               │
               v
     latex/unipd-notes.cls
               │
               ├───────────────┐
               │               │
               v               v
     latex/components/   latex/integration/
               │               │
               └───────┬───────┘
                       │
                       v
                  latex/tools/
                       │
                       v
                    .build/
                       │
                       v
          GitHub Actions / Releases


docs/                         Documentation and reference material
.github/                      Repository automation
root files                    Policies, licenses, and project entry points
```

The shared LaTeX layer is reusable across every course. Repository tools discover, build, validate, and package documents, while GitHub Actions orchestrates those tools rather than reimplementing their behavior.

## Repository layers

| Layer | Location | Responsibility |
|---|---|---|
| Course archives | `1/`, `2/`, `3/` | Course-specific LaTeX sources, assets, references, and course README files. |
| Shared document class | `latex/unipd-notes.cls` | Common document defaults and shared component loading. |
| LaTeX components | `latex/components/` | Reusable, focused typesetting features with isolated examples. |
| Integration examples | `latex/integration/` | End-to-end verification of the shared LaTeX system. |
| Fonts | `latex/fonts/` | Bundled typefaces, configuration, attribution, and licenses. |
| Repository tools | `latex/tools/` | Course creation, document discovery, compilation, validation, changelogs, packaging, and generated state. |
| Build environment | `compose.yaml` | Canonical pinned TeX Live environment used locally and in CI. |
| Documentation | `docs/` | User guides, reference material, contributor documentation, and development guides. |
| Automation | `.github/`, `.pre-commit-config.yaml` | CI orchestration, release publication, dependency updates, and local quality hooks. |
| Project policies | Root Markdown and license files | Public project entry point, contribution rules, conduct, security, and licensing. |

## Ownership boundaries

The repository distinguishes between files edited by contributors and files owned by tools or build processes.

| Class | Examples | Ownership |
|---|---|---|
| Source-owned | Course sources, `latex/`, `docs/`, tools, workflows, configuration | Edited and reviewed through normal Git history. |
| Tracked generated content | Generated README sections, `CHANGELOG/`, tracked component and integration fixtures | Updated only through the tool that owns them. |
| Build-owned output | `.build/<document>/` | Disposable local or CI output; never treated as source. |
| Release staging | `.build/release/` | Temporary packaging area owned by the release tooling. |
| Published artifacts | GitHub Release assets | Distributions produced from validated repository sources. |

Generated course `main.pdf` files are not source files. A normal course build places its PDF under `.build/<year>/<course>/main.pdf`; published copies are distributed separately through GitHub Releases.

## Dependency boundaries

A few rules keep the architecture predictable:

- course files may depend on the shared document class and components;
- shared LaTeX code must not depend on a specific course;
- reusable typesetting behavior belongs in the shared class or the appropriate component rather than inside a course;
- repository tools own generated state and packaging logic;
- workflows orchestrate repository tools instead of duplicating build, naming, validation, or packaging rules in shell;
- generated files should be changed through their owning tool, not edited as independent source;
- documentation should describe each concern in one canonical guide and link to it elsewhere.

Every course uses a single `<year>/<course>/main.tex` entry point. Component examples and integration projects are also independent buildable documents, but their detailed structure and build behavior belong in their dedicated guides.

## Where to go next

| Topic | Canonical guide |
|---|---|
| Course directory layout and file responsibilities | [Course structure](../user-guide/course-structure.md) |
| Shared class, options, lifecycle, and component loading | [Document class](../reference/unipd-notes-class.md) |
| Document discovery, selection, compilation, generated README content, and packaging | [Build system](build-system.md) |
| Repository checks, tests, CI artifacts, workflows, and release publication | [Validation, tests, and CI](tool-test-and-ci.md) |
| Canonical local TeX environment | [Docker builds](../getting-started/docker.md) |
| Contributor rules and generated-file expectations | [Contributing](../../../CONTRIBUTING.md) |
