# Installation

[← Documentation](../README.md) · [Docker builds](docker.md) · [Building documents](building-documents.md)

You do not need to install the project to read the notes. Open the compiled `main.pdf` inside a course directory.

This guide covers the tools and repository setup required to build the notes locally. See [Docker builds](docker.md) for the complete canonical-container workflow and [Building documents](building-documents.md) for build selection and validation options.

## Requirements

The canonical build environment requires:

| Tool | Requirement | Purpose |
|---|---|---|
| Git | Available on `PATH` | Clone and contribute to the repository |
| Docker | Docker Engine or Docker Desktop | Run the pinned TeX Live image |
| Docker Compose | Compose v2 (`docker compose`) | Use the same container configuration as CI |
| Python | 3.10+ on the host | Run validation and other non-LaTeX repository tools |

On Windows, install Docker Desktop and use Linux containers. On Linux, install Docker Engine and the Compose plugin. Docker Desktop includes Docker Compose. Python is included in the container for builds; the host installation is used by the local validation workflow.

## Clone the repository

```bash
git clone https://github.com/simonesiega/unipd-computer-engineering.git
cd unipd-computer-engineering
```

Run build commands from the repository root.

## Canonical TeX environment

[`compose.yaml`](../../../compose.yaml) pins the TeX Live image by digest. GitHub Actions uses this same Compose service, so package and LuaLaTeX versions cannot drift between canonical local builds and CI.

Pull the image before the first build:

```bash
docker compose pull texlive
```

See [Docker builds](docker.md) for tool checks, container behavior, platform-specific instructions, generated-file verification, cleanup, and troubleshooting.

## Verify the installation

Build one component example first:

```bash
docker compose run --rm texlive python3 latex/tools/build.py latex/components/diagrams/example
```

A successful build publishes `main.pdf` inside the example directory and stores temporary files under `.build/`. Continue with [Docker builds](docker.md) for the complete container workflow, [Creating a course](creating-a-course.md), or [Building documents](building-documents.md).

## Optional native TeX installation

A native installation can be useful for quick editor previews, but it is not the canonical environment for generated PDFs. Different LuaLaTeX or package versions can produce different PDF bytes even when the pages look identical. Before committing a generated `main.pdf`, rebuild it with the Docker Compose environment above.

Native builds require Python 3.10+, LuaLaTeX, `latexmk`, and Biber when a bibliography is present. Install them through a TeX distribution:

- **Windows:** TeX Live or MiKTeX
- **macOS:** MacTeX
- **Linux:** TeX Live

When using MiKTeX, `latexmk` may also require a Perl interpreter. Minimal TeX installations may not include every required package; a complete TeX installation is the easiest native setup.

Confirm the native commands with `python3` on Linux or macOS, or `py` on Windows:

```bash
python3 --version
lualatex --version
latexmk --version
biber --version
```

If LaTeX reports a missing package, install it through the native TeX distribution or use the canonical Docker environment.
