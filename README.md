# PartnerFit

Qualify a vendor for a community partnership in under 10 minutes.

By Lionel Sim, The AI Capitol — built from a live partnerships practice:
OpenBuilder (Singapore), 8,000+ builders, ~15,000 signups, 80 events.

## What it does
- **Hard exclusivity gate** — if an annual partner already holds the vendor's
  category, the verdict is BLOCKED: no score, no outreach draft.
- **Auditable 100-point score** across 7 dimensions: senior audience fit,
  buyer overlap, activation fit, APAC presence, budget signal, timing, warmth.
- **Price-book tier** — Anchor / Partner / Event / Nurture, from your config.
- **Approved drafts only** — outreach for vendors scoring 35+, written only
  from verified audience stats in your config, stamped DRAFT — NOT SENT.
  There is no send action, by design.

Full model: see `SPEC.md`.

## Quickstart
```bash
PYTHONPATH=src python3 -m partnerfit --config config/the-ai-capitol.json validate
PYTHONPATH=src python3 -m partnerfit --config config/the-ai-capitol.json demo
PYTHONPATH=src python3 -m partnerfit --config config/example.json batch --csv examples/vendors-sample.csv
python3 -m pytest tests/ -q
```

Vendor CSV columns: name, category, the 7 dimension scores (0–10),
activation_idea, evidence. All sample vendors are fictional.

## Config
Copy `config/example.json`, set your own verified community stats,
held categories, and price book. The bundled `config/the-ai-capitol.json`
carries The AI Capitol's verified Oct 2026 census
(9,834 unique people, 68 events, 46% senior) and current price book
(Anchor S$48,000/yr, Partner S$24,000/yr, Event S$6,000 nett).

## Licence
MIT
