# Evaluator — Web UI

> **Source:** Will be folded in via `git subtree` from
> [`aiappsgbb/AOAI-models-migration/model_migration_eval/`](https://github.com/aiappsgbb/AOAI-models-migration/tree/main/model_migration_eval).

A visual, side‑by‑side **model comparator**. You point it at two Azure OpenAI
deployments, give it a dataset, and it runs prompts through both and shows
per‑test‑case differences alongside aggregated metrics.

## Run it locally (against the upstream)

```bash
git clone https://github.com/aiappsgbb/AOAI-models-migration.git
cd AOAI-models-migration/model_migration_eval
pip install -r requirements.txt
python app.py
```

Then open <http://localhost:5000> (or whatever the app prints).

## Container Apps deployment

A follow‑on enhancement listed in the accelerator plan is an `azd` template
under `infra/` to spin this up in Azure Container Apps. Track in an issue
before implementing.
