# Third‑Party Notices

This project incorporates material from the projects listed below. The original
copyright notices and the licenses under which we received such material are
set out below. We have included only material that is licensed under permissive
open‑source terms (MIT or equivalent). If you believe attribution is missing or
incorrect, please open an issue.

---

## 1. modelmigration

- **Upstream:** <https://github.com/saurabhvartak1982/modelmigration>
- **Author:** Saurabh Vartak (with acknowledgement to Prafulla — `@prwani`)
- **License:** MIT (treated as MIT per upstream README; verify before
  redistribution)
- **Used in this repo:** `docs/01-methodology/`

```
MIT License

Copyright (c) Saurabh Vartak and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 2. azure-ai-deployment-scanner

- **Upstream:** <https://github.com/ElisaPiccin/azure-ai-deployment-scanner>
- **Author:** Elisa Piccin (`@ElisaPiccin`)
- **License:** MIT
- **Used in this repo:** `tools/discovery/Get-AzureAIDeployments.ps1`

```
MIT License

Copyright (c) 2025 Elisa Piccin.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 3. azure-openai-migration-guide

- **Upstream:** <https://github.com/fatimataayeb/azure-openai-migration-guide>
- **Author:** Fatima Taayeb (`@fatimataayeb`)
- **License:** MIT (per upstream repo)
- **Used in this repo:** `tools/audit/audit_codebase.py`, GPT‑4o → 5.1 sections
  in `docs/05-api-changes-by-model.md` and `docs/faq.md`, pointer to upstream
  PPTX from `presentation/`

```
MIT License

Copyright (c) Fatima Taayeb and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 4. AOAI-models-migration

- **Upstream:** <https://github.com/aiappsgbb/AOAI-models-migration>
- **Author:** AI Apps GBB (`@aiappsgbb`) and contributors
- **License:** MIT
- **Used in this repo:** the bulk of `docs/02‑08`, pointers from
  `tools/evaluator/`, `tools/evaluator/webui/`, `data/golden-datasets/`,
  `skills/`, `examples/notebooks/`, `examples/sdks/`

```
MIT License

Copyright (c) Microsoft Corporation and AI Apps GBB contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 5. foundry-model-availability-notifications

- **Upstream:** <https://github.com/JinLee794/foundry-model-availability-notifications>
- **Author:** Jin Lee (`@JinLee794`)
- **License:** MIT (per upstream repo)
- **Used in this repo:** pointer / consumption guidance in `tools/availability/`.
  No source files are vendored — the tracker is consumed via its live
  dashboard, JSON snapshots, and GitHub issue stream.

```
MIT License

Copyright (c) Jin Lee and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 6. azure-openai-to-responses

- **Upstream:** <https://github.com/Azure-Samples/azure-openai-to-responses>
- **Maintainer:** Azure‑Samples (Microsoft) and contributors
- **License:** MIT
- **Used in this repo:** pointer / consumption guidance in
  `tools/api-migration/`; the Chat Completions → Responses API mapping table
  in `docs/05-api-changes-by-model.md` is adapted from the upstream README.
  No source files are vendored.

```
MIT License

Copyright (c) Microsoft Corporation.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 7. foundry_model_audit

- **Upstream:** <https://github.com/anishek-microsoft/foundry_model_audit>
- **Author:** anishekkamal and contributors
- **License:** MIT
- **Used in this repo:** optional deep-discovery pointer and wrapper in
  `tools/discovery/deep-audit/` and `scripts/run_deep_audit.sh`; upstream can
  be vendored under `tools/discovery/deep-audit/_upstream` via `git subtree`.

```
MIT License

Copyright (c) 2026 anishekkamal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

> **Note on verification.** Repos #1 and #3 do not always ship an explicit
> `LICENSE` file. Before redistributing or relicensing, the maintainers should
> obtain written confirmation from the original authors that MIT terms apply,
> and update this document accordingly. Until then, treat those sections as
> "permissively licensed pending confirmation."
