# Installation

[← Documentation](../README.md) · [Docker builds](docker.md) · [Building documents](building-documents.md)

You do not need to install the repository to read the notes. Download compiled PDFs from the rolling [`notes-latest`](https://github.com/simonesiega/unipd-computer-engineering/releases/tag/notes-latest) release or from an immutable semester snapshot.

This guide covers the minimum setup required to build and contribute locally.

## Requirements

| Tool | Requirement | Purpose |
|---|---|---|
| Git | Available on `PATH` | Clone and contribute to the repository |
| Docker | Docker Engine or Docker Desktop | Run the canonical TeX environment |
| Docker Compose | Compose v2 (`docker compose`) | Use the same container configuration as CI |
| Python | 3.10+ on the host | Run validation and repository tooling |

Platform notes:

- **Windows:** use Docker Desktop with Linux containers;
- **macOS:** use Docker Desktop;
- **Linux:** use Docker Engine with the Compose v2 plugin.

Docker already provides Python inside the TeX container for document builds. The host Python installation is used for local validation and repository tools.

## Clone the repository

```bash
git clone https://github.com/simonesiega/unipd-computer-engineering.git
cd unipd-computer-engineering
```

Run repository commands from this directory.

## Install validation dependencies

Install the pinned development dependency set before running repository checks.

Linux or macOS:

```bash
python3 -m pip install -r .github/requirements-ci.txt
pre-commit install
```

Windows PowerShell:

```powershell
py -m pip install -r .github/requirements-ci.txt
pre-commit install
```

If the `pre-commit` executable is not available on `PATH` after installation, use `py -m pre_commit install` on Windows or `python3 -m pre_commit install` on Linux and macOS.

The installation command currently provides pre-commit itself. The first complete check creates the pinned hook environments used for Coverage.py, Ruff, mypy, Actionlint, and the repository validators. `pre-commit install` also enables these checks automatically for future local commits.

## Prepare the canonical TeX environment

The root [`compose.yaml`](../../../compose.yaml) pins the TeX Live image used by both local canonical builds and GitHub Actions.

Pull it before the first build:

```bash
docker compose pull texlive
```

For container details, platform-specific notes, cleanup, and troubleshooting, see [Docker builds](docker.md).

## Verify the setup

Build one component example:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py latex/components/diagrams/example
```

A successful build confirms that Docker, the mounted repository, the TeX environment, and the build tool are working correctly.

Run the complete repository checks:

```bash
pre-commit run --all-files --show-diff-on-failure
```

If GNU Make is available, the equivalent shortcut is:

```bash
make check
```

A fresh installation is ready for repository work when both the test-document build and complete pre-commit run succeed.

## Setup sequence

```text
Clone the repository
        ↓
Install validation dependencies and the Git hook
        ↓
Pull the pinned TeX Live image
        ↓
Build a test document
        ↓
Run make check or pre-commit
        ↓
Ready
```

Continue with:

| Task | Guide |
|---|---|
| Build or validate notes | [Building documents](building-documents.md) |
| Understand Docker-specific behavior | [Docker builds](docker.md) |
| Add a new course | [Creating a course](creating-a-course.md) |

## Optional native TeX setup

A native TeX installation can be useful for fast editor previews, but it is not the canonical environment for generated PDFs.

Use Docker for final review, CI-equivalent checks, tracked example regeneration, and release-equivalent builds.

If you still want native TeX, install:

- Python 3.10+;
- LuaLaTeX;
- `latexmk`;
- Biber when bibliography support is needed.

Typical distributions are:

| Platform | Distribution |
|---|---|
| Windows | TeX Live or MiKTeX |
| macOS | MacTeX |
| Linux | TeX Live |

Minimal installations may not contain every required package. When native output differs or a package is unavailable, use the canonical Docker environment instead.
