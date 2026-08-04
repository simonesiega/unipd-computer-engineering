<p align="center">
  <img src="docs/assets/unipd.png" alt="University of Padua" width="320" />
</p>

<h1 align="center">
  Contributing to UniPD Computer Engineering
</h1>

<p align="center">
  Guidelines for contributing study materials and repository improvements.
</p>

<p align="center">
  <img
    src="https://img.shields.io/badge/PRs-welcome-brightgreen"
    alt="Pull requests welcome"
  />
  <a href="LICENSE">
    <img
      src="https://img.shields.io/badge/Notes-CC%20BY--SA%204.0-EF9421?logo=creativecommons&logoColor=white"
      alt="Notes: Creative Commons Attribution-ShareAlike 4.0 International License"
    />
  </a>
  <a href="LICENSE-MIT">
    <img
      src="https://img.shields.io/badge/Code-MIT-yellow?logo=opensourceinitiative&logoColor=white"
      alt="Code: MIT License"
    />
  </a>
  <a href="https://github.com/simonesiega/unipd-computer-engineering/issues">
    <img
      src="https://img.shields.io/github/issues/simonesiega/unipd-computer-engineering"
      alt="Open issues"
    />
  </a>
</p>

## Overview

This repository is a shared, long-term archive of study materials for Computer Engineering students at the University of Padua. It is an unofficial, student-maintained project and is not affiliated with or endorsed by the University of Padua.

Contributions may correct or expand existing notes, add original material for new courses, improve diagrams and examples, or enhance the LaTeX system, documentation, build tools, and automation that support the archive.

Every contribution is valuable. A pull request may contain anything from a typo correction to a complete set of course notes.

## Quick workflow

| Step | Action |
|---:|---|
| 1 | Check the existing courses, documentation, issues, and pull requests. |
| 2 | Fork the repository and create a focused branch from `main`. |
| 3 | Make one coherent change. |
| 4 | Build and review the affected documents, then run the relevant checks. |
| 5 | Open a pull request describing the change and the validation performed. |

Small corrections, documentation improvements, and focused additions may normally go directly to a pull request.

Open an issue first when you plan to:

- add a new course;
- substantially reorganize existing notes;
- change the shared LaTeX system;
- modify repository-wide build, validation, or CI behaviour.

## Contribution paths

Choose the path closest to your change and follow the linked guide.

| Contribution | Main guide |
|---|---|
| Correct or expand notes | [Writing notes](docs/md/user-guide/writing-notes.md) |
| Add a new course | [Creating a course](docs/md/getting-started/creating-a-course.md) |
| Reorganize a course | [Course structure](docs/md/user-guide/course-structure.md) |
| Update course or document metadata | [Metadata](docs/md/user-guide/metadata.md) |
| Set up canonical PDF builds | [Docker builds](docs/md/getting-started/docker.md) |
| Build and validate documents | [Building documents](docs/md/getting-started/building-documents.md) |
| Modify the document class | [Document class](docs/md/reference/unipd-notes-class.md) |
| Modify shared components | [LaTeX components](latex/components/README.md) |
| Modify bundled fonts | [LaTeX fonts](latex/fonts/README.md) |
| Change repository infrastructure | [Architecture](docs/md/development/architecture.md) · [Build system](docs/md/development/build-system.md) · [Validation, Tests, and CI](docs/md/development/tool-test-and-ci.md) |

Before editing an existing course, review its current content, notation, terminology, structure, open issues, and pull requests. Preserve existing conventions unless the purpose of the contribution is to improve them.

## Quality standards

Contributed material should be useful to students beyond the original author or lecture group.

Aim for work that is:

- **accurate:** statements, notation, examples, and solutions have been checked;
- **clear:** assumptions, abbreviations, and non-obvious steps are explained;
- **structured:** topics follow a logical progression;
- **consistent:** language, terminology, notation, and formatting remain stable;
- **well-sourced:** borrowed material and substantial claims include appropriate references;
- **readable:** equations, code, diagrams, and tables remain legible in the compiled PDF;
- **maintainable:** source files are organized and avoid unnecessary local formatting.

Write notes in the language in which the course is taught: use Italian for courses taught in Italian and English for courses taught in English. Preserve that language when editing an existing course.

Clearly distinguish exercises from solutions, and state when a solution is informal, incomplete, or only one possible approach.

