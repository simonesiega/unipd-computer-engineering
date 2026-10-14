# Documentation

[← Project README](../README.md) · [Guide index](guides/README.md)

This is the project-wide documentation router. Choose a topic below; each destination owns its detailed instructions. Folder READMEs provide local navigation rather than another copy of those instructions.

## Start here

| Task | Starting point |
|---|---|
| Read published notes or browse course archives | [Project README](../README.md#browse-the-notes) |
| Set up a local checkout | [Installation](guides/getting-started/installation.md) |
| Write, build, or maintain notes | [Guide index](guides/README.md) |
| Understand the shared source tree | [LaTeX overview](../latex/README.md) |
| Contribute or report a problem | [Contributing](../CONTRIBUTING.md) |

## Directory contents

| Area | Router or reference |
|---|---|
| Contributor guides | [Guide index](guides/README.md): setup, writing, class usage, and repository development |
| Shared LaTeX infrastructure | [LaTeX router](../latex/README.md): class, components, fonts, tools, and examples |
| Components and isolated examples | [Component router](../latex/components/README.md) |
| Bundled fonts | [Font router](../latex/fonts/README.md) |
| English and Italian integration examples | [Integration directories](../latex/LATEX.md#integration-examples) |
| Published editions | [Release archive](../RELEASES.md) |
| Committed course history | [Generated changelogs](../CHANGELOG/) |

## Source references

| Document | Owns |
|---|---|
| [LATEX.md](../latex/LATEX.md) | Physical structure of `latex/` and the purpose of its directories. |
| [COMPONENTS.md](../latex/components/COMPONENTS.md) | Component interfaces, dependencies, example design, and extension rules. |
| [FONTS.md](../latex/fonts/FONTS.md) | Individual font files, LaTeX mappings, and font maintenance. |
| [TOOLS.md](../latex/tools/TOOLS.md) | File-by-file Python tool index and links to each tool's workflow. |
| [TESTS.md](../latex/tools/test/TESTS.md) | Individual test explanations and test-running commands. |

## Policies and agent guidance

| Topic | Document |
|---|---|
| Contribution workflow and academic integrity | [Contributing](../CONTRIBUTING.md) |
| Community standards and conduct reporting | [Code of Conduct](../CODE_OF_CONDUCT.md) |
| Private vulnerability reporting | [Security](../SECURITY.md) |
| Project licensing and academic disclaimer | [Project README](../README.md#license) · [Academic disclaimer](../README.md#academic-disclaimer) |
| Font attribution and license text | [Font licences](../latex/fonts/FONT-LICENSE.md) |
| Human review and AI disclosure | [AI-assisted development](guides/development/ai-assisted-development.md) |
| Repository rules and specialized agent workflows | [AGENTS.md](../AGENTS.md) and its [skill routing table](../AGENTS.md#skill-routing) |

## Documentation assets

[`assets/`](assets/) contains presentation files, not course material or compiled notes. For course-owned figures, use the [course asset conventions](guides/user-guide/course-structure.md#assets).

| Asset | Used for |
|---|---|
| [`unipd.png`](assets/unipd.png) | Project README image and website logo. |
| [`notes/computer-engineering-notes-preview.png`](assets/notes/computer-engineering-notes-preview.png) | Notes preview in the project README. |
| [`site.css`](assets/site.css) | Website presentation overrides, maintained through the [site guide](guides/development/documentation-site.md#sources-and-publication-boundary). |

## Documentation site

Browse the [website](https://simonesiega.github.io/unipd-computer-engineering/) once Pages is enabled. [Documentation site](guides/development/documentation-site.md) owns local builds, previews, public-file boundaries, PDF readers, and deployment instructions; the Markdown linked here is the website's source, not a second documentation set.
