# AI-Assisted Development

[← Documentation](../README.md) · [Contributing](../../../CONTRIBUTING.md) · [Validation, Tests, and CI](tool-test-and-ci.md)

This repository may use AI-assisted tools to help write, review, build, test, and maintain course material and supporting infrastructure. AI output is never treated as authoritative by itself: every contribution remains subject to human review for accuracy, clarity, originality, citations, licensing, academic integrity, and consistency with the surrounding material.

Repository-specific instructions for compatible AI coding agents are stored in [`AGENTS.md`](../../../AGENTS.md) and [`.agents/skills/`](../../../.agents/skills/). `AGENTS.md` defines the shared rules and routes each task to the most appropriate skill, while each `SKILL.md` contains a focused workflow for one area of the project.

## Agent guidance

| File | Responsibility |
|---|---|
| [`AGENTS.md`](../../../AGENTS.md) | Defines repository-wide rules, protected generated content, academic and licensing constraints, skill routing, normal workflows, and completion reporting. |
| [`unipd-note-writing`](../../../.agents/skills/unipd-note-writing/SKILL.md) | Writes and reviews course-specific prose, mathematics, examples, exercises, solutions, references, code explanations, and diagrams stored with course sources. |
| [`unipd-latex-component-development`](../../../.agents/skills/unipd-latex-component-development/SKILL.md) | Develops the shared document class, LaTeX components, component examples, fonts, public interfaces, dependencies, and related documentation. |
| [`unipd-python-tool-development`](../../../.agents/skills/unipd-python-tool-development/SKILL.md) | Develops, fixes, reviews, and tests Python repository tools while preserving the standard-library `unittest` architecture and deterministic isolated tests. |
| [`unipd-latex-build`](../../../.agents/skills/unipd-latex-build/SKILL.md) | Selects and compiles affected documents, diagnoses LaTeX failures, and regenerates PDFs and other build-owned outputs. |
| [`unipd-pdf-review`](../../../.agents/skills/unipd-pdf-review/SKILL.md) | Visually reviews generated PDFs for layout, readability, navigation, clipping, overlap, page-break, and rendering problems. |
| [`unipd-repository-validation`](../../../.agents/skills/unipd-repository-validation/SKILL.md) | Runs and diagnoses repository validation, pre-commit checks, structural rules, source hygiene, YAML, encoding, whitespace, and line-ending failures. |

These files guide AI-assisted work but do not replace the project documentation, validation tools, contribution requirements, or maintainer review. Contributors remain responsible for every submitted change and must disclose uncertainty, skipped checks, unavailable tools, and material that still requires verification.
