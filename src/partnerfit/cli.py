"""PartnerFit CLI: validate | score | batch | draft | check-category | demo"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from partnerfit.core import (DIMENSIONS, Vendor, category_status,  # noqa: E402
                             draft_outreach, load_config, score_batch,
                             score_vendor)


def _config(path: str) -> dict:
    return load_config(json.loads(Path(path).read_text()))


def _vendor(data: dict) -> Vendor:
    return Vendor(name=data["name"], category=data["category"],
                  **{d: float(data[d]) for d in DIMENSIONS},
                  activation_idea=data.get("activation_idea", ""),
                  evidence=data.get("evidence", ""))


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="partnerfit")
    p.add_argument("--config", required=True)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    s = sub.add_parser("score"); s.add_argument("--vendor", required=True)
    b = sub.add_parser("batch"); b.add_argument("--csv", required=True)
    d = sub.add_parser("draft"); d.add_argument("--vendor", required=True)
    c = sub.add_parser("check-category"); c.add_argument("--category", required=True)
    sub.add_parser("demo")
    a = p.parse_args(argv)
    cfg = _config(a.config)

    if a.cmd == "validate":
        print(json.dumps({"ok": True, "operator": cfg["operator"]["org"],
                          "held_categories": cfg["held_categories"]}, indent=2))
    elif a.cmd == "score":
        print(json.dumps(score_vendor(_vendor(json.loads(a.vendor)), cfg), indent=2))
    elif a.cmd == "batch":
        print(json.dumps(score_batch(Path(a.csv).read_text(), cfg), indent=2))
    elif a.cmd == "draft":
        print(json.dumps(draft_outreach(_vendor(json.loads(a.vendor)), cfg), indent=2))
    elif a.cmd == "check-category":
        print(json.dumps({"category": a.category,
                          "status": category_status(a.category, cfg)}, indent=2))
    elif a.cmd == "demo":
        demo_csv = Path(__file__).resolve().parents[2] / "examples" / "vendors-sample.csv"
        print(json.dumps(score_batch(demo_csv.read_text(), cfg), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
