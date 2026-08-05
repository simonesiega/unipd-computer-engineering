---
name: unipd-repository-validation
description: Run and diagnose repository structure and source-hygiene validation with latex/tools/check_repository.py and pre-commit. Use for course and component layouts, UTF-8, whitespace, YAML, line endings, case conflicts, merge markers, and related failures. Do not use for LaTeX compilation, PDF review, test authoring, shared LaTeX design, or CI debugging.
---

# UniPD Repository Validation

## Establish context

Inspect changed files, `.pre-commit-config.yaml`, and the working tree. Inspect `latex/tools/check_repository.py` or the validation documentation only when behavior or rules are unclear.

## Run checks

Repository validator:

```bash
python3 latex/tools/check_repository.py
```

Full local quality check:

```bash
pre-commit run --all-files --show-diff-on-failure
```

Use the available Python launcher on the current platform.

The repository validator checks the complete repository and accepts no per-file scope. Pre-commit hooks may modify files; inspect and preserve legitimate automatic fixes.

## Validation scope

Repository-specific structure includes:

```text
<year>/<course-name>/main.tex
latex/components/<component>/
├── <component>.sty
└── example/
    ├── main.tex
    └── main.pdf
```

Valid year roots are `1/`, `2/`, and `3/`. A course requires a direct kebab-case directory, `main.tex`, and `README.md` with one ordered generated-marker pair. Its entry point must select exactly one supported language on `unipd-notes`, contain a complete document environment, and define canonical `\unipdsetup` metadata. Required values include a non-empty course and version, a non-placeholder author, semester `1` or `2`, a degree year matching the directory, a cohort-consistent academic year, and an explicit date key that may be empty.

The validator also uses the Git index to reject tracked generated course PDFs under `1/**/main.pdf`, `2/**/main.pdf`, or `3/**/main.pdf`. An ignored local PDF is valid; a tracked one must be removed with `git rm --cached -- <path>`. Do not use `git add -f` or rewrite history to bypass this policy.

Markdown validation checks that repository-relative targets exist and that fragments identify GitHub-style ATX heading anchors. Headings inside fenced code blocks do not create anchors.

Source hygiene includes:

- valid UTF-8 for `.tex`, `.sty`, `.cls`, and `.bib`;
- no tabs, trailing whitespace, or unresolved merge markers;
- final newlines and LF endings;
- valid YAML;
- no case conflicts or oversized files;
- no text normalization of binary fonts, PDFs, or images.

## Diagnose failures

1. Identify the failing command or hook.
2. Read the first meaningful error.
3. Locate the file and line when possible.
4. Classify it as structural, textual, configuration-related, or tool-related.
5. Apply the smallest in-scope correction.
6. Re-run the focused hook when possible.
7. Re-run the original validation command.

Do not treat compilation or visual defects as validation failures.

Route specialized problems:

- Python tool or test failures → `unipd-python-tool-development`;
- compilation or stale build outputs → `unipd-latex-build`;
- visual defects → `unipd-pdf-review`;
- shared class or component behavior → `unipd-latex-component-development`.

## Review

Inspect automatic changes, confirm source normalization did not alter meaning, preserve pre-existing work, and re-run affected checks.

Report commands, passed and failed checks, accidentally tracked generated PDFs, automatic modifications, fixes, unresolved failures, and required follow-up skills.
