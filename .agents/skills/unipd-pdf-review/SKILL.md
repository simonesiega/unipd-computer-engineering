---
name: unipd-pdf-review
description: Visually inspect freshly compiled UniPD course, component, and integration PDFs for layout, legibility, pagination, links, and rendering regressions. Requires real inspection of rendered page images, not compilation or text extraction alone. Route content corrections and source implementation to the appropriate skills.
---

# UniPD PDF Review

## Select a verifiable build

Use a PDF produced **after the latest relevant source changes**:

- courses: `.build/<year>/<course-name>/main.pdf` or the matching CI PDF artifact;
- component examples: `.build/latex/components/<component>/example/main.pdf`;
- language integration examples: `.build/latex/integration/<language>/main.pdf`.

Tracked source-adjacent example PDFs are also valid only when regenerated from the current sources. Check-mode builds leave those fixtures unchanged; prefer their fresh `.build/` PDFs for review.

Confirm its source revision and build provenance when available. Never review an outdated document as evidence for current changes. Follow [output ownership](../../../docs/guides/getting-started/building-documents.md#review-the-output) and the [protected-content rules](../../../AGENTS.md#generated-and-protected-content).

If no current PDF exists, request or delegate a build to `unipd-latex-build`; this skill does not itself own compilation or LaTeX source edits.

## Perform a real visual review

1. Determine the PDF's page count and affected chapters/pages. Render the pages to image files with an available PDF renderer (for example `pdftoppm` or a compatible tool).
2. **Actually open and inspect the rendered images.** A successful render command, extracted text, file metadata, an image contact-sheet path, or an assertion that images were generated is not visual inspection.
3. For a small or release-candidate PDF, inspect every page. For a long PDF, first inspect a readable contact sheet covering every page; then inspect at full readable resolution the cover, front matter, contents, changed pages, neighboring pages, diagrams, tables, code, appendices/bibliography, and ending. For a requested *full* review, do not silently substitute sampling.
4. When necessary, zoom into difficult equations, small labels, multi-column content, glyphs, and dense code listings. Text extraction and PDF structure checks may supplement but never replace image inspection.
5. When previous output exists, compare affected and adjacent pages to catch unintended repagination or typographic regressions. Page shifts alone are not defects; assess actual readability and meaning.
6. If an image viewer fails, try another available inspection method or render format before declaring a blocker. If the images still cannot be viewed, mark the visual review **incomplete** and report precisely which pages could not be inspected.

Do not use OCR as the default means of visual assessment. Do not claim `PASS` solely because compilation, validation, or extracted text succeeded.

## Examine document-wide consistency

- Page size, margins, line lengths, running headers, footers, page numbers, blank pages, and front/main/appendix transitions.
- Consistent typography, font weights, language-appropriate hyphenation, paragraph spacing, hierarchy, and table-of-contents entries.
- Content clipped at edges, collisions, missing glyphs, off-page floats, duplicated elements, unreadably small text, and missing pages.
- Widows/orphans, awkwardly separated theorem or example statements, split captions, strange page breaks, and conspicuous accidental whitespace. Do not call every intentionally sparse page an error.

## Examine academic and technical material visually

- **Mathematics:** signs, subscripts, superscripts, delimiters, roots, accents, quantifiers, equation alignment, case distinctions, theorem/proof boxes, and visually misleading line breaks.
- **Diagrams and figures:** axes, arrows, label placement, legends, captions, resolution, scaling, and whether required information is visible.
- **Tables:** header association, column widths, multi-page continuation, wrapped cells, unit labels, alignment, and clipping.
- **Code and pseudocode:** indentation, line wraps, syntax colors/contrast, command/output separation, character fidelity, and terminal/text block boundaries.
- **Navigation:** legible references, table-of-contents destinations, hyperlink/bookmark behavior when inspectable, missing `??`, repeated destinations, and apparent cross-reference inconsistencies.
- **Front matter:** cover fields and attribution **as authored**; do not second-guess course-specific dates, versions, or channels without evidence and authorization.

If a rendered sign, exponent, symbol, or code indentation changes the meaning, flag it as a content-significant visual defect and hand off the source correction to `unipd-note-writing` or `unipd-latex-component-development` as appropriate. Do not independently redesign the document.

## Findings and pass criteria

For each issue, provide severity, exact PDF path, **physical PDF page**, printed page number if different, affected element, observed defect, likely source location, and minimal suggested correction.

Classify findings as:

- `blocking`: missing, unreadable, clipped/overlapping, incorrect or meaning-changing rendering;
- `important`: substantial readability, navigation, or consistency defect;
- `minor`: limited cosmetic defect;
- `observation`: benign or intentional characteristic worth noting.

Finish with one explicit result: `PASS`, `PASS WITH MINOR ISSUES`, `NEEDS CHANGES`, or `INCOMPLETE REVIEW`. Only `PASS`/`PASS WITH MINOR ISSUES` may follow actual review of the **declared required pages**. Report exactly which page ranges or all pages were visually inspected, any viewer failures, limitations, and what remains for publication.

A visual `PASS` does not certify mathematical or programming correctness, and a successful build does not certify visual quality.
