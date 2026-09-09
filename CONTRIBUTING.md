# Contributing

[← Project README](README.md) · [Code of Conduct](CODE_OF_CONDUCT.md) · [Security policy](SECURITY.md)

Contributions are welcome, from small corrections to complete course material, as long as they are accurate, focused, legally redistributable, and consistent with the rest of the archive.

## Quick workflow

| Step | Action |
|---:|---|
| 1 | Check the existing courses, documentation, issues, and Pull Requests. |
| 2 | Fork the repository and create a focused branch from `main`. |
| 3 | Make one coherent change. |
| 4 | Build and review the affected documents, then run the relevant checks. |
| 5 | Open a Pull Request describing what changed and how you validated it. |

Small corrections and documentation improvements can normally go directly to a Pull Request.

Open an issue first for substantial work such as adding a course, reorganizing a large part of an existing course, changing the shared LaTeX system, or modifying repository-wide build and CI behavior.

## What can I contribute?

| Contribution | Main guide |
|---|---|
| Correct or expand notes | [Writing notes](docs/md/user-guide/writing-notes.md) |
| Add a course from this cohort | [Creating a course](docs/md/getting-started/creating-a-course.md) |
| Reorganize a course | [Course structure](docs/md/user-guide/course-structure.md) |
| Update metadata | [Metadata](docs/md/user-guide/metadata.md) |
| Build and validate documents | [Building documents](docs/md/getting-started/building-documents.md) |
| Modify the document class | [Document class](docs/md/reference/unipd-notes-class.md) |
| Modify shared components | [LaTeX components](latex/components/README.md) |
| Modify bundled fonts | [LaTeX fonts](latex/fonts/README.md) |
| Change repository infrastructure | [Architecture](docs/md/development/architecture.md) · [Build system](docs/md/development/build-system.md) · [Validation, tests, and CI](docs/md/development/tool-test-and-ci.md) |

Before editing an existing course, review its current notation, terminology, structure, open issues, and Pull Requests. Preserve established conventions unless changing them is the purpose of the contribution.

## Quality standards

Study material should be useful beyond the original author or lecture group.

Keep contributions:

- **accurate** — check statements, notation, examples, and solutions;
- **clear** — explain assumptions, abbreviations, and non-obvious steps;
- **structured** — organize topics in a logical progression;
- **consistent** — preserve terminology, notation, language, and formatting;
- **well-sourced** — cite borrowed material and substantial external claims;
- **readable** — keep equations, code, diagrams, and tables legible in the compiled PDF;
- **maintainable** — follow the shared structure instead of adding unnecessary local formatting.

Write notes in the language in which the course is taught. Preserve that language when editing an existing course.

Clearly distinguish exercises from solutions, and state when a solution is informal, incomplete, or only one possible approach.

## Licensing and attribution

| Material | License |
|---|---|
| Study notes and academic materials under `1/`, `2/`, and `3/` | [CC BY-SA 4.0](LICENSE) |
| Compiled note PDFs distributed through GitHub Releases | Generated distributions of their corresponding [CC BY-SA 4.0](LICENSE) sources |
| Shared LaTeX system, build and validation tools, release packaging, documentation except `CODE_OF_CONDUCT.md`, CI configuration, and other supporting project files | [MIT](LICENSE-MIT) |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | Adapted from the Contributor Covenant and distributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Third-party fonts, assets, and bundled resources | Subject to their respective licenses. See [`latex/fonts/FONT-LICENSE.md`](latex/fonts/FONT-LICENSE.md) for font licensing information. |

By submitting a contribution, you confirm that you created the material or have the right to contribute it, that it may be distributed under the applicable repository license, and that required attribution and license notices have been preserved.

Do not upload material that cannot legally be redistributed, including textbook scans, paid or access-restricted resources, proprietary solution manuals, instructor material without permission, or copyrighted images, diagrams, code, and datasets without a compatible license.

Prefer original explanations and diagrams. When redistribution rights are unclear, link to the external source instead of copying it.

## AI-assisted contributions

AI-assisted contributions are allowed only after careful human review.

You remain responsible for accuracy, completeness, originality, citations, attribution, licensing, and consistency with the surrounding material.

Do not submit unreviewed generated content, fabricated references, or claims you have not verified.

## Repository conventions

Course structure, metadata, generated files, and source conventions are documented in [Course structure](docs/md/user-guide/course-structure.md), [Metadata](docs/md/user-guide/metadata.md), and [Building documents](docs/md/getting-started/building-documents.md).

Do not manually edit content between generated markers:

```html
<!-- GENERATED:START -->
<!-- GENERATED:END -->

<!-- RELEASE-CATALOG:START -->
<!-- RELEASE-CATALOG:END -->
```

Edit course-owned LaTeX sources, figures, bibliography files, and README content outside generated sections.

Generated course `main.pdf` files are build outputs and must not be committed. Local builds remain under:

```text
.build/<year>/<course>/main.pdf
```

Shared LaTeX, build-tool, font, and CI changes may affect multiple courses. Keep these changes focused, preserve compatibility, update the relevant documentation, and run the complete applicable validation workflow.

## Exam coverage

Adding or improving material does not automatically mark an exam as covered.

An exam becomes covered only when its intended notes are sufficiently complete, reviewed, and approved through an immutable snapshot release. The rolling `notes-latest` release does not establish covered status.

Coverage counts and tables are generated from published releases. Do not edit them manually.

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

Security vulnerabilities must not be reported publicly. Follow [`SECURITY.md`](SECURITY.md) and use [GitHub Private Vulnerability Reporting](https://github.com/simonesiega/unipd-computer-engineering/security/advisories/new).

## Validation

Before opening a Pull Request, build the affected documents using the canonical Docker environment and review the generated PDFs visually.

For a course build:

```bash
docker compose run --rm texlive python3 latex/tools/build.py 1/course-name
```

See [Docker builds](docs/md/getting-started/docker.md), [Building documents](docs/md/getting-started/building-documents.md), and [Validation, tests, and CI](docs/md/development/tool-test-and-ci.md) for the complete validation workflow.

Pull-request CI builds affected documents when possible. Repository-wide LaTeX, font, build-system, or CI changes may trigger compilation of the complete archive.

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

Confirm that:

- [ ] the contribution is in the correct course or repository area;
- [ ] the material is original or may legally be redistributed;
- [ ] sources, attribution, and third-party licenses are documented;
- [ ] course language, terminology, notation, and structure are consistent;
- [ ] source files follow the documented repository conventions;
- [ ] affected documents compile successfully in the canonical Docker environment;
- [ ] affected PDFs have been reviewed visually;
- [ ] generated sections and tracked examples are up to date;
- [ ] no generated course PDF is included in the Pull Request;
- [ ] relevant validation checks pass;
- [ ] the Pull Request explains the change, validation, material AI assistance when relevant, and any skipped checks;
- [ ] the contribution follows the [Code of Conduct](CODE_OF_CONDUCT.md).

Thanks for helping build a useful and reliable archive for the 2026–2029 Computer Engineering cohort.
