---
name: unipd-pdf-review
description: Visually inspect generated course or component PDFs for layout, readability, navigation, and rendering defects. Use only after a successful relevant build. Do not use for content writing, compilation, LaTeX implementation, tests, validation, or CI.
---

# UniPD PDF Review

## Select and inspect

Review the current generated PDF:

- `.build/<year>/<course-name>/main.pdf` for a local course build, or the corresponding PDF from the pull-request CI artifact;
- `latex/components/<component>/example/main.pdf` for a tracked component fixture;
- `latex/integration/<language>/main.pdf` for a tracked integration fixture.

Course PDFs are protected build outputs and must not be copied into, staged from, or committed under a course directory. Do not review an outdated PDF after source changes. If neither a current local build nor its CI artifact is available, report an incomplete review.

Inspect the full affected PDF when practical. For large documents, inspect at least the cover, front matter, table of contents, changed sections, adjacent pages, affected bibliography or appendices, and final page.

Render pages to images. Text extraction alone is not a visual review.

## Visual checklist

Check document-wide:

- page size, margins, headers, footers, numbering, hierarchy, spacing, and page breaks;
- blank, duplicated, clipped, overlapping, off-page, or unreadably small content;
- inconsistent typography or avoidable large empty areas.

Check front matter:

- title, course, academic year, author, version, contents, lists, and page-number transitions.

Check mathematics:

- symbols, delimiters, alignment, numbering, matrices, cases, theorem layout, and awkward page splits.

Check figures, diagrams, and tables:

- resolution, scaling, cropping, labels, legends, captions, source notes, wrapping, alignment, multi-page behavior, and legibility.

Check code and algorithms:

- monospace rendering, highlighting, indentation, line numbers, wrapping, clipping, captions, inputs, outputs, and page breaks.

Check references and navigation:

- cross-reference numbers, unresolved `??`, citations, bibliography, hyperlinks, bookmarks, and visible duplicate destinations.

Review visual correctness only; mathematical correctness belongs to note review unless rendering changes meaning.

## Findings

Classify each finding:

- `blocking`: missing, unreadable, clipped, overlapping, or meaningfully broken;
- `important`: clearly harms readability or consistency;
- `minor`: cosmetic with limited impact;
- `observation`: notable but not necessarily defective.

For each finding, report severity, PDF path, page, element, concise problem, likely source file when identifiable, and a correction when clear.

## Result

End with exactly one status:

- `PASS`
- `PASS WITH MINOR ISSUES`
- `NEEDS CHANGES`
- `INCOMPLETE REVIEW`

State which pages were reviewed. Never pass a missing or only partially inspectable required PDF.
