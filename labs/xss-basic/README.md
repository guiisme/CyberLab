# Cross-Site Scripting Basics

## Overview

This lab runs a small Nginx-hosted search page with an intentionally unsafe DOM
sink. The value of the `q` query parameter is rendered using `innerHTML`.

## Objectives

- Identify the vulnerable DOM sink.
- Demonstrate reflected DOM XSS with a harmless proof of concept.
- Propose a remediation using safe DOM APIs.

## Learning Outcomes

- Recognize unsafe use of `innerHTML` with untrusted input.
- Validate the impact of client-side XSS.
- Apply output encoding or `textContent` as a mitigation.

## References

## Run the lab

From the repository root:

```bash
export CYBERLAB_HOME="$PWD"
uv run cyberlab lab run xss-basic
```

Open `http://localhost:8080/?q=hello` in a browser. The `q` value is
intentionally inserted with `innerHTML` for this exercise.

Check the target or run a shell command:

```bash
uv run cyberlab lab status xss-basic
uv run cyberlab lab exec xss-basic -c "id"
```

Stop the target when finished:

```bash
uv run cyberlab lab stop xss-basic
```
