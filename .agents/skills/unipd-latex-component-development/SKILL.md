---
name: unipd-latex-component-development
description: Create, modify, or review shared LaTeX infrastructure in latex/unipd-notes.cls, latex/components/, or latex/fonts/. Use for component responsibilities, public interfaces, dependencies, examples, class behavior, fonts, and related documentation. Do not use for course content, builds, PDF review, Python tools, or validation.
---

# UniPD LaTeX Component Development

## Establish context

1. Identify the class, component, or font area involved.
2. Read `latex/components/README.md`.
3. Inspect the implementation, example, related components, and class loading order.
4. Consult class or font documentation when those areas change.

Extend the existing architecture instead of creating a parallel system.

## Component boundaries

Each component must have one responsibility. Reuse the existing owner of a behavior:

- `typography`: fonts, colors, and text rules;
- `metadata`: course and document information;
- `page-style`: geometry, headers, and footers;
- `figures-tables`: floats, captions, and tables;
- `diagrams`: TikZ and CircuitikZ styles;
- `mathematics`: mathematical notation and shared operators;
- `code` and `algorithms`: listings, terminal sessions, and pseudocode;
- `references`: labels, cross-references, and bibliography;
- `glossary`: terms, acronyms, and glossary printing;
- `front-back-matter`: prefaces, revision history, pagination transitions, and document lists;
- `environments`: definitions, results, examples, warnings, exercises, and solutions.

Do not solve a course-specific problem with a repository-wide special case.

## Component structure

Every component must contain at least:

```text
latex/components/<component>/
├── <component>.sty
└── example/
    ├── main.tex
    └── main.pdf
```

A new component must use an ASCII kebab-case name, provide a matching package and isolated example, be loaded by `latex/unipd-notes.cls`, and be listed in `latex/components/README.md`.

## Interfaces and dependencies

- Keep public commands semantic, small, consistently named, and backward-compatible when practical.
- Do not expose internal helpers unnecessarily.
- Do not rename public interfaces without an explicit migration.
- Reuse existing packages, colors, fonts, counters, lengths, and helpers.
- Load dependencies before consumers; avoid cycles and course dependencies.
- Confirm new packages exist in the supported TeX environment.
- Preserve LuaLaTeX compatibility and avoid fragile internal patches.

## Examples and documentation

Every public behavior change must be demonstrated by the component example.

Examples must be isolated, focused, realistic, and cover relevant options or edge cases. Update reference documentation when public commands, environments, class options, component boundaries, or font behavior change.

## Class changes

Keep component loading centralized and dependency-ordered. Preserve existing class options unless removal is explicitly requested. Keep component-specific behavior out of the class.

## Font changes

Verify redistribution rights and preserve licenses. Document configuration and fallback behavior. When affected, cover regular, italic, bold, bold italic, mathematics, and monospace use.

## Review

Confirm responsibility, public interfaces, dependencies, examples, documentation, compatibility, and licensing. Then use `unipd-latex-build` and `unipd-pdf-review`.
