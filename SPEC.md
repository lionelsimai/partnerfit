# PartnerFit — Spec v0.1

Author: Lionel Sim, The AI Capitol
Status: MVP built and tested 9 Nov 2026
Licence: MIT

## 1. Problem
Community and event operators get pitched by many vendors, and pitch many more.
Most qualify on gut feel. That wastes calls, breaks category exclusivity,
and leads to sponsor decks with inflated audience claims.

PartnerFit qualifies a vendor for a community partnership in under 10 minutes,
with an auditable score, a hard exclusivity gate, and a recommended entry tier
from a fixed price book. It drafts outreach only for qualified vendors.
It never sends anything.

## 2. Who it is for
- Solo community operators and founder-led GTM teams (primary)
- Sponsorship / partnerships leads at media and event companies
- AI vendors self-checking fit before they pitch a community (secondary)

## 3. Lionel's model, encoded
- Vendor-first: sponsors and partners pay for the room. The community is the asset.
- One partner per category at annual level. Exclusivity is the product.
- Guarantee held meetings only. Never revenue, deals, or impressions.
- Audience claims come only from verified counts in the config file.
  No number is invented, rounded up, or borrowed from another community.
- Every external draft is stamped DRAFT — NOT SENT and needs human approval.

## 4. Hard gates (checked before scoring)
1. Category clash: if the vendor's category is in `held_categories`
   (already held by an annual partner), verdict is BLOCKED,
   fit score is null, and no outreach draft is produced.
2. Missing evidence: each scoring input must be 0–10 with a reason the
   operator can point to (funding news, hiring, a past meeting, attendance).
   The CLI rejects out-of-range or non-numeric inputs instead of guessing.
3. No auto-send: there is no send action in this plugin, by design.

## 5. Scoring model (100 points)
All inputs are 0–10.

| Dimension | Weight | What good looks like |
|---|---|---|
| Senior audience fit | 20 | Sells to founders, directors, C-suite — the room's senior mix |
| Buyer / ICP overlap | 15 | Their ICP matches the community's actual attendees |
| Activation fit | 15 | Has a product that demos well live in a room |
| APAC enterprise presence | 15 | APAC team, customers, or a stated APAC expansion |
| Budget signal | 15 | Funding, hiring, regional launch, prior sponsorship spend |
| Timing / urgency | 10 | Launch, conference season, quarter-end push |
| Relationship warmth | 10 | Attended events, prior meeting, warm intro path |

Score = weighted sum, rounded to a whole number.

## 6. Verdict bands and price book
Prices come from the config file, never hard-coded in outreach copy.
Default config is The AI Capitol price book:

- Score 75–100: Anchor Partner — S$48,000 / year, category exclusive
- Score 55–74: Partner — S$24,000 / year
- Score 35–54: Event Partner — S$6,000 nett, start with one room
- Score 0–34: Nurture — community only, no partnership pitch yet
- Category clash: BLOCKED — no score, no draft

## 7. Actions (plugin contract)
1. `validate_config` — load and check a config: operator, verified
   community stats, held categories, price book.
2. `score_vendor` — score one vendor (JSON object) → score, band,
   per-dimension breakdown, reasons.
3. `score_batch` — score a CSV of vendors → ranked JSON, blocked vendors
   listed separately with the clashing category.
4. `draft_outreach` — for a scored, non-blocked vendor ≥35 only:
   a personal outreach draft using only verified stats from config,
   stamped DRAFT — NOT SENT.
5. `check_category` — is this category held, free, or free-but-adjacent?

## 8. Inputs
Vendor record fields: name, category, senior_audience_fit, buyer_overlap,
activation_fit, apac_presence, budget_signal, timing, warmth,
activation_idea (one line), evidence (one line, where the signals came from).

## 9. Outputs
JSON with: vendor, category, fit_score (or null), verdict / recommended_entry,
breakdown per dimension, evidence, and — when drafted — the draft text
with its approval stamp.

## 10. Non-goals
- No scraping, no lead database, no enrichment vendor lock-in.
- No sending, no CRM write-back in v0.1.
- No attendee PII in scoring or drafts.

## 11. Roadmap
- v0.2: renewal scoring (score existing partners on delivery vs promise)
- v0.3: optional MCP server wrapper over the same core
- v0.4: partner ROI report input, so fit score and delivered ROI sit side by side
