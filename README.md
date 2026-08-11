<p align="center">
  <img src="docs/assets/unipd.png" alt="University of Padua" width="420" />
</p>

<h1 align="center">UniPD Computer Engineering</h1>

<p align="center">
  <strong>This repository follows the 2026–2029 Computer Engineering cohort at the University of Padua.</strong>
</p>

<p align="center">
  <em>An unofficial, student-maintained project not affiliated with or endorsed by the University of Padua.</em>
</p>

<p align="center">
  <a href="https://www.unipd.it/corsi-di-laurea/ingegneria-informatica">
    <img
      src="https://img.shields.io/badge/BSc%20Computer%20Engineering-2026%E2%80%932029-A51C30"
      alt="BSc in Computer Engineering: 2026–2029"
    />
  </a>
  <a href="LICENSE">
    <img
      src="https://img.shields.io/badge/Notes-CC%20BY--SA%204.0-EF9421?logo=creativecommons&logoColor=white"
      alt="Notes: Creative Commons Attribution-ShareAlike 4.0 International License"
    />
  </a>
  <a href="LICENSE-MIT">
    <img
      src="https://img.shields.io/badge/Code-MIT-yellow?logo=opensourceinitiative&logoColor=white"
      alt="Code: MIT License"
    />
  </a>
  <a href="#exams-covered">
    <img
      src="https://img.shields.io/badge/Exams%20covered-0-2563eb"
      alt="Exams covered: 0"
    />
  </a>
</p>

<p align="center">
  <a href="https://www.unipd.it/"><strong>University of Padua</strong></a>
  &nbsp;·&nbsp;
  <a href="https://www.unipd.it/corsi-di-laurea/ingegneria-informatica"><strong>Computer Engineering degree programme</strong></a>
</p>

## Contents

