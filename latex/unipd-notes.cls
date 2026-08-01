\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{\@currpath\@currname}[2026/07/31 v0.1.0 Shared course notes class]

\edef\unipdcomponentpath{\@currpath components/}
\edef\unipdfontpath{\@currpath fonts/}
\edef\unipdlibertinusfontpath{\unipdfontpath Libertinus/}
\edef\unipdsourcefontpath{\unipdfontpath Source Sans 3/}
\edef\unipdmonofontpath{\unipdfontpath IBM Plex Mono/}

\RequirePackage{iftex}
\ifLuaTeX\else
  \ClassError{unipd-notes}{LuaLaTeX is required}{Compile this document with LuaLaTeX.}
\fi

\newif\ifunipdbibliography
\unipdbibliographyfalse
\DeclareOption{bibliography}{\unipdbibliographytrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrreprt}}
\ProcessOptions\relax

\LoadClass[
  11pt,
  a4paper,
  oneside,
  open=any,
  headings=normal
]{scrreprt}

\providecommand*{\input@path}{}
\edef\input@path{{\unipdcomponentpath}\input@path}
\RequirePackage{metadata/metadata}
\RequirePackage{typography/typography}
\RequirePackage{lists/lists}
\RequirePackage{mathematics/mathematics}
\RequirePackage{figures-tables/figures-tables}
\RequirePackage{diagrams/diagrams}
\RequirePackage{environments/environments}
\RequirePackage{code/code}
\RequirePackage{algorithms/algorithms}
\RequirePackage{document-structure/document-structure}
\RequirePackage{cover/cover}
\RequirePackage{table-of-contents/table-of-contents}
\RequirePackage{page-style/page-style}
\RequirePackage{navigation/navigation}
\RequirePackage{references/references}
\RequirePackage{glossary/glossary}
\RequirePackage{front-back-matter/front-back-matter}

\endinput
