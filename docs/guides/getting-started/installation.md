# Installation

[← Documentation](../README.md) · [Docker builds](docker.md) · [Building documents](building-documents.md)

To read without a local checkout, use [Browse the notes](../../../README.md#browse-the-notes).

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

Use a virtual environment for host-side checks. This avoids changing system Python packages and works with installations that prohibit global `pip` installs.

Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r .github/requirements-ci.txt
python -m pre_commit install
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .github/requirements-ci.txt
python -m pre_commit install
```

Activate `.venv` again in each new terminal. If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` in place of `python`; activation is not required to run that interpreter.

The requirements file installs pre-commit, not the individual check tools. The first check downloads the pinned hook environments, so it needs network access and takes longer. The Git hook runs relevant checks on staged files before each commit; use `--all-files` for the full pipeline.

## Prepare the canonical TeX environment

Follow [Prepare the environment](docker.md#prepare-the-environment) to pull and inspect the pinned container. [Docker builds](docker.md) owns container configuration, platform notes, cleanup, and troubleshooting.

## Verify the setup

1. Build the component example shown in [Build a document](building-documents.md#build-a-document) to check the mount, TeX environment, and build tool.
2. Run [Local quality checks](../development/tool-test-and-ci.md#local-quality-checks) from the activated validation environment.

The guides use the `pre-commit` executable; `python -m pre_commit` is equivalent. Without activation on Windows, invoke `.\.venv\Scripts\python.exe -m pre_commit` with the same arguments.

Both checks must succeed before treating the setup as working.

## Next steps

| Task | Guide |
|---|---|
| Build or validate notes | [Building documents](building-documents.md) |
| Understand Docker-specific behavior | [Docker builds](docker.md) |
| Add a new course | [Creating a course](creating-a-course.md) |

## Optional native TeX setup

A native TeX installation can be useful for fast editor previews, but it is not the canonical environment for generated PDFs.

Use Docker for final PDF review, generated-state checks, and tracked example regeneration. Host-side pre-commit checks still run outside the TeX container.

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
