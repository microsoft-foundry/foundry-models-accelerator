#!/usr/bin/env bash
# Foundry Models Accelerator — Audit wrapper
#
# Thin wrapper around tools/audit/audit_codebase.py.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

python3 "${REPO_ROOT}/tools/audit/audit_codebase.py" "$@"
