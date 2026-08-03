---
name: unipd-python-tool-development
description: Develop, fix, review, and test Python tools under latex/tools/ and latex/tools/test/. Use for regressions, filesystem and Git behavior, deterministic output, argument validation, and affected-document selection. Preserve the standard-library unittest architecture. Do not use for LaTeX builds, PDF review, course writing, shared LaTeX development, or repository validation.
---

# UniPD Python Tool Development and Testing

## Establish context

1. Identify the tool and observable behavior under test.
2. Inspect the implementation and closest existing test file.
3. Reuse existing helpers and temporary-repository patterns.
4. Consult `docs/md/development/tool-test-and-ci.md` when conventions are unclear.
5. Reproduce reported behavior when practical.

## Test architecture

Use only the Python standard library unless a migration is explicitly requested. Prefer `unittest`, `tempfile`, `pathlib`, `subprocess`, and `unittest.mock`.

Do not introduce pytest, third-party fixtures, coverage libraries, property testing, or snapshot dependencies.

Place tests under `latex/tools/test/`, use `test_*.py`, and add tests to the file that owns the behavior. Create a new file only for a separate responsibility.

## What to test

Prefer stable observable behavior:

- return values and exit codes;
- generated files, contents, and directory layouts;
- argument validation and interface-level errors;
- Git-history behavior;
- affected-document selection.

Avoid private implementation details unless no stable interface exists. Use focused tests with descriptive names and specific assertions.

## Regression workflow

1. Reproduce the failure.
2. Add a test that fails for the original behavior.
3. Apply the smallest implementation fix.
4. Run the new test and related tests.
5. Run the full suite when shared behavior changes.

Test the user-visible regression, not an implementation accident.

## Isolation and determinism

- Use temporary directories or repositories; never write into the real repository.
- Avoid network access, absolute paths, global Git configuration, uncontrolled time, locale assumptions, and filesystem ordering.
- Configure local Git identity and deterministic commits when history is required.
- Control dates, environment variables, and process inputs when they affect output.
- Sort collections before comparing unordered results.
- Clean up automatically.

## Commands

Focused file:

```bash
python3 latex/tools/test/test_<name>.py
```

Complete suite:

```bash
python3 -m unittest discover -s latex/tools/test -p 'test_*.py'
```

Use the available Python launcher on the current platform.

## Review

Confirm coverage, isolation, determinism, useful failures, and absence of new third-party dependencies.
