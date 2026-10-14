---
name: unipd-python-tool-development
description: Implement, review, and test repository Python tools in latex/tools/ and latex/tools/test/, including course creation, build selection, validation, changelogs, packaging, and release catalog generation. Preserve deterministic standard-library unittest tests. Delegate content writing, LaTeX compilation, PDF inspection, and pre-commit validation.
---

# UniPD Python Tool Development and Testing

## Establish observable behavior

1. Identify the tool and the public behavior being added, corrected, or reviewed. Read its current implementation, CLI behavior, related helpers, and closest tests.
2. Consult [Validation, tests, and CI](../../../docs/guides/development/tool-test-and-ci.md) and [Build system](../../../docs/guides/development/build-system.md) if selection, generation, packaging, or CI ownership is unclear.
3. Reproduce a reported failure before modifying code when practical. Identify expectations from existing tests and project policy, not assumptions based on one particular course.
4. Preserve the layout and language support of all course years, supported semesters, dated or topical structures, and allowed class languages. Do not hard-code course names, professors, course topics, lecture schedules, or temporary snapshot dates.

## Test architecture

Tests live under `latex/tools/test/`, follow `test_*.py`, and use only Python's standard-library test infrastructure. Prefer `unittest`, `tempfile`, `pathlib`, `subprocess`, `unittest.mock`, and local fake repositories. Put regression tests near the responsible feature; add new test modules only when responsibilities are genuinely separate.

Do **not** introduce pytest, Hypothesis/property-testing frameworks, third-party test fixtures, external network dependencies, or test-side coverage imports without an explicit approved migration. [Running tests](../../../latex/tools/test/TESTS.md#running-tests) owns the coverage-runner contract and threshold; design tests for real behavioral coverage, not merely a percentage.

## Implementation quality

- Keep CLI arguments, error output, exit status, generated files, paths, and documented interfaces stable unless a deliberate change is requested.
- Favor explicit validation and useful, actionable errors; distinguish user input errors from environmental failures.
- Make outputs deterministic: control ordering, encoding (UTF-8), line endings, timestamps, locales, environment variables, and Git history inputs where relevant.
- Use temporary directories, never writing test data into the real working repository. Avoid network access and global Git settings. Configure identity on temporary repositories only.
- Honor tool ownership of generated course README sections, component/integration fixtures, manifests, checksums, the README release catalogue and `RELEASES.md`, and changelogs. Regenerate release listings with `update_release_catalog.py` from published release data; never manually change release assets or immutable snapshots.
- Treat unexpected paths, symlinks, repository traversal, invalid metadata, duplicate asset names, missing sources, and partial failures according to the actual tool contract; do not assume happy-path input.
- Support all validated year/semester/language combinations without imposing subject-specific assumptions or externally inferred course metadata.
- Do not broaden repository-wide behavior to hide a single malformed course. Add appropriate regression coverage when a real invariant changes.

## Regression method

1. Demonstrate the bug or unmet requirement with a focused failing test.
2. Apply the smallest implementation correction.
3. Run that test and the closest affected tests.
4. Run the complete tool suite for changes to shared helpers, schemas, discovery, build selection, generation, validation, or packaging.
5. Inspect produced files or CLI output rather than asserting private implementation details where public behavior is available.
6. Confirm the fix does not change unrelated courses, fixtures, README manual content, or release metadata.

Key cases to cover when relevant: absent/invalid arguments; existing target files; duplicate or colliding slugs; inconsistent metadata; no-op/idempotent reruns; ordering across platforms; files with non-ASCII content; missing or stale generated files; Git renames or missing history; recoverable versus fatal failures; erroneous paths and escape attempts; and valid empty states.

## Commands

Use [TESTS.md: running tests](../../../latex/tools/test/TESTS.md#running-tests) for focused, complete, and coverage-enforced commands. Update the [test catalogue](../../../latex/tools/test/TESTS.md#maintaining-this-catalogue) when methods change.

Report unavailable dependencies and incomplete coverage checks explicitly. Delegate Ruff/mypy/pre-commit verification to `unipd-repository-validation` and generated-state compilation to `unipd-latex-build`.

## Completion

Report the observed bug or requested behavior, regression test coverage, exact commands and outcomes, modified files, output compatibility, and remaining limitations. Inspect the final diff and ensure no unrelated code or user work was altered. No commits, tags, or releases without explicit authorization.
