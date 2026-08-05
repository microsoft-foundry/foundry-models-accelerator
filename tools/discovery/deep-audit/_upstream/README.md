# Azure OpenAI / Foundry Deployment Audit

Python script for automatic auditing of Azure OpenAI and Foundry (Azure AI Services) deployments in a subscription, with the ability to search for specific models and versions, analyze usage, and flag upcoming retirements.

## 📋 Requirements

- **Azure CLI** - installed and configured (`az login`)
- **Python** 3.11+
- **Azure Permissions**:
  - `Reader` on subscription (for listing resources)
  - `Monitoring Reader` (for reading Azure Monitor metrics)
  - `Log Analytics Reader` (optional, for reading logs from Log Analytics)

Notes:
- There are no pip dependencies. Azure CLI is a separate install (not in requirements.txt).
- Install Azure CLI: https://learn.microsoft.com/cli/azure/install-azure-cli

## 🚀 Basic Usage

```bash
# Audit with default settings
python .\foundry_model_audit.py

# Switch default subscription (Azure CLI) then run
az account set --subscription "<subscription-id>"
python .\foundry_model_audit.py

# Audit with diagnostic settings enabled
python .\foundry_model_audit.py --enable-diag --diag-workspace-id "/subscriptions/.../resourceGroups/.../providers/Microsoft.OperationalInsights/workspaces/..."

# Audit for a specific subscription
python .\foundry_model_audit.py --subscription-id "12345678-1234-1234-1234-123456789abc"

# Search for custom models and versions (JSON string)
python .\foundry_model_audit.py --target-models "[{\"ModelName\":\"gpt-4\",\"Versions\":[\"1106-preview\",\"0613\"]},{\"ModelName\":\"gpt-35-turbo\",\"Versions\":[\"0301\"]}]"

# Search for custom models and versions (JSON file)
python .\foundry_model_audit.py --target-models .\target-models.json

# Include only specific account kinds (default: OpenAI,AIServices)
python .\foundry_model_audit.py --account-kinds "OpenAI,AIServices"
```

## 📊 What does the script do?

1. **Scans Azure OpenAI and Foundry accounts** in the subscription
2. **Lists all deployments** from each account
3. **Identifies searched models** according to the `TargetModels` parameter
4. **Retrieves usage metrics** (last 7 days) from Azure Monitor:
   - Number of API calls
   - Processed tokens (prompt tokens)
   - Generated tokens (completion tokens)
5. **Optionally retrieves detailed logs** from Log Analytics workspace (if configured)
6. **Generates model retirement alerts** using official retirement timelines

Retirement timelines are stored in model_retirements.json to allow updates without changing code.

## 🎯 Parameters

| Parameter | Default Value | Description |
|----------|------------------|------|
| `--subscription-id` | Current subscription | Azure subscription ID to scan |
| `--out-dir` | `./foundry-audit-[timestamp]` | Output directory for reports |
| `--enable-diag` | `false` | Enable automatic configuration of diagnostic settings |
| `--diag-workspace-id` | - | Log Analytics workspace resource ID (required when `--enable-diag` is set) |
| `--diag-name` | `openai-to-la` | Diagnostic setting name |
| `--target-models` | - | JSON string or path to JSON file |
| `--account-kinds` | `OpenAI,AIServices` | Comma-separated resource kinds to include |

### Default values for `TargetModels`

```json
[
  {"ModelName":"gpt-4o","Versions":["2025-08-06","2025-05-13"]},
  {"ModelName":"gpt-4o-mini","Versions":["2024-07-18"]}
]
```

## 📁 Output Files

The script creates a directory with a timestamp (e.g., `foundry-audit-20260120-143052`) containing:

### 1. `openai_deployments.csv`
**Complete list of all deployments** in all OpenAI accounts.

**Columns:**
- `account` - Azure OpenAI account name
- `resourceGroup` - resource group
- `location` - Azure region
- `deployment` - deployment name
- `modelName` - model name (e.g., gpt-4o)
- `modelVersion` - model version (e.g., 2025-08-06)
- `sku` - SKU type (Standard, ProvisionedManaged)
- `capacity` - capacity (PTU for Provisioned)
- `resourceId` - full ARM resource ID

**Purpose:** Complete inventory of all deployments in the subscription.

---

### 2. `targeted_deployments.csv`
**Report of searched deployments** matching `TargetModels` with usage metrics.

**Columns:**
- All columns from `openai_deployments.csv` plus:
- `totalCalls_7d` - number of API calls in the last 7 days
- `processedTokens_7d` - sum of processed tokens (prompt)
- `generatedTokens_7d` - sum of generated tokens (completion)

