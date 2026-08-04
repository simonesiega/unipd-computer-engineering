<p align="center">
  <img src="../assets/unipd.png" alt="University of Padua" width="320" />
</p>

# UniPD Computer Engineering Documentation

[← Project README](../../README.md) · [Browse the notes](../../README.md#browse-the-notes) · [Contributing](../../CONTRIBUTING.md)

This documentation is organized by task. The project README introduces the archive and provides access to the notes; the guides below explain how to create, write, build, and maintain them.

## Start here

- **Reading the notes?** Browse the degree-year directories from the [project README](../../README.md#browse-the-notes).
- **Setting up the repository?** Start with [Installation](getting-started/installation.md), then use [Docker builds](getting-started/docker.md) for the canonical PDF workflow.
- **Adding a course?** Follow [Creating a course](getting-started/creating-a-course.md), then read [Writing notes](user-guide/writing-notes.md).
- **Contributing a change?** Read [`CONTRIBUTING.md`](../../CONTRIBUTING.md) and [Building documents](getting-started/building-documents.md).
- **Reporting a problem or proposing a course?** Choose the appropriate [issue form](../../CONTRIBUTING.md#getting-help-and-reporting-problems).
- **Changing shared LaTeX or tooling?** Begin with [Architecture](development/architecture.md) and [Validation, Tests, and CI](development/tool-test-and-ci.md).

## Getting started

| Guide | Use it when |
|---|---|
| [Installation](getting-started/installation.md) | Installing the required tools and verifying a local build. |
| [Docker builds](getting-started/docker.md) | Running canonical builds, verifying generated files, and troubleshooting Docker. |
| [Creating a course](getting-started/creating-a-course.md) | Adding a new course directory and its initial `main.tex`. |
| [Building documents](getting-started/building-documents.md) | Compiling notes, refreshing generated files, and validating changes. |

## Writing notes

| Guide | Covers |
|---|---|
| [Course structure](user-guide/course-structure.md) | Course directories, sections, assets, generated files, and source organization. |
| [Writing notes](user-guide/writing-notes.md) | Language, headings, mathematics, examples, exercises, citations, and visual content. |
| [Metadata](user-guide/metadata.md) | Course, author, academic-year, document, and revision information. |

## LaTeX reference

| Guide | Covers |
|---|---|
| [Document class](reference/unipd-notes-class.md) | The `unipd-notes` class, document setup, and public commands. |
| [Components](../../latex/components/README.md) | Shared packages, responsibilities, examples, and extension rules. |
| [Fonts](../../latex/fonts/README.md) | Bundled families, typographic roles, configuration, and licensing. |

## Repository development

| Guide | Covers |
|---|---|
| [Architecture](development/architecture.md) | Repository layout, document discovery, generated outputs, and component boundaries. |
| [Build system](development/build-system.md) | Build selection, compilation, publishing, and generated README behavior. |
| [Validation, Tests, and CI](development/tool-test-and-ci.md) | Python tool tests, repository checks, affected-document builds, GitHub Actions, and artifacts. |

## Project policies

| Guide | Covers |
|---|---|
| [Contributing](../../CONTRIBUTING.md) | Contribution paths, issue forms, quality standards, licensing, pull requests, and review checks. |
| [Security](../../SECURITY.md) | Private vulnerability reporting and the distinction between security and content errors. |
| [License](../../README.md#license) | Licensing for academic materials, software, documentation, fonts, and third-party assets. |

## Documentation conventions

- Commands are shown from the repository root unless stated otherwise.
- Native commands use `python3` on Linux and macOS or `py` in Windows PowerShell; Docker commands use `python3` inside the container.
- Keep internal repository links relative.
- Link to the authoritative guide instead of repeating detailed procedures.
- Do not manually edit generated course or integration README sections.
