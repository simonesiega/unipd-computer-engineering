# Repository Architecture

[← Documentation](../README.md) · [Course structure](../user-guide/course-structure.md) · [Document class](../reference/unipd-notes-class.md) · [Build system](build-system.md) · [Validation, Tests, and CI](tool-test-and-ci.md)

The repository keeps reproducible course sources in Git and distributes compiled course PDFs through GitHub Actions and GitHub Releases. Shared presentation, compilation, validation, packaging, and automation remain centralized.

## System overview

```text
Course sources and assets ───┐
Shared class and components ─┤
Bundled fonts ────────────────┤
Component/integration tests ─┘
              │
              v
      affected/all selection
              │
              v
 canonical Docker compilation
              │
              v
 .build/<document>/main.pdf + logs + TOC
              │
              ├─> generated README validation
              ├─> pull request: temporary review artifact (about 14 days)
              └─> main/snapshot: package_notes.py
                               │
                               v
                    .build/release/
                    ├── <year>-<course-slug>.pdf
                    ├── manifest.json
                    ├── SHA256SUMS.txt
                    └── RELEASE_NOTES.md
                               │
                               ├─> rolling notes-latest release
                               └─> immutable semester snapshot
```

Repository validation runs separately from compilation. Pre-commit executes structural, Git-index, source, workflow, and Python checks. GitHub Actions coordinates quality checks, builds, temporary artifacts, packaging, and publication.

## Ownership boundaries

| Class | Location | Ownership and lifetime |
|---|---|---|
| Source-owned files | `1/`, `2/`, `3/`, `latex/`, `docs/`, scripts and configuration | Normal Git history; contributors edit and review these files |
| Tracked generated fixtures | `latex/components/*/example/main.pdf`, `latex/integration/*/main.pdf`, generated README blocks and `CHANGELOG/` | Regenerated only by their owning tools; course PDFs are not in this class |
| Build-owned files | `.build/<document>/` | Local or CI compilation output; ignored and disposable |
| Release staging | `.build/release/` | Cleaned and owned exclusively by `package_notes.py`; never committed |
| Temporary CI artifacts | Pull-request PDF bundles and failure logs | Review/diagnostic downloads retained for a limited period |
| Rolling release assets | GitHub Release tagged `notes-latest` | Latest complete successful `main` build; assets are replaced as one publication operation |
| Immutable snapshot assets | Maintainer-selected GitHub Release tags | Stable end-of-semester distributions; never overwritten |

Generated course PDFs matching `1/**/main.pdf`, `2/**/main.pdf`, and `3/**/main.pdf` are ignored. Git-aware repository validation rejects one if it is forced into the index. Source PDFs or third-party reference PDFs may still be tracked when licensing permits, so PDF files are not ignored globally and Git LFS is not used.

## Repository layers

| Layer | Location | Responsibility |
|---|---|---|
| Course archives | `1/`, `2/`, `3/` | Course-specific LaTeX sources, assets, references, and generated README contents |
| Shared typesetting | `latex/unipd-notes.cls` | Common document defaults and component loading |
| LaTeX components | `latex/components/` | Focused packages with isolated tracked examples |
| Integration examples | `latex/integration/` | End-to-end tracked verification across shared components |
| Fonts | `latex/fonts/` | Bundled typefaces, configuration, attribution, and licenses |
| Course creation, build, validation, changelogs, and packaging | `latex/tools/` | Deterministic discovery, compilation, generated state, repository checks, histories, and release assets |
| Canonical build environment | `compose.yaml` | Pinned TeX Live runtime shared by local and hosted builds |
| Documentation | `docs/md/` | User, contributor, maintainer, reference, and development guides |
| Automation | `.github/`, `.pre-commit-config.yaml` | Pull-request validation, release publication, changelogs, dependency updates, and local quality checks |

Root-level files define project policies, licenses, contribution rules, and the public entry point. `CHANGELOG/` mirrors the three degree-year directories and contains one generated Markdown history per course. Tracked `.gitkeep` placeholders preserve empty archive directories.

## Document model

Every course entry point is located at:

```text
<year>/<course-name>/main.tex
```

The build system also treats each `latex/components/<component>/example/main.tex` and `latex/integration/<example>/main.tex` as an independent document. All documents use the shared `unipd-notes` class. Course files may depend on the shared LaTeX system; shared components must not depend on a particular course.

## Build and distribution flow

For each selected document, `build.py` resolves `main.tex`, recreates a mirrored output directory under `.build/`, compiles with `latexmk` and LuaLaTeX in the pinned environment, and reads `main.toc`. Course PDFs remain only under `.build/`; their generated README link points to the stable rolling-release asset. Component and integration PDFs remain tracked compatibility fixtures and are published beside their sources when built normally.

For pull requests, changed paths are mapped to affected documents. Shared dependency changes select every document. Built PDFs under `.build/` are uploaded as a temporary review artifact, while failures upload available LaTeX logs. Pull-request code receives no write token and cannot publish a release.

For every push to `main`, `publish-notes.yml` runs all quality checks and compiles every document. `package_notes.py` then discovers all direct course sources, requires the corresponding `.build/<year>/<course>/main.pdf`, derives names from canonical year and course directory identity, rejects invalid paths and collisions, and recreates `.build/release/`. It emits a sorted manifest, Markdown index, and checksums using the source commit timestamp supplied by the workflow.

The publisher temporarily drafts the rolling release while replacing assets, removes assets no longer present, moves `notes-latest` to the successfully packaged `main` commit, and republishes it with the title **Latest compiled notes**. Drafting prevents a partial update from appearing successful. Repeated runs for the same commit replace rather than duplicate assets. The stable public URL is:

<https://github.com/simonesiega/unipd-computer-engineering/releases/tag/notes-latest>

A manual dispatch uses the same complete build and package. It requires a unique tag and title, accepts an optional description, records the source commit in generated metadata and release notes, and creates a draft before uploading. Existing snapshot tags or releases are rejected and are never overwritten.

## Change boundaries

| Change | Expected build impact |
|---|---|
| File inside one course | That course in pull requests; every document on `main` publication |
| File inside one component example | That example in pull requests |
| Shared class or component package | Every document |
| Bundled font | Every document |
| Canonical build environment or build workflow | Every document |
| Build tool | Every document |
| Release packaging tool | Tool tests and release packaging; no duplicate shell packaging implementation |
| Documentation or policy only | No LaTeX document unless it changes a shared build workflow |

New shared compilation paths must be added to the affected-document mapping. Release asset discovery and metadata generation must remain in `package_notes.py`, not be reimplemented in workflow shell.

## Licensing

Course notes and academic material are CC BY-SA 4.0. A compiled note PDF is a generated distribution of its corresponding source under that same license. Python tools, release packaging, workflows, documentation, and supporting infrastructure are MIT licensed. Third-party fonts and assets retain their own notices and licenses.

See [Docker builds](../getting-started/docker.md) for the canonical runtime, [Build system](build-system.md) for tool behavior, and [Validation, Tests, and CI](tool-test-and-ci.md) for checks, artifacts, and release operations.
