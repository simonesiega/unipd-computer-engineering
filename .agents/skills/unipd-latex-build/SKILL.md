---
name: unipd-latex-build
description: Select and compile affected UniPD LaTeX documents with latex/tools/build.py, diagnose compilation failures, and regenerate owned outputs. Use after course, component, class, font, or build-system changes. Do not use for content writing, PDF visual review, LaTeX design, repository validation, or CI debugging.
---

# UniPD LaTeX Build

## Establish scope

Inspect changed files and choose the smallest correct build scope. Consult the build documentation only when selection is unclear.

Run commands from the repository root using the available Python launcher.

One course:

```bash
python3 latex/tools/build.py <year>/<course-name>
```

One component example:

```bash
python3 latex/tools/build.py latex/components/<component>/example
```

Repository-wide dependency change:

```bash
python3 latex/tools/build.py --all --keep-going
```

Repository-wide changes include the class, shared component packages, bundled fonts, and build-tool behavior. Do not build everything for an isolated course edit without reason.

Use the repository build tool instead of calling `latexmk` or LuaLaTeX directly, except when diagnosing the build tool itself.

## Diagnose failures

1. Identify the first failed document.
2. Read the first meaningful LaTeX error.
3. Locate the source file and line when possible.
4. Separate source errors from dependency or environment failures.
5. Apply the smallest in-scope fix.
6. Rebuild the failed document.
7. Re-run the original build scope.

Ignore cascading errors until the first meaningful error is understood. Do not hide unresolved failures or warnings relevant to the task.

## Generated outputs

A course build may update:

- `<year>/<course-name>/main.pdf`;
- the generated section of its `README.md`.

A component build may update:

- `latex/components/<component>/example/main.pdf`.

Treat these as build outputs; never repair them manually.

## Generated-state verification

When requested or appropriate for a release-level change:

```bash
python3 latex/tools/build.py --all --keep-going --check-generated
```

## Review

Inspect the working tree after building. Confirm generated changes match affected sources, identify unexpected outputs, and preserve pre-existing changes.

Report build scope, commands, successful and failed documents, generated files, and unresolved first errors.
