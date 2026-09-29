---
name: unipd-note-writing
description: Write, expand, correct, reorganize, or review course-note content under 1/, 2/, or 3/, including course-specific diagrams. Use for explanations, definitions, proofs, examples, exercises, solutions, code explanations, labels, and references. Do not use for builds, PDF review, shared LaTeX infrastructure, Python tools, or validation.
---

# UniPD Note Writing

## Establish context

1. Identify the course, files, requested topic, and available source material.
2. Inspect the affected lecture and nearby content.
3. Preserve the course language, terminology, notation, labels, and established facts.
4. Inspect `main.tex` when document order or inclusion changes.
5. Consult `docs/md/user-guide/writing-notes.md` when conventions are unclear or the change is substantial.

Keep the diff limited to the requested course content and the relevant writing instructions.

## Educational writing

- Write explanations, not transcripts or disconnected notes. Produce concise, continuous exposition in the style of a university textbook or serious lecture notes, not a tutorial or generated-sounding checklist. Avoid filler, repetition, obvious restatements, announcements of what follows, and over-explanation of routine formulae.
- Use formal, precise, sober, impersonal academic Italian for Italian notes. Normally avoid first-person plural exposition such as «consideriamo», «vediamo», «definiamo», «dimostriamo», and «abbiamo». Prefer direct declarative or impersonal constructions without mechanically repeating «si».
- Stay faithful to supplied source material and the actual scope covered. Useful clarification is allowed; do not introduce unrelated theory or conventions merely to make the notes appear more complete. Never invent lecture dates or content.
- Define unfamiliar terms and symbols at first use where needed. State assumptions, domains, and conditions; explain non-obvious reasoning and enough steps to make proofs intelligible.
- Distinguish intuition from proof and definition, axiom, property, theorem, remark, example, and demonstration. Preserve course terminology where specified.

## Structure and LaTeX

Organize the document chronologically by lecture and supplied date. Each lecture is a primary unit with a number and concise descriptive title. Within a lecture, use only a small number of major numbered sections for autonomous conceptual blocks; do not create a numbered subsection merely because a minor concept has a name. Present related concepts in continuous prose, semantic mathematical environments, or concise unnumbered blocks. Keep the table of contents compact and useful throughout a full course; avoid excessive heading depth and tutorial-style fragmentation.

Prefer one substantial source file per lecture under the repository's existing `sections/` convention, for example `01-lezione.tex`. Keep `main.tex` focused on metadata, front matter, the compact conventions reference, lecture inclusions, and applicable back matter. Do not create placeholder lectures with invented dates.

Use existing semantic commands and environments. Keep course-specific diagrams in the course source and reuse shared diagram styles. Do not introduce local fonts, colors, spacing rules, heading styles, or duplicate shared commands.

Use environments by meaning:

- `definition` for concepts;
- `theorem`, `proposition`, `lemma`, `corollary`, and `proof` for formal results;
- `example` and `remark` for illustration and clarification;
- `important` and `warning` for essential information and common mistakes;
- `exercise` and `solution` for practice.

Use semantic environments rather than excessive headings. Do not use callouts merely for decoration.

## Mathematics, examples, and solutions

- Define symbols before relying on them and state relevant domains and conditions.
- Keep notation stable. Verify calculations, quantifiers, edge cases, and final results.
- Align multi-line calculations by meaning. Number equations only when referenced later.
- Make examples purposeful and consistent with the material already introduced.
- Make exercises unambiguous and dependent only on introduced material; clearly distinguish exercises and solutions.
- Never present an unverified derivation as correct.

## Glossary and conventions

Keep the glossary or conventions reference intentionally small enough to remain concise after many weeks of lectures. Include only course-specific conventions, ambiguous notation, and recurring symbols that are genuinely useful to look up. Explain ordinary standard notation briefly at first use instead of cataloguing it globally. Keep entries short; do not use the glossary to summarize mathematical theory or duplicate lesson definitions and results. The glossary never replaces a concept's first formal introduction in the lesson.

## Labels, cross-references, and sources

Use stable lowercase prefixes: `chap:` for lectures; `sec:` for major sections; `def:`, `thm:`, `prop:`, `lem:`, `cor:`, and `ex:` for reusable mathematical objects; and `eq:`, `fig:`, `tab:`, `lst:`, and `alg:` for referenced items.

Label a lecture (for example `chap:lezione-01`) and important reusable definitions, results, principles, and significant examples only when later reference is plausible. Labels should identify the mathematical object, not merely its location. Do not label every paragraph or unreferenced equation.

When a later lecture uses an earlier result, normally refer to its original label using the existing `\\cref` and hyperlink facilities rather than duplicating its statement or proof. References should read naturally in the exposition. Never hard-code page numbers. Check labels for uniqueness and all references for resolution.

Cite borrowed definitions, results, data, diagrams, quotations, and substantial claims. Prefer reliable sources and never invent citations. Mark unverifiable claims for human review.

## Code and diagrams

- Use `unipdcode` and `unipdterminal` for new listings and terminal sessions; retain generic compatibility aliases only in older material outside the requested scope.
- Identify the language or notation when unclear; explain purpose, assumptions, and limitations.
- Prefer original or reproducible diagrams and shared repository styles. Store course assets under `assets/`, and document third-party sources and licenses.

## Review

Read the result as a student. Check chronological progression, compact heading hierarchy and table of contents, formal impersonal register, concision, source fidelity, mathematical correctness, examples, citations, and scope. Check that previous results are referenced rather than duplicated, the glossary remains compact, labels are unique, and references resolve. Compile in the canonical environment and visually review the resulting PDF; report checks that could not be completed.
