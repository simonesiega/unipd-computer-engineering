# AGENTS.md

## Purpose

This repository archives University of Padua Computer Engineering note sources, shared LaTeX infrastructure, Python tooling, documentation, and automation. Compiled course PDFs are distributed outside normal Git history.

## Global rules

- Inspect relevant files before editing.
- Make the smallest coherent change that satisfies the request.
- Preserve existing language, terminology, notation, structure, and architecture.
- Follow repository conventions; do not create parallel systems.
- Do not modify unrelated files or revert pre-existing user changes.
- Never edit generated outputs directly; regenerate them with the owning repository tool.
- Never claim a build, test, validation, or visual review passed unless it completed successfully.
- Report anything that could not be verified.

## Generated and protected content

Do not manually edit:

- content between `<!-- GENERATED:START -->` and `<!-- GENERATED:END -->`;
- the README catalogue between `<!-- RELEASE-CATALOG:START -->` and `<!-- RELEASE-CATALOG:END -->`;
- files under `CHANGELOG/`;
- compiled PDFs or other generated outputs.

Course PDFs under `1/**/main.pdf`, `2/**/main.pdf`, and `3/**/main.pdf` are protected build outputs: keep them under `.build/` or obtain them from CI artifacts/releases, and never stage or commit them. Tracked component and integration example PDFs remain tool-owned fixtures. `latex/tools/package_notes.py` exclusively owns `.build/release/`, including release PDFs, manifests, checksums, and release notes.

Do not change covered-exam status or counts without explicit maintainer approval.

## Academic and licensing rules

- Preserve required attribution and license notices.
- Never fabricate citations, references, quotations, or results.
- Do not add restricted, confidential, leaked, or unlawfully redistributed material.
- Do not add answers intended for active graded work.
- Treat AI-assisted academic content as unverified until reviewed.

## Skill routing

Use the most specific skill available; a task may require several.

| Skill | Use for |
|---|---|
| `unipd-note-writing` | Course content and course-specific diagrams under `1/`, `2/`, or `3/` |
| `unipd-latex-component-development` | `latex/unipd-notes.cls`, `latex/components/`, and `latex/fonts/` |
| `unipd-python-tool-development` | Development and tests under `latex/tools/` and `latex/tools/test/` |
| `unipd-latex-build` | Selecting and compiling affected documents; regenerating outputs without staging course PDFs |
| `unipd-pdf-review` | Visual inspection of local `.build/` PDFs or CI artifacts |
| `unipd-repository-validation` | `check_repository.py`, pre-commit, tracked-PDF policy, structure, and source hygiene |

For documentation, automation, or CI without a matching skill, follow the global rules and inspect the relevant documentation or configuration.

Command examples use `python3`; substitute the available Python launcher when necessary.

## Normal workflows

Course-note change:

1. `unipd-note-writing`
2. `unipd-latex-build`
3. `unipd-pdf-review`
4. `unipd-repository-validation`

Shared LaTeX change:

1. `unipd-latex-component-development`
2. `unipd-latex-build`
3. `unipd-pdf-review`
4. `unipd-repository-validation`

Python tool change:

1. `unipd-python-tool-development`
2. `unipd-repository-validation`

Documentation, policy, skill, or agent-instruction change:

1. inspect the authoritative implementation or workflow for every behavioral claim;
2. preserve generated Markdown regions and legal notices;
3. run repository validation, including local-link and heading-anchor checks;
4. skip LaTeX compilation and PDF review unless the documentation change accompanies behavior that affects rendered documents.

A task that changes course sources normally requires rebuilding and visually reviewing the affected `.build/` PDF. Workflow steps may be omitted only when irrelevant; report the reason. Explicitly report unavailable Docker, skipped builds, unavailable artifacts, and PDFs that were not visually reviewed.

## Completion

Respect explicit file-scope restrictions from the user even when the normal workflow would edit generated outputs; report any resulting verification gap instead of expanding scope without permission.

Report changed, generated, and inspected-only files; skills used; commands run; PDF-review status; failures; skipped checks; and remaining uncertainty.
