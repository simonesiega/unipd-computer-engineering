---
name: unipd-latex-build
description: Select, compile, and diagnose affected UniPD LaTeX documents through the canonical latex/tools/build.py and Docker environment; verify tool-owned generated files. Use for course, component, integration, class, font, or build-environment changes. Does not replace academic, visual PDF, or repository-quality review.
---

# UniPD LaTeX Build

## Identify the correct scope

Inspect the working tree, changed paths, and document dependencies. Apply the [target-selection contract](../../../docs/guides/development/build-system.md#target-selection) to choose the smallest sound scope, including transitive shared effects. If a reliable comparison base is unavailable, prefer a complete build over claiming the selection was exhaustive.

Preserve each course's source layout and language; builds must not infer a common lecture numbering scheme or force a particular discipline's content.

Use the canonical commands in [Building documents](../../../docs/guides/getting-started/building-documents.md), with environment setup from [Docker builds](../../../docs/guides/getting-started/docker.md). Read the selection reference before using revision-based modes; it distinguishes committed comparisons from working-tree compilation. Use the repository build tool rather than ad hoc `latexmk`/LuaLaTeX calls unless debugging that tool.

## Diagnose compilation and generation

1. Record which documents were selected, the source revision, and the exact build command.
2. Inspect the **first meaningful error** in the failed document's log; ignore cascading messages until its cause is understood.
3. Identify the source file/line or component responsible. Distinguish an invalid source, missing dependency, stale generated state, environment failure, and a genuine tool regression.
4. Make the smallest authorized fix, or hand off to `unipd-note-writing`, `unipd-latex-component-development`, or `unipd-python-tool-development` based on ownership.
5. Rebuild the failed target, then repeat the original selection to establish that the whole affected scope succeeds.
6. Inspect warnings for new unresolved references, missing glyphs, overfull/underfull boxes, or unexpected font/language issues. Identify known nonblocking package warnings separately; do not silently dismiss new warnings.

A green build proves that the selected documents compiled. It does **not** prove that mathematical claims, executable listings, bibliography content, hyperlinks, or visual page layout are correct.

## Generated-file ownership

Follow [AGENTS.md: protected content](../../../AGENTS.md#generated-and-protected-content), [output ownership](../../../docs/guides/getting-started/building-documents.md#review-the-output), and [README generation](../../../docs/guides/development/build-system.md#generated-readme-content). Correct sources or tools and regenerate; preserve manual README prose and prior user work.

Compilation does not authorize [release packaging](../../../docs/guides/development/build-system.md#release-packaging), publication, staging, or commits.

## Generated-state and release readiness

For broad infrastructure changes or prepublication verification use `--all --keep-going --check-generated`. This detects stale tracked generated state but does not excuse unsound source content. If generated files need updating, regenerate using the canonical tool, inspect the diff, and repeat the check. Preserve the user's existing changes.

After successful compilation, request actual rendered-page inspection from `unipd-pdf-review` and repository hygiene/quality from `unipd-repository-validation` when required. A successful Docker run cannot be reported as completion of these other checks.

Report selected targets, exact commands, build results, changed generated files, warnings (new versus pre-existing), skipped/unavailable checks, and remaining issues. If Docker is unavailable, identify any alternative checks as **noncanonical**, not as equivalent to a passing canonical build.
