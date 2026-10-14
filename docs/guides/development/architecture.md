# Repository Architecture

[← Documentation](../README.md) · [Course structure](../user-guide/course-structure.md) · [Document class](../reference/unipd-notes-class.md) · [Build system](build-system.md) · [Validation, tests, and CI](tool-test-and-ci.md)

The repository separates course-owned material from shared typesetting, tooling, generated output, documentation, and automation. Course sources remain reproducible in Git, while compiled course PDFs are treated as build and release artifacts.

## System overview

```text
Documents                       Shared typesetting
  1/, 2/, 3/                      latex/unipd-notes.cls
  component examples              latex/components/<name>/<name>.sty
  integration examples            latex/fonts/
         │                               │
         └───────────────┬───────────────┘
                         v
                  latex/tools/build.py
                  (pinned TeX container)
                         │
                         v
                 .build/<document>/
                         │
                   course PDFs only
                         v
              latex/tools/package_notes.py
                         │
                         v
                  .build/release/
                         │
                 manual publication
                         v
                  GitHub Releases
```

GitHub Actions runs the same tools for validation and publication. Normal builds also refresh tracked README sections and example PDF fixtures; check mode verifies them without replacement.

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
| Documentation | `docs/guides/`, `docs/assets/`, `mkdocs.yml` | Markdown guides, public assets, and the MkDocs Material website configuration. |
| Automation | `.github/`, `.pre-commit-config.yaml` | CI orchestration, release publication, dependency updates, and local quality hooks. |
| Project policies | Root Markdown and license files | Public project entry point, contribution rules, conduct, security, and licensing. |

## Ownership boundaries

The repository distinguishes between files edited by contributors and files owned by tools or build processes.

| Class | Examples | Ownership |
|---|---|---|
| Source-owned | Course sources, `latex/`, `docs/`, tools, workflows, configuration | Edited and reviewed through normal Git history. |
| Tracked generated content | Generated README sections, `RELEASES.md`, `CHANGELOG/`, tracked component and integration fixtures | Updated only through the tool that owns them. |
| Build-owned output | `.build/<document>/`, `.build/docs-site/` | Disposable document and website output; never treated as source. |
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

## Course compatibility contract

Adding a course should not require infrastructure changes. The supported scope is all three degree years of the 2026–2029 cohort, either semester, and either Italian or English. There is no list of supported course names: creation, validation, build selection, README generation, and packaging work from the standard course path and metadata.

A new course needs no registration in the class, build tool, or CI workflows. Its generated README and release asset name follow the same rules as existing courses. Publication still requires a separate maintainer action; discovering a course does not approve its academic content or exam coverage.

### Content capabilities

The [component API catalogue](../../../latex/components/COMPONENTS.md#component-catalogue) supplies subject-independent primitives rather than one template per subject. Its [example router](../../../latex/components/README.md#component-catalogue) shows their use.

These capabilities do not prescribe a teaching sequence. Course-local organization follows [Course structure](../user-guide/course-structure.md#organizing-source-files) while retaining the same document hierarchy and build pipeline.

### Course-local extension points

- Keep subject-specific notation, glossary entries, bibliography entries, diagram content, plotting parameters, and data inside the course directory.
- Small semantic notation helpers or listing-language definitions may live in the course preamble or an included course-local source. Reuse existing public commands and shared visual styles rather than redefining them.
- A specialized LaTeX package or TikZ library may be loaded in the course preamble when compatible with the class and available in the pinned TeX environment. Verify it with a canonical build; storing an asset does not imply that LuaLaTeX can include its format directly or run an external converter.
- Promote a genuinely reusable typesetting feature into its existing component owner when needed. Do not introduce a course-specific class, build script, workflow branch, or shared component merely because a new subject is being added.

The [course-creation test catalogue](../../../latex/tools/test/TESTS.md#course-creation) documents the cross-tool compatibility cases and the limits of their synthetic outputs.

This does not guarantee compatibility with every additional package. New languages, cohorts, degree structures, or external preprocessing requirements need an explicit infrastructure review rather than hidden exceptions in course sources.

## Where to go next

| Topic | Canonical guide |
|---|---|
| Course directory layout and file responsibilities | [Course structure](../user-guide/course-structure.md) |
| Shared class, options, lifecycle, and component loading | [Document class](../reference/unipd-notes-class.md) |
| Document discovery, selection, compilation, generated README content, and packaging | [Build system](build-system.md) |
| Repository checks, tests, CI artifacts, workflows, and release publication | [Validation, tests, and CI](tool-test-and-ci.md) |
| Canonical local TeX environment | [Docker builds](../getting-started/docker.md) |
| Public documentation staging, website builds, and Pages deployment | [Documentation site](documentation-site.md) |
| Contributor rules | [Contributing](../../../CONTRIBUTING.md) |
| Physical shared-LaTeX directory tree | [LATEX.md](../../../latex/LATEX.md) |
| Tool files and individual test assertions | [TOOLS.md](../../../latex/tools/TOOLS.md) · [TESTS.md](../../../latex/tools/test/TESTS.md) |
