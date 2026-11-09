import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from partnerfit.core import (Vendor, category_status, draft_outreach,
                             load_config, score_batch, score_vendor)

CFG = load_config(json.loads(
    (Path(__file__).resolve().parents[1] / "config" / "example.json").read_text()))


def v(**kw):
    base = dict(name="TestCo", category="dev tools", senior_audience_fit=9,
                buyer_overlap=8, activation_fit=9, apac_presence=7,
                budget_signal=8, timing=7, warmth=6,
                activation_idea="a live demo night", evidence="test")
    base.update(kw)
    return Vendor(**base)


def test_category_clash_blocks_with_no_score():
    # example config holds "voice AI"
    r = score_vendor(v(category="voice AI"), CFG)
    assert r["fit_score"] is None and "BLOCKED" in r["verdict"]
    assert category_status("Voice AI", CFG) == "held"  # case-insensitive


def test_high_fit_gets_anchor_tier():
    r = score_vendor(v(), CFG)
    assert r["fit_score"] >= 75 and "Anchor" in r["recommended_entry"]


def test_low_fit_is_nurture_and_gets_no_draft():
    low = v(senior_audience_fit=1, buyer_overlap=1, activation_fit=1,
            apac_presence=1, budget_signal=1, timing=1, warmth=1)
    r = score_vendor(low, CFG)
    assert r["fit_score"] < 35 and "Nurture" in r["recommended_entry"]
    assert draft_outreach(low, CFG)["draft"] is None


def test_blocked_vendor_gets_no_draft():
    assert draft_outreach(v(category="voice AI"), CFG)["draft"] is None


def test_draft_is_stamped_and_uses_only_config_stats():
    d = draft_outreach(v(), CFG)["draft"]
    assert "DRAFT — NOT SENT" in d
    assert "1,000 unique people" in d  # from example config, not invented


def test_out_of_range_input_rejected():
    try:
        v(senior_audience_fit=11)
        raise AssertionError("should have raised")
    except ValueError:
        pass


def test_batch_ranks_and_separates_blocked():
    csv_text = (Path(__file__).resolve().parents[1] / "examples" / "vendors-sample.csv").read_text()
    # example config holds voice AI, so the voice sample must be blocked
    out = score_batch(csv_text, CFG)
    assert len(out["blocked"]) == 1
    scores = [x["fit_score"] for x in out["scored"]]
    assert scores == sorted(scores, reverse=True)