**Purpose:** Quick identification of searched models and their actual usage.

**Example:**
```csv
account,resourceGroup,location,deployment,modelName,modelVersion,sku,capacity,totalCalls_7d,processedTokens_7d,generatedTokens_7d,resourceId
openai-prod,rg-ai,eastus2,gpt4o-deployment,gpt-4o,2025-08-06,Standard,,223,15847,8932,/subscriptions/.../openai-prod
```

---

### 3. `openai_no_diagnostics.csv`
**List of accounts without configured diagnostic settings.**

**Columns:**
- `resourceGroup`
- `account`
- `resourceId`

**Purpose:** Identification of accounts for which detailed logs cannot be retrieved.

---

### 4. `log_analytics_detailed_logs.csv`
**Detailed usage logs from Log Analytics workspace** (only if diagnostic settings are configured).

**Columns:**
- `workspaceId` - Log Analytics workspace ID
- `TimeGenerated` - query timestamp
- `ResourceId` - resource that handled the query
- `Operation` - operation type
- `CallerIP` - client IP address
- `Identity` - caller identity (managed identity, SPN, user)
- `UserAgent` - client agent
- `Properties` - full query properties (JSON with parameters, tokens, etc.)

**Purpose:** Deep analysis - who, when, from where, and how the searched models were used.

**⚠️ Note:** This file is generated only when:
- OpenAI accounts have diagnostic settings configured
- Diagnostic settings point to a Log Analytics workspace
- Logs from `Audit` or `RequestResponse` categories are available in the workspace

---

### 5. `model_retirement_alerts.csv`
**Retirement alerts for deployed models** based on official retirement timelines.

**Columns:**
- `account` - Azure OpenAI/Foundry account name
- `resourceGroup` - resource group
- `location` - Azure region
- `deployment` - deployment name
- `modelName` - model name
- `modelVersion` - model version
- `legacyDate` - date model entered legacy (if applicable)
- `deprecationDate` - date model entered deprecation (if applicable)
- `retirementDate` - retirement date
- `replacementModel` - suggested replacement model (if provided)
- `source` - `Foundry Models` or `Azure OpenAI in Foundry Models`
- `resourceId` - full ARM resource ID

**Purpose:** Notify which models need upgrades and suggested replacements.

---

## 🔄 Updating the model retirement list

Update model_retirements.json with the latest timelines from:
- https://learn.microsoft.com/azure/ai-foundry/concepts/model-lifecycle-retirement?view=foundry-classic
- https://learn.microsoft.com/azure/ai-foundry/openai/concepts/model-retirements?view=foundry-classic&tabs=text

You can also use the helper script to update the file from CSV or JSON inputs:

```bash
python .\update_model_retirements.py --foundry-csv .\foundry_retirements.csv --azure-openai-csv .\azure_openai_retirements.csv
```

CSV columns:
- Foundry: Model, Legacy, Deprecation, Retirement, Replacement
- Azure OpenAI: Model, Version, Deprecation, Retirement, Replacement

Format:
```json
{
  "foundry": [{"Model":"...","Legacy":"...","Deprecation":"...","Retirement":"...","Replacement":"..."}],
  "azure_openai": [{"Model":"...","Version":"...","Deprecation":"...","Retirement":"...","Replacement":"..."}]
}
```
Use null for unknown dates or replacements.

---

## 💡 Usage Examples

### Scenario 1: Quick audit without Log Analytics
```bash
python .\foundry_model_audit.py
```
**Result:** 
- List of all deployments
- Usage metrics for gpt-4o (2025-08-06, 2025-05-13) and gpt-4o-mini (2024-07-18)
- No detailed logs

---

### Scenario 2: Full audit with diagnostics enabled
```bash
# First create a Log Analytics workspace or use an existing one
$workspaceId = "/subscriptions/12345.../resourceGroups/rg-monitoring/providers/Microsoft.OperationalInsights/workspaces/la-audit"

# Run the script with automatic diagnostics configuration
python .\foundry_model_audit.py --enable-diag --diag-workspace-id $workspaceId
```
**Result:**
- All accounts receive diagnostic settings
- Logs start flowing to Log Analytics
- **Note:** Logs appear with delay (5-15 minutes), so on first run `log_analytics_detailed_logs.csv` may be empty

---

### Scenario 3: Searching for older model versions
```bash
# Check if old versions of gpt-4 and gpt-3.5-turbo are still being used
python .\foundry_model_audit.py --target-models "[{\"ModelName\":\"gpt-4\",\"Versions\":[\"0314\",\"0613\",\"1106-preview\"]},{\"ModelName\":\"gpt-35-turbo\",\"Versions\":[\"0301\",\"0613\"]}]"
```

