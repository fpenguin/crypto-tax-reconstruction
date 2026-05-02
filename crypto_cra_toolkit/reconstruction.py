"""Reconstruction — generate the smallest defensible set of "anchor" Buy rows
that closes each missing-ACB gap.

Anchor entries are written in the same CoinStats-CSV column layout the parser
expects, so the user can re-import them as a manual source on the next run.

For each missing event we:
1. pick a CAD price using the cause label:
     * stablecoin_redeem    -> $1.00 CAD per unit (rough par)
     * fiat_origin_missing  -> proceeds-per-unit on the sale date (neutral
       proxy; user should override with real fiat statement)
     * airdrop_or_income    -> proceeds-per-unit (= FMV at later sale; the
       user should replace this with the FMV at *receipt*)
     * transfer_in_unmatched / defi_swap_missing -> proceeds-per-unit
2. backdate the anchor by one day so it is unambiguously prior to the sale.
3. stamp the source-of-evidence note so the audit memo can quote it.
"""

from __future__ import annotations

import pandas as pd


CAUSE_PRICE_RULES = {
    "stablecoin_redeem":    "par_one_cad",
    "fiat_origin_missing":  "fmv_proxy",
    "airdrop_or_income":    "fmv_proxy",
    "transfer_in_unmatched": "fmv_proxy",
    "defi_swap_missing":    "fmv_proxy",
    "unknown":              "fmv_proxy",
}

CAUSE_NOTES = {
    "stablecoin_redeem":     "Anchor ACB at $1.00 CAD par (stablecoin assumption).",
    "fiat_origin_missing":   "Anchor ACB at sale-date FMV (placeholder; replace with fiat-onramp record).",
    "airdrop_or_income":     "Anchor ACB at FMV (placeholder; replace with FMV at the actual receipt date).",
    "transfer_in_unmatched": "Anchor ACB at sale-date FMV (placeholder; import source wallet/exchange).",
    "defi_swap_missing":     "Anchor ACB at sale-date FMV (placeholder; trace swap to find true cost).",
    "unknown":               "Anchor ACB at sale-date FMV (placeholder).",
}


def build_anchor_entries(classified_missing: pd.DataFrame) -> pd.DataFrame:
    """Return a CSV-ready DataFrame of synthetic Buy rows."""
    if classified_missing.empty:
        return pd.DataFrame(columns=[
            "Portfolio", "Coin Name", "Coin Symbol", "Exchange", "Pair",
            "Type", "Amount", "Price", "Price CAD",
            "Fee Percent", "Fee Amount", "Fee Currency", "Date", "Notes",
            "anchor_cause", "anchor_confidence", "anchor_value_cad",
        ])

    rows = []
    for _, ev in classified_missing.iterrows():
        cause = ev.get("cause", "unknown")
        rule = CAUSE_PRICE_RULES.get(cause, "fmv_proxy")
        sell_qty = float(ev["qty_sold"])
        proceeds = float(ev["proceeds_cad"])
        missing_qty = float(ev["missing_qty"])
        per_unit_fmv = (proceeds / sell_qty) if sell_qty > 0 else 0.0

        if rule == "par_one_cad":
            price_cad = 1.0
        else:
            price_cad = per_unit_fmv

        anchor_date = (pd.to_datetime(ev["date"]) - pd.Timedelta(days=1)).strftime("%-m/%-d/%Y, %-I:%M:%S %p")
        portfolio = ev.get("portfolio", "Reconstruction")

        rows.append({
            "Portfolio":   f"{portfolio} (Reconstruction)",
            "Coin Name":   ev["asset"],
            "Coin Symbol": ev["asset"],
            "Exchange":    "",
            "Pair":        "",
            "Type":        "Buy",
            "Amount":      missing_qty,
            "Price":       "",
            "Price CAD":   price_cad,
            "Fee Percent": "",
            "Fee Amount":  "",
            "Fee Currency": "",
            "Date":        anchor_date,
            "Notes":       CAUSE_NOTES.get(cause, CAUSE_NOTES["unknown"]),
            "anchor_cause":      cause,
            "anchor_confidence": ev.get("cause_confidence", 0.5),
            "anchor_value_cad":  round(price_cad * missing_qty, 2),
        })

    return pd.DataFrame(rows)


def rank_priority(classified_missing: pd.DataFrame) -> pd.DataFrame:
    """Rank missing events by tax impact: largest gains first.

    The ranking score is the imputed gain on the missing portion, weighted by
    (1 - cause_confidence) so high-confidence stablecoin redemptions sink to
    the bottom (we already know how to fix them).
    """
    if classified_missing.empty:
        return classified_missing
    df = classified_missing.copy()
    df["_weight"] = 1.0 - df["cause_confidence"].astype(float).fillna(0.5) * 0.5
    df["priority_score"] = (df["gain_on_missing_cad"].astype(float) * df["_weight"]).round(2)
    df = df.sort_values("priority_score", ascending=False).drop(columns=["_weight"]).reset_index(drop=True)
    df.insert(0, "priority_rank", df.index + 1)
    return df
