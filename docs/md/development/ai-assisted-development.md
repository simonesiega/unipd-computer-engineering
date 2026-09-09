# AI-Assisted Development

[← Documentation](../README.md) · [Contributing](../../../CONTRIBUTING.md) · [Validation, tests, and CI](tool-test-and-ci.md)

AI-assisted tools may help write, review, build, test, and maintain course material and repository infrastructure.

Their output is never authoritative by itself. Every contribution remains subject to human review for accuracy, clarity, originality, citations, licensing, academic integrity, and consistency with the surrounding material.

## Repository guidance

Repository-specific instructions for compatible coding agents live in [`AGENTS.md`](../../../AGENTS.md) and [`.agents/skills/`](../../../.agents/skills/).

`AGENTS.md` defines repository-wide rules, protected generated content, academic and licensing constraints, task routing, normal workflows, and completion reporting. Each `SKILL.md` provides a focused workflow for one area of the project.

| Skill | Responsibility |
|---|---|
| [`unipd-note-writing`](../../../.agents/skills/unipd-note-writing/SKILL.md) | Write and review course prose, mathematics, examples, exercises, solutions, references, code explanations, and diagrams. |
| [`unipd-latex-component-development`](../../../.agents/skills/unipd-latex-component-development/SKILL.md) | Develop the shared document class, exact component structure, responsibility boundaries, examples, fonts, public interfaces, dependencies, and related documentation. |
| [`unipd-python-tool-development`](../../../.agents/skills/unipd-python-tool-development/SKILL.md) | Develop, fix, review, and test Python repository tooling while preserving deterministic isolated tests and the standard-library `unittest` architecture. |
| [`unipd-latex-build`](../../../.agents/skills/unipd-latex-build/SKILL.md) | Select and compile affected documents, diagnose LaTeX failures, and regenerate build-owned outputs. |
| [`unipd-pdf-review`](../../../.agents/skills/unipd-pdf-review/SKILL.md) | Review generated PDFs for layout, readability, navigation, clipping, overlap, page breaks, and rendering problems. |
| [`unipd-repository-validation`](../../../.agents/skills/unipd-repository-validation/SKILL.md) | Run and diagnose repository validation, pre-commit checks, structural rules, source hygiene, YAML, encoding, whitespace, and line-ending failures. |

## Contributor responsibility

AI guidance does not replace the project documentation, validation tools, contribution requirements, or maintainer review.

Contributors remain responsible for every submitted change and must disclose:

- uncertainty or material that still requires verification;
- validation or review steps that were skipped;
- tools or environments that were unavailable;
- AI-assisted material that could not be independently confirmed.

Do not submit generated content, references, or technical claims that have not been reviewed and verified.
