# Creating a Course

[← Documentation](../README.md) · [Installation](installation.md) · [Building documents](building-documents.md)

This guide covers the minimum steps required to add a course to the archive. Note-writing conventions, metadata details, and build options belong to their dedicated guides.

## Before starting

Check that the course is not already present under `1/`, `2/`, or `3/`.

Open an issue before adding a new course so its name, degree year, and scope can be agreed upon.

## Create the course directory

Place the course directly inside its degree-year directory:

```text
<year>/<course-name>/
├── main.tex
├── sections/    # optional
└── assets/      # optional
```

`<year>` must be `1`, `2`, or `3`. Use lowercase kebab-case for `<course-name>`, for example:

```text
1/fondamenti-di-informatica/
```

Only `main.tex` is required initially. Use `sections/` for substantial topics and `assets/` for images, diagrams, data, and supporting files.

## Create `main.tex`

Use the shared document class and the official course information:

```latex
\documentclass{unipd-notes}

\unipdsetup{
  course = {Official Course Name},
  short-course = {Short Name},
  professor = {Prof. Name},
  academic-year = {2026--2027},
  degree-year = {1},
  semester = {1},
  document-type = {Appunti delle lezioni},
  author = {Your Name},
  date = {\today},
  version = {0.1.0}
}

\begin{document}
\makecoursecover
\makecoursetableofcontents

\chapter{Introduction}

Add the course content here.

\end{document}
```

Write the notes in the language in which the course is taught. For larger documents, move chapters or sections into separate files and include them from `main.tex`.

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
