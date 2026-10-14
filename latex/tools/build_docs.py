"""Build and validate the public MkDocs site without exposing the repository tree."""

from __future__ import annotations

import argparse
import html
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from build import strip_latex
from check_repository import EXCLUDED_DIRECTORIES, MARKDOWN_LINK
from create_course import DEGREE_START_YEAR
from package_notes import asset_filename, course_metadata, sha256_file
from update_release_catalog import PDF_ASSET, ReleasedPdf

REPOSITORY_URL = "https://github.com/simonesiega/unipd-computer-engineering"
ROOT_DOCUMENTS = (
    "README.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "AGENTS.md",
    "RELEASES.md",
    "LICENSE",
    "LICENSE-MIT",
)
REFERENCE_DOCUMENTS = (
    "latex/README.md",
    "latex/LATEX.md",
    "latex/tools/TOOLS.md",
    "latex/tools/test/TESTS.md",
    "latex/components/README.md",
    "latex/components/COMPONENTS.md",
    "latex/fonts/README.md",
    "latex/fonts/FONTS.md",
    "latex/fonts/FONT-LICENSE.md",
    "latex/integration/english/README.md",
    "latex/integration/italian/README.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
)
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".css"}
SITE_SUFFIXES = ASSET_SUFFIXES | {
    ".html",
    ".js",
    ".json",
    ".xml",
    ".gz",
    ".map",
    ".woff",
    ".woff2",
    ".ttf",
}
HTML_LINK = re.compile(r'\b(?:href|src)=["\']([^"\']+)["\']')
YEARS = ("1", "2", "3")


def public_file(root: Path, source: Path) -> None:
    """Reject private, traversing, or symlinked inputs before reading them."""
    relative = source.relative_to(root)
    if any(part == ".." or part in EXCLUDED_DIRECTORIES for part in relative.parts):
        raise ValueError(f"Private or unsafe documentation input: {source}")
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"Public documentation symlink is not allowed: {current}")
    if not source.is_file():
        raise ValueError(f"Missing public documentation file: {source}")


def tree_files(
    root: Path,
    directory: Path,
    assets: bool = False,
    ignored_names: frozenset[str] = frozenset(),
) -> list[Path]:
    """Discover Markdown and approved assets, rejecting unexpected public inputs."""
    if directory.is_symlink():
        raise ValueError(f"Public documentation symlink is not allowed: {directory}")
    if not directory.exists():
        return []
    files: list[Path] = []
    for parent, directories, names in os.walk(directory, followlinks=False):
        directories[:] = sorted(
            name for name in directories if name not in EXCLUDED_DIRECTORIES
        )
        parent_path = Path(parent)
        for name in directories:
            if (parent_path / name).is_symlink():
                raise ValueError(
                    f"Public documentation symlink is not allowed: {parent_path / name}"
                )
        for name in names:
            path = parent_path / name
            public_file(root, path)
            if name in ignored_names:
                continue
            if path.suffix == ".md" or (
                assets
                and path.is_relative_to(root / "docs/assets")
                and path.suffix.lower() in ASSET_SUFFIXES
            ):
                files.append(path)
            else:
                raise ValueError(f"Unexpected documentation file: {path}")
    return sorted(files)


def site_path(path: Path) -> Path:
    """Give policy wrappers and hidden repository documents public site paths."""
    if path.as_posix() in {"LICENSE", "LICENSE-MIT"}:
        return path.with_suffix(".md")
    if path == Path(".github/PULL_REQUEST_TEMPLATE.md"):
        return Path("PULL_REQUEST_TEMPLATE.md")
    if path.parts and path.parts[0] == ".agents":
        return Path("agents", *path.parts[1:])
    return path


def html_path(path: Path) -> Path:
    """Match MkDocs' README routing with file-style URLs."""
    return (
        path.with_name("index.html")
        if path.name == "README.md"
        else path.with_suffix(".html")
    )


def github_target(root: Path, source: Path) -> str:
    """Link excluded implementation files to their GitHub source, not a local copy."""
    kind = "tree" if source.is_dir() else "blob"
    return f"{REPOSITORY_URL}/{kind}/main/{quote(source.relative_to(root).as_posix())}"


