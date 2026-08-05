# Discovery — Azure AI Deployments Scanner

> **Source:** Verbatim copy (with attribution header) of
> [`Get-AzureAIDeployments.ps1`](https://github.com/ElisaPiccin/azure-ai-deployment-scanner/blob/main/Get-AzureAIDeployments.ps1)
> by [Elisa Piccin](https://github.com/ElisaPiccin), used under the MIT License.
> See [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md).

> **⚠️ DISCLAIMER.** This script is **not an official Microsoft solution** and
> is **not supported** under any Microsoft support program. It is provided
> **as‑is**. Use at your own risk.

This is the **first step** in the accelerator lifecycle: inventory every model
deployment in your Azure tenant, enriched with retirement dates and recent
usage metrics, and write the results to an Excel (or CSV) workbook.

## What it does

- Scans every accessible subscription (or a specific one) for Azure OpenAI and
  Microsoft Foundry model deployments.
- Fetches the latest model **retirement schedule** from the official Microsoft
  docs and joins it with each deployment.
- Pulls Azure Monitor metrics — `AzureOpenAIRequests`, `ProcessedPromptTokens`,
  `GeneratedTokens` — for the last *N* days (default 7) so you can see which
  deployments are actually used.
- Saves results to a timestamped `deployments-results-v3-YYYYMMDD-HHMMSS.xlsx`
  (or `.csv`).

## Prerequisites

- Azure CLI 2.37+
- PowerShell 5.1+ (PowerShell 7 / `pwsh` recommended)
- The [`ImportExcel`](https://www.powershellgallery.com/packages/ImportExcel)
  module for Excel output (the script installs it automatically if needed).
- **Reader** permissions on the target subscription(s) — sufficient for
  scanning deployments and metrics.

## Quick start (Azure Cloud Shell — recommended)

1. Open [Azure Cloud Shell](https://shell.azure.com) and switch to PowerShell:
   `pwsh`.
2. Upload `Get-AzureAIDeployments.ps1` (Manage files → Upload).
3. Run it:

   ```powershell
   ./Get-AzureAIDeployments.ps1
   ```

4. Download the output file (Manage files → Download).

## Common invocations

```powershell
# Default — scan all accessible subscriptions, all deployments, last 7 days of metrics
./Get-AzureAIDeployments.ps1

# Just the current subscription, filter to gpt-4o
./Get-AzureAIDeployments.ps1 -CurrentSubscriptionOnly -ModelFilter "gpt-4o"

# Specific subscription + resource group, last 30 days
./Get-AzureAIDeployments.ps1 -SubscriptionId "<sub-id>" -ResourceGroupName "rg-aoai" -DaysBack 30

# CSV output, no metrics
./Get-AzureAIDeployments.ps1 -All -OutputFormat CSV -NoMetrics

# Full help
./Get-AzureAIDeployments.ps1 -Help
```

## Output columns

| Group | Columns |
|-------|---------|
| Identity | `SubscriptionId`, `SubscriptionName`, `ResourceGroup`, `Resource`, `Deployment` |
| Model | `Model`, `Version`, `Status`, `Sku`, `Capacity`, `Endpoint`, `Location`, `CreatedDate`, `VersionUpgradeOption` |
| Retirement (unless `-NoRetirementData`) | `RetirementDate`, `ReplacementModel` |
| Metrics (unless `-NoMetrics`) | `TotalRequests_<N>d`, `PromptTokens_<N>d`, `GeneratedTokens_<N>d` |

## Where this fits in the lifecycle

```
[ DISCOVER ]  ──▶  Assess  ──▶  Migrate  ──▶  Evaluate  ──▶  Roll out
   you are
   here
```

Once you have the inventory, feed it into the
[feasibility assessment](../../docs/03-feasibility-assessment.md) and the
[retirement timeline](../../docs/04-retirement-timeline.md) so each deployment
gets a target model and a migration priority.

## Optional deep discovery audit

For deeper operational triage, use the optional deep-audit companion in
[`deep-audit/`](./deep-audit/) and run it via
[`scripts/run_deep_audit.sh`](../../scripts/run_deep_audit.sh).

Choose the baseline scanner in this folder when you want broad inventory with
minimal setup. Choose deep audit when you need targeted model/version hunt,
retirement alert exports, optional diagnostics auto-enable, and Log Analytics
identity-level usage attribution.

## Demo GIFs

Demo recordings (`demo-start-cloudshell.gif`, `demo-download-output.gif`) live
upstream — see the
[original README](https://github.com/ElisaPiccin/azure-ai-deployment-scanner#readme).
They will be copied into [`media/`](./media/) when the upstream is folded in
via `git subtree`.
