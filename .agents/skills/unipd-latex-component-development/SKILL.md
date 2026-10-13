---
name: unipd-latex-component-development
description: Design, modify, and review reusable UniPD LaTeX class infrastructure, components, and fonts under latex/. Use for shared interfaces, localized presentation, dependencies, examples, and compatibility across all courses. Delegate compilation, PDF inspection, validation, Python tooling, and course content to their respective skills.
---

# UniPD LaTeX Component Development

## Discover the existing owner

1. Read `latex/components/README.md` and the relevant implementation, component example, and load sequence in `latex/unipd-notes.cls`.
2. Inspect impacted public commands, callers, neighboring components, and documentation. Check both supported language configurations (`italian`, `english`) and course-specific uses where relevant.
3. Prefer extending the responsible existing component over adding new packages, redundant macros, global patches, or one-off course workarounds.
4. Do not change shared behavior merely to address a unique example in one subject; shared changes must be defensible across different disciplines, course structures, notation, and languages.

## Responsibility map

- `typography`: fonts, colors, hierarchy, text spacing and paragraph rules.
- `metadata`: course/document information, localized defaults and translation interfaces.
- `cover`: cover presentation using shared metadata.
- `page-style`: geometry, headers, footers and numbering presentation.
- `document-structure`: chapters, sections, appendices and document hierarchy.
- `table-of-contents`: contents structure and front-matter presentation.
- `lists`: enumerations, descriptions, nested and procedural lists.
- `figures-tables`: figures, floats, captions, source notes and tables.
- `diagrams`: common TikZ/CircuitikZ styles and helpers.
- `mathematics`: shared operators, symbols and mathematical typography.
- `code`: source code, terminal blocks, syntax formatting and listings.
- `algorithms`: pseudocode, inputs/outputs, numbering and algorithm captions.
- `references`: labels, cross-reference formats and bibliography support.
- `navigation`: links, URLs, PDF bookmarks and navigation.
- `glossary`: terminology and glossary interfaces.
- `front-back-matter`: prefaces, revision material, document lists and pagination transitions.
- `environments`: definitions, results, proofs, examples, exercises, solutions and callouts.

Respect ownership boundaries and explicit dependency ordering. No shared component should silently depend on course files.

## Structure and public API

The canonical component layout is:

```text
latex/components/<component>/
├── <component>.sty
└── example/
    ├── main.tex
    └── main.pdf
```

Follow this layout exactly; the repository validator expects an isolated example and no unrelated files beneath a component directory. New component names are ASCII kebab-case. Register a new package in the class's dependency-ordered loading and in the component catalogue.

- Keep commands and environments semantic, focused, documented, and backward-compatible whenever reasonable. Avoid exposing internal helpers or renaming established interfaces without a migration requirement.
- Reuse shared fonts, colors, lengths, counters, translations, theorem styles, and LaTeX packages. Avoid duplicate package loading and circular dependencies.
- Preserve LuaLaTeX compatibility and the supported class options. Prefer documented public interfaces over fragile redefinitions of upstream internals.
- Make language-dependent strings configurable/localized; do not hard-code Italian or English display text in shared presentation logic.
- Preserve mathematically correct rendering, accessibility of symbols, code indentation, `\cref` behavior, hyperlink targets, and numbering semantics. Visual embellishments must not change academic meaning.
- Avoid assuming that all courses use dated lectures, mathematical theorem environments, Python listings, glossaries, or identical front matter.

## Fonts, licensing, and reproducibility

Check font availability in the pinned TeX environment, fallback behavior, and glyph coverage for regular, italic, bold, math, and monospace content as applicable. Review mathematics and technical code where font changes could alter distinct symbols or legibility.

Preserve font and third-party asset licenses and attribution; consult `latex/fonts/FONT-LICENSE.md`. Do not add unverified or improperly distributable assets.

## Examples, migration, and documentation

- Demonstrate each changed public behavior in the owning `example/main.tex`, including relevant error cases, labels, mathematical content, code, captions, or long-line stress cases when applicable.
- Update related component/class documentation whenever options, interfaces, responsibilities, or expected behavior change. Do not make examples into unrelated showcases.
- If a shared change might affect cross-component behavior or localization, inspect the integration examples for both supported languages.
- Never hand-edit the tracked example `main.pdf`: it is a generated visual fixture, updated by the canonical build.

## Validation and handoff

After implementation, hand off to `unipd-latex-build` for the component and all affected documents (repository-wide for shared class/component/font changes), to `unipd-pdf-review` for actual rendered-page verification, and to `unipd-repository-validation` for structural checks. If tool behavior must change, use `unipd-python-tool-development`.

Inspect the diff for compatibility breaks, unintended global typography changes, unreviewed generated PDFs, and unrelated edits. Report tested languages, affected documents, API changes, fixture updates, limitations, and remaining risks. Do not commit, tag, or publish without authorization.