def rewrite_target(
    root: Path,
    stage: Path,
    page: Path,
    target: str,
    raw_html: bool = False,
    source_page: Path | None = None,
) -> str:
    """Keep public-page links local and route other repository links to GitHub."""
    parsed = urlsplit(html.unescape(target))
    if parsed.scheme or parsed.netloc or not parsed.path:
        return target
    requested = unquote(parsed.path)
    source = Path(os.path.abspath(root / (source_page or page).parent / requested))
    try:
        relative = source.relative_to(root)
    except ValueError as error:
        raise ValueError(
            f"Documentation link outside the repository: {page}: {target}"
        ) from error
    if any(part in EXCLUDED_DIRECTORIES for part in relative.parts):
        raise ValueError(f"Private documentation link: {page}: {target}")
    if source.is_symlink():
        raise ValueError(f"Documentation link to a symlink: {page}: {target}")
    staged = site_path(relative)
    if (stage / staged).is_dir() and (stage / staged / "README.md").is_file():
        staged /= "README.md"
    if (stage / staged).is_file():
        if raw_html and staged.suffix == ".md":
            staged = html_path(staged)
        local = posixpath.relpath(staged.as_posix(), page.parent.as_posix())
        return urlunsplit(("", "", quote(local), parsed.query, parsed.fragment))
    if not source.exists():
        raise ValueError(f"Missing documentation target: {page}: {target}")
    return urlunsplit(
        (
            "https",
            "github.com",
            urlsplit(github_target(root, source)).path,
            parsed.query,
            parsed.fragment,
        )
    )


def rewrite_document(
    root: Path, stage: Path, page: Path, content: str, source_page: Path | None = None
) -> str:
    """Rewrite links only in staged prose, leaving fenced examples and sources intact."""
    lines: list[str] = []
    fence = ""
    for line in content.splitlines(keepends=True):
        stripped = line.lstrip()
        marker = re.match(r"`{3,}|~{3,}", stripped)
        if marker:
            run = marker.group()
            if not fence:
                fence = run
            elif (
                run[0] == fence[0]
                and len(run) >= len(fence)
                and not stripped[len(run):].strip()
            ):
                fence = ""
            lines.append(line)
            continue
        if fence:
            lines.append(line)
            continue

        def markdown_link(match: re.Match[str]) -> str:
            target = match.group(1) or match.group(2)
            replacement = rewrite_target(
                root, stage, page, target, source_page=source_page
            )
            start, end = match.span(1 if match.group(1) else 2)
            offset = match.start()
            return (
                match.group(0)[: start - offset]
                + replacement
                + match.group(0)[end - offset :]
            )

        def html_link(match: re.Match[str]) -> str:
            replacement = html.escape(
                rewrite_target(
                    root,
                    stage,
                    page,
                    match.group(1),
                    raw_html=True,
                    source_page=source_page,
                ),
                quote=True,
            )
            return match.group(0).replace(match.group(1), replacement, 1)

        lines.append(HTML_LINK.sub(html_link, MARKDOWN_LINK.sub(markdown_link, line)))
    return "".join(lines)


def published_pdfs(root: Path) -> dict[tuple[int, str], ReleasedPdf]:
    """Choose each course's first PDF from the tool-owned, newest-first archive."""
    pdfs: dict[tuple[int, str], ReleasedPdf] = {}
    prefix = f"{REPOSITORY_URL}/releases/download/"
    for link in MARKDOWN_LINK.finditer(
        (root / "RELEASES.md").read_text(encoding="utf-8")
    ):
        target = link.group(1) or link.group(2)
        filename = urlsplit(target).path.rsplit("/", 1)[-1]
        match = PDF_ASSET.fullmatch(filename)
        if match is None:
            continue
        if (
            not target.startswith(prefix)
            or re.fullmatch(
                r"[A-Za-z0-9][A-Za-z0-9._-]*/" + re.escape(filename),
                target.removeprefix(prefix),
            )
            is None
        ):
            raise ValueError(f"Invalid published PDF URL: {target}")
        year, slug = int(match.group(1)), match.group(2)
        pdfs.setdefault((year, slug), ReleasedPdf(year, slug, filename, target))
    return pdfs


