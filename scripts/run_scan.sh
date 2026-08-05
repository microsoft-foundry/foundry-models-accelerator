#!/usr/bin/env bash
# Foundry Models Accelerator — Discovery wrapper
#
# Runs the upstream PowerShell scanner from tools/discovery/ with sensible
# defaults. Forwards any extra args you pass through.
#
# Requires: pwsh (PowerShell 7+) and Azure CLI, both already authenticated.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SCANNER="${REPO_ROOT}/tools/discovery/Get-AzureAIDeployments.ps1"

if ! command -v pwsh >/dev/null 2>&1; then
  echo "error: pwsh (PowerShell 7+) is required." >&2
  echo "       Install: https://learn.microsoft.com/powershell/scripting/install/" >&2
  exit 1
fi

pwsh -NoProfile -File "${SCANNER}" "$@"
