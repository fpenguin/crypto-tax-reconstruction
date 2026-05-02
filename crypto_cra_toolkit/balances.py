"""Year-end (Dec 31) token balances + CAD valuation.

How balances are computed
-------------------------
The ACB engine already stamps ``engine_acb_qty_after`` (and ``engine_acb_cad_after``)
on every processed row. For each calendar year, we take the *last* such value
per canonical asset on or before Dec 31 — that's the closing position. Years
where an asset had no activity carry forward the previous year's snapshot.

Display symbol vs canonical bucket
----------------------------------
The pool is keyed on the canonical bucket (so ETH and WETH share a pool), but
users want to see them under a recognisable name. We use the most recent
non-empty display symbol seen in that bucket.

CAD valuation
-------------
Each balance is paired with the most recent non-zero ``price_cad`` observed
for the asset on or before the snapshot date. This gives you a defensible
"closest-known price" valuation; it is not a guarantee of Dec-31 spot price.
A user wanting strict CRA-aligned year-end FMV should override these prices
from a historical-price service.

Dust filter
-----------
``dust_threshold_cad`` removes rows where the |CAD value| is below the cutoff
*and* the absolute quantity is below 1 unit. This keeps small fractional
positions of high-value assets visible (e.g. 0.0001 BTC) while hiding
6-decimal scrap dust (e.g. 0.00000123 SHIB).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import pandas as pd

# Fiat held inside crypto exchanges (Coinbase USD account, NDAX CAD, Korean
# fiat exchanges) is not a crypto asset and shouldn't show up in year-end
# *crypto* holdings. The engine still tracks them internally (so the CAD
# proceeds of crypto→fiat sales remain accurate), but the balances report
# hides them by default.
FIAT_SYMBOLS_BLOCKLIST: set[str] = {"USD", "CAD", "EUR", "GBP", "KRW", "JPY", "AUD"}


@dataclass
class BalanceSnapshot:
    year: int
    asset_canonical: str
    asset_display: str
    qty: float
    acb_cad: float
    price_cad: float
    value_cad: float
    last_activity_date: Optional[pd.Timestamp]


def compute_year_end_balances(
    annotated_df: pd.DataFrame,
    dust_threshold_cad: float = 0.05,
) -> pd.DataFrame:
    """Return a long-format frame of year-end positions per (year, asset).

    Columns: year, asset, asset_canonical, qty, acb_cad, avg_acb_per_unit_cad,
    price_cad, value_cad, last_activity_date, is_dust.
    """
    if annotated_df.empty:
        return pd.DataFrame(columns=[
            "year", "asset", "asset_canonical", "qty", "acb_cad",
            "avg_acb_per_unit_cad", "price_cad", "value_cad",
            "last_activity_date", "is_dust",
        ])

    df = annotated_df.copy()
    df = df[df["engine_acb_qty_after"].notna()].copy()
    df["engine_acb_qty_after"] = df["engine_acb_qty_after"].astype(float)
    df["engine_acb_cad_after"] = df["engine_acb_cad_after"].astype(float)
    df = df.sort_values("date").reset_index(drop=True)

    if df.empty:
        return pd.DataFrame()

    # Snapshot every calendar year between first and last activity (inclusive)
    # so quiet years still appear with forward-filled balances.
    activity_years = df["year"].dropna().astype(int)
    years = list(range(int(activity_years.min()), int(activity_years.max()) + 1))
    canonicals = df["asset_canonical"].unique()

    # For each canonical asset, build its full activity timeline, then for each
    # target year find the last row with date.year <= target_year.
    snapshots: List[BalanceSnapshot] = []

    # Pre-index by canonical asset for fast lookup.
    by_asset: Dict[str, pd.DataFrame] = {
        canon: g.sort_values("date").reset_index(drop=True)
        for canon, g in df.groupby("asset_canonical", dropna=False)
    }

    for canon in canonicals:
        timeline = by_asset[canon]
        # Most recent non-empty display symbol — used for the report label.
        display_candidates = timeline.loc[
            timeline["asset"].astype(str).str.len() > 0, "asset"
        ]
        display = display_candidates.iloc[-1] if not display_candidates.empty else canon

        for y in years:
            cutoff = pd.Timestamp(year=int(y), month=12, day=31, hour=23, minute=59, second=59)
            relevant = timeline[timeline["date"] <= cutoff]
            if relevant.empty:
                continue  # asset didn't exist yet at end of this year
            last = relevant.iloc[-1]
            qty = float(last["engine_acb_qty_after"])
            acb = float(last["engine_acb_cad_after"])

            # Most recent non-zero price for valuation.
            priced = relevant[relevant["price_cad"].astype(float) > 0]
            price = float(priced.iloc[-1]["price_cad"]) if not priced.empty else 0.0
            value = qty * price

            snapshots.append(BalanceSnapshot(
                year=int(y),
                asset_canonical=str(canon),
                asset_display=str(display),
                qty=qty,
                acb_cad=acb,
                price_cad=price,
                value_cad=value,
                last_activity_date=last["date"],
            ))

    out = pd.DataFrame([{
        "year": s.year,
        "asset": s.asset_display,
        "asset_canonical": s.asset_canonical,
        "qty": s.qty,
        "acb_cad": round(s.acb_cad, 2),
        "avg_acb_per_unit_cad": round(s.acb_cad / s.qty, 6) if s.qty > 0 else 0.0,
        "price_cad": round(s.price_cad, 6),
        "value_cad": round(s.value_cad, 2),
        "last_activity_date": s.last_activity_date,
    } for s in snapshots])

    if out.empty:
        return out

    # Dust mask: small CAD value AND small absolute quantity. This keeps a few
    # thousand SHIB visible if it's worth $0.10, but hides 0.000003 of a token
    # whose price we never knew.
    out["is_dust"] = (out["value_cad"].abs() < dust_threshold_cad) & (out["qty"].abs() < 1.0)

    # Mark fiat held in exchanges as dust by default — the user usually doesn't
    # think of "USD on Coinbase" as a crypto holding.
    out.loc[out["asset"].isin(FIAT_SYMBOLS_BLOCKLIST), "is_dust"] = True

    return out.sort_values(["year", "value_cad"], ascending=[True, False]).reset_index(drop=True)


def latest_year_summary(balances: pd.DataFrame) -> pd.DataFrame:
    """Return only the most recent year's non-dust positions, sorted by value."""
    if balances.empty:
        return balances
    last_year = int(balances["year"].max())
    out = balances[(balances["year"] == last_year) & (~balances["is_dust"])].copy()
    return out.sort_values("value_cad", ascending=False).reset_index(drop=True)
