# Python Tool Test Catalogue

[← Tool index](../TOOLS.md) · [LaTeX structure](../../LATEX.md) · [Documentation](../../../docs/README.md)

This catalogue explains every `test_*` method in `latex/tools/test/`, grouped by source file. Each row describes one method; a method may cover several inputs through `subTest` cases. Fixture builders, setup helpers, and `unittest.main()` entry points are supporting code rather than separate tests.

The suite uses standard-library `unittest`, temporary directories and Git repositories, and mocked compilation/network calls. It does not compile LaTeX, run MkDocs, download published assets, or visually review PDFs. This catalogue describes assertions, not the outcome of a test run.

## Test files

| File | Main responsibility |
|---|---|
| [test_build_selection.py](#build-selection) | Build arguments, affected-document selection, strict compilation orchestration, and generated README behavior. |
| [test_changelog_generation.py](#changelog-generation) | Committed history, baselines, per-course changes, renames, and directory placeholders. |
| [test_course_creation.py](#course-creation) | Metadata validation, localized scaffolds, CLI behavior, cleanup, and cross-tool integration. |
| [test_documentation_site.py](#documentation-site) | Public staging, readers, published-PDF copying, link rewriting, and rendered-output validation. |
| [test_gitignore.py](#git-ignore-rules) | Local-context and generated-course-PDF ignore boundaries. |
| [test_notes_packaging.py](#notes-packaging) | Stable assets, release metadata, checksums, deterministic output, and staging safety. |
| [test_release_catalog.py](#release-catalogue) | Published-release parsing, coverage selection, recent releases, and archive updates. |
| [test_repository_validation.py](#repository-validation) | Course/shared layouts, metadata, tracked PDFs, source hygiene, and Markdown links. |

## Running tests

See [Installation](../../../docs/guides/getting-started/installation.md) for Python/Git versions and Windows launcher conventions. Run these commands from the repository root; they require neither Docker nor TeX. The coverage command additionally needs Coverage.py.

```bash
# All tests, without requiring Coverage.py or a TeX installation
python3 -m unittest discover -s latex/tools/test -p 'test_*.py'

# One file
python3 latex/tools/test/test_build_selection.py

# One method in that file
python3 latex/tools/test/test_build_selection.py BuildSelectionTests.test_course_change_selects_only_that_course

# Complete suite with branch coverage; requires Coverage.py
python3 latex/tools/run_tool_tests.py
```

The coverage runner enforces an aggregate minimum of 80% for production tools. A bare `unittest` run does not enforce coverage. The pinned pre-commit environment can provide the coverage dependency without installing it globally:

```bash
pre-commit run course-tool-tests --all-files --show-diff-on-failure
```

See [Validation, tests, and CI](../../../docs/guides/development/tool-test-and-ci.md) for environment setup, repository checks, and the separate strict MkDocs build.

## Build selection

Source: [test_build_selection.py](test_build_selection.py) · Class: `BuildSelectionTests`.

These tests exercise `build.py` with temporary sources, real temporary Git histories where needed, and mocked `latexmk` calls.

| Test | What it checks |
|---|---|
| `test_build_argument_validation_rejects_conflicting_modes` | Rejects incompatible generated-check flags, missing selection modes, and simultaneous explicit targets/`--all`. |
| `test_keep_going_collects_partial_build_failures` | Records a failed document while continuing to process the next target. |
| `test_build_main_cleans_outputs_after_success` | Removes `.build/` after a successful run with `--clean`. |
| `test_build_main_reports_failures_and_empty_selection` | Returns failure and reports failed targets; rejects an explicit selection that discovers no documents. |
| `test_changed_file_selection_can_be_a_valid_no_op` | Returns the no-op selection when a changed-file list contains only an unrelated README. |
| `test_changed_selection_includes_both_courses_after_an_input_moves` | Selects both old and new course owners after an input moves, using either Git revisions or a NUL-delimited file list. |
| `test_git_and_file_list_preserve_accented_and_spaced_paths` | Preserves accented characters and spaces in Git/file-list paths and maps them to the correct course. |
| `test_changed_file_list_preserves_newlines_inside_paths` | Keeps embedded newlines inside NUL-delimited paths and accepts an empty list. |
| `test_changed_file_list_rejects_legacy_or_truncated_records` | Rejects newline-delimited legacy input and an unterminated final record. |
| `test_reference_warning_failure_preserves_published_outputs` | Uses strict `latexmk` warning handling and leaves existing course/component PDFs and README content unchanged after failure. |
| `test_successful_strict_build_keeps_course_pdf_in_build_directory` | Requires strict compilation and retains course PDFs under `.build/`, including generated-state checks, without copying them beside sources. |
| `test_document_discovery_finds_courses_and_component_examples` | Discovers course, component-example, and integration entry points. |
| `test_explicit_document_must_remain_inside_repository` | Rejects an explicit target outside the repository. |
| `test_course_change_selects_only_that_course` | Maps a course-section edit to its owning course only. |
| `test_shared_changes_select_every_document` | Selects all documents for shared environment, workflow, build-helper, class, package, or font changes. |
| `test_component_change_selects_only_its_example` | Selects only the owning component example for an example-source edit. |
| `test_unrelated_change_selects_no_documents` | Leaves the affected-document set empty for an unrelated root README edit. |
| `test_generated_readme_uses_document_language` | Renders English/Italian PDF labels, contents headings, entries, and empty-state text. |
| `test_document_language_ignores_commented_class_declarations` | Detects the active class language rather than a commented-out declaration. |
| `test_toc_parser_handles_nested_formatting_and_ignores_unknown_levels` | Converts nested formatting and escaped title characters into contents text while ignoring unsupported heading levels. |
| `test_generated_file_comparison_detects_missing_and_stale_outputs` | Distinguishes missing, stale, and byte-identical generated fixtures. |
| `test_integration_build_generates_localized_readme` | Uses existing synthetic build output to generate correctly localized integration README contents in both languages. |
| `test_no_compile_preserves_readme_when_toc_is_missing` | Fails without changing an existing README when reused build output lacks its `.toc`. |
| `test_course_readme_links_to_rolling_release_asset` | Generates the stable rolling-release URL, reads optional identifiers from the preamble only, and avoids a source-adjacent course PDF. |
| `test_integration_change_selects_its_document` | Maps an integration-source edit to its own document. |

## Changelog generation

Source: [test_changelog_generation.py](test_changelog_generation.py) · Class: `ChangelogGenerationTests`.

These tests exercise Git-history parsing and generated course histories, including real commits in temporary repositories.

| Test | What it checks |
|---|---|
| `test_real_git_history_is_read_newest_first` | Reads actual commits in newest-first order with the expected changed-file status and path. |
| `test_history_can_start_after_a_baseline_commit` | Excludes the baseline commit and older history. |
| `test_reset_baseline_records_head_and_can_be_read` | Writes the current `HEAD` to `CHANGELOG/BASELINE` and reads it back. |
| `test_shallow_repository_is_rejected_before_reading_history` | Refuses incomplete history before attempting changelog generation. |
| `test_history_is_split_by_course_and_includes_every_changed_file` | Groups commits by course, retains all relevant files, and renders date groups, statuses, and commit links. |
| `test_rename_is_recorded_in_both_course_histories` | Attributes a cross-course rename to both its old and new course. |
| `test_required_empty_directories_are_preserved` | Creates `.gitkeep` placeholders for course years and changelog directories even with no history. |

## Course creation

Source: [test_course_creation.py](test_course_creation.py) · Class: `CourseCreationTests`.

These tests cover generator input, localized scaffolds, and interoperability. The cross-tool test uses synthetic PDFs and contents data, not actual TeX compilation.

| Test | What it checks |
|---|---|
| `test_kebab_case_normalizes_names` | Normalizes spacing and accented course names to stable kebab-case slugs. |
| `test_latex_metadata_characters_are_escaped` | Escapes LaTeX special characters while preserving ordinary Unicode text. |
| `test_author_names_reject_blank_and_known_placeholders` | Trims real author names and rejects blank or known placeholder values. |
| `test_optional_course_identifiers_are_validated` | Accepts supported course-code/channel forms and rejects malformed alternatives. |
| `test_course_start_dates_are_validated_and_localized` | Validates real ISO dates and renders Italian/English course-start labels. |
| `test_cli_help_identifies_date_as_the_course_start_date` | Makes the `--date` meaning explicit in actual CLI help. |
| `test_academic_year_follows_degree_year` | Maps the three degree years to their cohort-consistent academic years. |
| `test_standard_layout_and_metadata_are_created` | Creates the Italian scaffold, required directories/placeholders, explicit metadata, and document lifecycle commands. |
| `test_english_course_scaffold_is_localized` | Creates English document/README text and empty optional identifiers. |
| `test_new_courses_integrate_without_registration_for_all_supported_metadata` | Exercises all year/semester/language combinations through validation, discovery, affected-file selection, README generation, release links, and packaging. |
| `test_partial_course_is_removed_when_scaffolding_fails` | Removes the newly created course directory after a simulated README write failure. |
| `test_cli_main_creates_course_with_explicit_author` | Creates courses through CLI parsing, preserves explicit author/date/identifiers, supports omitted identifiers, and prints the next canonical build command. |
| `test_duplicate_slug_is_rejected_across_years` | Rejects a course slug already present in another degree year. |
| `test_invalid_course_values_are_rejected` | Rejects unsupported year/semester/language values, placeholder authors, and invalid CLI date/language input. |

## Documentation site

Source: [test_documentation_site.py](test_documentation_site.py) · Class: `DocumentationSiteTests`.

These tests use temporary public-source fixtures and synthetic HTML. MkDocs subprocesses and download responses are mocked; separate site builds check actual rendered output.

| Test | What it checks |
|---|---|
| `test_stage_excludes_private_state_sources_fonts_and_pdfs` | Stages public course/license/asset/index pages without copying private state, font binaries, or source-adjacent course PDFs. |
| `test_latex_structure_tools_and_test_catalogues_are_public_pages` | Stages the LaTeX landing page and scoped component/font/tool/test references, keeps their index links local and original sources unchanged, routes test-source links to GitHub, and excludes unlisted tooling files. |
| `test_nested_private_directories_are_not_published` | Prunes excluded local/private directories even when nested inside otherwise public trees. |
| `test_long_fences_preserve_nested_examples_and_resume_prose` | Leaves nested fenced examples literal and resumes link rewriting only after a valid closing fence. |
| `test_links_resolve_to_staged_pages_or_github_sources` | Rewrites Markdown/HTML links to local public pages or GitHub implementations while preserving remote links, literal fenced examples, and source content. |
| `test_reader_routes_and_unpublished_courses` | Generates stable reader routes, source links, and an unpublished-course message without an iframe. |
| `test_readers_cover_all_years_and_escape_course_metadata` | Creates readers/year-index links for later years and escapes special characters in course titles. |
| `test_latest_pdf_follows_catalogue_order_not_rolling_tag_preference` | Selects the newest catalogued matching PDF rather than always preferring `notes-latest`. |
| `test_reader_without_downloads_links_to_release_but_does_not_embed` | Keeps the default build network-free, with release links and no local PDF directory or iframe. |
| `test_online_reader_embeds_an_unchanged_same_origin_release_copy` | Copies exact mocked release bytes, embeds a same-origin PDF, and supplies new-tab/download actions without a source-adjacent PDF. |
| `test_reader_route_collisions_fail_without_overwriting_guides` | Rejects a reader route that conflicts with the documentation directory without replacing guides. |
| `test_year_index_routes_cannot_be_used_by_course_readers` | Reserves all degree-year index routes against course-reader collisions. |
| `test_catalogue_rejects_untrusted_or_malformed_pdf_urls` | Rejects foreign hosts, non-release locations, query-bearing URLs, and traversal-like release tags. |
| `test_pdf_download_errors_and_non_pdf_responses_are_not_hidden` | Rejects non-PDF response headers and propagates download errors. |
| `test_complete_pdf_downloads_keep_exact_bytes_and_leave_no_temporary_file` | Accepts a complete advertised-length PDF, preserves its exact bytes including trailing whitespace, and removes temporary output. |
| `test_incomplete_pdf_downloads_preserve_existing_copies` | Rejects partial HTTP status, length mismatches, and missing end markers while preserving an existing destination. |
| `test_interrupted_pdf_copy_cleans_up_partial_output` | Removes partial temporary output after an interrupted copy. |
| `test_rendered_validation_allows_only_named_release_pdf_copies` | Accepts canonical named PDFs under `pdfs/` but rejects an arbitrary PDF elsewhere in site output. |
| `test_cli_enables_pdf_downloads_only_when_requested` | Enables PDF copying only when the CLI receives `--with-pdfs`. |
| `test_public_aliases_keep_original_source_relative_links` | Publishes hidden policy/skill files through public aliases while resolving links from their original locations and preserving originals. |
| `test_unpublished_local_builds_are_not_linked_as_site_assets` | Rejects a page link into private local context instead of publishing that material. |
| `test_unexpected_assets_and_missing_links_fail` | Rejects unsupported asset files and missing repository-relative targets. |
| `test_course_index_discovers_years_and_escapes_names` | Builds cohort/year labels and reader/source links, escapes Markdown-sensitive names, and handles empty years without inferring coverage. |
| `test_private_and_traversing_public_inputs_are_rejected` | Rejects direct staging inputs in private directories or outside the repository through `..`. |
| `test_symlinked_parent_is_rejected` | Rejects a public input reached through a symlinked parent directory. |
| `test_missing_public_file_and_symlinked_tree_are_rejected` | Rejects missing required public files and symlinked documentation-tree roots. |
| `test_link_traversal_outside_repository_is_rejected` | Rejects a repository-relative link that escapes the repository. |
| `test_built_links_queries_images_and_anchors_pass` | Accepts valid synthetic HTML links, query strings, images, fragments, and remote targets. |
| `test_project_site_root_urls_resolve_without_escaping_output` | Validates root-relative, absolute, and protocol-relative same-site links and anchors under the canonical project prefix; ignores external projects and rejects escaping root-relative paths. |
| `test_built_missing_targets_anchors_and_traversal_fail` | Reports separate errors for missing rendered targets, absent fragments, and links outside the output tree. |
| `test_missing_build_and_unexpected_public_files_fail` | Rejects a missing homepage and an implementation file leaked into site output. |
| `test_rendered_symlinks_are_rejected_without_reading_them` | Rejects symlinked output roots, homepages, and HTML files before reading their contents. |
| `test_build_uses_strict_mkdocs_and_validates_output` | Invokes strict MkDocs with checked subprocess status and a temporary allowlisted `UNIPD_DOCS_DIR`, then validates output. |
| `test_build_failures_and_symlinked_output_are_not_hidden` | Propagates MkDocs failures, rejects missing rendered homepages, and refuses symlinked output parents. |
| `test_site_dependency_pins_match_the_precommit_hook` | Keeps documentation requirements aligned with the pre-commit hook's dependency pins. |
| `test_github_urls_quote_spaces_and_directory_paths` | Quotes source paths with spaces, distinguishes GitHub file/directory URLs, and maps README routes to `index.html`. |

## Git ignore rules

Source: [test_gitignore.py](test_gitignore.py) · Class: `GitignoreTests`.

This test applies the repository's actual ignore rules inside a temporary Git repository.

| Test | What it checks |
|---|---|
| `test_local_context_and_only_generated_course_main_pdfs_are_ignored` | Ignores `.context/` and generated course `main.pdf` files in all three years, but not reference PDFs or component PDF fixtures. |

## Notes packaging

Source: [test_notes_packaging.py](test_notes_packaging.py) · Class: `NotesPackagingTests`.

These tests use synthetic compiled bytes to check packaging and output ownership, not PDF content validity.

| Test | What it checks |
|---|---|
| `test_slug_and_asset_names_are_url_safe_and_stable` | Produces stable normalized slugs/asset names and rejects invalid slugs or degree years. |
| `test_course_metadata_ignores_comments_and_preserves_escaped_percent` | Ignores commented setup blocks while retaining an escaped percent sign in active metadata. |
| `test_packaging_rejects_missing_or_malformed_course_metadata` | Rejects missing, unclosed, or empty course-name metadata. |
| `test_release_timestamp_must_be_an_iso_datetime_with_offset` | Accepts a trimmed offset-aware ISO timestamp and rejects blank, date-only, naive, or malformed values. |
| `test_manifest_checksums_and_ordering_are_deterministic` | Produces byte-identical reruns with deterministic course order, manifest provenance/size/hash fields, sorted checksums, and release-note content. |
| `test_cli_main_packages_description_and_explicit_release_metadata` | Packages through the CLI entry point with explicit provenance/title and a repository-relative description file. |
| `test_missing_compiled_pdf_fails_without_partial_assets` | Clears stale staging and fails on a missing compiled PDF without leaving partial release assets. |
| `test_invalid_course_paths_are_rejected` | Rejects course entry points nested below the supported direct course layout. |
| `test_duplicate_asset_names_are_rejected_without_overwrite` | Detects colliding release filenames before writing a conflicting asset. |
| `test_output_outside_owned_release_staging_is_rejected` | Refuses to clean an output directory outside `.build/release/` and preserves its existing content. |
| `test_empty_course_archive_generates_metadata_assets` | Produces an empty manifest, explanatory release notes, and checksums when no courses exist. |

## Release catalogue

Source: [test_release_catalog.py](test_release_catalog.py) · Class: `ReleaseCatalogTests`.

These tests use prepared JSON-like release records; they do not query GitHub or approve real exam coverage. Snapshot classification follows the catalogue's release policy, not GitHub's immutable-release setting.

| Test | What it checks |
|---|---|
| `test_parser_handles_slurped_pages_and_ignores_drafts_and_non_course_assets` | Flattens paginated/slurped release input and ignores draft releases and non-course assets. |
| `test_parser_rejects_non_array_release_and_asset_data` | Rejects non-array release input and non-array asset collections. |
| `test_only_immutable_snapshots_cover_exams_and_duplicates_are_removed` | Excludes rolling releases from coverage, deduplicates courses across snapshots, and selects the newest snapshot asset. |
| `test_catalog_contains_counts_courses_and_recent_published_releases` | Renders snapshot-derived counts and course names while retaining published rolling releases in the newest-first releases table. |
| `test_empty_catalog_and_atomic_readme_update` | Renders empty states, preserves manual README text around the generated block, and makes an unchanged rerun a no-op. |
| `test_recent_releases_and_complete_archive_share_rows` | Limits the README to five recent releases, retains all archive entries, shares row formatting, and supports changed/unchanged/empty archive updates. |

## Repository validation

Source: [test_repository_validation.py](test_repository_validation.py) · Class: `RepositoryValidationTests`.

These tests construct valid and invalid source/layout fixtures and inspect the validator's diagnostics and exit status.

| Test | What it checks |
|---|---|
| `test_valid_course_entry_point_passes` | Accepts a complete course entry point with valid metadata and ordered README markers. |
| `test_source_only_course_has_no_tracked_pdf_error` | Accepts a source-only course and an index containing no generated course PDF. |
| `test_tracked_generated_course_pdf_is_rejected_with_removal_guidance` | Rejects an indexed course PDF and provides local-build, release-download, and index-removal guidance. |
| `test_invalid_course_location_and_incomplete_document_are_reported` | Reports nested entry points, missing class/document structure, and invalid directory names. |
| `test_optional_course_code_and_channel_formats_are_validated` | Reports malformed optional identifiers. |
| `test_generated_latex_escapes_are_valid_metadata_values` | Accepts escaped punctuation and nested LaTeX metadata commands produced by the generator. |
| `test_course_metadata_and_readme_requirements_are_reported` | Reports conflicting languages, missing/empty fields, placeholder authors, inconsistent year/semester metadata, and malformed README markers. |
| `test_course_requires_readme_setup_and_supported_class` | Requires the shared class, a pre-document setup block, and a course README. |
| `test_repository_main_reports_partial_course_structures` | Returns failure and useful diagnostics for a year path that is a file and a course directory missing `main.tex`. |
| `test_repository_main_accepts_empty_archive_with_valid_shared_layout` | Accepts an empty course archive with mocked valid shared layout while ignoring invalid/private context files. |
| `test_local_environments_are_ignored_but_new_sources_are_checked` | Prunes local environments/caches/editors but still validates new unstaged course sources and Markdown. |
| `test_component_validation_requires_exact_package_and_example_layout` | Accepts the standard component layout and rejects invalid names or extra example files. |
| `test_integration_projects_require_source_pdf_and_readme` | Requires both language examples, their expected files, and no extra integration output. |
| `test_markdown_link_validation_reports_missing_local_targets` | Accepts valid local/external links and reports missing files/fragments with source line numbers. |
| `test_markdown_anchor_generation_handles_duplicates_and_fences` | Generates punctuation-normalized and duplicate-suffixed heading anchors while ignoring fenced examples. |
| `test_source_hygiene_errors_are_reported` | Reports CRLF, missing final newline, conflict markers, tabs, and trailing whitespace. |

## Maintaining this catalogue

When adding, renaming, or removing a test method, update its row in the corresponding file section. Describe the observable assertion rather than just expanding the method name. Keep fixture helpers out of the test list, and do not treat mocked output or passing unit tests as compilation, academic review, visual sign-off, or deployment evidence.
