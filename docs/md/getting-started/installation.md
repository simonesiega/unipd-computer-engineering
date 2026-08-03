# Installation

[← Documentation](../README.md) · [Creating a course](creating-a-course.md) · [Building documents](building-documents.md)

You do not need to install the project to read the notes. Open the compiled `main.pdf` inside a course directory.

This guide covers the tools and repository setup required to build the notes locally. Build commands and validation options belong to the [building guide](building-documents.md).

## Requirements

| Tool | Requirement | Purpose |
|---|---|---|
| Git | Available on `PATH` | Clone and contribute to the repository |
| Python | 3.10+ and available on `PATH` | Run build and validation scripts |
| LuaLaTeX | Available on `PATH` | Compile the notes |
| `latexmk` | Available on `PATH` | Manage LaTeX builds |
| Biber | Available on `PATH` when using a bibliography | Process bibliography data |

Install LuaLaTeX, `latexmk`, and Biber through a TeX distribution:

- **Windows:** TeX Live or MiKTeX
- **macOS:** MacTeX
- **Linux:** TeX Live

When using MiKTeX, `latexmk` may also require a Perl interpreter.

Minimal TeX installations may not include every required package. A complete TeX installation is the easiest supported setup.

Git is required to clone and contribute to the repository, but not to compile an already downloaded copy.

Confirm the required commands.

Linux or macOS:

```bash
git --version
python3 --version
lualatex --version
latexmk --version
```

Windows PowerShell:

```powershell
git --version
py --version
lualatex --version
latexmk --version
```

For courses using bibliography support, also confirm that `biber --version` succeeds.

## Clone the repository

```bash
git clone https://github.com/simonesiega/unipd-computer-engineering.git
cd unipd-computer-engineering
```

Run build commands from the repository root.

## Verify the installation

Build one component example first.

Linux or macOS:

```bash
python3 latex/tools/build.py latex/components/diagrams/example
```

Windows PowerShell:

```powershell
py latex/tools/build.py latex/components/diagrams/example
```

A successful build publishes `main.pdf` inside the example directory and stores temporary files under `.build/`.

To verify all courses, component examples, and integration examples, run:

Linux or macOS:

```bash
python3 latex/tools/build.py --all --keep-going
```

Windows PowerShell:

```powershell
py latex/tools/build.py --all --keep-going
```

If LaTeX reports a missing package, install it through your TeX distribution or switch to a complete TeX installation.

Continue with [Creating a course](creating-a-course.md) or [Building documents](building-documents.md).
