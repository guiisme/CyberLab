# Legacy CLI

## Purpose

`cyberlab legacy` is a temporary compatibility boundary for the command-line
interface that predates the Typer composition root. It delegates to the old
`argparse` parser and the compatibility services in `cyberlab.legacy_services`.

The boundary exists so existing scripts can be migrated incrementally without
forcing a breaking release. It is not the extension point for new commands.

## When to use it

Use the legacy namespace only when an existing script still depends on the old
command names or positional arguments, for example:

```bash
uv run cyberlab legacy create-lab meu-lab
uv run cyberlab legacy exec meu-lab /bin/bash
uv run cyberlab legacy status meu-lab
```

New workflows must use the Typer commands:

```bash
uv run cyberlab lab create meu-lab
uv run cyberlab lab exec meu-lab
uv run cyberlab lab status meu-lab
```

The legacy parser does not automatically gain new features. In particular,
new template/profile options and the Docker interactive console belong to the
`lab` namespace.

## Removal policy

Removing this namespace requires an explicit breaking-change release. Until
then, changes to the legacy adapter should be limited to compatibility fixes;
new application behavior belongs in the Typer command layer and its shared
application/infrastructure contracts.
