#!/usr/bin/env bash
# Foundry Models Accelerator -- Deep discovery audit wrapper
#
# Runs the optional deep-audit upstream script from:
#   tools/discovery/deep-audit/_upstream/foundry_model_audit.py
#
# This wrapper keeps deep audit optional and separate from the baseline
# PowerShell scanner in tools/discovery/Get-AzureAIDeployments.ps1.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEEP_AUDIT_SCRIPT="${REPO_ROOT}/tools/discovery/deep-audit/_upstream/foundry_model_audit.py"

if ! command -v python3 >/dev/null 2>&1; then
  if ! command -v python >/dev/null 2>&1; then
    echo "error: python3 or python is required." >&2
    exit 1
  fi
  PYTHON_BIN="python"
else
  PYTHON_BIN="python3"
fi

if [[ ! -f "${DEEP_AUDIT_SCRIPT}" ]]; then
  echo "error: deep-audit upstream script not found:" >&2
  echo "       ${DEEP_AUDIT_SCRIPT}" >&2
  echo >&2
  echo "Initialize it first (recommended via git subtree):" >&2
  echo "  git remote add foundry-model-audit https://github.com/anishek-microsoft/foundry_model_audit.git" >&2
  echo "  git subtree add --prefix=tools/discovery/deep-audit/_upstream foundry-model-audit main --squash" >&2
  exit 1
fi

"${PYTHON_BIN}" "${DEEP_AUDIT_SCRIPT}" "$@"
