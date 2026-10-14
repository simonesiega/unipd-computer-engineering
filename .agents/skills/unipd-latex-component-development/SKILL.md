---
name: unipd-latex-component-development
description: Design, modify, and review reusable UniPD LaTeX class infrastructure, components, and fonts under latex/. Use for shared interfaces, localized presentation, dependencies, examples, and compatibility across all courses. Delegate compilation, PDF inspection, validation, Python tooling, and course content to their respective skills.
---

# UniPD LaTeX Component Development

## Discover the existing owner

1. Read the [component reference](../../../latex/components/COMPONENTS.md), use the [router](../../../latex/components/README.md) to locate the example, and inspect the implementation and class load sequence.
2. Inspect impacted public commands, callers, neighboring components, and documentation. Check both supported language configurations (`italian`, `english`) and course-specific uses where relevant.
3. Prefer extending the responsible existing component over adding new packages, redundant macros, global patches, or one-off course workarounds.
4. Do not change shared behavior merely to address a unique example in one subject; shared changes must be defensible across different disciplines, course structures, notation, and languages.

## Responsibility map

Use the [component API catalogue](../../../latex/components/COMPONENTS.md#component-catalogue) and [responsibility boundaries](../../../latex/components/COMPONENTS.md#responsibility-boundaries) as the ownership map. Inspect actual dependencies before extending an owner; do not maintain a parallel map in agent instructions.

## Structure and public API

Follow the exact [component structure](../../../latex/components/COMPONENTS.md#component-structure) and [registration workflow](../../../latex/components/COMPONENTS.md#adding-or-changing-a-component). The reference owns layout, naming, and catalogue requirements.

Apply the [component API requirements](../../../latex/components/COMPONENTS.md#component-requirements) and [localized dependency rules](../../../latex/components/COMPONENTS.md#responsibility-boundaries). Check callers before changing interfaces; avoid exposing internal helpers or renaming established commands without an explicit migration requirement.

- Preserve mathematically correct rendering, accessibility of symbols, code indentation, `\cref` behavior, hyperlink targets, and numbering semantics. Visual embellishments must not change academic meaning.
- Avoid assuming that all courses use dated lectures, mathematical theorem environments, Python listings, glossaries, or identical front matter.

## Fonts, licensing, and reproducibility

Check font availability in the pinned TeX environment, fallback behavior, and glyph coverage for regular, italic, bold, math, and monospace content as applicable. Review mathematics and technical code where font changes could alter distinct symbols or legibility.

Follow [font maintenance](../../../latex/fonts/FONTS.md#changing-the-font-system) and preserve [font notices](../../../latex/fonts/FONT-LICENSE.md). Do not add unverified or improperly distributable assets.

## Examples, migration, and documentation

- Demonstrate each changed public behavior in the owning `example/main.tex`, including relevant error cases, labels, mathematical content, code, captions, or long-line stress cases when applicable.
- Update related component/class documentation whenever options, interfaces, responsibilities, or expected behavior change. Do not make examples into unrelated showcases.
- If a shared change might affect cross-component behavior or localization, inspect the integration examples for both supported languages.
- Never hand-edit the tracked example `main.pdf`: it is a generated visual fixture, updated by the canonical build.

## Validation and handoff

After implementation, hand off to `unipd-latex-build` for the component and all affected documents (repository-wide for shared class/component/font changes), to `unipd-pdf-review` for actual rendered-page verification, and to `unipd-repository-validation` for structural checks. If tool behavior must change, use `unipd-python-tool-development`.

Inspect the diff for compatibility breaks, unintended global typography changes, unreviewed generated PDFs, and unrelated edits. Report tested languages, affected documents, API changes, fixture updates, limitations, and remaining risks. Do not commit, tag, or publish without authorization.
