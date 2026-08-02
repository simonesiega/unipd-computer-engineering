# Metadata

[← Documentation](../README.md) · [Creating a course](../getting-started/creating-a-course.md) · [Course structure](course-structure.md) · [Writing notes](writing-notes.md)

This guide documents the course and document information configured through `\unipdsetup`. Metadata is used by the cover, running page style, and other shared components.

## Course setup

Place `\unipdsetup` in `main.tex` after `\documentclass` and before `\begin{document}`:

```latex
\documentclass{unipd-notes}

\unipdsetup{
  course = {Fondamenti di Ingegneria Informatica},
  short-course = {Fondamenti di Ingegneria},
  professor = {Prof. Mario Rossi},
  academic-year = {2026--2027},
  degree-year = {1},
  semester = {1},
  document-type = {Appunti delle lezioni},
  author = {Your Name},
  date = {\today},
  version = {0.1.0}
}
```

Use the official course title and accurate information for the specific edition of the notes.

## Course-specific fields

| Field | Purpose |
|---|---|
| `course` | Official full course name |
| `short-course` | Short title used where space is limited |
| `professor` | Instructor for the documented course edition |
| `academic-year` | Academic year in `YYYY--YYYY` form |
| `degree-year` | Degree year: `1`, `2`, or `3` |
| `semester` | Semester or teaching period |
| `document-type` | Type of material, such as `Appunti delle lezioni` |
| `author` | Author or authors of the notes |
| `date` | Document date; defaults to `\today` |
| `version` | Revision identifier, starting from `0.1.0` for new notes |

Set `author` explicitly. Its shared default is the repository maintainer and would incorrectly attribute notes created by another contributor.

`short-course`, `professor`, `semester`, and `version` may be omitted when they are unknown or not applicable. `date` defaults to `\today`; set `date = {}` explicitly to hide it. Blank optional fields are not displayed on the cover.

## Shared defaults

The metadata system already defines:

| Field | Default |
|---|---|
| `university` | Università degli Studi di Padova |
| `degree` | Corso di laurea triennale in Ingegneria informatica |
| `repository` | Computer Engineering — UniPD |
| `license` | CC BY-SA 4.0 |
| `unofficial-notice` | Materiale didattico non ufficiale, non approvato né pubblicato dall'Università degli Studi di Padova. |

These values keep every course consistent. Override them only when the document genuinely requires different information.

## Using metadata

Retrieve a value inside the document with:

```latex
\unipdmetadata{course}
```

Use `\unipdifmetadata` when content should appear only if a field is present:

```latex
\unipdifmetadata{professor}
  {Docente: \unipdmetadata{professor}}
  {Docente non specificato}
```

`\unipdheadcourse` returns `short-course` when available and otherwise falls back to `course`.

Keep metadata in `main.tex`; do not repeat it in section files. Update the academic year, professor, date, and version when publishing notes for a new course edition.

Continue with [Writing notes](writing-notes.md) for content conventions or [Building documents](../getting-started/building-documents.md) to regenerate and review the PDF.
