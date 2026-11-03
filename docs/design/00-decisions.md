# Bawaba (بوابة) — Requirements & Decisions Record

> Source of truth for the design. Every other design document must be consistent with this file.
> Captured from the requirements interview with the project owner on 2026-11-03.
> "Owner" below = the project owner (the human who runs Bawaba for their company).

## 1. What Bawaba is

Bawaba is a secure API gateway that sits **in front of the existing Shamel Pro Web API** (Shamel Financial
Software by ISCO — Isra' Software & Computer, Nablus). Shamel's own API has a single credential model
(Shamel username + password → session token), no permissions beyond Shamel's salesman scoping, parameters in
HTTP headers, JSON-in-form-field writes (`obj=`), every error returned as HTTP 500 with raw details, and no
pagination. The upstream reference is transcribed in `docs/upstream/shamel-api.md`.

Goals, in the owner's words: "make as many API tokens as I want, more security and permissions, maybe expanding
the API itself, better documentation, and a firewall."

## 2. Scope & audience

| Topic | Decision |
|---|---|
| Who it is for (v1) | **The owner's own company only.** Selling Bawaba to other Shamel users is "way later". |
| Selling later | Keep a *latent* tenant concept in the data model so a future SaaS **and** self-hosted product is possible without a rewrite. **No billing, licensing, plans, or quotas-for-billing in v1.** |
| Token consumers | Tools and dashboards **the owner builds (mostly built by AI agents)**, each needing different permissions; plus internal automation. |
| Shamel servers | **One now, more later.** Model "upstreams" (Shamel servers) as a first-class entity; routing per token/tenant. |
| Expected load | **Medium now** (hundreds → ~1,000 req/min), but code and structure must handle **heavy** load; "the bottleneck should only ever be hardware". → stateless, horizontally scalable gateway nodes. |
| Hosting | **Decide later.** Ship Docker Compose + standalone binaries; document both cloud VPS and on-prem. Linux primary; Connector must also run on Windows (Shamel likely on a Windows server). |
| Where is Shamel today | **Unknown** (owner will check with ISCO / IT). Design must work whether Shamel is on an office LAN, exposed, or hosted. |

## 3. Technology

| Topic | Decision |
|---|---|
| Language | **Go** — chosen for performance, concurrency and load (owner: "whatever is best for performance, speed and load"). Gateway, Connector and CLI in Go. |
| Name | **Bawaba (بوابة)**. CLI binary: `bawaba`. Docker images `bawaba/*`. |
| Design doc language | English. |
| Product docs & dashboard | **Bilingual Arabic + English**, full RTL support for Arabic. |

## 4. Security & "firewall"

Owner's definition of the firewall: *"The firewall should not allow any hacker to try to get into Shamel itself or
the IP information of Shamel. Our gateway encrypts everything and is very secure; they won't be able to access
things even if they try to find vulnerabilities."*

Decisions:
- **Origin hiding is the core requirement.** Nothing about Shamel (IP, hostname, port, software/server version,
  internal paths, image URLs, raw error text, stack traces, SQL) may ever reach a client.
- **Connector: support both** — (a) a small **Bawaba Connector** installed next to Shamel that opens an
  **outbound encrypted tunnel** to the gateway so Shamel needs no public IP / no open inbound port (preferred), and
  (b) **direct URL** mode for when the Connector can't be installed (Shamel's firewall must then allow only the
  gateway's egress IP).
- **Edge: Cloudflare in front** — public hostname (e.g. `api.<company>.com`) proxied by Cloudflare; the gateway
  origin accepts traffic only from Cloudflare (IP allowlist + authenticated origin pulls) or via a Cloudflare
  Tunnel with no open ports. This hides even Bawaba's own IP and absorbs DDoS.
- Upstream errors are **never forwarded**: sanitized error codes + request id to the client, details to the
  encrypted audit log only.
- Strip identifying upstream headers; rewrite/proxy any upstream URLs (e.g. item catalog image paths).
- API tokens stored **hashed only**; Shamel credentials and sensitive data **encrypted at rest** (envelope
  encryption, AES-256-GCM).
- **Master encryption key: key file on the server**, root-only permissions, outside the database; auto-start after
  reboot. A stolen DB or backup alone must be useless. (Vault/KMS = future option.)
- Firewall features: global + per-token IP allow/deny lists, auto-ban on repeated auth failures, strict request
  schema validation and size limits, TLS everywhere. Geo-blocking was not requested (Cloudflare can do it if needed).
- **AI agents never touch Shamel directly** and never see Shamel credentials/IP. They only talk to Bawaba,
  bounded by token permissions (see §6).

## 5. Tokens & permissions

| Topic | Decision |
|---|---|
| Upstream Shamel login | **Configurable per token**: each upstream has a default Shamel service account; any token can instead be pinned to a specific Shamel user (e.g. a salesman, preserving Shamel's own salesman scoping). |
| Permission levels (all requested) | **Per endpoint/resource scopes** (e.g. `customers:read`); **per voucher type** (e.g. may create Orders but not Sales Invoices); **data scoping** (restrict to stores, salesmen, customers, currencies, price classes); **field hiding** (e.g. strip `purchase_price`, balances, credit limits, accounts); presets like **read-only, write-only**, etc. |
| Token features | **Per-token IP allowlist**; **usage analytics** (counts, errors, latency, last used). Instant revoke. |
| Expiry | **Never expire by default; optional expiry per token**; tokens unused for 90 days are flagged. |
| Rate limits | Not requested as a token feature by the owner; see §8 (overload) for the agreed approach. |
| Browser vs server callers | **Not sure → support both, default server-only.** Browser ("publishable") tokens are opt-in, read-only, locked to allowed origins (CORS). |

## 6. AI agents, approvals & sandbox

- AI agents (e.g. Claude) build the owner's tools/dashboards. They run **off-server** (owner's PC or the cloud) and
  reach Bawaba only over the network with an **agent token**.
- **"Request, you approve" model:** an agent token can *request* new tool tokens / permission changes; nothing takes
  effect until the **owner approves on the server** (localhost dashboard or CLI). An agent can never request or
  grant more than its own token holds. An agent can never approve.
- **Sandbox: yes.** Test tokens (`…_test_…`) are routed to a **built-in mock Shamel** with realistic fake data, so AI
  can build and test tools without touching real accounting data. Owner switches a tool to a live token once trusted.
- **Write safety:** **approval queue** (writes from selected tokens wait for owner approval before reaching Shamel)
  and **undo-friendly audit** (every write recorded with full payload + Shamel reference id). Dry-run and amount
  limits were *not* selected for v1.
- **Inform the AI:** rather than only restricting, Bawaba must actively teach AI agents to build well-behaved tools:
  AI-friendly docs (OpenAPI 3.1, llms.txt, examples, documented error codes), rate-limit/usage headers, response
  warnings when a tool polls too aggressively, guidance to use webhooks/snapshots instead of tight polling.

## 7. Administration

| Topic | Decision |
|---|---|
| Admin UI | **Web dashboard, bilingual (ar/en), localhost-only** (bound to 127.0.0.1, reached via SSH tunnel). Still requires owner login (defense in depth). |
| CLI | **Full CLI** (`bawaba ...`) with machine-readable **JSON output** — "AI will be building the dashboards etc. so it will be better for it". Owner actions via local CLI on the server; agent-level actions (requests, docs, own usage) via the network API with an agent token. |
| Admin roles | Owner (full). Approve/firewall/live-token creation only from the server (localhost). |
| Alerts | **Email** (SMTP): attacks, IP bans, unusual usage, abusive/buggy tools, approvals waiting. |

## 8. Data freshness, performance, overload

| Topic | Decision |
|---|---|
| Caching | **Always live.** No stale data caching of business data. |
| Paging | **Short snapshots**: page 1 does one live fetch; pages 2..N reuse that snapshot for ~60s (cursor-bound). **Request coalescing**: identical concurrent requests share one live upstream call. |
| Overload | Owner prefers to **inform the AI** so it doesn't build buggy dashboards (docs, headers, warnings, owner email alerts on abusive tokens). A global upstream concurrency cap (queue instead of crashing Shamel) remains as an invisible safety net; per-token limits default generous and adjustable. |

## 9. API shape & expansions

- **Clean, modern `/v1` REST API** (resources, query params, JSON bodies, proper status codes, consistent naming
  that fixes Shamel's typos), **plus an optional legacy-compatible passthrough** (Shamel's original paths/quirks)
  enabled per token, so existing integrations can migrate by changing URL + token. Both paths go through the
  same auth, permission, firewall and audit pipeline. (Owner delegated this choice.)
- Expansions (all selected): **webhooks / change events**, **paging & search** (over snapshots), **safe posting &
  batches** (idempotency keys, batch posting), **combined endpoints** (e.g. customer 360, stock across stores).
- **Webhooks: change detection polls Shamel every 5 minutes** (configurable), only for subscribed events.
  Deliveries HMAC-signed with retries.
- **Milestone 1 priority: everything that reads data** — customers + balances + statements + prices, items +
  stock + groups + serials + catalog + last-price report, vouchers (read) + deliveries + status, cost-center
  reports, master data (currencies, rates, banks, cities, stores, price classes, salesmen). Writes come after.

## 10. Audit log

- **Everything, full**: every request and response body, encrypted.
- Owner: **"optimize it"** → storage must be engineered: content-addressed de-duplication of bodies (identical
  responses stored once), compression (zstd), encryption, time-partitioned storage, tiered retention with sensible
  configurable defaults, size caps with alerts.

## 11. Open questions for ISCO (owner will ask them)

Owner confirmed they can contact ISCO. Design doc must include a precise question list (e.g. GetSalesmen response
shape, Shamel token lifetime/expiry behaviour, HTTPS support, rate/concurrency limits, pagination support, error
format, `lastupdatedate` semantics and timezone, permission to wrap/resell their API later, versioning).
