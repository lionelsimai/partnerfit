---
name: partnerfit
description: Qualify a vendor for a community partnership — category exclusivity gate, 100-point fit score, price-book entry tier, human-approved outreach draft. Use when asked to score sponsor/partner fit, check a category clash, or rank a vendor list for partnerships.
---

# PartnerFit

Run from the plugin root with the operator's config.

1. Validate first: `PYTHONPATH=src python3 -m partnerfit --config config/the-ai-capitol.json validate`
2. Score one vendor: `... score --vendor '<json>'` — inputs are the 7 dimensions
   in SPEC.md, each 0–10, each backed by evidence the operator can point to.
3. Score a list: `... batch --csv examples/vendors-sample.csv`
4. Draft only at 35+: `... draft --vendor '<json>'`
   Blocked (category clash) and nurture (<35) vendors get no draft.
5. Check a category any time: `... check-category --category "voice AI"`

Rules:
- Category clash is a hard block. No score, no draft, no workarounds.
- Outreach copy uses only the verified stats in the config. Never add numbers.
- Every draft is DRAFT — NOT SENT. A human approves and sends, outside this tool.
- Guarantee held meetings only. Never revenue, deals, or impressions.
