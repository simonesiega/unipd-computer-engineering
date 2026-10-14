---
name: unipd-note-writing
description: Draft, extend, edit, or academically review course notes and course-specific assets under 1/, 2/, or 3/. Use for exposition, proofs, exercises, calculations, technical explanations, program listings, and sources. Delegate builds, visual PDF inspection, repository validation, tooling, and shared LaTeX implementation to their respective skills.
---

# UniPD Note Writing

## Scope and evidence

1. Establish whether the request is to draft new content, revise existing material, or conduct a correctness-only review. Follow the requested scope; review is not permission to rewrite everything.
2. Read the relevant course `main.tex`, surrounding sections, existing notation, and any supplied lecture material before making changes. For a whole-course review, inspect the complete included text and relevant assets rather than isolated excerpts.
3. Consult [Writing notes](../../../docs/guides/user-guide/writing-notes.md) and the relevant course README when necessary. Treat the course's documented conventions and explicit maintainer decisions as authoritative for that course; do not infer dates, channels, versions, or completeness from external expectations.
4. Separate what supplied materials establish from independent verification or added explanation. When lectures or external sources are missing or ambiguous, report the gap rather than inventing content.
5. Preserve the course language (`italian` or `english`), intended level, terminology, structure, and existing valid labels. These skills apply to every course and must not impose conventions borrowed from a different subject.

## Academic prose and continuity

- Write connected, accurate exposition suitable for a university textbook or serious lecture notes, not a transcript, chat explanation, or bullet-point summary. Favor concise, self-contained paragraphs with natural transitions.
- For Italian courses, use sober, fluent, impersonal academic Italian. Avoid habitual first-person narration, awkward repeated passive constructions, unexplained jargon, redundant restatements, filler, and formula-by-formula commentary. For English courses, apply equivalent standards in natural academic English.
- Preserve the author's established voice. Correct meaningful grammar, spelling, punctuation, ambiguity, and terminology problems; do not rephrase sound sentences for variety or formality alone.
- Ensure concepts are introduced before use, or clearly linked to an earlier definition. Keep terminology and notation consistent from introductory sections through exercises and appendices.
- Explain non-obvious reasoning without expanding routine steps unnecessarily. Distinguish definitions, assumptions, conventions, intuition, claims, proofs, worked examples, and exercises.
- Match the actual syllabus and available materials. Do not add unrelated advanced theory, speculative coverage, invented lectures, or missing-looking sections merely to make the notes seem comprehensive.

## Verify mathematics and quantitative content

Independently check every changed or reviewed mathematical statement, calculation, proof, and worked result; never infer validity from an attractive final answer.

- State the domain, hypotheses, quantifiers, units, conventions, and applicable ranges before relying on them.
- Check equivalences versus implications; necessary versus sufficient conditions; existence and uniqueness; boundary, empty, zero, negative, infinite, and degenerate cases where relevant.
- For induction, verify the actual starting case, exact inductive hypothesis, admissibility of the next step, and closure of the argument.
- For inequalities, verify signs before multiplying/dividing, direction changes, and whether cited results apply to the elements' actual domain. Do not use a theorem proved only for a narrower set without justifying extension.
- For limits, bounds, optimization, algebra, discrete mathematics, statistics, or other course-specific mathematics, verify definitions and hypotheses according to that field; do not impose Analysis-specific notation on other subjects.
- Recalculate numeric examples and consistency of approximations, precision, rounding, indexing, and claimed outputs. Use independent computation when useful, while preserving mathematical justification.
- Never silently change a theorem's meaning to repair its proof; make the smallest sound correction and identify any substantive ambiguity that requires an instructor or maintainer decision.

## Verify algorithms, programs, and technical claims

- Distinguish formal models, pseudocode, program text, commands, and sample output. Never present invalid executable syntax as executable code; label deliberate metasyntax explicitly.
- Check algorithm inputs, outputs, preconditions, invariants, termination, complexity claims, and exceptional cases when relevant.
- For included programming languages, verify syntax and semantics using the specified language/version and applicable runtime. Execute **safe, self-contained** examples in isolated temporary locations where feasible; avoid user data, production systems, network calls, or side effects. Explicitly report examples that were not executed.
- Verify representations, conversions, numeric widths, character encodings, and implementation-specific behavior against their stated assumptions; do not generalize a language- or platform-specific result without qualification.
- Keep diagrams, tables, code, formulas, and prose mutually consistent. A source snippet can be syntactically correct yet still demonstrate the wrong behavior.

## Course structure and shared LaTeX

Apply [Course structure](../../../docs/guides/user-guide/course-structure.md) for file ownership and teaching organization, [Metadata](../../../docs/guides/user-guide/metadata.md) for document information, and [Writing notes](../../../docs/guides/user-guide/writing-notes.md) for environments, mathematics, code, figures, and labels. Consult the [component router](../../../latex/components/README.md) for actual examples rather than inventing local interfaces.

Preserve existing valid labels and the course's own organization. Keep glossaries selective and first-use explanations explicit. If the required behavior is genuinely shared, hand it off to component development instead of adding course-local typography patches.

## Sources, authorship, and minimal edits

- Cite borrowed results, nontrivial factual claims, diagrams, datasets, and quotations using the course's existing citation approach. Verify references; never fabricate citations or assume that a source's license permits redistribution.
- Respect the notes' original scope and declared omissions. Do not invent lecture content, claim official university approval, or alter course metadata, release coverage, licensing, or version policy without a request.
- Prefer the smallest justified source diff. Protect prior work and unrelated files; avoid bulk stylistic churn. When a suspected defect is unverified, leave it as a clearly identified concern rather than making a speculative correction.

## Completion and handoff

After editing, read the full affected passages in context and inspect `git diff` for regressions. Record exact locations and distinguish confirmed corrections from optional suggestions.

Hand off compilation to `unipd-latex-build`, **actual rendered-page inspection** to `unipd-pdf-review`, and hygiene checks to `unipd-repository-validation`. Their successful results must be reported separately; do not claim to have performed them merely because the notes were reviewed.

Report what was inspected, changed, independently verified, left uncertain, and not checked. Do not commit, push, tag, or publish unless explicitly authorized.
