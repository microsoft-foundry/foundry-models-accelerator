# Golden Dataset Templates

> **Source:** Adapted from
> [fatimataayeb/azure-openai-migration-guide/datasets/templates/](https://github.com/fatimataayeb/azure-openai-migration-guide/tree/master/datasets/templates).

Empty‑schema starting points for scenarios you don't yet have production data
for. Fill them in following the patterns in
[`docs/06-building-golden-datasets.md`](../../../docs/06-building-golden-datasets.md).

Once you have at least ~10 well‑labeled cases per scenario, drop the file
under `data/golden-datasets/` (no `templates/` subfolder) and reference it from
your `scripts/run_eval.py` invocation.
