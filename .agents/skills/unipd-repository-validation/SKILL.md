---
name: unipd-repository-validation
description: Run, interpret, and repair repository-level structure and source hygiene checks, Markdown references, pre-commit hooks, and tracked/generated-file rules. Use for validation before pull requests or releases. Do not substitute these checks for academic verification, canonical LaTeX compilation, visual PDF review, or Python test authoring.
---

# UniPD Repository Validation

## Establish the exact scope

Inspect the working tree and changed files, then read `.pre-commit-config.yaml` and any relevant repository validation documentation. Use `latex/tools/check_repository.py` as the source of truth for structural invariants; do not infer new rules from the layout of a single course.

Validation checks hygiene, paths, metadata shape, links, and generated-file ownership. It does not judge whether a lecture, theorem, exercise, Python algorithm, or complete course syllabus is academically correct.

## Standard checks

From the repository root:

```bash
# Repository structure and links
python3 latex/tools/check_repository.py

# Canonical all-file local quality pipeline
pre-commit run --all-files --show-diff-on-failure

# Unstaged diff hygiene
git diff --check
```

Use `python3` or an appropriate platform launcher (for example `py` in PowerShell). If the pinned `pre-commit` command is missing, use the environment setup instructions in `docs/guides/development/tool-test-and-ci.md`; do not claim the full suite passed based on `check_repository.py` or `git diff --check` alone. `--all-files` runs hooks on Git-tracked files, not newly untracked files: check the latter separately (the repository validator scans them for Markdown links). Pre-commit can modify source files: inspect automatic edits and rerun the relevant checks.

## Structural invariants

- Year roots are `1/`, `2/`, and `3/`. Course sources reside directly in `<year>/<course-name>/`, with valid kebab-case naming and a `main.tex` and `README.md`.
- A course entry point declares one supported class language (`italian` or `english`), a complete document environment, and required `\unipdsetup` metadata. Course code and channel are optional subject to their format constraints; the date key may be intentionally empty.
- Validate metadata **structure**, consistency of degree year and academic cohort, and mandatory fields. Do not replace legitimate professor, channel, start date, course version, or intentional course-coverage decisions based solely on external expectations; escalate plausible factual conflicts for maintainer confirmation.
- Course and integration README generated content belongs between exactly one correctly ordered `<!-- GENERATED:START -->` / `<!-- GENERATED:END -->` marker pair. Check that links and GitHub-style heading anchors resolve, including headings outside fenced code.
- Course PDFs under `1/**/main.pdf`, `2/**/main.pdf`, and `3/**/main.pdf` must not be **tracked**. An ignored `.build/` PDF is valid. If an accidental course PDF is staged/tracked, correct the index without deleting the local file (`git rm --cached -- <path>`); do not force-add the file or rewrite history.
- Components use a package plus isolated tracked source/PDF example; integration examples follow their documented structure. Check requirements against the current validator rather than imposing additional files.
- Source hygiene includes UTF-8, LF endings, trailing/newline rules, tabs, merge markers, YAML validity, case conflicts, link targets, and file-size limits. Exempt binary fonts, images, and PDFs from text normalization.

## Triage and repair

1. Record the exact failing command and its first actionable diagnostic.
2. Classify the failure: path/metadata, Markdown/link, whitespace/encoding, generated state, test/lint/typecheck, or build/environment.
3. Identify the owning file and established repository rule. Fix only confirmed violations without changing unrelated documents or user-approved content.
4. When hooks apply automatic formatting or source rewrites, check `git diff` before accepting them; do not discard unrelated working-tree changes.
5. Re-run the focused hook/check when available, followed by the original complete command. A skipped or unavailable check must be reported as such, never as a pass.
6. For stale README or PDF fixtures, ask `unipd-latex-build` to regenerate; never edit tool-owned generated blocks manually.

Routing:

- Academic writing, calculations, formal proofs, programming examples → `unipd-note-writing`.
- Source compilation or stale canonical outputs → `unipd-latex-build`.
- Actual rendered-page layout and readability → `unipd-pdf-review`.
- Shared `.cls`, `.sty`, fonts, localization, public LaTeX interfaces → `unipd-latex-component-development`.
- Repository Python tooling or failing unit tests requiring code changes → `unipd-python-tool-development`.

## Release-level readiness

A full validation report should distinguish: (a) repository/pre-commit quality, (b) canonical build and generated-state verification, (c) academic/technical content review, and (d) visual inspection of the **current** PDFs. Do not state global publication readiness when another required category is incomplete; report the actual gap instead.

The publication workflow and the maintainer determine release dates, versioning, coverage semantics, snapshot tags, and release authorization. This skill must never commit, push, publish, or change release/catalog policy without an explicit request.

Report commands, scope, passed/failed/skipped checks, changed or accidentally tracked artifacts, confirmed repairs, remaining warnings, and the exact unfinished work.
