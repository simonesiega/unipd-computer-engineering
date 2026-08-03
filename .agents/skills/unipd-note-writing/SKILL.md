---
name: unipd-note-writing
description: Write, expand, correct, reorganize, or review course-note content under 1/, 2/, or 3/, including course-specific diagrams. Use for explanations, definitions, proofs, examples, exercises, solutions, code explanations, labels, and references. Do not use for builds, PDF review, shared LaTeX infrastructure, Python tools, or validation.
---

# UniPD Note Writing

## Establish context

1. Identify the course, files, and requested topic.
2. Inspect the affected section and nearby content.
3. Preserve its language, terminology, notation, labels, and style.
4. Inspect `main.tex` only when organization or inclusion changes.
5. Consult `docs/md/user-guide/writing-notes.md` when conventions are unclear or the change is substantial.

Keep the diff limited to the requested topic.

## Educational writing

- Write explanations, not lecture transcripts or disconnected notes.
- Define unfamiliar terms, symbols, and abbreviations before use.
- State assumptions, domains, units, and conditions.
- Explain non-obvious reasoning and enough intermediate steps.
- Connect related concepts and use examples that improve understanding.
- Avoid filler, repetition, unsupported claims, and unnecessary language mixing.

## Structure and LaTeX

Use heading levels in order:

```latex
\chapter
\section
\subsection
\subsubsection
```

Place material in the most appropriate existing section file. Create a new file only for a coherent new unit. Keep `main.tex` focused on configuration and inclusion.

Use existing semantic commands and environments. Keep course-specific diagrams in the course source and reuse shared diagram styles. Do not introduce local fonts, colors, spacing rules, heading styles, or duplicate shared commands.

Use environments by meaning:

- `definition` for concepts;
- `theorem`, `proposition`, `lemma`, `corollary`, and `proof` for formal results;
- `example` and `remark` for illustration and clarification;
- `important` and `warning` for essential information and common errors;
- `exercise` and `solution` for practice.

## Mathematics, examples, and solutions

- Define symbols and required conditions.
- Keep notation stable.
- Verify calculations, edge cases, and final results.
- Distinguish exact and approximate results.
- Number equations only when referenced.
- Make examples purposeful, realistic, and consistent with prior notation.
- Make exercises unambiguous and dependent only on introduced material.
- Explain solution reasoning and mark informal, partial, or approximate solutions.

Never present an unverified derivation as correct.

## Code and algorithms

- Identify the language or notation when unclear.
- Explain purpose, inputs, outputs, assumptions, and limitations.
- Verify syntax, logic, pseudocode, invariants, and complexity when relevant.
- Avoid listings that add no educational value.

## Labels and sources

Use stable lowercase prefixes: `ch:`, `sec:`, `eq:`, `fig:`, `tab:`, `lst:`, and `alg:`.

Place labels near their targets and use LaTeX cross-references instead of hard-coded numbers.

Cite borrowed definitions, results, substantial claims, data, quotations, and adapted examples. Prefer official course information, standard textbooks, peer-reviewed work, official documentation, and standards.

Mark unverifiable claims for human review; never invent source details.

## Review

Read the result as a student. Check clarity, progression, terminology, notation, mathematics, examples, solutions, citations, and scope.
