# Font Reference and Maintenance

[← Font router](README.md) · [Font licences](FONT-LICENSE.md) · [Component reference](../components/COMPONENTS.md)

This reference owns the bundled font files, their LaTeX mappings, and font-specific maintenance requirements. Directory locations are indexed in [LATEX.md](../LATEX.md#fonts); exact release attribution and legal notices remain in [FONT-LICENSE.md](FONT-LICENSE.md).

## Font system

Bundled OpenType files keep canonical builds independent of host-installed fonts. The shared components load them automatically; course authors use semantic LaTeX commands rather than choosing files directly.

| Family | Role |
|---|---|
| Libertinus Serif | Body text and long-form academic content. |
| Libertinus Math | Mathematical notation and symbols. |
| Source Sans 3 | Headings, captions, labels, navigation, and structural text. |
| IBM Plex Mono | Code, terminal output, paths, commands, and technical identifiers. |

## Font catalogue

| Family | File | Primary role |
|---|---|---|
| Libertinus Math | [`LibertinusMath-Regular.otf`](Libertinus/LibertinusMath-Regular.otf) | Mathematical equations, operators, and symbols. |
| Libertinus Serif | [`LibertinusSerif-Regular.otf`](Libertinus/LibertinusSerif-Regular.otf) | Normal paragraphs and long-form text. |
| Libertinus Serif | [`LibertinusSerif-Italic.otf`](Libertinus/LibertinusSerif-Italic.otf) | Emphasis and italic academic text. |
| Libertinus Serif | [`LibertinusSerif-SemiboldItalic.otf`](Libertinus/LibertinusSerif-SemiboldItalic.otf) | Face mapped to bold italic body text. |
| Libertinus Serif | [`LibertinusSerif-Bold.otf`](Libertinus/LibertinusSerif-Bold.otf) | Strong body-text emphasis. |
| Source Sans 3 | [`SourceSans3-Regular.otf`](Source%20Sans%203/SourceSans3-Regular.otf) | Captions, labels, headers, footers, and structural text. |
| Source Sans 3 | [`SourceSans3-It.otf`](Source%20Sans%203/SourceSans3-It.otf) | Italic sans-serif text. |
| Source Sans 3 | [`SourceSans3-Semibold.otf`](Source%20Sans%203/SourceSans3-Semibold.otf) | Subheadings and medium-emphasis structure. |
| Source Sans 3 | [`SourceSans3-Bold.otf`](Source%20Sans%203/SourceSans3-Bold.otf) | Chapter titles, section headings, and prominent labels. |
| IBM Plex Mono | [`IBMPlexMono-Regular.otf`](IBM%20Plex%20Mono/IBMPlexMono-Regular.otf) | Code, terminal sessions, filenames, paths, and identifiers. |
| IBM Plex Mono | [`IBMPlexMono-Italic.otf`](IBM%20Plex%20Mono/IBMPlexMono-Italic.otf) | Italic monospaced emphasis. |
| IBM Plex Mono | [`IBMPlexMono-Medium.otf`](IBM%20Plex%20Mono/IBMPlexMono-Medium.otf) | Programming-language keywords and medium emphasis. |
| IBM Plex Mono | [`IBMPlexMono-Bold.otf`](IBM%20Plex%20Mono/IBMPlexMono-Bold.otf) | Strong monospaced emphasis. |

## LaTeX mapping

[`typography.sty`](../components/typography/typography.sty) configures text families through `fontspec`; [`mathematics.sty`](../components/mathematics/mathematics.sty) configures Libertinus Math through `unicode-math`.

| LaTeX interface | Font family |
|---|---|
| Normal text and `\rmfamily` | Libertinus Serif |
| Mathematics | Libertinus Math |
| `\sffamily` | Source Sans 3 |
| `\ttfamily` and `\texttt` | IBM Plex Mono |

Bold italic serif text uses the bundled Libertinus Semibold Italic face. Bold italic sans-serif and monospace text use their bold faces with `FakeSlant=0.2`, not system-font fallbacks. Separate semibold sans-serif and medium monospace commands support subheadings and listing keywords.

## Font requirements

Keep each file inside its designated family directory with the filename expected by the shared configuration. Load it through the shared font-path definitions, give it a clear typographic role, and preserve compatibility with the class's LuaLaTeX engine.

Do not substitute host-local fonts for canonical builds: different metrics can change line breaks, pagination, and generated PDFs. No unrelated files belong inside a font-family directory.

## Changing the font system

1. Update the relevant font-family directory and its loader in `typography.sty` or `mathematics.sty`.
2. Update this catalogue and mappings, and preserve the exact-release notices required by [FONT-LICENSE.md](FONT-LICENSE.md).
3. Follow [Building documents](../../docs/guides/getting-started/building-documents.md) for canonical compilation, PDF review, and generated-state verification. Font changes affect the complete document set under the [selection rules](../../docs/guides/development/build-system.md#target-selection).

During visual review, pay particular attention to glyph identity and coverage, regular/italic/bold weights, code indentation, mathematical symbols, and changes to text wrapping or pagination in both languages. Automated builds do not replace that font-specific inspection.