---

### Scenario 4: Audit only Provisioned deployments with specific version
```bash
# Find all gpt-4o version 2025-08-06 (potentially expensive Provisioned)
python .\foundry_model_audit.py --target-models "[{\"ModelName\":\"gpt-4o\",\"Versions\":[\"2025-08-06\"]}]"
```
**Goal:** Identify unused Provisioned deployments that generate costs (filter in targeted_deployments.csv).

---

## 🔍 How do metrics work?

The script retrieves metrics from **Azure Monitor** (does not require diagnostic settings):

1. **Tries filtering by `DeploymentName`** (deployment name)
2. **If that doesn't work, tries by `ModelName`** (model name)
3. **Aggregates data from the last 7 days** in 1-hour intervals
4. **Sums values:**
   - `Requests` or `AzureOpenAIRequests` → `totalCalls_7d`
   - `ProcessedPromptTokens` → `processedTokens_7d`
   - `GeneratedTokens` → `generatedTokens_7d`

### Results interpretation

| totalCalls_7d | Meaning |
|---------------|-----------|
| `0` | Deployment unused in the last week |
| `1-100` | Low usage (test, rare) |
| `100-1000` | Medium usage |
| `>1000` | High usage (production) |

---

## 🛠️ Troubleshooting

### Problem: "No usage detected" even though I know the model is being used

**Causes:**
1. Azure Monitor metrics have delay (up to 5 minutes)
2. Filtering by `DeploymentName` may not work for all API versions
3. Metric naming differs between regions

**Solution:**
- Wait 10 minutes after using the model
- Check metrics manually in Azure portal (Monitoring → Metrics)
- Run the script again

---

### Problem: "log_analytics_detailed_logs.csv" is empty

**Causes:**
1. Diagnostic settings are not configured
2. Logs haven't reached Log Analytics yet (5-15 min delay)
3. No usage of searched models during the period when logs were collected

**Solution:**
```bash
# 1. Enable diagnostic settings
python .\foundry_model_audit.py --enable-diag --diag-workspace-id "<workspace-id>"

# 2. Wait 15-20 minutes

# 3. Use the searched models (make a few API calls)

# 4. Run again (without --enable-diag)
python .\foundry_model_audit.py
```

---

### Problem: Script stops with an error

**Most common causes:**
1. Lack of permissions to subscription
2. Azure CLI not logged in: `az login`

**Diagnostics:**
```bash
# Check login status
az account show

# Manually test resource listing
az resource list --resource-type "Microsoft.CognitiveServices/accounts" --query "[?kind=='OpenAI' || kind=='AIServices']"
```

---

## 📚 Additional Information

### Costs

The script **does not generate costs** - it only reads data:
- ✅ Resource listing - free
- ✅ Reading metrics from Azure Monitor - free
- ✅ Reading logs from Log Analytics - free*

\* *Log Analytics costs relate to ingestion (writing logs), not reading. Enabling diagnostic settings (`-EnableDiag`) may generate ingestion costs.*

### Security

The script **only reads data** - it does not modify deployments or configurations (except optional `-EnableDiag`).

**Sensitive data in logs:**
- `log_analytics_detailed_logs.csv` may contain IPs, identities, and user agents
- **Do not commit this file to repo!**
- Add to `.gitignore`:
  ```
  foundry-audit-*/
  ```

### Limitations

- Metrics available only for **last 90 days** (Azure Monitor limit)
- KQL query in Log Analytics: max **5000 rows** (change `take 5000` in script if needed)
- Script scans OpenAI and Foundry resources via `Microsoft.CognitiveServices/accounts` (`OpenAI` and `AIServices` kinds)
- Retirement alerts are based on published documentation and may change over time

---

## 🤝 Contributing

Suggestions? Found a bug? Open an Issue or Pull Request!

---

## 📄 License

MIT License - use freely, at your own risk.

---

## 🔗 Useful Links

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure Monitor Metrics](https://learn.microsoft.com/azure/azure-monitor/essentials/metrics-supported#microsoftcognitiveservicesaccounts)
- [Diagnostic Settings](https://learn.microsoft.com/azure/azure-monitor/essentials/diagnostic-settings)
- [KQL Query Language](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
- [Foundry model lifecycle and retirement](https://learn.microsoft.com/azure/ai-foundry/concepts/model-lifecycle-retirement?view=foundry-classic)
- [Azure OpenAI model retirements](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/model-retirements?view=foundry-classic&tabs=text)
