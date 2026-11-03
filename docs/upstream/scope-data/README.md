# Shamel Pro API — structured scope data

Machine-readable research behind [`docs/pdf/Shamel-API-Scope.pdf`](../../pdf/Shamel-API-Scope.pdf). Everything
was extracted from ISCO's Shamel Pro API manual (20 pages) and checked against it. Page numbers (`page`, "p. N")
refer to that manual. AI agents building tools can read these files directly.

| File | Contents |
|---|---|
| `dict-master-customers.json` | Data dictionary: login result, currencies, rates, banks, branches, cities, stores, price classes, salesmen (undocumented), customers (read and write models), classifications, contacts, balances, special-price rows |
| `dict-items.json` | Data dictionary: items (read and write models), stock per store, item details, groups, catalog images, serials, last-price report rows |
| `dict-vouchers.json` | Data dictionary: vouchers (header, lines, cheques, accounts), results, filters, account statements, cost centers; enums `VoucherTypes` (13 values with code prefixes) and order status (0–4) |
| `endpoints.json` | All 30 endpoints (inputs, returns, sync support, notes, ISCO question ids, matching Bawaba route) and a capability matrix per business entity |
| `usecases.json` | 30 tool ideas with the endpoints they need and a feasibility rating (ready / partial / blocked) |
| `limits.json` | 30 limits and gaps with impact and how Bawaba mitigates each |
| `README-research-brief.md` | The rules the research followed |

Every field meaning carries a `source`: `manual` (stated in English), `manual-ar` (from an Arabic comment, translated),
`inferred` (our reading, with the reason in `note`) or `undocumented`. Field names are kept exactly as printed,
including the manual's misspellings (`sale_parice1`, `orgnization_code`, `refrenceId`).

Rebuild the PDF: `tools/pdf/scope/build.sh` (see [`tools/pdf/README.md`](../../../tools/pdf/README.md)).
