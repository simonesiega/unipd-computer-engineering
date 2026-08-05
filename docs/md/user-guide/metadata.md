# Metadata

[← Documentation](../README.md) · [Creating a course](../getting-started/creating-a-course.md) · [Course structure](course-structure.md) · [Writing notes](writing-notes.md)

This guide documents the course and document information configured through `\unipdsetup`. Metadata is used by the cover, running page style, and other shared components.

## Course setup

Place `\unipdsetup` in `main.tex` after `\documentclass` and before `\begin{document}`:

```latex
\documentclass[italian]{unipd-notes}

\unipdsetup{
  course = {Fondamenti di Ingegneria Informatica},
  short-course = {Fondamenti di Ingegneria},
  professor = {Prof. Mario Rossi},
  academic-year = {2026--2027},
  degree-year = {1},
  semester = {1},
  document-type = {Appunti delle lezioni},
  author = {Ada Lovelace},
  date = {3 agosto 2026},
  version = {0.1.0}
}
```

Use the official course title and accurate information for the specific edition of the notes. Select `italian` or `english` as a document-class option; shared labels and language-dependent defaults follow that selection.

## Course-specific fields

| Field | Purpose |
|---|---|
| `course` | Official full course name |
| `short-course` | Short title used where space is limited |
| `professor` | Instructor for the documented course edition |
| `academic-year` | Academic year in `YYYY--YYYY` form |
| `degree-year` | Degree year: `1`, `2`, or `3` |
| `semester` | Semester `1` or `2` |
| `document-type` | Type of material, such as `Appunti delle lezioni` or `Lecture notes` |
| `author` | Author or authors of the notes |
| `date` | Explicit publication date stored in the document source |
| `version` | Revision identifier, starting from `0.1.0` for new notes |

Set `author` explicitly. Its shared default is empty to prevent accidental attribution; the cover omits the author field when it is empty. Repository validation rejects empty or placeholder authors in course documents.

Repository course validation requires `course`, `academic-year`, `degree-year`, `semester`, `author`, `date`, and `version`. The course name and version must be non-empty; the author must also be non-placeholder. The degree year must match the parent directory, and the academic year must match the repository cohort (`2026--2027`, `2027--2028`, or `2028--2029`).

`short-course`, `professor`, and `document-type` may be omitted when they are unknown or not applicable. Set `date` explicitly to the publication date, or use `date = {}` explicitly to hide it. `create_course.py` accepts a valid ISO input such as `2026-09-28` and writes the localized form into `main.tex`; manually maintained metadata uses the displayed localized text. The field has no automatic date because reproducible builds fix TeX's clock and would make `\today` misleading. Blank optional fields are not displayed on the cover.

## Shared defaults

The metadata system defines language-dependent institutional defaults:

| Field | Italian | English |
|---|---|---|
| `university` | Università degli Studi di Padova | University of Padua |
| `degree` | Corso di laurea triennale in Ingegneria informatica | Bachelor's Degree in Computer Engineering |
| `repository` | Computer Engineering — UniPD | Computer Engineering — UniPD |
| `license` | CC BY-SA 4.0 | CC BY-SA 4.0 |
| `unofficial-notice` | Materiale didattico non ufficiale, non approvato né pubblicato dall'Università degli Studi di Padova. | Unofficial teaching material, not approved or published by the University of Padua. |

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
