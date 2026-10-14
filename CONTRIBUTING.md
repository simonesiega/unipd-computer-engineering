# Contributing

[← Project README](README.md) · [Code of Conduct](CODE_OF_CONDUCT.md) · [Security policy](SECURITY.md)

Corrections, new notes, and improvements to the LaTeX system, tools, and documentation are welcome. Keep each change focused and contribute only material you may legally share.

## Quick workflow

| Step | Action |
|---:|---|
| 1 | Check existing courses, guides, issues, and pull requests. |
| 2 | Fork the repository and create a focused branch from `main`. |
| 3 | Make one coherent change. |
| 4 | Build and review the affected documents, then run the relevant checks. |
| 5 | Open a Pull Request describing what changed and how you validated it. |

Small corrections and documentation improvements can go directly to a pull request.

Open an issue first for substantial work such as adding a course, reorganizing a large part of an existing course, changing the shared LaTeX system, or modifying repository-wide build and CI behavior.

## What can I contribute?

| Contribution | Main guide |
|---|---|
| Correct or expand notes | [Writing notes](docs/guides/user-guide/writing-notes.md) |
| Add a course from this cohort | [Creating a course](docs/guides/getting-started/creating-a-course.md) |
| Reorganize a course | [Course structure](docs/guides/user-guide/course-structure.md) |
| Update metadata | [Metadata](docs/guides/user-guide/metadata.md) |
| Build and validate documents | [Building documents](docs/guides/getting-started/building-documents.md) |
| Modify the document class | [Document class](docs/guides/reference/unipd-notes-class.md) |
| Modify shared components | [LaTeX components](latex/components/COMPONENTS.md#adding-or-changing-a-component) |
| Modify bundled fonts | [LaTeX fonts](latex/fonts/FONTS.md#changing-the-font-system) |
| Change repository infrastructure | [Architecture](docs/guides/development/architecture.md) · [Build system](docs/guides/development/build-system.md) · [Validation, tests, and CI](docs/guides/development/tool-test-and-ci.md) |
| Update guides or the website | [Documentation site](docs/guides/development/documentation-site.md) |

Before editing an existing course, review its current notation, terminology, structure, open issues, and Pull Requests. Preserve established conventions unless changing them is the purpose of the contribution.

## Quality standards

Follow [Writing notes](docs/guides/user-guide/writing-notes.md) for academic prose, language, notation, examples, attribution, and content review. Shared infrastructure follows its [component](latex/components/COMPONENTS.md) and [font](latex/fonts/FONTS.md) references; tooling follows the [tool index](latex/tools/TOOLS.md) and [test catalogue](latex/tools/test/TESTS.md).

## Licensing and attribution

The [project licensing table](README.md#license) identifies the license for each material type; [FONT-LICENSE.md](latex/fonts/FONT-LICENSE.md) owns the bundled font notices.

By submitting a contribution, you confirm that you created the material or have the right to contribute it, that it may be distributed under the applicable repository license, and that required attribution and license notices have been preserved.

Do not upload material that cannot legally be redistributed, including textbook scans, paid or access-restricted resources, proprietary solution manuals, instructor material without permission, or copyrighted images, diagrams, code, and datasets without a compatible license.

Prefer original explanations and diagrams. When redistribution rights are unclear, link to the external source instead of copying it.

## AI-assisted contributions

Follow [AI-assisted development](docs/guides/development/ai-assisted-development.md) for human review, contributor responsibility, disclosure, and agent guidance.

## Repository conventions

Course structure, metadata, generated files, and source conventions are documented in [Course structure](docs/guides/user-guide/course-structure.md), [Metadata](docs/guides/user-guide/metadata.md), and [Building documents](docs/guides/getting-started/building-documents.md).

Use [generated-output ownership and review](docs/guides/getting-started/building-documents.md#review-the-output) before including tool-owned changes. The [release catalogue](docs/guides/development/tool-test-and-ci.md#release-catalogue) and [changelogs](docs/guides/development/tool-test-and-ci.md#course-changelogs) have separate owners. Shared changes must respect the [dependency boundaries](docs/guides/development/architecture.md#dependency-boundaries).

## Exam coverage

The [coverage definition](README.md#coverage) and maintainer-only [snapshot publication process](docs/guides/development/tool-test-and-ci.md#immutable-snapshots) govern covered-exam status. A contribution is not approval to change that status.

## Issues and getting help

Search the [existing issues](https://github.com/simonesiega/unipd-computer-engineering/issues) before opening a new one.

| Request | Form |
|---|---|
| Inaccurate, unclear, incomplete, or outdated notes | [Report a content error](https://github.com/simonesiega/unipd-computer-engineering/issues/new?template=content-error.yml) |
| A course missing from this cohort archive | [Submit a course proposal](https://github.com/simonesiega/unipd-computer-engineering/issues/new?template=course-proposal.yml) |
| A reproducible build, validation, generated-file, or CI failure | [Report a build problem](https://github.com/simonesiega/unipd-computer-engineering/issues/new?template=build-problem.yml) |
| Anything else | [Ask a general question](https://github.com/simonesiega/unipd-computer-engineering/issues/new?template=general-question.yml) |

You can also [open the issue chooser](https://github.com/simonesiega/unipd-computer-engineering/issues/new/choose) to compare all available forms.

For content reports, include the precise course and location. For build reports, include reproduction steps, environment details, and sanitized logs.

For security vulnerabilities, use the private process in [SECURITY.md](SECURITY.md#reporting-a-vulnerability), not these public forms.

## Validation

Use the workflow that matches the change:

| Change | Required instructions |
|---|---|
| Notes or rendered LaTeX behavior | [Build, review, and verify generated state](docs/guides/getting-started/building-documents.md) |
| Any contribution | [Local quality checks](docs/guides/development/tool-test-and-ci.md#local-quality-checks) |
| Python tools | [Test commands and coverage](latex/tools/test/TESTS.md#running-tests) |
| Documentation or website | [Strict site build and browser review](docs/guides/development/documentation-site.md#build-and-review-locally) |

The [CI guide](docs/guides/development/tool-test-and-ci.md#pull-requests-and-main) explains automated build selection and review artifacts.

## Branches and Pull Requests

Keep each Pull Request focused on one course or one coherent repository change.

Short branch names are enough:

| Change | Example |
|---|---|
| Notes | `notes/analysis-1-limits` |
| Fix | `fix/programming-pointer-example` |
| Documentation | `docs/course-contribution-guide` |
| LaTeX | `latex/improve-theorem-spacing` |

Use clear Pull Request titles, for example:

```text
notes(analysis-1): add limits and continuity chapter
fix(programming): correct pointer ownership example
docs: clarify how students can add course notes
latex(diagrams): improve automata edge labels
```

GitHub automatically loads [the Pull Request template](.github/PULL_REQUEST_TEMPLATE.md). Complete every applicable section and explain why any checklist item or validation step was skipped.

The Pull Request description should explain what changed, identify the affected course or repository area, cite relevant sources when needed, and state how the change was validated.

Include generated README changes and affected tracked example outputs when required, but never include generated course PDFs.

Draft Pull Requests are welcome for substantial work that would benefit from early feedback.

## Academic integrity

This archive exists to support learning and must not enable academic misconduct.

Do not contribute:

- confidential, leaked, or unlawfully obtained examination material;
- answers intended for an active graded assignment, test, or examination;
- another student's work without permission and attribution;
- material whose publication violates a university, course, or instructor rule;
- personal or sensitive information about students, instructors, or staff.

Past exercises and exam-style problems may be included only when they can be shared lawfully and their source is stated clearly.

Contributors are responsible for following applicable university rules and course-specific instructions.

## Before you send it

Complete the [Pull Request template](.github/PULL_REQUEST_TEMPLATE.md), including its validation, licensing, integrity, and AI-disclosure declarations. Explain every inapplicable or skipped check rather than marking it passed.

Thanks for contributing.
