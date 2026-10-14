# Documentation Guides

[← Documentation](../README.md) · [Project README](../../README.md) · [Contributing](../../CONTRIBUTING.md) · [Code of Conduct](../../CODE_OF_CONDUCT.md)

These guides explain how to read, contribute to, and maintain the 2026–2029 Computer Engineering archive. Use the reading paths below, then consult the tables for a short description of each document.

## Start here

| Task | Starting point |
|---|---|
| Read the notes | Use [Browse the notes](../../README.md#browse-the-notes). |
| Set up the repository | Start with [Installation](getting-started/installation.md), then use [Docker builds](getting-started/docker.md) for the canonical PDF workflow. |
| Add a course | Follow [Creating a course](getting-started/creating-a-course.md), then read [Writing notes](user-guide/writing-notes.md). |
| Contribute a change | Read [Contributing](../../CONTRIBUTING.md) and [Building documents](getting-started/building-documents.md). |
| Report a problem or propose a course | Choose the appropriate [issue form](../../CONTRIBUTING.md#issues-and-getting-help). |
| Change shared LaTeX or tooling | Begin with [Architecture](development/architecture.md) and [Validation, tests, and CI](development/tool-test-and-ci.md). |
| Publish notes | Read the [publication workflow](development/tool-test-and-ci.md#release-publication). For snapshots, prepare a description using the [release template](release/example.md). |

## Getting started

Prepare a local environment, create a course, and compile its sources.

| Guide | Description |
|---|---|
| [Installation](getting-started/installation.md) | Required tools, validation dependencies, and checks for a working local setup. |
| [Docker builds](getting-started/docker.md) | The pinned TeX environment, platform-specific setup, cleanup, and troubleshooting. |
| [Creating a course](getting-started/creating-a-course.md) | Generator options, course metadata, initial files, and the first build. |
| [Building documents](getting-started/building-documents.md) | Daily commands, build outputs, generated files, and validation before contributing. |

## Writing notes

Organize course material and keep its prose, notation, and metadata consistent.

| Guide | Description |
|---|---|
| [Course structure](user-guide/course-structure.md) | Course directories, entry points, sections, assets, and generated-file ownership. |
| [Writing notes](user-guide/writing-notes.md) | Language, headings, mathematics, code, figures, exercises, references, and review. |
| [Metadata](user-guide/metadata.md) | Course and author fields, academic-year rules, shared defaults, and metadata commands. |

## LaTeX reference

Use the shared class and its existing interfaces before adding custom typesetting.

| Guide | Description |
|---|---|
| [Document class](reference/unipd-notes-class.md) | Class options, loaded components, document lifecycle, numbering, and public commands. |

Shared component and font references are indexed by the [LaTeX router](../../latex/README.md).

## Repository development

Understand the infrastructure, run its checks, and prepare documentation or releases.

| Guide | Description |
|---|---|
| [Architecture](development/architecture.md) | Repository layers, ownership boundaries, dependencies, and course compatibility. |
| [Build system](development/build-system.md) | Document discovery, target selection, compilation, README generation, and release packaging. |
| [Validation, tests, and CI](development/tool-test-and-ci.md) | Tool tests, repository checks, CI artifacts, changelogs, release publication, and coverage rules. |
| [Documentation site](development/documentation-site.md) | Local website builds, PDF readers, public-file boundaries, rendered checks, and Pages deployment. |
| [AI-assisted development](development/ai-assisted-development.md) | Contributor responsibility, human review, disclosure, and specialized agent guidance. |
| [Release description template](release/example.md) | A starting point for a snapshot's scope, included courses, and known limitations. |

## Project policies

For policies, agent guidance, infrastructure indexes, and documentation assets, return to the [project-wide documentation router](../README.md#policies-and-agent-guidance).
