---
name: unipd-repository-validation
description: Run, interpret, and repair repository-level structure and source hygiene checks, Markdown references, pre-commit hooks, and tracked/generated-file rules. Use for validation before pull requests or releases. Do not substitute these checks for academic verification, canonical LaTeX compilation, visual PDF review, or Python test authoring.
---

# UniPD Repository Validation

## Establish the exact scope

Inspect the working tree and changed files, then read `.pre-commit-config.yaml` and any relevant repository validation documentation. Use `latex/tools/check_repository.py` as the source of truth for structural invariants; do not infer new rules from the layout of a single course.

Validation checks hygiene, paths, metadata shape, links, and generated-file ownership. It does not judge whether a lecture, theorem, exercise, Python algorithm, or complete course syllabus is academically correct.

## Standard checks

Run the commands maintained in [Local quality checks](../../../docs/guides/development/tool-test-and-ci.md#local-quality-checks), using [Installation](../../../docs/guides/getting-started/installation.md#install-validation-dependencies) for missing dependencies. That guide owns all-file versus untracked-file coverage and automatic-fixer behavior.

Inspect fixer edits against the initial working tree, check new files separately, and report partial checks as partial—not as a complete pre-commit pass.

## Structural invariants

Use the [validator responsibility table](../../../docs/guides/development/tool-test-and-ci.md#repository-validation), [course layout](../../../docs/guides/user-guide/course-structure.md), [metadata rules](../../../docs/guides/user-guide/metadata.md), [component structure](../../../latex/components/COMPONENTS.md#component-structure), and [integration layout](../../../latex/LATEX.md#integration-examples). The current implementation remains the source of truth for diagnostics; do not invent extra layout requirements.

Validate metadata structure, not externally guessed professor/channel/date/version or coverage status. Escalate factual conflicts. Follow [protected-output policy](../../../AGENTS.md#generated-and-protected-content) and the [accidentally tracked PDF remedy](../../../docs/guides/getting-started/building-documents.md#if-a-course-pdf-was-accidentally-tracked), preserving local files and user work. Never normalize binary fixtures as text.

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
- Actual PDF layout and readability → `unipd-pdf-review`.
- Shared `.cls`, `.sty`, fonts, localization, public LaTeX interfaces → `unipd-latex-component-development`.
- Repository Python tooling or failing unit tests requiring code changes → `unipd-python-tool-development`.

## Release-level readiness

A full validation report should distinguish: (a) repository/pre-commit quality, (b) canonical build and generated-state verification, (c) academic/technical content review, and (d) visual inspection of the **current** PDFs. Do not state global publication readiness when another required category is incomplete; report the actual gap instead.

The publication workflow and the maintainer determine release dates, versioning, coverage semantics, snapshot tags, and release authorization. This skill must never commit, push, publish, or change release/catalog policy without an explicit request.

Report commands, scope, passed/failed/skipped checks, changed or accidentally tracked artifacts, confirmed repairs, remaining warnings, and the exact unfinished work.
