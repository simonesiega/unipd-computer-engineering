---
name: unipd-latex-build
description: Select and compile affected UniPD LaTeX documents with latex/tools/build.py, diagnose compilation failures, and regenerate owned outputs. Use after course, component, class, font, or build-system changes. Do not use for content writing, PDF visual review, LaTeX design, repository validation, or CI debugging.
---

# UniPD LaTeX Build

## Establish scope

Inspect changed files and choose the smallest correct build scope. Consult the build documentation only when selection is unclear.

Run commands from the repository root through the canonical Docker Compose service.

One course:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py <year>/<course-name>
```

One component example:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py latex/components/<component>/example
```

Repository-wide dependency change:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py --all --keep-going
```

Repository-wide changes include the canonical Compose environment, CI build workflow, class, shared component packages, bundled fonts, and build-tool behavior. Do not build everything for an isolated course edit without reason.

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

- `.build/<year>/<course-name>/main.pdf`;
- the generated section of `<year>/<course-name>/README.md`.

Course PDFs are ignored release outputs. Never copy them beside course sources, add them with `git add -f`, or stage them. The release packaging tool, not this skill, owns `.build/release/`, asset renaming, manifests, checksums, and release notes.

A component build may update `latex/components/<component>/example/main.pdf`. An integration build may update `latex/integration/<language>/main.pdf` and its generated README block.

Treat these as build outputs; never repair them manually. A shared class, component package, font, canonical environment, or build-tool change requires the repository-wide build because every document depends on it.

## Generated-state verification

When requested or appropriate for a release-level change:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py --all --keep-going --check-generated
```

## Review

Inspect the working tree after building. Confirm generated changes match affected sources, identify unexpected outputs, preserve pre-existing changes, and verify that no course `main.pdf` is staged or tracked.

Report build scope, commands, successful and failed documents, generated files, unavailable Docker or other skipped checks, and unresolved first errors.
