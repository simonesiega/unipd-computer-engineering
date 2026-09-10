<p align="center">
  <img src="docs/assets/unipd.png" alt="University of Padua" width="420" />
</p>

<h1 align="center">UniPD Computer Engineering</h1>

<p align="center">
  <strong>Notes, exercises, diagrams, and study material for the 2026–2029 Computer Engineering cohort at the University of Padua.</strong>
</p>

<p align="center">
  <em>Unofficial and student-maintained. Not affiliated with or endorsed by the University of Padua.</em>
</p>

<p align="center">
  <a href="#browse-the-notes">Browse notes</a> ·
  <a href="#coverage">Coverage</a> ·
  <a href="#build-locally">Build locally</a> ·
  <a href="#documentation">Documentation</a> ·
  <a href="#contributing">Contributing</a>
</p>

<p align="center">
  <a href="https://www.unipd.it/corsi-di-laurea/ingegneria-informatica">
    <img src="https://img.shields.io/badge/BSc%20Computer%20Engineering-2026%E2%80%932029-A51C30" alt="BSc in Computer Engineering: 2026–2029" />
  </a>
  <a href="https://github.com/simonesiega/unipd-computer-engineering/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/simonesiega/unipd-computer-engineering/ci.yml?branch=main&label=build%20%26%20checks" alt="Build and validation status" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/Notes-CC%20BY--SA%204.0-EF9421?logo=creativecommons&logoColor=white" alt="Notes: Creative Commons Attribution-ShareAlike 4.0 International License" />
  </a>
  <a href="LICENSE-MIT">
    <img src="https://img.shields.io/badge/Code-MIT-yellow?logo=opensourceinitiative&logoColor=white" alt="Code: MIT License" />
  </a>
</p>

<p align="center">
  <a href="https://www.unipd.it/"><strong>University of Padua</strong></a>
  &nbsp;·&nbsp;
  <a href="https://www.unipd.it/corsi-di-laurea/ingegneria-informatica"><strong>Computer Engineering degree programme</strong></a>
</p>

<details>
<summary><strong>Preview the notes</strong></summary>

<br />

<p align="center">
  <img
    src="docs/assets/notes/computer-engineering-notes-preview.png"
    alt="Preview of a Computer Engineering note"
    width="760"
  />
</p>

The preview shows the shared layout used across the archive for headings, text, diagrams, equations, references, source notes, and code listings.

</details>

## Overview

This repository is a student-maintained academic archive for the 2026–2029 three-year Bachelor's degree programme in Computer Engineering at the [University of Padua](https://www.unipd.it/).

Courses are organized by degree year and share the same LaTeX system for structure, typography, metadata, and reproducible builds. Source files live in Git; compiled PDFs are published separately through GitHub Releases.

## Browse the notes

| Degree year | Academic year | Course directory |
|---|---|---|
| First year | 2026–2027 | [`1/`](1/) |
| Second year | 2027–2028 | [`2/`](2/) |
| Third year | 2028–2029 | [`3/`](3/) |

