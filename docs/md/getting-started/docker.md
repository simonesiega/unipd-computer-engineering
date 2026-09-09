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

Generated files remain available on the host under `.build/`.

Native TeX installations are useful for quick editor previews, but canonical review and release output should use Docker.

## Prerequisites

Install Git and Docker:

| Platform | Recommended setup |
|---|---|
| Windows | Docker Desktop with Linux containers |
| macOS | Docker Desktop |
| Linux | Docker Engine with the Compose v2 plugin |

Confirm Docker is available:

```bash
docker --version
docker compose version
docker info
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

Build one course:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py 1/course-name
```

Build every document:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py --all --keep-going
```

Build only documents affected since `origin/main`:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py \
    --changed-from origin/main \
    --keep-going
```

Generated PDFs are written under the mirrored `.build/` path.

For the full build workflow and available options, see [Building documents](building-documents.md) and [Build system](../development/build-system.md).

## Verify generated state

Run the canonical generated-file check:

```bash
docker compose run --rm --no-deps texlive \
  python3 latex/tools/build.py \
    --all \
    --keep-going \
    --check-generated
```

This verifies generated README sections and tracked component/integration fixtures.

Course PDFs remain under `.build/` and should be reviewed visually rather than committed.

## Platform notes

### Windows

Docker Desktop must be running in Linux-container mode.

The repository must be stored in a location Docker Desktop can access. Docker commands work from PowerShell, Command Prompt, or Git Bash when Docker is available on `PATH`.

Examples in this documentation use the POSIX `\` line continuation. In PowerShell, either run the command on one line or replace each trailing `\` with a backtick.

If Docker cannot connect to the daemon, confirm Docker Desktop has finished starting:

```bash
docker info
```

### Linux

Docker may create files owned by `root`.

If needed, run builds using your host user and group:

```bash
docker compose run --rm \
  --user "$(id -u):$(id -g)" \
  texlive \
  python3 latex/tools/build.py --all --keep-going
```

Prefer configuring normal non-root Docker access instead of permanently adding `sudo` to repository commands.

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

Retry:

```bash
docker compose pull texlive
```

Do not replace the pinned digest with an unpinned image tag as a workaround.

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

Run a normal canonical build, inspect the changed generated files, then rerun `--check-generated`.

Do not copy a course PDF from `.build/` into `1/`, `2/`, or `3/`.

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

You can also use the build tool's `--clean` option after a successful build.

## Updating the pinned image

Changing the TeX Live image digest affects the whole repository.

After updating `compose.yaml`:

1. pull the new image;
2. rebuild every document;
3. visually review generated PDFs;
4. rerun `--check-generated`;
5. run the repository validation pipeline;
6. commit the environment change and affected generated source-owned files, but no generated course PDF.

For repository-wide validation and CI behavior, see [Validation, tests, and CI](../development/tool-test-and-ci.md).
