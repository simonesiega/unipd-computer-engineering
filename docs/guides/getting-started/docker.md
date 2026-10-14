# Docker Builds

[← Documentation](../README.md) · [Installation](installation.md) · [Building documents](building-documents.md) · [Build system](../development/build-system.md)

Docker provides the canonical TeX environment used for repository builds, generated-file verification, and release-equivalent output.

Use this guide for environment setup and Docker-specific troubleshooting. For normal build commands and contributor workflows, see [Building documents](building-documents.md).

## Why Docker is canonical

The repository uses the `texlive` service defined in [`compose.yaml`](../../../compose.yaml).

Its image is pinned by digest so local builds and GitHub Actions use the same TeX Live environment. This reduces differences caused by LuaLaTeX, package, font, and tool versions across machines.

The repository is mounted inside the container at:

```text
/workspace
```

The bind mount makes generated output available on the host. [Review the output](building-documents.md#review-the-output) explains which files a build creates or replaces.

The service has `network_mode: none`: install or pull dependencies before building. The container cannot fetch remote images, datasets, or packages during compilation.

For editor-only alternatives, see [Optional native TeX setup](installation.md#optional-native-tex-setup).

## Prerequisites

Install the tools listed in [Installation requirements](installation.md#requirements).

Confirm Docker is available:

```bash
docker --version
docker compose version
```

Run all repository commands from the project root.

## Prepare the environment

Pull the pinned TeX Live image before the first build and whenever `compose.yaml` changes:

```bash
docker compose pull texlive
```

You can verify the main tools inside the container with:

```bash
docker compose run --rm texlive python3 --version
docker compose run --rm texlive lualatex --version
docker compose run --rm texlive latexmk --version
docker compose run --rm texlive biber --version
```

Each command creates a temporary container and removes it when finished.

## Build with Docker

Use [Build a document](building-documents.md#build-a-document) for course, component, and integration commands, or [Build only changed documents](building-documents.md#build-only-changed-documents) for revision-based selection. The [build-system reference](../development/build-system.md#target-selection) owns option semantics.

## Verify generated state

Follow [Validate your changes](building-documents.md#validate-your-changes) for the canonical generated-state command and required follow-up checks.

## Platform notes

### Windows

Docker Desktop must be running in Linux-container mode.

The repository must be stored in a location Docker Desktop can access. Docker commands work from PowerShell, Command Prompt, or Git Bash when Docker is available on `PATH`.

Examples in this documentation use the POSIX `\` line continuation. In PowerShell, either run the command on one line or replace each trailing `\` with a backtick.

If the client cannot connect, follow [Docker is not running](#docker-is-not-running) after Docker Desktop starts.

### Linux

Docker may create files owned by `root`.

If needed, run builds using your host user and group:

```bash
docker compose run --rm \
  --user "$(id -u):$(id -g)" \
  texlive \
  python3 latex/tools/build.py --all --keep-going
```

Running the container as your user controls output-file ownership; permission to access the Docker daemon is a separate setting. Follow Docker's installation guidance for your system, and remember that membership in the `docker` group grants root-level privileges.

### macOS

Docker Desktop handles the repository bind mount automatically.

On Apple silicon, the pinned TeX Live image may run through AMD64 emulation, so the first build can be slower than on a native AMD64 host.

## Troubleshooting

### Docker is not running

Check the daemon:

```bash
docker info
```

Start Docker Desktop or Docker Engine if necessary.

### The image cannot be pulled

Retry the pull in [Prepare the environment](#prepare-the-environment). Do not replace the pinned digest with an unpinned image tag as a workaround.

### Repository files are missing

Confirm the working directory and mounted files:

```bash
docker compose run --rm texlive pwd
docker compose run --rm texlive ls
```

The first command should print:

```text
/workspace
```

The second should show the repository contents.

### Generated output is stale

Follow [generated-state verification](building-documents.md#validate-your-changes) for stale fixtures and [output ownership](building-documents.md#review-the-output) for files that may be replaced.

### Remove build output

Delete `.build/` when no build is running.

Linux, macOS, or Git Bash:

```bash
rm -rf .build
```

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .build
```

For automatic cleanup and its scope, see [`--clean` in the build options](../development/build-system.md#build-options). Review or save any PDFs you need before cleanup.

## Updating the pinned image

Changing the TeX Live image digest affects the whole repository.

After updating `compose.yaml`, pull the new image and follow the complete [build, PDF-review, and generated-state workflow](building-documents.md). An environment change selects the full archive under the [selection rules](../development/build-system.md#target-selection). Include its required tracked outputs in the same change, following [output ownership](building-documents.md#review-the-output).