def download_pdf(pdf: ReleasedPdf, destination: Path) -> None:
    """Copy a published PDF byte-for-byte; never use an unpublished local build."""
    request = Request(
        pdf.download_url, headers={"User-Agent": "unipd-notes-documentation"}
    )
    temporary = destination.with_suffix(".pdf.tmp")
    try:
        with urlopen(request, timeout=60) as response:
            if getattr(response, "status", 200) != 200:
                raise ValueError(f"Incomplete PDF response: {pdf.download_url}")
            header = response.read(5)
            if header != b"%PDF-":
                raise ValueError(f"Missing PDF header in release asset: {pdf.download_url}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            with temporary.open("w+b") as output:
                output.write(header)
                shutil.copyfileobj(response, output)
                size = output.tell()
                length = getattr(response, "headers", {}).get("Content-Length")
                if length is not None and size != int(length):
                    raise ValueError(f"Incomplete PDF download: {pdf.download_url}")
                output.seek(max(0, size - 1024))
                if not output.read().rstrip().endswith(b"%%EOF"):
                    raise ValueError(f"Missing PDF end marker: {pdf.download_url}")
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def course_name(main: Path) -> str:
    """Read a display title without exposing LaTeX escapes in site controls."""
    return strip_latex(course_metadata(main).get("course", "")) or main.parent.name


def stage_course_readers(root: Path, stage: Path, with_pdfs: bool) -> None:
    """Generate stable /<course-slug>/ pages and optional same-origin PDF copies."""
    pdfs = published_pdfs(root)
    reserved = {path.name.casefold() for path in stage.iterdir() if path.is_dir()}
    reserved.update({"assets", "pdfs", *YEARS})
    for year in YEARS:
        for readme in sorted((root / year).glob("*/README.md")):
            public_file(root, readme)
            main = readme.with_name("main.tex")
            public_file(root, main)
            slug = readme.parent.name
            asset_filename(int(year), slug)
            if slug in reserved:
                raise ValueError(f"Conflicting course reader route: /{slug}/")
            reserved.add(slug)
            name = course_name(main)
            title = re.sub(r"([\\\[\]*_`])", r"\\\1", html.escape(name))
            lines = [
                f"# {title}",
                "",
                f"[Courses](../courses.md) · [Contents and sources](../{year}/{slug}/README.md)",
                "",
            ]
            pdf = pdfs.get((int(year), slug))
            if pdf is None:
                lines.append("No PDF has been published for this course yet.")
            else:
                tag = pdf.download_url.rsplit("/", 2)[-2]
                lines.extend((f"Latest published PDF: `{tag}`.", ""))
                if with_pdfs:
                    destination = stage / "pdfs" / pdf.filename
                    download_pdf(pdf, destination)
                    local = f"../pdfs/{pdf.filename}?v={sha256_file(destination)[:16]}"
                    lines.extend(
                        (
                            '<p class="course-pdf-actions">',
                            f'<a class="md-button md-button--primary" href="{local}" target="_blank" rel="noopener">Open PDF in a new tab</a>',
                            f'<a class="md-button" href="{local}" download="{pdf.filename}">Download PDF</a>',
                            "</p>",
                            "",
                            f'<iframe class="course-pdf" src="{local}#view=FitH" title="PDF: {html.escape(name, quote=True)}" loading="lazy"></iframe>',
                            "",
                            "If the embedded viewer is unavailable in your browser, open the PDF in a new tab or download it.",
                            "",
                        )
                    )
                else:
                    lines.extend(
                        (
                            f"[Download the latest published PDF]({pdf.download_url})",
                            "",
                            "This documentation-only build omits the embedded PDF. Build with `--with-pdfs` to preview it locally.",
                            "",
                        )
                    )
                lines.append(
                    "PDF copies refresh when the site is deployed. The source contents may be newer than this published edition."
                )
            destination = stage / slug / "README.md"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
            )