**[Download the latest complete set of compiled notes](https://github.com/simonesiega/unipd-computer-engineering/releases/tag/notes-latest).**

The rolling `notes-latest` release tracks the latest successfully published `main` commit. Stable end-of-semester editions are published as immutable snapshot releases, while pull-request builds are available temporarily through GitHub Actions for review.

Weekly generated changelogs under [`CHANGELOG/`](CHANGELOG/) record committed course-source changes and link them to the corresponding commits.

## Coverage

An exam is considered **covered** only when its intended notes are sufficiently complete, reviewed, and approved through an immutable snapshot release. The tables below are generated from published GitHub Releases and should not be edited manually.

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
| [`notes-latest`](https://github.com/simonesiega/unipd-computer-engineering/releases/tag/notes-latest) | 2026-09-10 | Latest compiled notes | [1-analisi-matematica-1.pdf](https://github.com/simonesiega/unipd-computer-engineering/releases/download/notes-latest/1-analisi-matematica-1.pdf)<br>[1-fondamenti-di-informatica.pdf](https://github.com/simonesiega/unipd-computer-engineering/releases/download/notes-latest/1-fondamenti-di-informatica.pdf) |
<!-- RELEASE-CATALOG:END -->

## Build locally

Clone the repository and build a course with the pinned TeX Live environment used by CI:

```bash
git clone https://github.com/simonesiega/unipd-computer-engineering.git
cd unipd-computer-engineering
docker compose run --rm texlive python3 latex/tools/build.py 1/course-name
```

For daily work, use the shorter Make target:

```bash
make build COURSE=1/course-name
```

Generated PDFs stay under `.build/<year>/<course>/main.pdf` and must not be committed.

See [Installation](docs/md/getting-started/installation.md), [Docker builds](docs/md/getting-started/docker.md), and [Building documents](docs/md/getting-started/building-documents.md) for the complete setup and build workflow.

## Documentation

Start with the [documentation hub](docs/md/README.md), or jump directly to the area you need:

| Area | Guides |
|---|---|
| Getting started | [Installation](docs/md/getting-started/installation.md) · [Docker builds](docs/md/getting-started/docker.md) · [Creating a course](docs/md/getting-started/creating-a-course.md) · [Building documents](docs/md/getting-started/building-documents.md) |
| Writing notes | [Course structure](docs/md/user-guide/course-structure.md) · [Writing notes](docs/md/user-guide/writing-notes.md) · [Metadata](docs/md/user-guide/metadata.md) |
| LaTeX reference | [Document class](docs/md/reference/unipd-notes-class.md) · [Components](latex/components/README.md) · [Fonts](latex/fonts/README.md) |
| Repository development | [Architecture](docs/md/development/architecture.md) · [Build system](docs/md/development/build-system.md) · [Validation, tests, and CI](docs/md/development/tool-test-and-ci.md) · [AI-assisted development](docs/md/development/ai-assisted-development.md) |
| Project policies | [Contributing](CONTRIBUTING.md) · [Code of Conduct](CODE_OF_CONDUCT.md) · [Security](SECURITY.md) |

## Contributing

Contributions to the study material, LaTeX system, documentation, and repository tooling are welcome.

Before opening an issue or pull request, read [`CONTRIBUTING.md`](CONTRIBUTING.md) for the project workflow, quality standards, validation steps, licensing requirements, and academic-integrity rules. All participation must follow the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

AI-assisted contributions remain subject to human review. Contributors are responsible for correctness, originality, citations, licensing, and disclosing uncertainty or unverified material. See [AI-assisted development](docs/md/development/ai-assisted-development.md) for the full policy.

Security vulnerabilities involving scripts, dependencies, automation, or configuration should be reported according to [`SECURITY.md`](SECURITY.md).

## Academic disclaimer

This is an independent and unofficial repository. It is not affiliated with, maintained by, or endorsed by the University of Padua.

The material is intended to complement lectures and official course resources, not replace them. Notes may contain errors, omissions, outdated information, personal interpretations, or inaccurate AI-assisted content, so important information should always be verified against official university resources, instructors, syllabi, textbooks, and teaching material.

The University of Padua name, logo, and related marks belong to their respective owners. Their use here is solely for identification and does not imply affiliation, authorization, or endorsement.

## License

| Material | License |
|---|---|
| Study notes and academic materials under `1/`, `2/`, and `3/` | [CC BY-SA 4.0](LICENSE) |
| Compiled note PDFs distributed through GitHub Releases | Generated distributions of their corresponding [CC BY-SA 4.0](LICENSE) sources |
| Shared LaTeX system, build and validation tools, release packaging, documentation except `CODE_OF_CONDUCT.md`, CI configuration, and other supporting project files | [MIT](LICENSE-MIT) |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | Adapted from the Contributor Covenant and distributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Third-party fonts, assets, and bundled resources | Subject to their respective licenses. See [`latex/fonts/FONT-LICENSE.md`](latex/fonts/FONT-LICENSE.md) for font licensing information. |

## Contributors

<p align="center">
  <a href="https://github.com/simonesiega/unipd-computer-engineering/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=simonesiega/unipd-computer-engineering&max=24&columns=12" alt="Contributors" />
  </a>
</p>
