#!/usr/bin/env python3
"""Compile repository documents and refresh generated READMEs."""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

START_MARKER = "<!-- GENERATED:START -->"
END_MARKER = "<!-- GENERATED:END -->"
DOCUMENT_ROOTS = ("1", "2", "3", "latex/components", "latex/integration")
SOURCE_DATE_EPOCH = "1785542400"
LEVEL_DEPTH = {
    "part": 0,
    "chapter": 0,
    "section": 1,
    "subsection": 2,
    "subsubsection": 3,
}
README_LABELS = {
    "italian": {
        "pdf": "Apri il PDF compilato",
        "contents": "Indice dei contenuti",
        "empty": "Nessuna voce numerata.",
        "page": "p.",
    },
    "english": {
        "pdf": "Open the compiled PDF",
        "contents": "Table of contents",
        "empty": "No numbered entries.",
        "page": "p.",
    },
}
DOCUMENT_CLASS_PATTERN = re.compile(r"\\documentclass\s*(?:\[([^]]*)\])?\s*\{")


@dataclass(frozen=True)
class TocEntry:
    level: str
    title: str
    page: str


def repository_root() -> Path:
    """Return the absolute path to the repository root directory."""
    return Path(__file__).resolve().parents[2]


def discover_documents(root: Path) -> list[Path]:
    """Discover every main.tex file in the repository document roots."""
    documents: list[Path] = []
    for relative_root in DOCUMENT_ROOTS:
        search_root = root / relative_root
        if search_root.exists():
            documents.extend(search_root.rglob("main.tex"))
    return sorted(path.resolve() for path in documents)