def course_index(root: Path, year: str | None = None) -> str:
    """List course sources without inferring exam coverage or inventing release URLs."""
    title = "Courses" if year is None else f"Year {year} courses"
    prefix = "" if year is None else "../"
    lines = [
        f"# {title}",
        "",
        "Open a course to read its latest published PDF in your browser, or browse its source contents.",
        "",
        (
            f"For published PDFs, use the [download catalogue]({prefix}README.md#coverage) "
            f"or the [release archive]({prefix}RELEASES.md). Rolling links may be unavailable before publication."
        ),
        "",
    ]
    for degree_year in (year,) if year else YEARS:
        start = DEGREE_START_YEAR + int(degree_year) - 1
        lines.extend((f"## Year {degree_year} · {start}–{start + 1}", ""))
        courses = sorted((root / degree_year).glob("*/README.md"))
        if not courses:
            lines.extend(("No course sources yet.", ""))
        for readme in courses:
            public_file(root, readme)
            main = readme.with_name("main.tex")
            public_file(root, main)
            name = re.sub(r"([\\\[\]*_`])", r"\\\1", html.escape(course_name(main)))
            relative = readme.relative_to(root).as_posix()
            reader = f"{prefix}{readme.parent.name}/README.md"
            lines.append(
                f"- [{name}]({reader}) · [Contents and sources]({prefix}{relative})"
            )
        lines.append("")
    return "\n".join(lines)


def stage_documents(root: Path, stage: Path, with_pdfs: bool = False) -> None:
    """Copy an explicit public allowlist, then adapt only the temporary copies."""
    sources = [root / name for name in (*ROOT_DOCUMENTS, *REFERENCE_DOCUMENTS)]
    sources += tree_files(root, root / "docs", assets=True)
    sources += tree_files(root, root / ".agents/skills")
    sources += tree_files(
        root, root / "CHANGELOG", ignored_names=frozenset({".gitkeep", "BASELINE"})
    )
    for year in YEARS:
        sources += sorted((root / year).glob("*/README.md"))
    source_pages: dict[Path, Path] = {}
    for source in sorted(set(sources)):
        public_file(root, source)
        original = source.relative_to(root)
        relative = site_path(original)
        source_pages[relative] = original
        destination = stage / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.name in {"LICENSE", "LICENSE-MIT"}:
            destination.write_text(
                f"# {source.name}\n\n```text\n{source.read_text(encoding='utf-8')}\n```\n",
                encoding="utf-8",
                newline="\n",
            )
        else:
            shutil.copyfile(source, destination)
    stage_course_readers(root, stage, with_pdfs)
    (stage / "courses.md").write_text(
        course_index(root), encoding="utf-8", newline="\n"
    )
    for year in YEARS:
        destination = stage / year / "README.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(course_index(root, year), encoding="utf-8", newline="\n")
    history = [
        "# Course changelogs",
        "",
        "Committed course-source changes, generated from Git history.",
        "",
    ]
    history.extend(
        f"- [{path.stem}]({path.relative_to(stage).as_posix()})"
        for path in sorted((stage / "CHANGELOG").rglob("*.md"))
    )
    if len(history) == 4:
        history.append("No course changelogs yet.")
    (stage / "changelogs.md").write_text(
        "\n".join(history) + "\n", encoding="utf-8", newline="\n"
    )
    for document in sorted(stage.rglob("*.md")):
        page = document.relative_to(stage)
        content = rewrite_document(
            root,
            stage,
            page,
            document.read_text(encoding="utf-8"),
            source_pages.get(page),
        )
        document.write_text(content, encoding="utf-8", newline="\n")


class SitePage(HTMLParser):
    """Collect link targets and explicit anchors from rendered HTML."""

    def __init__(self, content: str) -> None:
        super().__init__(convert_charrefs=True)
        self.targets: list[str] = []
        self.anchors: set[str] = set()
        self.canonical = ""
        self.feed(content)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "link" and attributes.get("rel") == "canonical":
            self.canonical = attributes.get("href") or ""
        for name, value in attrs:
            if value is not None:
                if name in {"href", "src"}:
                    self.targets.append(value)
                if name == "id" or (tag == "a" and name == "name"):
                    self.anchors.add(value)


