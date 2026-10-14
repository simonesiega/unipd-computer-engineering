# Writing Notes

[← Documentation](../README.md) · [Course structure](course-structure.md) · [Metadata](metadata.md) · [LaTeX components](../../../latex/components/README.md)

Write notes that a student can follow without the original lecture beside them. These conventions cover prose, notation, examples, and attribution; see [Course structure](course-structure.md) for files and [Building documents](../getting-started/building-documents.md) for checks.

## Language and consistency

Write notes in the language in which the course is taught. Preserve the existing language when editing a course.

Use consistent terminology, notation, capitalization, and abbreviations throughout the document. Define unfamiliar terms, symbols, and abbreviations before relying on them.

Follow the course’s established notation unless there is a clear reason to improve it. Explain any deliberate change or alternative convention.

## Structure and prose

Organize topics in a logical learning order using `\chapter`, `\section`, `\subsection`, and `\subsubsection`; do not skip heading levels. Preserve the course's [source organization](course-structure.md#organizing-source-files) rather than imposing a universal lecture sequence.

Write explanatory prose rather than a transcript of the lecture. State assumptions, connect related ideas, and explain non-obvious steps.

Prefer semantic LaTeX commands and shared environments over manual formatting. Do not introduce local fonts, colors, spacing rules, or duplicate commands already provided by the document class.

## Mathematics

- Define symbols before use and state relevant domains, units, and conditions.
- Show enough intermediate steps for non-trivial derivations.
- Align multi-line calculations by meaning, not only by appearance.
- Number and label equations only when they are referenced later.
- Use LaTeX for mathematical content instead of screenshots.
- Verify calculations, examples, edge cases, and final results.

Keep notation stable across definitions, proofs, examples, and exercises. Use `\given` and `\suchthat` for ordinary relation-sized vertical bars. Inside a matching `\left` and `\right` construction, use `\givenscaled` or `\suchthatscaled` when the bar should scale with the delimiters.

## Educational environments

Use the shared environments according to their meaning:

| Environment | Use |
|---|---|
| `definition` | A precise term or concept |
| `theorem`, `proposition`, `lemma`, `corollary` | Formal mathematical results |
| `proof` | A proof of a stated result |
| `example` | A worked application or illustration |
| `remark` | Supporting context or clarification |
| `important`, `warning` | Essential information or common mistakes |
| `exercise`, `solution` | Practice tasks and their solutions |

Clearly distinguish exercises from solutions. State when a solution is informal, incomplete, or only one possible approach.

Do not use callout environments merely for decoration.

## Code, algorithms, figures, and tables

Use the shared [LaTeX components](../../../latex/components/README.md) and inspect their examples before introducing custom formatting.

Use the `unipdcode` and `unipdterminal` environments for source listings and terminal sessions. Both accept `listings` options, for example:

```latex
\begin{unipdcode}[language=Python,caption={An identity function},label={lst:identity}]
def identity(value):
    return value
\end{unipdcode}
```

The older names `code` and `terminal` remain compatibility aliases; use the prefixed names for new material.

Code and algorithms should be relevant, readable, and accompanied by enough explanation to understand their purpose. Identify the language or notation when it is not obvious.

Figures, diagrams, tables, listings, and algorithms should have useful captions when they require identification or explanation, and labels whenever they are referenced. Keep visual material legible in the compiled PDF and store course-specific files under `assets/`.

Prefer original or reproducible diagrams over screenshots. Include the source and license of third-party material.

## Labels and references

Use descriptive lowercase labels with a stable prefix:

```text
chap:memory-hierarchy
sec:cache
eq:average-access-time
fig:cache-levels
tab:latency-comparison
lst:cache-simulation
alg:replacement-policy
```

For educational blocks, use descriptive prefixes such as `def:`, `thm:`, `prop:`, `lem:`, `cor:`, or `ex:` as appropriate.

Place figure, table, and algorithm labels after their captions; place heading and theorem labels immediately after the heading or environment begins. Use `\cref{label}` in a sentence and `\Cref{label}` at its start for localized element names. Prefer these to positional descriptions such as “the figure above” or hard-coded numbers such as “Section 3.”

## Sources and attribution

Cite borrowed definitions, results, data, diagrams, quotations, and substantial factual claims. Use `references.bib` when a course needs a bibliography and enable the document class's [bibliography option](../reference/unipd-notes-class.md#bibliography).

Prefer original explanations and follow the contribution policy's [redistribution and licensing requirements](../../../CONTRIBUTING.md#licensing-and-attribution).

Use only measurements and datasets whose origin and meaning can be verified. When synthetic or hypothetical values are useful for an example, label them explicitly and never present them as observed results.

AI-assisted material must be checked by a human for accuracy, originality, consistency, citations, and licensing. Never include fabricated references. See [AI-assisted development](../development/ai-assisted-development.md) for repository-wide responsibilities and disclosure expectations.

## Review

Before contributing notes:

- read the affected section from a student’s perspective;
- verify terminology, notation, examples, and solutions;
- check citations and third-party licenses;
- check that explanations, figures, and code agree and that no unverified claim is presented as established.

Then follow [Building documents](../getting-started/building-documents.md) for compilation, PDF review, generated-state checks, and validation. [Metadata](metadata.md) owns document information.