## Licensing and attribution

Study notes and academic materials under `1/`, `2/`, and `3/` are distributed under [CC BY-SA 4.0](LICENSE). Compiled PDFs published through GitHub Releases are generated distributions of those corresponding licensed sources.

The shared LaTeX system, tools, release packaging, documentation, CI configuration, and other supporting project files are distributed under the [MIT License](LICENSE-MIT).

By submitting a contribution, you confirm that:

- you created the material or have the right to contribute it;
- it may be distributed under the applicable repository license;
- all required attribution and license notices have been preserved.

Do not upload material that cannot be redistributed legally, including:

- scans or copies of textbooks;
- paid or access-restricted resources;
- lecture slides, recordings, handouts, or instructor material without permission;
- copyrighted diagrams, images, code, or datasets without a compatible license;
- proprietary solution manuals;
- personal, confidential, or sensitive information.

Prefer original explanations and diagrams. When redistribution rights are unclear, link to the external source instead of copying it.

Clearly identify quotations and third-party material, including its source and applicable license.

## AI-assisted content

AI-assisted contributions are permitted only after careful human review.

Contributors remain responsible for the material's:

- accuracy and completeness;
- originality;
- citations and attribution;
- licensing;
- consistency with the surrounding notes.

Do not submit unreviewed generated content or fabricated references.

## Repository conventions

Course structure, generated files, metadata, and source conventions are documented in:

- [Course structure](docs/md/user-guide/course-structure.md)
- [Metadata](docs/md/user-guide/metadata.md)
- [Building documents](docs/md/getting-started/building-documents.md)

Do not manually edit content between generated markers:

```html
<!-- GENERATED:START -->
<!-- GENERATED:END -->
```

Edit course-owned LaTeX sources, figures, bibliography files, and README content outside the generated markers. A course build keeps its PDF under `.build/<year>/<course>/main.pdf` and refreshes the generated README section. Generated course PDFs under `1/`, `2/`, and `3/` are ignored build outputs and must not be added to Git. Component and integration example PDFs remain tracked fixtures and are regenerated through the pinned Docker Compose environment when affected.

If a course PDF was accidentally forced into the index, remove it without deleting the local build with:

```bash
git rm --cached -- <year>/<course>/main.pdf
```

Do not rewrite repository history during normal contributions. Historical binary cleanup, if ever desired, is a separate disruptive maintainer operation outside this migration.

Shared LaTeX, build-tool, font, or CI changes may affect multiple courses and examples. Keep them focused, preserve compatibility, update the relevant documentation, and follow the complete validation workflow.

## Exam coverage

Adding or improving material does not automatically make an exam covered.

A contributor may propose covered status, but the repository maintainer makes the final decision during pull-request review. Approval depends on whether the intended course topics are represented, no substantial known gaps remain, and the compiled notes have been reviewed.

Update covered-exam counts and tables only after maintainer approval.

## Getting help and reporting problems

