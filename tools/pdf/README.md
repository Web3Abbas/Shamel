# Design PDFs

Builds the two PDFs in [`docs/pdf/`](../../docs/pdf/):

| PDF | Source | What it is |
|---|---|---|
| `Bawaba-Visual-Overview.pdf` | `overview/part*.html` + `overview/base.css` | Hand-designed ~20-page visual summary (diagrams, decisions, flows) |
| `Bawaba-Design-Reference.pdf` | `docs/design/*.md`, `docs/upstream/shamel-api.md` | Every design document rendered with diagrams, contents and bookmarks |

```bash
cd tools/pdf
npm install            # Chromium comes from Playwright (npx playwright install chromium if missing)
npm run build          # or: npm run overview / npm run reference
```

Notes
- Mermaid diagrams are rendered in headless Chromium. Wide flowcharts are automatically re-laid out top-to-bottom
  or placed on a landscape page, whichever is more legible.
- Fonts (Inter, IBM Plex Sans Arabic, JetBrains Mono) are bundled via `@fontsource`, so Arabic renders without
  system fonts.
- `render-overview.mjs` reports any page whose content overflows its A4 box; keep that list empty.
- The overview's numbers (performance targets, audit storage estimates, retention, alert names) are taken from the
  design documents. Update both when the design changes.