- [Example preview](#example-preview)
- [Overview](#overview)
- [Browse the notes](#browse-the-notes)
- [Exams covered](#exams-covered)
- [Releases](#releases)
- [Quick start](#quick-start)
- [Documentation](#documentation)
- [AI-assisted development](#ai-assisted-development)
- [Contributing](#contributing)
- [Academic disclaimer](#academic-disclaimer)
- [License](#license)
- [Contributors](#contributors)

## Example preview

<p align="center">
  <img
    src="docs/assets/notes/computer-engineering-notes-preview.png"
    alt="Preview of an Italian Computer Engineering note about embedded rack monitoring"
    width="760"
  />
</p>

The preview shows a representative page from the archive, demonstrating the shared layout for headings, text, diagrams, equations, cross-references, source notes, and code listings.

## Overview

This repository is the academic archive for the 2026–2029 cohort of the three-year Bachelor's degree programme in Computer Engineering at the University of Padua.

It collects notes, summaries, diagrams, exercises, references, and other study material produced throughout this cohort's degree. Courses are organized by degree year and use a shared LaTeX system to keep their structure, typography, metadata, and generated distributions consistent. LaTeX sources live in the normal Git repository; compiled course PDFs are published separately.

The archive serves both as an active study workspace and as a record of the material covered for each exam.

## Browse the notes

The archive uses the following fixed degree-year and academic-year mapping:

| Degree year | Academic year | Course directory |
|---|---|---|
| First year | 2026–2027 | [`1/`](1/) |
| Second year | 2027–2028 | [`2/`](2/) |
| Third year | 2028–2029 | [`3/`](3/) |

**[Download the latest complete set of compiled notes](https://github.com/simonesiega/unipd-computer-engineering/releases/tag/notes-latest).** The rolling `notes-latest` release always represents the latest successfully published `main` commit. Its assets use stable names such as `1-calculus-1.pdf` and include a manifest, SHA-256 checksums, and a Markdown index.

The degree-year directories contain the LaTeX sources and supporting files needed to reproduce each PDF. Pull-request builds are uploaded as temporary GitHub Actions artifacts for review and retained for approximately 14 days. Stable end-of-semester editions are published as immutable snapshot releases. Weekly generated changelogs under [`CHANGELOG/`](CHANGELOG/) record committed course-source changes, grouped by date and linked to the corresponding commit.

## Exams covered

The archive is updated as new material is written, reviewed, and completed. An exam is considered **covered** only when its intended notes are sufficiently complete, have been reviewed, and have been approved by the repository maintainer. Publishing an immutable semester snapshot explicitly approves every PDF included in that snapshot; the tables below are generated from published GitHub Releases and must not be edited manually.

<!-- RELEASE-CATALOG:START -->
| Degree year | Exams covered |
|---|---:|
| First year | 0 |
| Second year | 0 |
| Third year | 0 |
| **Total** | **0** |

Current covered exams:

| Year | Exam | Course archive | Compiled notes |
|---:|---|---|---|
| — | _No exams covered yet_ | — | — |

## Releases

| Release | Date | Title | PDFs |
|---|---|---|---|
| [`notes-latest`](https://github.com/simonesiega/unipd-computer-engineering/releases/tag/notes-latest) | 2026-08-04 | Latest compiled notes | — |
<!-- RELEASE-CATALOG:END -->

## Quick start

Clone the repository, then build a course in the pinned TeX Live environment used by CI. Replace `1/course-name` with the course path you want to build.

```bash
git clone https://github.com/simonesiega/unipd-computer-engineering.git
cd unipd-computer-engineering
docker compose run --rm texlive python3 latex/tools/build.py 1/course-name
```

For daily work, the equivalent shortcut is `make build COURSE=1/course-name`; run `make help` to list the other thin wrappers.

The course PDF remains under `.build/<year>/<course>/main.pdf` for local review; generated course PDFs must not be committed. The canonical build requires Docker Compose. Native TeX installations remain useful for previews, but release and CI builds use the pinned container. See [Installation](docs/md/getting-started/installation.md) for prerequisites, [Docker builds](docs/md/getting-started/docker.md) for container setup and troubleshooting, and [Building documents](docs/md/getting-started/building-documents.md) for build options.

## Documentation

The [documentation hub](docs/md/README.md) is the main reference for using, building, and extending the archive.

| Area | Guides |
|---|---|
| Getting started | [Installation](docs/md/getting-started/installation.md) · [Docker builds](docs/md/getting-started/docker.md) · [Creating a course](docs/md/getting-started/creating-a-course.md) · [Building documents](docs/md/getting-started/building-documents.md) |
| Writing notes | [Course structure](docs/md/user-guide/course-structure.md) · [Writing notes](docs/md/user-guide/writing-notes.md) · [Metadata](docs/md/user-guide/metadata.md) |
| LaTeX reference | [Document class](docs/md/reference/unipd-notes-class.md) · [Components](latex/components/README.md) · [Fonts](latex/fonts/README.md) |
| Repository internals | [Architecture](docs/md/development/architecture.md) · [Build system](docs/md/development/build-system.md) · [Validation, Tests, and CI](docs/md/development/tool-test-and-ci.md) · [AI-assisted development](docs/md/development/ai-assisted-development.md) |
| Project policies | [Contributing](CONTRIBUTING.md) · [Report a problem](CONTRIBUTING.md#getting-help-and-reporting-problems) · [Security](SECURITY.md) |

## AI-assisted development

AI-assisted tools may support course material and repository maintenance, but their output is never authoritative and remains subject to human review. Contributors remain responsible for accuracy, originality, citations, licensing, academic integrity, and disclosing uncertainty or skipped verification.

See [AI-assisted development](docs/md/development/ai-assisted-development.md) for the repository's agent guidance, responsibilities, and review requirements.

## Contributing

Contributions to the 2026–2029 cohort's study materials, LaTeX system, documentation, and repository tooling are welcome from all students and other contributors. Before opening an issue or pull request, read [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution paths, quality standards, licensing requirements, validation steps, and academic-integrity rules.

Security vulnerabilities involving scripts, dependencies, automation, or configuration should be reported according to [`SECURITY.md`](SECURITY.md).

## Academic disclaimer

This is an independent and unofficial repository. It is not affiliated with, maintained by, or endorsed by the University of Padua.

The materials may contain errors, incomplete explanations, missing topics, personal interpretations, outdated information, or inaccurate AI-assisted content. They are intended to complement lectures and official course resources, not replace them, and are provided without guarantees of accuracy, completeness, or suitability for a particular academic purpose.

Always verify important information against official university resources, course instructors, syllabi, textbooks, and teaching materials. The University of Padua name, logo, and related marks are the property of their respective owners. The logo is displayed solely to identify the institution associated with the degree programme; its use does not imply affiliation, authorization, or endorsement.

## License

| Material | License |
|---|---|
| Study notes and academic materials under `1/`, `2/`, and `3/` | [CC BY-SA 4.0](LICENSE) |
| Compiled note PDFs distributed through GitHub Releases | Generated distributions of their corresponding [CC BY-SA 4.0](LICENSE) sources |
| Shared LaTeX system, build and validation tools, release packaging, documentation, CI configuration, and other supporting project files | [MIT](LICENSE-MIT) |

Third-party fonts, assets, and other bundled resources remain subject to their respective licenses. Font licensing information is available in [`latex/fonts/FONT-LICENSE.md`](latex/fonts/FONT-LICENSE.md).

## Contributors

<p align="center">
  <a href="https://github.com/simonesiega/unipd-computer-engineering/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=simonesiega/unipd-computer-engineering&max=24&columns=12" alt="Contributors" />
  </a>
</p>
