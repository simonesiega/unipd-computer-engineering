# Docker Builds

[← Documentation](../README.md) · [Installation](installation.md) · [Building documents](building-documents.md)

This guide explains how to compile and verify the repository's PDFs in the canonical Docker environment. Use it for final builds before committing generated files. For build-tool arguments and document selection, see [Building documents](building-documents.md).

## Why Docker is canonical

The repository commits each document's `main.pdf`, and CI compares rebuilt PDFs with those files byte for byte. A fixed `SOURCE_DATE_EPOCH` removes time-dependent variation, but different LuaLaTeX and package versions can still produce different bytes.

The root [`compose.yaml`](../../../compose.yaml) therefore defines one `texlive` service whose image is pinned by digest. Local Docker builds and GitHub Actions both use that service. The service uses a fixed `/workspace` mount, runs without network access, and selects the image's `linux/amd64` platform explicitly. Native TeX installations remain useful for editor previews, but they are not suitable for regenerating PDFs that will be committed.

## Prerequisites

Install Git and one of the following Docker setups:

- **Windows or macOS:** Docker Desktop with Docker Compose;
- **Linux:** Docker Engine with the Compose v2 plugin.

On Windows, Docker Desktop must be running in Linux-container mode. Confirm the installation from a terminal:

```bash
docker --version
docker compose version
docker info
```

Clone the repository if necessary, then run all commands below from its root:

```bash
git clone https://github.com/simonesiega/unipd-computer-engineering.git
cd unipd-computer-engineering
```

## Prepare the image

Pull the pinned image before the first build and whenever `compose.yaml` changes:

```bash
docker compose pull texlive
```

The `latest` tag lets Dependabot discover image updates, while the accompanying digest determines the exact immutable image that Docker runs. Docker reuses the downloaded image until that digest changes.

Check the tools provided by the container:

```bash
docker compose run --rm texlive python3 --version
docker compose run --rm texlive lualatex --version
docker compose run --rm texlive latexmk --version
docker compose run --rm texlive biber --version
```

Each command creates a temporary container and removes it afterward. The repository is bind-mounted at `/workspace`, so generated PDFs and `.build/` outputs remain available on the host.

## Build documents

Build one course, component example, or integration example by passing its directory:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py latex/components/diagrams/example
```

Build multiple explicit targets:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py 1/course-a 1/course-b
```

Build every discovered document:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py --all --keep-going
```

Build only documents affected since another Git revision:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py --changed-from origin/main --keep-going
```

A normal build publishes each generated `main.pdf` beside its `main.tex`. Course and integration builds also refresh generated README sections. Temporary compilation files are stored under `.build/`.

## Verify committed outputs

Run the same generated-file check used by CI:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py --all --keep-going --check-generated
```

This command compiles under `.build/` without replacing committed files. It fails if a selected PDF differs byte for byte or if a generated README section is missing or stale.

If it reports stale outputs, regenerate them in the same environment and verify again:

```bash
docker compose run --rm texlive \
  python3 latex/tools/build.py --all --keep-going

docker compose run --rm texlive \
  python3 latex/tools/build.py --all --keep-going --check-generated
```

Review the changed PDFs visually and commit the regenerated PDFs and README changes with their source changes.

## Platform notes

### Windows

Start Docker Desktop before running a build and keep it in Linux-container mode. The repository must be located in a drive or directory that Docker Desktop is allowed to share. Docker commands work in PowerShell, Command Prompt, and Git Bash when Docker is available on `PATH`.

The multiline examples use the POSIX-shell `\` continuation used by Git Bash, Linux, and macOS. In PowerShell, enter each command on one line or replace each trailing `\` with a backtick. In Command Prompt, enter each command on one line.

If Docker reports that it cannot connect to the daemon, wait for Docker Desktop to finish starting and rerun `docker info`.

### Linux

The container normally runs as `root`. If generated files become owned by `root`, remove the existing `.build/` directory or restore its ownership, then run subsequent builds with the host user and group:

```bash
docker compose run --rm --user "$(id -u):$(id -g)" texlive \
  python3 latex/tools/build.py --all --keep-going
```

If Docker requires elevated privileges, configure Docker's documented non-root access instead of adding `sudo` to repository commands permanently.

### macOS

Docker Desktop handles the bind mount automatically. Keep the repository in a directory shared with Docker Desktop if volume mounting is restricted in its settings.

The pinned TeX Live image currently publishes an AMD64 build. On Apple silicon, Docker Desktop runs it through platform emulation; the first build may therefore be slower than on an AMD64 host.

## Troubleshooting

### The Docker daemon is unavailable

Confirm that Docker Desktop or Docker Engine is running:

```bash
docker info
```

### The image cannot be pulled

Check network access to GitHub Container Registry, then retry:

```bash
docker compose pull texlive
```

Do not replace the pinned digest with an unpinned tag as a workaround.

### Repository files are missing in the container

Run commands from the repository root and confirm the mount:

```bash
docker compose run --rm texlive pwd
docker compose run --rm texlive ls
```

The first command must print `/workspace`, and the second must show the repository files.

### Generated PDFs are stale

Regenerate with a normal Docker build, inspect the changed files, and rerun `--check-generated`. Do not copy PDFs from a native MiKTeX, MacTeX, or TeX Live build into the commit.

### Remove temporary build files

The repository build tool stores temporary outputs under `.build/`. Delete that directory on the host when no build is running.

Linux, macOS, or Git Bash:

```bash
rm -rf .build
```

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .build
```

The build tool's `--clean` option can instead remove `.build/` automatically after a successful build.

## Updating the pinned environment

Treat a `compose.yaml` image-digest change as a repository-wide build change:

1. update the digest in `compose.yaml`;
2. pull the new image;
3. regenerate every document with `--all --keep-going`;
4. visually review the generated PDFs;
5. rerun `--all --keep-going --check-generated`;
6. run the repository validation workflow;
7. commit the Compose change and all affected generated files together.

The affected-document selector treats `compose.yaml` and the CI build workflow as shared infrastructure, so CI checks every document when the canonical environment or its automation changes.