def changed_files(root: Path, base: str, head: str) -> list[Path]:
    """Return repository-relative paths changed between two Git revisions."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMRD", base, head, "--"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return [Path(line) for line in result.stdout.splitlines() if line]


def read_changed_files(root: Path, filename: str) -> list[Path]:
    """Read repository-relative changed paths prepared outside the TeX container."""
    path = Path(filename)
    if not path.is_absolute():
        path = root / path
    return [
        Path(line) for line in path.read_text(encoding="utf-8").splitlines() if line
    ]


def affected_documents(root: Path, paths: list[Path]) -> list[Path]:
    """Map changed files to documents that may depend on them."""
    affected: set[Path] = set()

    for path in paths:
        parts = path.parts

        # The class, component packages, fonts, and build tool are shared by all
        # documents, so a change to any of them requires a complete build.
        shared_latex = (
            path == Path("latex/unipd-notes.cls")
            or path == Path("latex/tools/build.py")
            or (
                len(parts) >= 3
                and parts[:2] == ("latex", "components")
                and path.suffix == ".sty"
            )
            or (
                len(parts) >= 3
                and parts[:2] == ("latex", "fonts")
                and path.suffix.lower() in {".otf", ".ttf"}
            )
        )
        if shared_latex:
            return discover_documents(root)

        # Any file in a course directory can be an input to that course.
        if len(parts) >= 2 and parts[0] in {"1", "2", "3"}:
            document = (root / parts[0] / parts[1] / "main.tex").resolve()
            if document.is_file():
                affected.add(document)
            continue

        # Example changes affect only the corresponding example document.
        if (
            len(parts) >= 4
            and parts[:2] == ("latex", "components")
            and parts[3] == "example"
        ):
            document = (
                root / parts[0] / parts[1] / parts[2] / "example" / "main.tex"
            ).resolve()
            if document.is_file():
                affected.add(document)
            continue

        if len(parts) >= 3 and parts[:2] == ("latex", "integration"):
            document = (root / parts[0] / parts[1] / parts[2] / "main.tex").resolve()
            if document.is_file():
                affected.add(document)

    return sorted(affected)


def resolve_document(root: Path, value: str) -> Path:
    """Resolve a user-provided path to an absolute main.tex file path."""
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    if path.is_dir():
        path = path / "main.tex"
    path = path.resolve()
    if path.name != "main.tex" or not path.is_file():
        raise FileNotFoundError(f"Expected an existing main.tex: {path}")
    return path


def build_directory(root: Path, document: Path) -> Path:
    """Return the absolute .build directory for a document."""
    relative_directory = document.parent.relative_to(root)
    return root / ".build" / relative_directory


def compile_document(
    root: Path, document: Path, publish: bool = True
) -> tuple[Path, Path]:
    """Compile a document and return its built PDF and table-of-contents paths."""
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        raise RuntimeError("latexmk was not found in PATH")

    output_directory = build_directory(root, document)
    if output_directory.exists():
        shutil.rmtree(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    command = [
        latexmk,
        "-lualatex",
        "-halt-on-error",
        "-interaction=nonstopmode",
        "-file-line-error",
        f"-outdir={output_directory}",
        "main.tex",
    ]
    environment = os.environ.copy()
    environment["TEXINPUTS"] = (
        str(root / "latex") + os.pathsep + environment.get("TEXINPUTS", "")
    )
    environment["SOURCE_DATE_EPOCH"] = SOURCE_DATE_EPOCH
    environment["FORCE_SOURCE_DATE"] = "1"
    environment["TZ"] = "UTC"
    subprocess.run(command, cwd=document.parent, env=environment, check=True)

    built_pdf = output_directory / "main.pdf"
    toc_file = output_directory / "main.toc"

    if not built_pdf.is_file():
        raise RuntimeError(f"Compilation did not produce {built_pdf}")

    if publish:
        final_pdf = document.parent / "main.pdf"
        temporary_pdf = final_pdf.with_suffix(".pdf.tmp")
        try:
            shutil.copy2(built_pdf, temporary_pdf)
            os.replace(temporary_pdf, final_pdf)
        finally:
            temporary_pdf.unlink(missing_ok=True)
    return built_pdf, toc_file


def parse_group(text: str, position: int) -> tuple[str, int]:
    """Parse a braced LaTeX argument and return it with the new position."""
    while position < len(text) and text[position].isspace():
        position += 1
    if position >= len(text) or text[position] != "{":
        raise ValueError("Expected a braced LaTeX argument")

    depth = 0
    start = position + 1
    position += 1
    while position < len(text):
        character = text[position]
        escaped = position > 0 and text[position - 1] == "\\"
        if character == "{" and not escaped:
            depth += 1
        elif character == "}" and not escaped:
            if depth == 0:
                return text[start:position], position + 1
            depth -= 1
        position += 1
    raise ValueError("Unclosed braced LaTeX argument")


def strip_latex(text: str) -> str:
    """Strip LaTeX commands and formatting from text."""
    text = text.replace("\\protect", "")
    text = re.sub(r"\\numberline\s*\{([^{}]*)\}", r"\1 ", text)
    for _ in range(4):
        text = re.sub(
            r"\\(?:textbf|textit|textsl|emph|texttt|textrm|textsf)\s*\{([^{}]*)\}",
            r"\1",
            text,
        )
    replacements = {
        r"\&": "&",
        r"\%": "%",
        r"\_": "_",
        r"\#": "#",
        r"\textendash": "–",
        r"\textemdash": "—",
        "~": " ",
    }
    for source, destination in replacements.items():
        text = text.replace(source, destination)
    text = re.sub(r"\\[a-zA-Z@]+\*?", "", text)
    text = text.replace("{", "").replace("}", "")
    text = re.sub(r"\s+", " ", text).strip()
    return html.unescape(text)


def parse_toc(toc_file: Path) -> list[TocEntry]:
    """Parse a LaTeX table-of-contents file."""
    if not toc_file.is_file():
        return []

    text = toc_file.read_text(encoding="utf-8", errors="replace")
    entries: list[TocEntry] = []
    cursor = 0
    command = "\\contentsline"
    while True:
        cursor = text.find(command, cursor)
        if cursor < 0:
            break
        cursor += len(command)
        try:
            level, cursor = parse_group(text, cursor)
            title, cursor = parse_group(text, cursor)
            page, cursor = parse_group(text, cursor)
            _, cursor = parse_group(text, cursor)
        except ValueError:
            continue
        level = level.strip()
        if level in LEVEL_DEPTH:
            entries.append(TocEntry(level, strip_latex(title), strip_latex(page)))
    return entries


def document_language(document: Path) -> str:
    """Return the language selected by a document class option."""
    source = document.read_text(encoding="utf-8", errors="replace")
    match = DOCUMENT_CLASS_PATTERN.search(source)
    if match is None or match.group(1) is None:
        return "italian"
    options = {option.strip() for option in match.group(1).split(",")}
    return "english" if "english" in options else "italian"


def render_generated_markdown(
    entries: list[TocEntry], language: str = "italian"
) -> str:
    """Render table-of-contents entries as localized README Markdown."""
    labels = README_LABELS[language]
    lines = [
        f"[{labels['pdf']}](main.pdf)",
        "",
        f"## {labels['contents']}",
    ]
    if not entries:
        lines.append(f"- {labels['empty']}")
    else:
        for entry in entries:
            indentation = "  " * LEVEL_DEPTH[entry.level]
            page = f" — {labels['page']} {entry.page}" if entry.page else ""
            lines.append(f"{indentation}- {entry.title}{page}")
    return "\n".join(lines)


def is_component_example(root: Path, document: Path) -> bool:
    """Return whether a document is a component example without a README."""
    relative = document.relative_to(root)
    return (
        len(relative.parts) == 5
        and relative.parts[:2] == ("latex", "components")
        and relative.parts[-2:] == ("example", "main.tex")
    )


def generated_readme_content(directory: Path, generated_markdown: str) -> str:
    """Insert generated Markdown between README markers."""
    readme = directory / "README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8")
    else:
        content = f"# {directory.name}\n"

    start_count = content.count(START_MARKER)
    end_count = content.count(END_MARKER)
    replacement = f"{START_MARKER}\n{generated_markdown}\n{END_MARKER}"

    if start_count == 0 and end_count == 0:
        content = content.rstrip() + "\n\n" + replacement + "\n"
    elif start_count == 1 and end_count == 1:
        start = content.find(START_MARKER)
        end = content.find(END_MARKER)
        if end <= start:
            raise ValueError(f"Invalid generated markers in {readme}")
        end += len(END_MARKER)
        content = content[:start] + replacement + content[end:]
    else:
        raise ValueError(f"Invalid generated markers in {readme}")

    return content


def update_readme(directory: Path, generated_markdown: str) -> None:
    """Update a document README with generated Markdown."""
    content = generated_readme_content(directory, generated_markdown)
    readme = directory / "README.md"
    temporary_readme = directory / ".README.md.tmp"
    try:
        temporary_readme.write_text(content, encoding="utf-8", newline="\n")
        os.replace(temporary_readme, readme)
    finally:
        temporary_readme.unlink(missing_ok=True)


def generated_file_error(generated: Path, committed: Path) -> str | None:
    """Return an error when a generated file differs from its committed file."""
    if not committed.is_file():
        return f"Generated file is not committed: {committed}"
    if generated.read_bytes() != committed.read_bytes():
        return f"Generated file is stale: {committed}"
    return None


def process_document(
    root: Path,
    document: Path,
    compile_enabled: bool,
    readme_enabled: bool,
    check_generated: bool,
) -> None:
    """Compile one document, update its README, and verify generated files."""
    relative = document.relative_to(root)
    print(f"==> {relative}", flush=True)

    if compile_enabled:
        pdf_file, toc_file = compile_document(
            root, document, publish=not check_generated
        )
    else:
        pdf_file = document.parent / "main.pdf"
        toc_file = build_directory(root, document) / "main.toc"
        if not toc_file.exists():
            local_toc = document.parent / "main.toc"
            if local_toc.exists():
                toc_file = local_toc

    generated_errors: list[str] = []
    if check_generated:
        pdf_error = generated_file_error(pdf_file, document.parent / "main.pdf")
        if pdf_error:
            generated_errors.append(pdf_error)

    if readme_enabled:
        if not pdf_file.is_file():
            raise FileNotFoundError(f"Compiled PDF was not found: {pdf_file}")
        if not is_component_example(root, document):
            entries = parse_toc(toc_file)
            markdown = render_generated_markdown(entries, document_language(document))
            if check_generated:
                expected_readme = generated_readme_content(document.parent, markdown)
                committed_readme = document.parent / "README.md"
                if (
                    not committed_readme.is_file()
                    or committed_readme.read_text(encoding="utf-8") != expected_readme
                ):
                    generated_errors.append(
                        f"Generated README content is stale: {committed_readme}"
                    )
            else:
                update_readme(document.parent, markdown)

    if generated_errors:
        details = "\n    ".join(generated_errors)
        raise RuntimeError(
            f"Generated outputs do not match. Run build.py for this document:\n    {details}"
        )


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "targets", nargs="*", help="Document directories or main.tex files"
    )
    parser.add_argument(
        "--all", action="store_true", help="Discover every repository document"
    )
    parser.add_argument(
        "--changed-from",
        metavar="REVISION",
        help="Build documents affected by files changed since this Git revision",
    )
    parser.add_argument(
        "--changed-to",
        metavar="REVISION",
        default="HEAD",
        help="End revision used with --changed-from (default: HEAD)",
    )
    parser.add_argument(
        "--changed-file-list",
        metavar="FILE",
        help="Build documents affected by repository-relative paths listed in FILE",
    )
    parser.add_argument(
        "--no-compile",
        action="store_true",
        help="Reuse an existing PDF and generated .toc data",
    )
    parser.add_argument(
        "--no-readme",
        action="store_true",
        help="Compile without updating generated README files",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove the external .build directory after success",
    )
    parser.add_argument(
        "--keep-going",
        action="store_true",
        help="Build every target and report all failures at the end",
    )
    parser.add_argument(
        "--check-generated",
        action="store_true",
        help="Build in .build and fail if committed PDFs or READMEs are stale",
    )
    return parser.parse_args()


def main() -> int:
    """Select and process requested documents."""
    arguments = parse_arguments()
    root = repository_root()

    if arguments.check_generated and arguments.no_compile:
        raise ValueError("--check-generated cannot be combined with --no-compile")
    if arguments.check_generated and arguments.no_readme:
        raise ValueError("--check-generated cannot be combined with --no-readme")

    selection_modes = sum(
        (
            bool(arguments.all),
            bool(arguments.changed_from),
            bool(arguments.changed_file_list),
            bool(arguments.targets),
        )
    )
    if selection_modes != 1:
        raise ValueError(
            "Use exactly one of explicit targets, --all, --changed-from, "
            "or --changed-file-list"
        )

    if arguments.all:
        documents = discover_documents(root)
    elif arguments.changed_from or arguments.changed_file_list:
        if arguments.changed_from:
            paths = changed_files(root, arguments.changed_from, arguments.changed_to)
        else:
            paths = read_changed_files(root, arguments.changed_file_list)
        documents = affected_documents(root, paths)
        if not documents:
            print("No changed files affect a LaTeX document.", flush=True)
            return 0
        print(
            f"Selected {len(documents)} affected document(s) "
            f"from {len(paths)} changed file(s)."
        )
    else:
        documents = [resolve_document(root, value) for value in arguments.targets]

    if not documents:
        raise RuntimeError("No main.tex files were discovered")

    failures: list[tuple[Path, Exception]] = []
    for document in documents:
        try:
            process_document(
                root,
                document,
                compile_enabled=not arguments.no_compile,
                readme_enabled=not arguments.no_readme,
                check_generated=arguments.check_generated,
            )
        except (
            OSError,
            RuntimeError,
            ValueError,
            subprocess.CalledProcessError,
        ) as caught_error:
            if not arguments.keep_going:
                raise
            failures.append((document.relative_to(root), caught_error))
            print(
                f"error: {document.relative_to(root)}: {caught_error}",
                file=sys.stderr,
            )

    if failures:
        print(
            f"Failed {len(failures)} of {len(documents)} document(s):", file=sys.stderr
        )
        for document, failure in failures:
            print(f"  - {document}: {failure}", file=sys.stderr)
        return 1
    if arguments.clean:
        shutil.rmtree(root / ".build", ignore_errors=True)
    print(f"Completed {len(documents)} document(s).", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