Search the [existing issues](https://github.com/simonesiega/unipd-computer-engineering/issues) first, then use the form that best matches the request:

| Request | Form |
|---|---|
| Inaccurate, unclear, incomplete, or outdated notes | [Report a content error](https://github.com/simonesiega/unipd-computer-engineering/issues/new?template=content-error.yml) |
| A new course archive | [Submit a course proposal](https://github.com/simonesiega/unipd-computer-engineering/issues/new?template=course-proposal.yml) |
| A reproducible local build, validation, generated-file, or CI failure | [Report a build problem](https://github.com/simonesiega/unipd-computer-engineering/issues/new?template=build-problem.yml) |

For a request that does not fit these forms, start a [general issue](https://github.com/simonesiega/unipd-computer-engineering/issues/new). A draft pull request is also welcome when you want feedback on work already in progress.

Include precise paths and locations in content reports. Build reports should contain reproduction steps, environment details, and sanitized logs. Course proposals should link to the official public course page and explain the planned scope and redistribution rights.

Security vulnerabilities must not be reported publicly. Submit them through [GitHub Private Vulnerability Reporting](https://github.com/simonesiega/unipd-computer-engineering/security/advisories/new) and follow [`SECURITY.md`](SECURITY.md).

## Validation

Before opening a pull request, follow [Docker builds](docs/md/getting-started/docker.md) and [Building documents](docs/md/getting-started/building-documents.md), then complete the applicable items in the review checklist below.

For pull requests, CI compiles only documents affected by the proposed changes when selection is possible. A change inside a course builds that course, and a change inside a component example builds that example. Changes to the shared document class, component packages, bundled fonts, canonical Compose environment, CI build workflow, or build tool compile every document because they may have repository-wide impact. Reviewers can download the `latex-pdfs-<commit-sha>` workflow artifact from the pull-request run; it is retained for approximately 14 days. Failed compilation logs are uploaded separately when available.

Pushes to `main` run all quality checks, compile the complete archive, package course PDFs as `<degree-year>-<course-slug>.pdf`, and replace the assets of the rolling [`notes-latest`](https://github.com/simonesiega/unipd-computer-engineering/releases/tag/notes-latest) release. Packaging also creates `manifest.json`, `SHA256SUMS.txt`, and `RELEASE_NOTES.md`.

### Maintainer release procedure

The rolling release is automatic after a successful push to `main`; it is titled **Latest compiled notes**, its tag is moved to that `main` commit, and stale assets are removed. Re-running the same commit is idempotent.

For an immutable end-of-semester snapshot, open **Actions → Publish compiled notes → Run workflow**, then provide a new release tag, title, and optional Markdown description. Tags such as `2026-2027-semester-1` are recommended. The workflow compiles and packages the complete archive with the same code as the rolling release and fails if either the requested tag or release already exists. Never reuse or overwrite a snapshot tag.

For packaging failures, inspect the named missing course PDF, duplicate asset name, manifest, or checksum error in **Compile and package complete archive**. For publication failures, inspect the `gh` command output and any draft release left intentionally to prevent partial assets from appearing successful. A failed snapshot draft must be inspected and explicitly deleted before retrying the same tag; published snapshots must never be deleted merely to replace their contents. No repository secret is required because publication uses the workflow token.

## Pull requests

Keep each pull request focused on one course or one coherent repository change.

Use concise branch names, for example:

```text
notes/analysis-1-limits
fix/programming-pointer-example
docs/course-contribution-guide
latex/improve-theorem-spacing
```

Use a clear pull-request title, for example:

```text
notes(analysis-1): add limits and continuity chapter
fix(programming): correct pointer ownership example
docs: clarify how students can add course notes
latex(diagrams): improve automata edge labels
```

GitHub automatically loads [the pull-request template](.github/PULL_REQUEST_TEMPLATE.md). Complete every applicable section; if a validation item does not apply, state why.

The pull-request description should:

- explain what was added, corrected, or reorganized;
- identify the affected course or repository area;
- cite relevant sources for technical corrections;
- state which validation steps were completed;
- include generated README changes and any affected tracked example outputs, but no generated course PDF;
- confirm that affected PDFs were reviewed visually, locally or from the CI artifact;
- disclose new third-party material and its license or permission.

Draft pull requests are welcome for substantial contributions that would benefit from early feedback.

## Academic integrity

This archive is intended to support learning and must not enable academic misconduct.

Do not contribute:

- confidential, leaked, or unlawfully obtained examination material;
- answers intended for an active graded assignment, test, or examination;
- another student's work without permission and attribution;
- material whose publication violates a university, course, or instructor rule;
- personal or sensitive information about students, instructors, or staff.

Past exercises and exam-style problems may be included only when they can be shared lawfully and their source is stated clearly.

Contributors remain responsible for following applicable university rules and course-specific instructions.

## Review checklist

Before opening a pull request, confirm that:

- [ ] the contribution is in the correct course or repository area;
- [ ] the material is original or may be redistributed legally;
- [ ] sources, attribution, and third-party licenses are documented;
- [ ] the course language, terminology, notation, and structure are consistent;
- [ ] source files follow the documented repository conventions;
- [ ] affected documents compile successfully in the canonical Docker environment;
- [ ] affected PDFs have been reviewed visually;
- [ ] tracked generated examples and generated README sections pass the canonical `--check-generated` check;
- [ ] no generated course `main.pdf` is tracked or included in the pull request;
- [ ] the relevant validation checks pass;
- [ ] the pull-request description explains the change and validation;
- [ ] covered-exam status changes only after maintainer approval.

Thank you for helping build a useful, reliable, and long-term archive for Computer Engineering students.
