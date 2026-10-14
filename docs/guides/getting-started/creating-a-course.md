# Creating a Course

[← Documentation](../README.md) · [Installation](installation.md) · [Building documents](building-documents.md) · [Course structure](../user-guide/course-structure.md)

Use `create_course.py` to scaffold a course in the 2026–2029 cohort archive. It creates the entry point, README, and empty content directories; it does not supply course material.

## Before you start

Check that the course is not already present under `1/`, `2/`, or `3/`.

Use the [contribution workflow](../../../CONTRIBUTING.md#quick-workflow) to agree the official name, degree year, and scope before creating it.

## Create the course

Run the generator from the repository root. The values below are illustrative: replace the course title, instructor, author, semester, and start date with the agreed course information before running the command. Existing courses, including Analisi Matematica 1, cannot be created again.

Linux or macOS:

```bash
python3 latex/tools/create_course.py \
  --year 1 \
  --course "Corso di Esempio" \
  --short-course "Esempio" \
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
  --course "Corso di Esempio" `
  --short-course "Esempio" `
  --professor "Name" `
  --semester 1 `
  --author "Ada Lovelace" `
  --date "2026-09-28" `
  --language italian
```

## Generator options

| Option | Accepted value | Purpose |
|---|---|---|
| `--year` | `1`, `2`, or `3` | Degree year |
| `--course` | Non-empty text | Official course name |
| `--short-course` | Non-empty text | Short title used in running page elements |
| `--course-code` | Optional identifier; see [field rules](../user-guide/metadata.md#course-specific-fields) | Official University of Padua activity code |
| `--channel` | Optional identifier; see [field rules](../user-guide/metadata.md#course-specific-fields) | Teaching channel |
| `--professor` | Non-empty text | Professor associated with this edition |
| `--semester` | `1` or `2` | Teaching semester |
| `--author` | Non-empty, non-placeholder text | Author or authors credited for the notes |
| `--date` | ISO `YYYY-MM-DD` | Course start date |
| `--language` | `italian` or `english` | Document language |

The generator derives the academic year from `--year`, converts the ISO `--date` to fixed localized text, and leaves omitted optional identifiers empty. [Metadata](../user-guide/metadata.md#course-specific-fields) owns the cohort mapping, field meanings, and display rules.

## Generated course

The tool converts the official name to lowercase ASCII kebab-case: `Corso di Esempio` becomes `1/corso-di-esempio/`. [Standard course layout](../user-guide/course-structure.md#standard-layout) owns the resulting file tree and distinguishes generated scaffold files from optional additions.

The generator validates metadata before writing, rejects a course slug already present in any degree year, escapes LaTeX-sensitive input, and cleans up a partially created course if generation fails.

No course registry, class change, or CI configuration change is needed. The tools discover the new entry point from its path and metadata; see the [course compatibility contract](../development/architecture.md#course-compatibility-contract).

For file responsibilities and recommended source organization, see [Course structure](../user-guide/course-structure.md).

## Build the new course

Use the path printed by the generator with [Build a document](building-documents.md#build-a-document), then follow that guide's output-review and validation steps. Review the initial cover against the agreed course information before adding content.

Scaffolding is not publication approval; see the maintainer's [snapshot requirements](../development/tool-test-and-ci.md#immutable-snapshots).

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
