"""DeFi swap detector — link Sell A + Buy B that occurred together.

Why
---
Most CoinStats Sell+Buy rows on a Metamask wallet at the same timestamp are a
single Uniswap-style swap: you spent token A and received token B in one tx.
Tagging them as a swap pair lets us:
1. confirm the Buy side is *not* a fiat acquisition (it inherits cost basis
   from the Sell side's proceeds);
2. surface "swap with no Sell side" cases where the user disposed of an asset
   we had no record of acquiring.

Heuristic
---------
Sell row at time T with same Portfolio as a Buy row at time T (or within
``window_seconds``) => one swap. We do not require equal CAD value because
slippage and price-feed lag often disagree. We require both rows to have a
non-zero Price CAD; otherwise the link is too speculative.

Output columns added
--------------------
* ``swap_id``    — unique id per pair, repeated on the Sell and Buy rows
* ``swap_role``  — "sell" or "buy"
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd


@dataclass
class SwapDetectorSummary:
    sell_rows: int = 0
    buy_rows: int = 0
    swaps_detected: int = 0
    sells_paired: int = 0
    buys_paired: int = 0
    sells_unpaired: int = 0


def detect_defi_swaps(df: pd.DataFrame, window_seconds: int = 120) -> tuple[pd.DataFrame, SwapDetectorSummary]:
    out = df.copy()
    out["swap_id"] = pd.NA
    out["swap_role"] = pd.NA

    summary = SwapDetectorSummary()
    summary.sell_rows = int((out["type_norm"] == "sell").sum())
    summary.buy_rows = int((out["type_norm"] == "buy").sum())

    win = pd.Timedelta(seconds=window_seconds)

    # Index Buy rows by Portfolio for quick neighbour lookup.
    buys_by_portfolio: Dict[str, List[int]] = {}
    buys = out[out["type_norm"] == "buy"].sort_values("date")
    for idx, row in buys.iterrows():
        buys_by_portfolio.setdefault(str(row["Portfolio"]), []).append(idx)

    used_buys: set[int] = set()
    next_id = 1
    sells = out[out["type_norm"] == "sell"].sort_values("date")
    for sidx, srow in sells.iterrows():
        candidates = buys_by_portfolio.get(str(srow["Portfolio"]), [])
        best_idx = None
        best_dt = win + pd.Timedelta(seconds=1)
        for bidx in candidates:
            if bidx in used_buys:
                continue
            brow = out.loc[bidx]
            dt = abs(brow["date"] - srow["date"])
            if dt > win:
                continue
            # Don't pair a Sell of asset X with a Buy of the same asset X — that's
            # not a swap (and would imply a same-asset round-trip).
            if str(brow["asset"]).upper() == str(srow["asset"]).upper():
                continue
            if dt < best_dt:
                best_dt = dt
                best_idx = bidx
        if best_idx is None:
            summary.sells_unpaired += 1
            continue
        sid = f"S{next_id:06d}"
        next_id += 1
        out.at[sidx, "swap_id"] = sid
        out.at[sidx, "swap_role"] = "sell"
        out.at[best_idx, "swap_id"] = sid
        out.at[best_idx, "swap_role"] = "buy"
        used_buys.add(best_idx)
        summary.swaps_detected += 1
        summary.sells_paired += 1
        summary.buys_paired += 1

    return out, summary
