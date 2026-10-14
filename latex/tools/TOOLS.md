# Python Tool Index

[← LaTeX router](../README.md) · [Documentation](../../docs/README.md) · [Test catalogue](test/TESTS.md)

This index identifies each top-level source file in `latex/tools/` and routes to the guide that owns its instructions. It does not duplicate command references or workflow policies.

## Files

| File | Responsibility and scoped reference |
|---|---|
| [`build.py`](build.py) | Document discovery, selection, compilation, and generated README/fixture checks. [Build-system reference](../../docs/guides/development/build-system.md). |
| [`build_docs.py`](build_docs.py) | Public-site staging, link adaptation, readers, and rendered validation. [Documentation-site guide](../../docs/guides/development/documentation-site.md). |
| [`check_repository.py`](check_repository.py) | Read-only structural, source-hygiene, Markdown, and tracked-PDF checks. [Repository validation](../../docs/guides/development/tool-test-and-ci.md#repository-validation). |
| [`create_course.py`](create_course.py) | Metadata validation and localized course scaffolding. [Course-creation guide](../../docs/guides/getting-started/creating-a-course.md). |
| [`generate_changelog.py`](generate_changelog.py) | Per-course committed histories and changelog baselines. [Changelog workflow](../../docs/guides/development/tool-test-and-ci.md#course-changelogs). |
| [`latex_source.py`](latex_source.py) | Import-only helpers that detect escaping and strip unescaped LaTeX comments while preserving line boundaries. It neither interprets TeX nor writes files. |
| [`package_notes.py`](package_notes.py) | Deterministic release assets from existing compiled course PDFs. [Packaging reference and staging ownership](../../docs/guides/development/build-system.md#release-packaging). |
| [`run_tool_tests.py`](run_tool_tests.py) | Coverage-enforced test entry point; saves Coverage.py data, normally as `.coverage` in the working directory. [Test commands and coverage contract](test/TESTS.md#running-tests). |
| [`update_release_catalog.py`](update_release_catalog.py) | Updates the generated README catalogue and release archive from prepared release JSON. [Release-catalogue workflow](../../docs/guides/development/tool-test-and-ci.md#release-catalogue). |
| `TOOLS.md` | This manually maintained file index. |

The [`test/`](test/TESTS.md) directory owns the test catalogue. Local `__pycache__/` directories are disposable interpreter caches, not additional tools.

## Running the tools

| Task | Instructions |
|---|---|
| Install host prerequisites and validation dependencies | [Installation](../../docs/guides/getting-started/installation.md) |
| Compile documents and inspect generated output | [Building documents](../../docs/guides/getting-started/building-documents.md) |
| Create a course | [Creating a course](../../docs/guides/getting-started/creating-a-course.md#create-the-course) |
| Run repository checks | [Local quality checks](../../docs/guides/development/tool-test-and-ci.md#local-quality-checks) |
| Run all tests or a focused method | [Running tests](test/TESTS.md#running-tests) |
| Build or preview the website | [Build and review locally](../../docs/guides/development/documentation-site.md#build-and-review-locally) |
| Package or publish an edition | [Packaging](../../docs/guides/development/build-system.md#release-packaging) · [Publication authorization and workflow](../../docs/guides/development/tool-test-and-ci.md#release-publication) |

Consult the scoped reference before running a generation tool: some commands replace protected outputs or clean owned staging directories. The physical tool/test layout is documented in [LATEX.md](../LATEX.md#tools-and-tests).
