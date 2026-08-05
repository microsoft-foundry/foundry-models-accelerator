# Contributing

Thanks for your interest in improving the Foundry Models Accelerator!

## How this repo is organized

This is a **consolidated** repository. Several folders started life in separate
community projects (see [`ATTRIBUTION.md`](./ATTRIBUTION.md)). When changing a
file, please:

1. Preserve any upstream attribution header at the top of the file.
2. If a fix is also upstream‑relevant, consider opening the same fix in the
   source repo so changes don't diverge.

## Local development

```bash
# Python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ruff check .
pytest -q

# PowerShell (requires PowerShell 7+)
pwsh -c 'Install-Module -Name PSScriptAnalyzer -Scope CurrentUser -Force'
pwsh -c 'Invoke-ScriptAnalyzer -Path ./tools/discovery -Recurse'
```

## Pull requests

- Keep changes focused — one concern per PR.
- Update docs alongside code when behavior changes.
- New target‑model content should appear as **sections inside** the existing
  per‑lifecycle docs, not as new top‑level docs. Add an entry to the API
  changes matrix in [`docs/05-api-changes-by-model.md`](./docs/05-api-changes-by-model.md).
- New evaluation scenarios go under `data/golden-datasets/` with a short
  description in [`data/golden-datasets/README.md`](./data/golden-datasets/README.md).

## CI

PRs run:

- `ruff` and `pytest` on Python files
- `PSScriptAnalyzer` on PowerShell files
- A markdown link checker on changed `.md` files

## Code of Conduct

This project follows the
[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For questions or concerns, contact [opencode@microsoft.com](mailto:opencode@microsoft.com).
