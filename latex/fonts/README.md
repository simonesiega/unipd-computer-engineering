# LaTeX Fonts

[← Documentation](../../docs/README.md) · [License](#licensing) · [`unipd-notes` class](../../docs/md/reference/unipd-notes-class.md) · [Components](../components/README.md) · [Docker builds](../../docs/md/getting-started/docker.md)

This directory contains the OpenType fonts bundled with the repository and used by the [`unipd-notes`](../unipd-notes.cls) document class.

Bundling the fonts keeps canonical builds independent from fonts installed on the host operating system.

## Font system

The repository bundles three font families, with Libertinus providing both serif text and mathematics:

| Family | Role |
|---|---|
| **Libertinus Serif** | Body text and long-form academic content |
| **Libertinus Math** | Mathematical notation and symbols |
| **Source Sans 3** | Headings, captions, labels, navigation, and structural text |
| **IBM Plex Mono** | Source code, terminal output, paths, commands, and technical identifiers |

The shared LaTeX components load these files automatically. Course authors should use semantic LaTeX commands and environments rather than selecting font files directly.

## Directory structure

```text
fonts/
├── IBM Plex Mono/
│   ├── IBMPlexMono-Bold.otf
│   ├── IBMPlexMono-Italic.otf
│   ├── IBMPlexMono-Medium.otf
│   └── IBMPlexMono-Regular.otf
├── Libertinus/
│   ├── LibertinusMath-Regular.otf
│   ├── LibertinusSerif-Bold.otf
│   ├── LibertinusSerif-Italic.otf
│   ├── LibertinusSerif-Regular.otf
│   └── LibertinusSerif-SemiboldItalic.otf
└── Source Sans 3/
    ├── SourceSans3-Bold.otf
    ├── SourceSans3-It.otf
    ├── SourceSans3-Regular.otf
    └── SourceSans3-Semibold.otf
```

No unrelated files belong inside a font-family directory.

## Font catalogue

| Family | File | Primary role |
|---|---|---|
| **Libertinus Math** | [`LibertinusMath-Regular.otf`](Libertinus/LibertinusMath-Regular.otf) | Mathematical equations, operators, symbols, and formula labels |
| **Libertinus Serif** | [`LibertinusSerif-Regular.otf`](Libertinus/LibertinusSerif-Regular.otf) | Normal paragraphs and long-form text |
| **Libertinus Serif** | [`LibertinusSerif-Italic.otf`](Libertinus/LibertinusSerif-Italic.otf) | Emphasis and italic academic text |
| **Libertinus Serif** | [`LibertinusSerif-SemiboldItalic.otf`](Libertinus/LibertinusSerif-SemiboldItalic.otf) | Combined semibold and italic emphasis |
| **Libertinus Serif** | [`LibertinusSerif-Bold.otf`](Libertinus/LibertinusSerif-Bold.otf) | Strong body-text emphasis |
| **Source Sans 3** | [`SourceSans3-Regular.otf`](Source%20Sans%203/SourceSans3-Regular.otf) | Captions, labels, headers, footers, and structural text |
| **Source Sans 3** | [`SourceSans3-It.otf`](Source%20Sans%203/SourceSans3-It.otf) | Italic sans-serif text |
| **Source Sans 3** | [`SourceSans3-Semibold.otf`](Source%20Sans%203/SourceSans3-Semibold.otf) | Subheadings and medium-emphasis structure |
| **Source Sans 3** | [`SourceSans3-Bold.otf`](Source%20Sans%203/SourceSans3-Bold.otf) | Chapter titles, section headings, and prominent labels |
| **IBM Plex Mono** | [`IBMPlexMono-Regular.otf`](IBM%20Plex%20Mono/IBMPlexMono-Regular.otf) | Code, terminal sessions, filenames, paths, and identifiers |
| **IBM Plex Mono** | [`IBMPlexMono-Italic.otf`](IBM%20Plex%20Mono/IBMPlexMono-Italic.otf) | Italic monospaced emphasis |
| **IBM Plex Mono** | [`IBMPlexMono-Medium.otf`](IBM%20Plex%20Mono/IBMPlexMono-Medium.otf) | Programming-language keywords and medium emphasis |
| **IBM Plex Mono** | [`IBMPlexMono-Bold.otf`](IBM%20Plex%20Mono/IBMPlexMono-Bold.otf) | Strong monospaced emphasis |

## LaTeX mapping

Font loading is owned by the shared components:

- [`typography.sty`](../components/typography/typography.sty) configures text families through `fontspec`;
- [`mathematics.sty`](../components/mathematics/mathematics.sty) configures Libertinus Math through `unicode-math`.

The effective mapping is:

| LaTeX interface | Font family |
|---|---|
| Normal text and `\rmfamily` | Libertinus Serif |
| Mathematics | Libertinus Math |
| `\sffamily` | Source Sans 3 |
| `\ttfamily` and `\texttt` | IBM Plex Mono |

The bundled subsets do not contain every possible combined style. Where necessary, `fontspec` derives missing combined faces from the bundled files instead of falling back to system fonts.

## Font requirements

Every bundled font file must:

1. remain inside its designated family directory;
2. retain the filename expected by the shared configuration;
3. be loaded through the repository's shared font-path definitions;
4. have a clear typographic role;
5. be available to every canonical build;
6. remain compatible with the current LuaLaTeX configuration.

System-local substitutes must not be used in canonical builds because different font files can change metrics, line breaks, page breaks, and generated PDFs.

LuaLaTeX is required by the shared font system.

## Changing the font system

When adding, replacing, renaming, or removing a font:

1. update the relevant family directory;
2. update [`typography.sty`](../components/typography/typography.sty) or [`mathematics.sty`](../components/mathematics/mathematics.sty);
3. update this directory tree and catalogue;
4. rebuild affected component and integration examples;
5. run the complete canonical document build;
6. inspect text wrapping, page breaks, headings, captions, code, and mathematical output;
7. run generated-state validation before committing.

Font changes are repository-wide presentation changes and should be reviewed across both textual and mathematical content.

For canonical build and validation commands, see [Building documents](../../docs/md/getting-started/building-documents.md).

## Licensing

Bundled fonts remain subject to their original open-source licenses.

Release-specific attribution and license information is documented in [`FONT-LICENSE.md`](FONT-LICENSE.md).

Do not remove or redistribute bundled font files without preserving the applicable license information.
