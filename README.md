# Bawaba (بوابة)

A secure, high-performance API gateway in front of the **Shamel Pro** accounting API.

Bawaba lets you issue as many scoped API tokens as you need, fine-grained permissions (per endpoint,
per voucher type, data scoping, field hiding), a firewall that keeps the Shamel server completely hidden,
a clean documented `/v1` API (plus a legacy-compatible mode), full encrypted audit logging, a sandbox for
AI-built tools, and an approval flow so nothing an AI agent requests goes live without the owner.

> **Status:** design phase. Start with [`docs/design/README.md`](docs/design/README.md).

| Document | Purpose |
|---|---|
| [`docs/design/00-decisions.md`](docs/design/00-decisions.md) | Requirements & decisions record (source of truth) |
| [`docs/design/`](docs/design/) | Architecture, security, API, permissions, operations, milestones |
| [`docs/upstream/shamel-api.md`](docs/upstream/shamel-api.md) | Transcribed reference of the upstream Shamel Pro API |
