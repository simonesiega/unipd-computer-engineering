# Creating a Course

[← Documentation](../README.md) · [Installation](installation.md) · [Building documents](building-documents.md)

This guide covers the minimum steps required to add a course to the archive. Note-writing conventions, metadata details, and build options belong to their dedicated guides.

## Before starting

Check that the course is not already present under `1/`, `2/`, or `3/`.

External contributors should open an issue before adding a new course so that its name, degree year, and scope can be agreed upon. The repository maintainer may create courses directly.

## Create the course

Run the course-creation tool from the repository root. On Linux or macOS:

```bash
python3 latex/tools/create_course.py \
  --year 1 \
  --course "Analisi Matematica 1" \
  --short-course "Analisi 1" \
  --professor "Name" \
  --semester 1 \
  --date "3 agosto 2026" \
  --language italian
```

On Windows PowerShell:

```powershell
py latex/tools/create_course.py `
  --year 1 `
  --course "Analisi Matematica 1" `
  --short-course "Analisi 1" `
  --professor "Name" `
  --semester 1 `
  --date "3 agosto 2026" `
  --language italian
```

The command requires the following seven metadata options:

| Option | Accepted value | Purpose |
|---|---|---|
| `--year` | `1`, `2`, or `3` | Degree year; also determines the generated academic year |
| `--course` | Non-empty text | Official course name; also used to derive the directory name |
| `--short-course` | Non-empty text | Short title used in running page elements |
| `--professor` | Non-empty text | Professor associated with this edition of the course |
| `--semester` | `1` or `2` | Teaching semester |
| `--date` | Non-empty text | Explicit publication date stored in `main.tex` |
| `--language` | `italian` or `english` | Language used by the document and generated files |

Display the complete CLI reference with `python3 latex/tools/create_course.py --help` on Linux or macOS, or `py latex/tools/create_course.py --help` on Windows.

The tool converts the official course name to a lowercase ASCII kebab-case directory name. For example, `Probabilità e Statistica` becomes `probabilita-e-statistica`. It rejects a course with the same generated name anywhere in the archive, validates metadata before writing files, escapes LaTeX-sensitive characters, and removes a partially created course if writing fails.

For the example above it creates:

```text
1/analisi-matematica-1/
├── main.tex
├── sections/
│   └── .gitkeep
├── assets/
│   └── .gitkeep
└── README.md
```

The empty `.gitkeep` files ensure that Git preserves `sections/` and `assets/` until course content is added.

The generated `main.tex` uses the supplied metadata and the academic year associated with this degree archive:

| Degree year | Academic year |
|---:|---|
| 1 | `2026--2027` |
| 2 | `2027--2028` |
| 3 | `2028--2029` |

After a successful run, the command prints the created repository-relative path, selected academic year, and next build command. Invalid values and duplicate directories produce an error and a non-zero exit status.

The publication date is written literally into the generated source. Update it whenever publishing a new edition; do not replace it with `\today`, because reproducible builds intentionally use a fixed TeX clock.

The selected language is written as the `italian` or `english` class option. It localizes the generated document type, initial chapter, README text, and shared LaTeX labels.

Replace the `author = {Your Name}` placeholder before publishing the notes.

Write the notes in the selected language. For larger documents, move chapters or sections into separate files and include them from `main.tex`.

See [Metadata](../user-guide/metadata.md), [Course structure](../user-guide/course-structure.md), and [Writing notes](../user-guide/writing-notes.md) before expanding the document.

## Build the course

Run the build command from the repository root.

Linux or macOS:

```bash
python3 latex/tools/build.py 1/course-name
```

Windows PowerShell:

```powershell
py latex/tools/build.py 1/course-name
```

Replace `1/course-name` with the course directory you created.

A successful build publishes `main.pdf` and creates or updates the generated section of the course `README.md`. Do not manually edit content between the generated markers.

Review the PDF visually, then continue with [Building documents](building-documents.md) for validation and generated-file checks.
