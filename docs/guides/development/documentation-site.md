# Documentation Site

[← Documentation](../README.md) · [Architecture](architecture.md) · [Validation, tests, and CI](tool-test-and-ci.md)

The site uses MkDocs Material and GitHub Pages, the same documentation stack as [European Tech Opportunities](https://github.com/simonesiega/european-tech-opportunities-2027). It renders this repository's Markdown rather than maintaining a second set of guides.

The configured address is **https://simonesiega.github.io/unipd-computer-engineering/**.

## What readers get

- Searchable setup, writing, LaTeX, development, and policy guides.
- A course index for all three degree years, with source contents and dedicated PDF-reader pages.
- The existing published-release catalogue and archive, with direct PDF-download links.
- Course changelogs, agent instructions, and component references.
- Light/dark modes and copy buttons for commands.

GitHub Releases remains the canonical PDF distribution. The site build copies the latest catalogued PDF for each course into disposable website output for inline viewing; it never compiles notes, commits PDF bytes, or changes covered-exam status. A course's source contents can be newer than its published PDF.

## Build and review locally

From the repository root, use the [validation environment](../getting-started/installation.md#install-validation-dependencies), then install the site dependencies:

```bash
python -m pip install -r .github/requirements-docs.txt
python latex/tools/build_docs.py --with-pdfs
```

`--with-pdfs` downloads the latest published course PDFs and includes their browser viewers, just like the documentation workflow. Omit it for a network-free documentation check: course pages keep their release-download links but explain that the embedded copy is omitted.

If GNU Make is installed, `make docs` is the documentation-only shortcut; use `make docs PYTHON=python` to select the activated environment's launcher. Use the Python command above for the full PDF-enabled preview.

The command stages public inputs in a temporary directory, builds with `mkdocs build --strict`, and checks the rendered HTML for missing local links, images, and anchors. Output stays under `.build/docs-site/`; no authored or generated repository Markdown is rewritten.

Preview the result:

```bash
python -m http.server 8000 --bind 127.0.0.1 --directory .build/docs-site
```

Open **http://127.0.0.1:8000/**. Check the home page, PDF links, course pages, navigation, search, code blocks, and tables on desktop and mobile, in both themes. Stop the server with Ctrl+C. This serves the completed build, not a live source watcher: rebuild after editing Markdown or CSS.

The pre-commit `documentation-site` hook uses the same pinned MkDocs versions without installing them into your host environment:

```bash
pre-commit run documentation-site --all-files --show-diff-on-failure
```

On Windows, use the activated environment's `python`, or its full interpreter path if PowerShell activation is blocked. No TeX installation is needed for the site.

## Course PDF readers

A course source such as `1/analisi-matematica-1/` gets a reader at **`/unipd-computer-engineering/analisi-matematica-1/`**. The degree-year prefix stays in the PDF filename (`1-analisi-matematica-1.pdf`) but not in the reader URL. Course indexes link to both the reader and the original source contents; adding a course needs no hand-written viewer page.

The builder chooses the first matching asset in the tool-owned, newest-first `RELEASES.md` archive. That can be `notes-latest` or a snapshot, depending on which is newer in the catalogue. It does not assume the rolling release exists or prefer an older rolling PDF over a newer snapshot. Unpublished courses get an explanatory page instead of a broken viewer. Conflicting reader routes stop the build rather than overwriting another course or guide.

GitHub release assets are served as attachments, so embedding their download URL does not reliably display a PDF. With `--with-pdfs`, the builder downloads only canonical PDF assets from this repository's release catalogue into temporary `pdfs/` files, checks the HTTP status, advertised length, PDF header, and end marker, and copies the bytes unchanged into `.build/docs-site/pdfs/`. Pages serves these same-origin copies to the browser's native PDF viewer. Open-in-new-tab and download buttons remain available when inline viewing is unsupported, particularly on mobile. Content-hash query strings avoid reusing a cached older PDF after a new site deployment.

PDF selection reflects the catalogue at the last successful site deployment, not live source edits. Publication-triggered refreshes update the copies after the catalogue changes. A missing asset, failed download, or non-PDF response fails the PDF-enabled build; it never silently substitutes an older PDF. No course `main.pdf` or local `.build/` compilation is used as a substitute.

## Sources and publication boundary

| Input | Handling |
|---|---|
| Root README and release archive | Rendered with their existing catalogue and download links |
| `docs/guides/` and documentation assets | Published from the same sources used on GitHub |
| Course README files and metadata | Discovered automatically; source pages and slug-based PDF readers need no per-course registration |
| Shared LaTeX README files, structure/tool/test indexes, and font-license notice | Published as reference pages |
| Root policies, licenses, agent skills, pull-request template, and changelogs | Published as supporting documentation |
| LaTeX implementations, examples, fonts, workflows, and other source links | Link to their GitHub location instead of copying implementation files |
| Canonical published release PDFs | Downloaded only with `--with-pdfs`; disposable website copies stay outside Git history |
| `.context/`, local environments/caches, `.build/` inputs, and source-adjacent course PDFs | Never copied into the site |

`latex/tools/build_docs.py` owns staging, generated course/history indexes, and rendered checks. It preserves repository-relative paths where possible, adapting links only in temporary copies. License text is wrapped for display without changing its source. Hidden agent paths and the pull-request template receive public site paths so the Pages upload does not omit them.

Never set MkDocs `docs_dir` to the repository root. The wrapper supplies `UNIPD_DOCS_DIR` to the allowlisted temporary tree; running MkDocs directly bypasses this boundary. Symlinked public inputs and unexpected documentation assets stop the build.

`mkdocs.yml` owns navigation, appearance, and the site address. `docs/assets/site.css` holds the small UniPD color and responsive-image overrides. Built HTML, search indexes, and generated course lists must not be committed.

When adding or moving a guide, update the source index, inbound links, and MkDocs navigation. New courses and changelogs are discovered automatically. To update MkDocs versions, keep `.github/requirements-docs.txt` and the pre-commit hook dependencies aligned.

## Enable GitHub Pages

A maintainer must:

1. Merge the reviewed site sources into `main`.
2. In **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source.
3. Check the `github-pages` environment rules and allow deployment from `main`.
4. Run **Actions → Documentation site → Run workflow** on `main`, or use the next normal push.
5. Confirm the deployment URL, assets, search, and PDF links on the live site.

No custom domain, DNS change, analytics, or extra secret is required. If a custom domain is added later, review Pages/DNS settings and `site_url` together.

The documentation workflow's build job has `contents: read` and `pages: read`; the deployment job has `pages: write` and `id-token: write`. It builds and checks every pull request, but only trusted `main` runs deploy. Pull-request builds are downloadable as `documentation-site-<commit-sha>` artifacts, retained for 14 days. Extract the artifact and serve it with a local HTTP server for review.

Release-catalogue and changelog commits use `[skip ci]`. Successful runs of **Publish compiled notes** and **Course changelogs** therefore also trigger a site refresh via `workflow_run`, always checking out the updated `main` branch. This includes snapshots dispatched from another ref, because publication still updates the catalogue on `main`. This refresh does not create GitHub Releases or modify either catalogue; it republishes the site with updated PDF copies. A manual documentation run can refresh the site after another intentionally skipped commit.

## Limits of the checks

The rendered validator checks local targets and anchors, including PDF iframe sources and absolute links under the site's canonical address. Links to external sites or other projects are not fetched. Documentation-only builds use the committed catalogue without network access once dependencies are installed; PDF-enabled builds additionally require the selected release assets to be reachable. Download-integrity checks are not a PDF-content or layout review. A passing build does not establish academic correctness, PDF quality, browser support for inline viewing, or a successful live deployment.
