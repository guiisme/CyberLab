#!/usr/bin/env bash

set -euo pipefail

LABS=(
  "sqli-basic"
  "idor-basic"
  "csrf-basic"
  "command-injection"
  "file-upload"
  "ssrf-basic"
  "jwt-basic"
  "xxe-basic"
  "ssti-basic"
)

ROOT="labs"

for LAB in "${LABS[@]}"; do
    echo "Creating ${ROOT}/${LAB}..."

    mkdir -p \
        "${ROOT}/${LAB}/application" \
        "${ROOT}/${LAB}/scripts" \
        "${ROOT}/${LAB}/seed"

    touch \
        "${ROOT}/${LAB}/lab.yaml" \
        "${ROOT}/${LAB}/README.md" \
        "${ROOT}/${LAB}/compose.yaml"
done

echo
echo "✅ Laboratory template structure created successfully."
