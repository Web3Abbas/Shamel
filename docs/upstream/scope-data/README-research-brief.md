# Brief: "Shamel API — capabilities and scope" research

Goal: a PDF for the owner of a company that uses Shamel Pro (accounting/ERP by ISCO, Nablus) that fully scopes what the
Shamel Pro Web API can do: which business data can be read, what can be written, filters, reports, what can be built,
and the limits. The audience is the owner (business-minded, not a developer) plus the AI agents that will build tools.

SOURCES (authoritative order):
1. The ISCO manual PDF (20 pages; pages 2-3 Arabic): /tmp/claude-0/-home-user-Shamel/2fa345b5-da1a-5636-a894-5f783b11f933/scratchpad/src/shamel-api-manual.pdf
   Read it with the Read tool using pages "1-10" and "11-20". It is the ONLY evidence for what Shamel does.
2. A verified transcription of it (easier to search): /home/user/Shamel/docs/upstream/shamel-api.md
3. For "how Bawaba exposes it" columns only: /home/user/Shamel/docs/design/03-api.md (§6 endpoint catalogue, §7 coverage matrix).
4. Open questions already sent to ISCO: /home/user/Shamel/docs/design/08-isco-questions.md (ids ISCO-01..55) — cite ids
   where a capability depends on an unknown.

RULES:
- Never claim something the manual does not say. Mark every meaning as one of: "manual" (stated in English),
  "manual-ar" (stated in an Arabic comment — give the English translation and keep the Arabic), "inferred" (reasonable
  reading, say why), "undocumented" (no meaning given).
- Keep Shamel's original field names exactly as printed (including misspellings like sale_parice1, orgnization_code).
- Cite manual page numbers ("p. N") for facts.
- Write valid JSON (UTF-8, Arabic allowed). Write ONLY your assigned output file. Do NOT run git.
