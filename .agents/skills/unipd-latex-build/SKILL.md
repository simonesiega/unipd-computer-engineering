---
name: unipd-latex-build
description: Select, compile, and diagnose affected UniPD LaTeX documents through the canonical latex/tools/build.py and Docker environment; verify tool-owned generated files. Use for course, component, integration, class, font, or build-environment changes. Does not replace academic, visual PDF, or repository-quality review.
---

# UniPD LaTeX Build

## Identify the correct scope

Inspect the working tree, changed paths, and document dependencies before building. Use the smallest sound selection while respecting transitive effects:

- A course-local content, figure, or `main.tex` change normally affects that course.
- A component example change affects at least that example; a shared component/class change can affect every course and integration fixture.
- Shared class, component packages, fonts, canonical Docker/Compose environment, and build-tool logic require repository-wide verification.
- Use affected-document selection based on a reliable Git comparison when appropriate; if the base is unavailable, prefer a complete build over claiming the selection was exhaustive.

Preserve each course's source layout and language; builds must not infer a common lecture numbering scheme or force a particular discipline's content.

Run from the repository root using the **pinned Docker Compose environment**, which is the reference for CI and releases:

```bash
# One course
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py <year>/<course-name>

# Component example
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py latex/components/<component>/example

# Integration example
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py latex/integration/<language>

# Affected documents since a known base
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py --changed-from origin/main --keep-going

# Complete archive and tracked generated-state verification
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py --all --keep-going --check-generated
```

`--changed-from` requires a locally available reliable revision; do not assume `origin/main` exists. Explicit targets and `--all` are alternatives. For further options, consult `docs/guides/getting-started/building-documents.md` or `build.py --help`. Use the build tool instead of ad hoc `latexmk`/LuaLaTeX commands unless debugging the tool itself.

## Diagnose compilation and generation

1. Record which documents were selected, the source revision, and the exact build command.
2. Inspect the **first meaningful error** in the failed document's log; ignore cascading messages until its cause is understood.
3. Identify the source file/line or component responsible. Distinguish an invalid source, missing dependency, stale generated state, environment failure, and a genuine tool regression.
4. Make the smallest authorized fix, or hand off to `unipd-note-writing`, `unipd-latex-component-development`, or `unipd-python-tool-development` based on ownership.
5. Rebuild the failed target, then repeat the original selection to establish that the whole affected scope succeeds.
6. Inspect warnings for new unresolved references, missing glyphs, overfull/underfull boxes, or unexpected font/language issues. Identify known nonblocking package warnings separately; do not silently dismiss new warnings.

A green build proves that the selected documents compiled. It does **not** prove that mathematical claims, executable listings, bibliography content, hyperlinks, or visual page layout are correct.

## Generated-file ownership

The tool may produce:

- courses: `.build/<year>/<course-name>/main.pdf` and generated content inside `<year>/<course-name>/README.md`;
- component examples: tracked `latex/components/<component>/example/main.pdf`;
- integration examples: tracked `latex/integration/<language>/main.pdf` and tool-owned README regions.

Do not edit generated README blocks between `<!-- GENERATED:START -->` and `<!-- GENERATED:END -->` manually. Instead correct the source/tool and regenerate. Preserve hand-authored README content outside these markers.

Course PDFs are ignored outputs. Never place or stage `main.pdf` within `1/`, `2/`, or `3/`, or override ignore rules with `git add -f`. Component and integration fixture PDFs may be tracked and should reflect the canonical build.

The publishing workflow, not the build skill, owns `.build/release/`, asset naming, manifests, checksums, releases, tags, and publication. Never publish or commit as a side effect of compiling.

## Generated-state and release readiness

For broad infrastructure changes or prepublication verification use `--all --keep-going --check-generated`. This detects stale tracked generated state but does not excuse unsound source content. If generated files need updating, regenerate using the canonical tool, inspect the diff, and repeat the check. Preserve the user's existing changes.

After successful compilation, request actual rendered-page inspection from `unipd-pdf-review` and repository hygiene/quality from `unipd-repository-validation` when required. A successful Docker run cannot be reported as completion of these other checks.

Report selected targets, exact commands, build results, changed generated files, warnings (new versus pre-existing), skipped/unavailable checks, and remaining issues. If Docker is unavailable, identify any alternative checks as **noncanonical**, not as equivalent to a passing canonical build.
