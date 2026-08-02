# Building Documents

[← Documentation](../README.md) · [Installation](installation.md) · [Creating a course](creating-a-course.md)

This guide covers local compilation, generated files, and the checks to run before contributing. Install the required tools first by following the [installation guide](installation.md).

Run every command from the repository root.

## Build documents

| Task | Linux or macOS | Windows PowerShell |
|---|---|---|
| Build one course | `python3 latex/tools/build.py 1/course-name` | `py latex/tools/build.py 1/course-name` |
| Build one component example | `python3 latex/tools/build.py latex/components/diagrams/example` | `py latex/tools/build.py latex/components/diagrams/example` |
| Build multiple targets | `python3 latex/tools/build.py 1/course-a 1/course-b` | `py latex/tools/build.py 1/course-a 1/course-b` |
| Build the complete archive | `python3 latex/tools/build.py --all --keep-going` | `py latex/tools/build.py --all --keep-going` |

Replace the example paths with the directories or `main.tex` files you want to build.

For a course, a successful build publishes `main.pdf` and refreshes the generated section of its `README.md`. Component examples publish only their `main.pdf`. Temporary files are stored under `.build/`.

Do not manually edit content between:

```html
<!-- GENERATED:START -->
<!-- GENERATED:END -->
```

## Build changed documents

Build only documents affected by changes since another Git revision:

| Platform | Command |
|---|---|
| Linux or macOS | `python3 latex/tools/build.py --changed-from origin/main --keep-going` |
| Windows PowerShell | `py latex/tools/build.py --changed-from origin/main --keep-going` |

Course-local changes build that course, component-example changes build that example, and shared LaTeX or build-system changes build the complete archive. Documentation-only changes do not compile a document.

## Validate changes

Check repository structure and source conventions:

| Platform | Command |
|---|---|
| Linux or macOS | `python3 latex/tools/check_repository.py` |
| Windows PowerShell | `py latex/tools/check_repository.py` |

The validation checks course and component structure, UTF-8 source files, tabs, trailing whitespace, and unresolved merge-conflict markers.

Verify that every committed PDF and generated course README is current:

| Platform | Command |
|---|---|
| Linux or macOS | `python3 latex/tools/build.py --all --keep-going --check-generated` |
| Windows PowerShell | `py latex/tools/build.py --all --keep-going --check-generated` |

`--check-generated` builds under `.build/` and fails when committed generated files are missing or stale without replacing them.

## Useful options

| Option | Purpose |
|---|---|
| `--keep-going` | Build every selected target and report all failures at the end |
| `--check-generated` | Verify committed PDFs and generated README sections |
| `--no-readme` | Compile without updating course README files |
| `--clean` | Remove `.build/` after a successful run |

Always review affected PDFs visually before opening a pull request.

For automated checks and affected-document selection in GitHub Actions, see [Validation and CI](../development/validation-and-ci.md).
