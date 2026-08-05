"""Run the Python tool tests and enforce branch-coverage reporting."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

from coverage import Coverage

MINIMUM_COVERAGE = 80


def main() -> int:
    """Run the complete tool suite and report coverage for production tools."""
    tools_directory = Path(__file__).resolve().parent
    coverage = Coverage(
        branch=True,
        source=[str(tools_directory)],
        omit=[str(tools_directory / "test" / "*"), str(Path(__file__).resolve())],
    )
    coverage.start()
    suite = unittest.defaultTestLoader.discover(
        str(tools_directory / "test"), pattern="test_*.py"
    )
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    coverage.stop()
    coverage.save()
    covered_percent = coverage.report(show_missing=True)
    coverage_sufficient = covered_percent >= MINIMUM_COVERAGE
    if not coverage_sufficient:
        print(
            f"Coverage {covered_percent:.1f}% is below {MINIMUM_COVERAGE}%",
            file=sys.stderr,
        )
    return 0 if result.wasSuccessful() and coverage_sufficient else 1


if __name__ == "__main__":
    sys.exit(main())
