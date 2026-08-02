<p align="center">
  <img src="docs/assets/unipd.png" alt="University of Padua" width="420" />
</p>

<h1 align="center">UniPD Computer Engineering</h1>

<p align="center">
  <strong>A structured archive of course notes and academic material for the bachelor's degree in Computer Engineering at the University of Padua.</strong>
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

- [Overview](#overview)
- [Browse the notes](#browse-the-notes)
- [Exams covered](#exams-covered)
- [Quick start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Academic disclaimer](#academic-disclaimer)
- [License](#license)
- [Contributors](#contributors)

## Overview

This repository is a long-term academic archive for students in the three-year bachelor's degree in Computer Engineering at the University of Padua.

It collects notes, summaries, diagrams, exercises, references, and other study material produced throughout the degree. Courses are organized by degree year and use a shared LaTeX system to keep their structure, typography, metadata, and compiled PDFs consistent.

The archive serves both as an active study workspace and as a record of the material covered for each exam.

## Browse the notes

Choose the directory corresponding to your degree year:

| Degree year | Course directory |
|---|---|
| First year | [`1/`](1/) |
| Second year | [`2/`](2/) |
| Third year | [`3/`](3/) |

Inside each course directory, open or download `main.pdf` to access the latest compiled notes. The LaTeX sources and supporting files are available alongside the PDF. Per-course changelogs under [`CHANGELOG/`](CHANGELOG/) record every committed file change, grouped by date and linked to the corresponding commit.

## Exams covered

The archive is updated as new material is written, reviewed, and completed. An exam is considered **covered** only when its intended notes are sufficiently complete, have been reviewed, and have been approved by the repository maintainer.

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

## Quick start

Clone the repository, then build a course by passing its directory to the build script. Replace `1/course-name` with the course path you want to build.

```bash
git clone https://github.com/simonesiega/unipd-computer-engineering.git
cd unipd-computer-engineering
python3 latex/tools/build.py 1/course-name
```

Building requires Python, `latexmk`, and LuaLaTeX. See the [installation guide](docs/md/getting-started/installation.md) for setup instructions and [building documents](docs/md/getting-started/building-documents.md) for the complete workflow.

## Documentation

The [documentation hub](docs/md/README.md) is the main reference for using, building, and extending the archive.

| Area | Guides |
|---|---|
| Getting started | [Installation](docs/md/getting-started/installation.md) · [Creating a course](docs/md/getting-started/creating-a-course.md) · [Building documents](docs/md/getting-started/building-documents.md) |
| Writing notes | [Course structure](docs/md/user-guide/course-structure.md) · [Writing notes](docs/md/user-guide/writing-notes.md) · [Metadata](docs/md/user-guide/metadata.md) |
| LaTeX reference | [Document class](docs/md/reference/unipd-notes-class.md) · [Components](latex/components/README.md) · [Fonts](latex/fonts/README.md) |
| Repository internals | [Architecture](docs/md/development/architecture.md) · [Build system](docs/md/development/build-system.md) · [Validation, Tests, and CI](docs/md/development/tool-test-and-ci.md) |
| Project policies | [Contributing](CONTRIBUTING.md) · [Report a problem](CONTRIBUTING.md#getting-help-and-reporting-problems) · [Security](SECURITY.md) |

## Contributing

Contributions to the study materials, LaTeX system, documentation, and repository tooling are welcome. Before opening an issue or pull request, read [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution paths, quality standards, licensing requirements, validation steps, and academic-integrity rules.

Security vulnerabilities involving scripts, dependencies, automation, or configuration should be reported according to [`SECURITY.md`](SECURITY.md).

## Academic disclaimer

This is an independent and unofficial repository. It is not affiliated with, maintained by, or endorsed by the University of Padua.

The materials may contain errors, incomplete explanations, missing topics, personal interpretations, outdated information, or inaccurate AI-assisted content. They are intended to complement lectures and official course resources, not replace them, and are provided without guarantees of accuracy, completeness, or suitability for a particular academic purpose.

Always verify important information against official university resources, course instructors, syllabi, textbooks, and teaching materials. The University of Padua name, logo, and related marks are the property of their respective owners. The logo is displayed solely to identify the institution associated with the degree programme; its use does not imply affiliation, authorization, or endorsement.

## License

| Material | License |
|---|---|
| Study notes and academic materials under `1/`, `2/`, and `3/`, including LaTeX sources and compiled PDFs | [CC BY-SA 4.0](LICENSE) |
| Shared LaTeX system, build and validation tools, documentation, CI configuration, and other supporting project files | [MIT](LICENSE-MIT) |

Third-party fonts, assets, and other bundled resources remain subject to their respective licenses. Font licensing information is available in [`latex/fonts/FONT-LICENSE.md`](latex/fonts/FONT-LICENSE.md).

## Contributors

<p align="center">
  <a href="https://github.com/simonesiega/unipd-computer-engineering/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=simonesiega/unipd-computer-engineering&max=24&columns=12" alt="Contributors" />
  </a>
</p>
