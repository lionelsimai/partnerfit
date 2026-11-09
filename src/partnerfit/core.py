"""PartnerFit core: score a vendor for a community partnership.

Stdlib only. Hard gate on category exclusivity before any scoring.
No send action exists, by design.
"""
from __future__ import annotations

import csv
import io
from dataclasses import dataclass, field

WEIGHTS = {
    "senior_audience_fit": 2.0,   # -> 20
    "buyer_overlap": 1.5,         # -> 15
    "activation_fit": 1.5,        # -> 15
    "apac_presence": 1.5,         # -> 15
    "budget_signal": 1.5,         # -> 15
    "timing": 1.0,                # -> 10
    "warmth": 1.0,                # -> 10
}  # total max = 100

DIMENSIONS = list(WEIGHTS.keys())


@dataclass
class Vendor:
    name: str
    category: str
    senior_audience_fit: float
    buyer_overlap: float
    activation_fit: float
    apac_presence: float
    budget_signal: float
    timing: float
    warmth: float
    activation_idea: str = ""
    evidence: str = ""

    def __post_init__(self):
        for d in DIMENSIONS:
            v = getattr(self, d)
            if not isinstance(v, (int, float)) or not (0 <= v <= 10):
                raise ValueError(f"{d} must be a number 0-10, got {v!r}")


def load_config(raw: dict) -> dict:
    for key in ("operator", "community_stats", "held_categories", "price_book"):
        if key not in raw:
            raise ValueError(f"config missing '{key}'")
    for tier in ("anchor", "partner", "event"):
        if tier not in raw["price_book"]:
            raise ValueError(f"price_book missing '{tier}'")
    return raw


def category_status(category: str, config: dict) -> str:
    held = [c.lower() for c in config["held_categories"]]
    return "held" if category.strip().lower() in held else "free"


def score_vendor(vendor: Vendor, config: dict) -> dict:
    if category_status(vendor.category, config) == "held":
        return {
            "vendor": vendor.name,
            "category": vendor.category,
            "fit_score": None,
            "verdict": "BLOCKED — category already held by an annual partner",
            "recommended_entry": None,
            "breakdown": None,
            "evidence": vendor.evidence,
        }
    breakdown = {d: round(getattr(vendor, d) * WEIGHTS[d], 1) for d in DIMENSIONS}
    score = round(sum(breakdown.values()))
    pb = config["price_book"]
    if score >= 75:
        entry = pb["anchor"]
    elif score >= 55:
        entry = pb["partner"]
    elif score >= 35:
        entry = pb["event"]
    else:
        entry = "Nurture — community only, no partnership pitch yet"
    return {
        "vendor": vendor.name,
        "category": vendor.category,
        "fit_score": score,
        "verdict": "SCORED",
        "recommended_entry": entry,
        "breakdown": breakdown,
        "evidence": vendor.evidence,
    }


def score_batch(csv_text: str, config: dict) -> dict:
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    scored, blocked = [], []
    for r in rows:
        vendor = Vendor(
            name=r["name"], category=r["category"],
            **{d: float(r[d]) for d in DIMENSIONS},
            activation_idea=r.get("activation_idea", ""),
            evidence=r.get("evidence", ""),
        )
        result = score_vendor(vendor, config)
        (blocked if result["fit_score"] is None else scored).append(result)
    scored.sort(key=lambda x: -x["fit_score"])
    return {"scored": scored, "blocked": blocked}


def draft_outreach(vendor: Vendor, config: dict) -> dict:
    result = score_vendor(vendor, config)
    if result["fit_score"] is None:
        return {"vendor": vendor.name, "draft": None,
                "reason": "Blocked: category clash. No draft produced."}
    if result["fit_score"] < 35:
        return {"vendor": vendor.name, "draft": None,
                "reason": "Score below 35: nurture only, no partnership draft."}
    s = config["community_stats"]
    stats = (f"{s['unique_people']:,} unique people across {s['events']} events "
             f"({s['census_label']}), {s['senior_pct']}% senior")
    idea = vendor.activation_idea or "a curated partner night"
    draft = (
        f"Subject: A room of senior APAC buyers for {vendor.name}\n\n"
        f"Hi — I run {config['operator']['org']}: {stats}. "
        f"I'd like to show you how {idea} would put {vendor.name} in front of "
        f"that room, with held meetings — not impressions — as the measure. "
        f"Recommended entry based on fit ({result['fit_score']}/100): "
        f"{result['recommended_entry']}. 20 minutes next week?\n\n"
        f"{config['operator']['name']}, {config['operator']['title']} — "
        f"{config['operator']['presentation_url']}\n\n"
        f"[DRAFT — NOT SENT. Human approval required.]"
    )
    return {"vendor": vendor.name, "fit_score": result["fit_score"],
            "recommended_entry": result["recommended_entry"], "draft": draft}
