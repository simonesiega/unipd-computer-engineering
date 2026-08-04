# LaTeX Fonts

This directory contains the font files used by the [`unipd-notes`](../unipd-notes.cls) document class. The fonts are bundled with the repository so that all builds produce consistent output without depending on fonts installed on the operating system.

The type system has three specific responsibilities:

- Libertinus Serif and Libertinus Math provide body text and mathematics;
- Source Sans 3 provides headings, captions, labels, and structural text;
- IBM Plex Mono provides source code, terminal output, and technical identifiers.

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
│   ├── LibertinusSerif-Semibold.otf
│   └── LibertinusSerif-SemiboldItalic.otf
└── Source Sans 3/
    ├── SourceSans3-Bold.otf
    ├── SourceSans3-It.otf
    ├── SourceSans3-Regular.otf
    └── SourceSans3-Semibold.otf
```

No additional files belong inside a font-family directory.

## Font catalogue

| Family | File | Role |
|---|---|---|
| **Libertinus Math** | [`LibertinusMath-Regular.otf`](Libertinus/LibertinusMath-Regular.otf) | Mathematical equations, operators, symbols, and formula labels. |
| **Libertinus Serif** | [`LibertinusSerif-Regular.otf`](Libertinus/LibertinusSerif-Regular.otf) | Normal paragraphs and long-form academic text. |
| **Libertinus Serif** | [`LibertinusSerif-Italic.otf`](Libertinus/LibertinusSerif-Italic.otf) | Emphasis, introduced terminology, source notes, and publication titles. |
| **Libertinus Serif** | [`LibertinusSerif-Semibold.otf`](Libertinus/LibertinusSerif-Semibold.otf) | Semibold emphasis where a stronger hierarchy is required. |
| **Libertinus Serif** | [`LibertinusSerif-SemiboldItalic.otf`](Libertinus/LibertinusSerif-SemiboldItalic.otf) | Combined semibold and italic emphasis. |
| **Libertinus Serif** | [`LibertinusSerif-Bold.otf`](Libertinus/LibertinusSerif-Bold.otf) | Strong emphasis in body text. |
| **Source Sans 3** | [`SourceSans3-Regular.otf`](Source%20Sans%203/SourceSans3-Regular.otf) | Captions, labels, headers, footers, and structural text. |
| **Source Sans 3** | [`SourceSans3-It.otf`](Source%20Sans%203/SourceSans3-It.otf) | Italic sans-serif text. |
| **Source Sans 3** | [`SourceSans3-Semibold.otf`](Source%20Sans%203/SourceSans3-Semibold.otf) | Subheadings and medium-emphasis structural text. |
| **Source Sans 3** | [`SourceSans3-Bold.otf`](Source%20Sans%203/SourceSans3-Bold.otf) | Chapter titles, section headings, and prominent labels. |
| **IBM Plex Mono** | [`IBMPlexMono-Regular.otf`](IBM%20Plex%20Mono/IBMPlexMono-Regular.otf) | Source code, terminal sessions, paths, and technical identifiers. |
| **IBM Plex Mono** | [`IBMPlexMono-Italic.otf`](IBM%20Plex%20Mono/IBMPlexMono-Italic.otf) | Italic emphasis inside monospaced content. |
| **IBM Plex Mono** | [`IBMPlexMono-Medium.otf`](IBM%20Plex%20Mono/IBMPlexMono-Medium.otf) | Medium-emphasis technical text. |
| **IBM Plex Mono** | [`IBMPlexMono-Bold.otf`](IBM%20Plex%20Mono/IBMPlexMono-Bold.otf) | Keywords and strongly emphasized code. |

## Usage

The [`typography`](../components/typography/typography.sty) component loads and configures the font files through `fontspec`. The [`mathematics`](../components/mathematics/mathematics.sty) component configures Libertinus Math through `unicode-math`.

The shared class applies the following mappings automatically:

| LaTeX interface | Font family | Typical use |
|---|---|---|
| `\rmfamily` and normal text | Libertinus Serif | Paragraphs, definitions, theorems, proofs, and explanations. |
| Mathematics | Libertinus Math | Inline and displayed mathematics. |
| `\sffamily` | Source Sans 3 | Titles, headings, captions, labels, and navigation elements. |
| `\ttfamily` and `\texttt` | IBM Plex Mono | Code, commands, filenames, paths, protocols, and identifiers. |

Authors should use semantic LaTeX commands and environments instead of selecting font files or font families manually.

## Typographic roles

| Content | Default face | Typical size |
|---|---|---:|
| Body text | Libertinus Serif Regular | 11 pt |
| Mathematical content | Libertinus Math | Matched to surrounding text |
| Chapter and section headings | Source Sans 3 Bold | 16–24 pt |
| Subheadings | Source Sans 3 Semibold | 11–14 pt |
| Figure and table captions | Source Sans 3 Regular | 9 pt |
| Code and terminal blocks | IBM Plex Mono Regular | 9.5 pt |
| Inline technical identifiers | IBM Plex Mono Regular | Matched to surrounding text |

## Requirements

LuaLaTeX is required because the font system uses OpenType files through `fontspec` and `unicode-math`. pdfLaTeX and XeLaTeX are not supported by the shared class.

Every font file must:

1. remain inside its current family directory;
2. retain its exact filename;
3. be loaded through the shared font-path definitions;
4. have a clear typographic role;
5. be available to every repository build;
6. preserve compatibility with the current LuaLaTeX configuration.

Do not install or reference system-local substitutes, because they can change line breaks, page breaks, mathematical metrics, and generated PDFs.

## Building and validation

From the repository root, compile all documents in the [canonical Docker environment](../../docs/md/getting-started/docker.md) and verify the bundled fonts with:

```bash
docker compose run --rm texlive python3 latex/tools/build.py --all --keep-going
```

A successful validation must not report missing fonts, substituted font families, missing mathematical glyphs, or compilation errors. Regenerated PDFs must also pass the canonical `--check-generated` check.

## Changing the font system

When adding, replacing, renaming, or removing a font file:

1. update the relevant font-family directory;
2. update [`typography.sty`](../components/typography/typography.sty) or [`mathematics.sty`](../components/mathematics/mathematics.sty);
3. update the catalogue and directory tree in this README;
4. compile every component example;
5. compile both integration examples;
6. inspect line wrapping, page breaks, captions, code, and mathematics visually;
7. regenerate all affected PDFs before committing.

Do not change the bundled font set without verifying both textual and mathematical output.

## Licensing

The bundled font files remain subject to their respective open-source licences. The licence text and release-specific attribution notices are stored in [`FONT-LICENSE.md`](FONT-LICENSE.md).

Do not remove, replace, or redistribute the font files without preserving the corresponding licence information.
