# Security

## Reporting security issues

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, report them to the Microsoft Security Response Center (MSRC) at
<https://msrc.microsoft.com/create-report>. If you prefer email, send to
[secure@microsoft.com](mailto:secure@microsoft.com); if possible encrypt your
message with the [MSRC PGP key](https://aka.ms/opensource/security/pgpkey).

You should receive a response within 24 hours. Please include:

- Type of issue (e.g., credential exposure, code injection, prompt injection)
- Full paths of source file(s) related to the issue
- Step‑by‑step reproduction
- Any special configuration required
- Impact and how an attacker might exploit it

See <https://aka.ms/opensource/security/policy> for Microsoft's full policy.

## Scope notes for this repo

This accelerator includes scripts that:

- Enumerate Azure resources (`tools/discovery/`) — requires Azure CLI auth and
  Reader permissions only.
- Scan local source code for migration patterns (`tools/audit/`) — purely local,
  no network calls.
- Call Azure OpenAI endpoints from `tools/evaluator/` — requires `AZURE_OPENAI_*`
  environment variables. **Do not commit `.env`.** Use Azure Key Vault or
  Managed Identity in production.

If you find an issue specific to one of the upstream repos this consolidates,
please also notify the upstream maintainer (see
[`ATTRIBUTION.md`](./ATTRIBUTION.md) for links).
