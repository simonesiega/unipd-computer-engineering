# Creating a Course

[← Documentation](../README.md) · [Installation](installation.md) · [Building documents](building-documents.md) · [Course structure](../user-guide/course-structure.md)

This guide covers the minimum workflow for adding a course to the 2026–2029 cohort archive.

For course layout, metadata semantics, and note-writing conventions, use the dedicated guides instead of duplicating those rules here.

## Before you start

Check that the course is not already present under `1/`, `2/`, or `3/`.

External contributors should open an issue before adding a new course so its official name, degree year, and scope can be agreed on first.

## Create the course

Run the generator from the repository root.

Linux or macOS:

```bash
python3 latex/tools/create_course.py \
  --year 1 \
  --course "Analisi Matematica 1" \
  --short-course "Analisi 1" \
  --course-code "IN0000225" \
  --channel "B" \
  --professor "Name" \
  --semester 1 \
  --author "Ada Lovelace" \
  --date "2026-09-28" \
  --language italian
```

Windows PowerShell:

```powershell
py latex/tools/create_course.py `
  --year 1 `
  --course "Analisi Matematica 1" `
  --short-course "Analisi 1" `
  --course-code "IN0000225" `
  --channel "B" `
  --professor "Name" `
  --semester 1 `
  --author "Ada Lovelace" `
  --date "2026-09-28" `
  --language italian
```

## Required metadata

| Option | Accepted value | Purpose |
|---|---|---|
| `--year` | `1`, `2`, or `3` | Degree year |
| `--course` | Non-empty text | Official course name |
| `--short-course` | Non-empty text | Short title used in running page elements |
| `--course-code` | Two to four uppercase letters followed by seven or eight digits | Optional official University of Padua activity code |
| `--channel` | Uppercase letters or digits, optionally separated by hyphens | Optional teaching channel such as `B` or `A-K` |
| `--professor` | Non-empty text | Professor associated with this edition |
| `--semester` | `1` or `2` | Teaching semester |
| `--author` | Non-empty, non-placeholder text | Author or authors credited for the notes |
| `--date` | ISO `YYYY-MM-DD` | Course start date |
| `--language` | `italian` or `english` | Document language |

The degree year determines the academic year automatically:

| Degree year | Academic year |
|---:|---|
| 1 | `2026--2027` |
| 2 | `2027--2028` |
| 3 | `2028--2029` |

The course start date must be a real ISO calendar date. The generated source stores it as a localized fixed date instead of deriving it from `\today` or the document build time. Omit `--course-code` or `--channel` when that information is not applicable or not yet known; the corresponding optional metadata key is generated with an empty value and is hidden from the cover and README.

For the complete meaning and validation rules of each field, see [Metadata](../user-guide/metadata.md).

## Generated course

The tool converts the official course name to lowercase ASCII kebab-case.

For example:

```text
Analisi Matematica 1
└── 1/analisi-matematica-1/
```

The generated directory contains:

```text
1/analisi-matematica-1/
├── main.tex
├── README.md
├── sections/
│   └── .gitkeep
└── assets/
    └── .gitkeep
```

The generator validates metadata before writing, rejects duplicate course identities, escapes LaTeX-sensitive input, and cleans up a partially created course if generation fails.

For file responsibilities and recommended source organization, see [Course structure](../user-guide/course-structure.md).

## Build the new course

After creation, build it in the canonical Docker environment:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py 1/analisi-matematica-1
```

The generated PDF is written to:

```text
.build/1/analisi-matematica-1/main.pdf
```

Review that PDF visually before adding substantial content.

The build also refreshes the generated section of the course `README.md`, including the course code and channel when supplied. Do not edit content between:

```html
<!-- GENERATED:START -->
<!-- GENERATED:END -->
```

Do not copy or commit the generated course PDF into the course directory.

## Next steps

Continue with:

| Task | Guide |
|---|---|
| Understand the course directory layout | [Course structure](../user-guide/course-structure.md) |
| Review or edit course metadata | [Metadata](../user-guide/metadata.md) |
| Start writing content | [Writing notes](../user-guide/writing-notes.md) |
| Build and validate later changes | [Building documents](building-documents.md) |

Display the generator's built-in help with:

```bash
python3 latex/tools/create_course.py --help
```

On Windows PowerShell, use `py` instead of `python3`.