def validate_site(site: Path, base_path: str | None = None) -> list[str]:
    """Check local rendered links, anchors, images, and the public-output boundary."""
    if site.is_symlink():
        return ["Unexpected site file: ."]
    if (site / "index.html").is_symlink():
        return ["Unexpected site file: index.html"]
    if not (site / "index.html").is_file():
        return [f"Missing site homepage: {site / 'index.html'}"]
    site = site.resolve()
    errors: list[str] = []
    pages: dict[Path, SitePage] = {}
    for path in sorted(site.rglob("*")):
        release_pdf = (
            path.parent == site / "pdfs" and PDF_ASSET.fullmatch(path.name) is not None
        )
        if path.is_symlink():
            errors.append(f"Unexpected site file: {path.relative_to(site)}")
            continue
        if (
            path.is_file()
            and path.suffix.lower() not in SITE_SUFFIXES
            and not release_pdf
        ):
            errors.append(f"Unexpected site file: {path.relative_to(site)}")
        if path.is_file() and path.suffix == ".html":
            pages[path] = SitePage(path.read_text(encoding="utf-8"))
    canonical = urlsplit(pages[site / "index.html"].canonical)
    if base_path is None:
        base_path = posixpath.dirname(unquote(canonical.path)).rstrip("/") + "/"
    for path, page in pages.items():
        for target in page.targets:
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                same_site = (
                    parsed.scheme in {"", canonical.scheme}
                    and parsed.netloc.casefold() == canonical.netloc.casefold()
                    and unquote(parsed.path).startswith(base_path)
                )
                if not same_site:
                    continue
            requested = unquote(parsed.path)
            if requested.startswith("/"):
                if not requested.startswith(base_path):
                    errors.append(
                        f"Link outside the site: {path.relative_to(site)}: {target}"
                    )
                    continue
                destination = (site / requested.removeprefix(base_path)).resolve()
            else:
                destination = (path.parent / requested).resolve() if requested else path
            if not destination.is_relative_to(site):
                errors.append(
                    f"Link outside the site: {path.relative_to(site)}: {target}"
                )
                continue
            if destination.is_dir():
                destination /= "index.html"
            if not destination.is_file():
                errors.append(
                    f"Missing site target: {path.relative_to(site)}: {target}"
                )
            elif (
                parsed.fragment
                and destination in pages
                and unquote(parsed.fragment) not in pages[destination].anchors
            ):
                errors.append(
                    f"Missing site anchor: {path.relative_to(site)}: {target}"
                )
    return errors


def build_site(root: Path, with_pdfs: bool = False) -> None:
    """Strictly build the staged site and fail on any rendered-link regression."""
    output = root / ".build/docs-site"
    if output.is_symlink() or output.parent.is_symlink():
        raise ValueError("Documentation build output must not be a symlink")
    with tempfile.TemporaryDirectory(prefix="unipd-docs-") as directory:
        stage = Path(directory)
        stage_documents(root, stage, with_pdfs=with_pdfs)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "mkdocs",
                "build",
                "--strict",
                "--config-file",
                str(root / "mkdocs.yml"),
                "--site-dir",
                str(output),
            ],
            cwd=root,
            check=True,
            env={
                **os.environ,
                "UNIPD_DOCS_DIR": str(stage),
                "PYTHONIOENCODING": "utf-8",
            },
        )
    errors = validate_site(output)
    if errors:
        raise ValueError(
            "Rendered documentation validation failed:\n  - " + "\n  - ".join(errors)
        )
    print(f"Built and checked documentation in {output.relative_to(root)}.")


def main() -> int:
    """Build documentation using the installed, pinned MkDocs environment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--with-pdfs",
        action="store_true",
        help="download the latest catalogued release PDFs for in-browser readers",
    )
    arguments = parser.parse_args()
    build_site(Path(__file__).resolve().parents[2], with_pdfs=arguments.with_pdfs)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
