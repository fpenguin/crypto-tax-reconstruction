"""Transfer matcher — pair Sent rows with Received rows.

A matched pair is treated as a non-taxable wallet-to-wallet transfer:
the Sent side is no longer a fake disposal, and the Received side is no longer
a phantom acquisition. Unmatched Sent/Received rows are kept as-is so the rest
of the pipeline can reason about them.

Matching criteria
-----------------
* Same canonical asset (so ETH↔WETH, USDT↔BSC-USD count as the same coin
  at lower confidence).
* |sent.amount - received.amount| / max(amount) <= ``tolerance`` (default 1%).
  Crypto bridges and L2 deposits frequently shave a small fee off the amount
  delivered, hence the tolerance band.
* Received timestamp is within ``window`` of the Sent timestamp.
  Default ±10 minutes; bridges (Wormhole, Stargate, etc.) can take longer, so
  callers can widen the window for those cases.
* Only pair rows from *different* portfolios. A Send + Receive on the same
  wallet at the same instant is almost always a contract interaction, not a
  transfer (and we want the DeFi swap detector to see it instead).
* Each row matches at most once. We greedy-match earliest-Sent → nearest-Received
  inside the window so deterministic.

Confidence scoring
------------------
Each match gets a confidence in [0, 1]:
  +0.5  base (same canonical asset within window)
  +0.2  exact symbol match (no wrap/bridge mapping needed)
  +0.2  amount difference < 0.1 %
  +0.1  time difference < 60 s
  -0.2  amount difference > 0.5 %  (likely fee'd by bridge — still a transfer)

Output
------
The matched dataframe is annotated with two new columns:
* ``transfer_match_id``  unique id; same id on the Sent and Received rows
* ``transfer_confidence`` [0,1] confidence
* ``transfer_role``       'sent' or 'received'
* ``is_matched_transfer`` bool, True on both sides of a match
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import pandas as pd


@dataclass
class TransferMatchSummary:
    total_sent: int = 0
    total_received: int = 0
    matched_pairs: int = 0
    matched_sent: int = 0
    matched_received: int = 0
    avg_confidence: float = 0.0
    cross_symbol_matches: int = 0  # ETH↔WETH style
    notes: List[str] = field(default_factory=list)


def _confidence(
    sent_amt: float,
    rec_amt: float,
    sent_time: pd.Timestamp,
    rec_time: pd.Timestamp,
    same_symbol: bool,
) -> float:
    score = 0.5
    if same_symbol:
        score += 0.2
    diff = abs(sent_amt - rec_amt) / max(sent_amt, rec_amt, 1e-12)
    if diff < 0.001:
        score += 0.2
    if diff > 0.005:
        score -= 0.2
    if abs((rec_time - sent_time).total_seconds()) < 60:
        score += 0.1
    return max(0.0, min(1.0, score))


def match_transfers(
    df: pd.DataFrame,
    window_minutes: int = 10,
    tolerance: float = 0.01,
) -> tuple[pd.DataFrame, TransferMatchSummary]:
    """Return (annotated_df, summary). df is not mutated."""
    out = df.copy()
    out["transfer_match_id"] = pd.NA
    out["transfer_confidence"] = pd.NA
    out["transfer_role"] = pd.NA
    out["is_matched_transfer"] = False

    summary = TransferMatchSummary()
    summary.total_sent = int((out["type_norm"] == "sent").sum())
    summary.total_received = int((out["type_norm"] == "received").sum())

    window = pd.Timedelta(minutes=window_minutes)
    rec_taken: set[int] = set()  # received-row index pool
    confidences: List[float] = []
    next_id = 1

    # Iterate Sent rows oldest→newest. For each, scan candidate Received rows in
    # the same canonical-asset bucket within the window, pick the highest score.
    rec_by_asset: Dict[str, List[int]] = {}
    rec_view = out[out["type_norm"] == "received"].sort_values("date")
    for idx, row in rec_view.iterrows():
        rec_by_asset.setdefault(row["asset_canonical"], []).append(idx)

    sent_view = out[out["type_norm"] == "sent"].sort_values("date")
    for sidx, srow in sent_view.iterrows():
        if srow["amount_abs"] <= 0:
            continue
        candidates = rec_by_asset.get(srow["asset_canonical"], [])
        best_idx: Optional[int] = None
        best_score = -1.0
        best_diff = 1.0
        for ridx in candidates:
            if ridx in rec_taken:
                continue
            rrow = out.loc[ridx]
            dt = rrow["date"] - srow["date"]
            # Received must come at-or-after Sent (allow 60s slack for clock skew).
            if dt < -pd.Timedelta(seconds=60) or dt > window:
                continue
            if rrow["Portfolio"] == srow["Portfolio"]:
                continue  # likely contract interaction, not a transfer
            ramt, samt = float(rrow["amount_abs"]), float(srow["amount_abs"])
            if max(samt, ramt) <= 0:
                continue
            diff = abs(samt - ramt) / max(samt, ramt)
            if diff > tolerance:
                continue
            same_symbol = (str(rrow["asset"]).upper() == str(srow["asset"]).upper())
            score = _confidence(samt, ramt, srow["date"], rrow["date"], same_symbol)
            # Prefer higher confidence; break ties on smaller amount diff,
            # then on earlier received timestamp (most adjacent).
            better = (
                score > best_score
                or (score == best_score and diff < best_diff)
            )
            if better:
                best_score = score
                best_idx = ridx
                best_diff = diff

        if best_idx is None:
            continue

        match_id = f"T{next_id:06d}"
        next_id += 1
        out.at[sidx, "transfer_match_id"] = match_id
        out.at[best_idx, "transfer_match_id"] = match_id
        out.at[sidx, "transfer_confidence"] = best_score
        out.at[best_idx, "transfer_confidence"] = best_score
        out.at[sidx, "transfer_role"] = "sent"
        out.at[best_idx, "transfer_role"] = "received"
        out.at[sidx, "is_matched_transfer"] = True
        out.at[best_idx, "is_matched_transfer"] = True
        rec_taken.add(best_idx)

        confidences.append(best_score)
        summary.matched_pairs += 1
        if str(out.at[sidx, "asset"]).upper() != str(out.at[best_idx, "asset"]).upper():
            summary.cross_symbol_matches += 1

    summary.matched_sent = summary.matched_pairs
    summary.matched_received = summary.matched_pairs
    summary.avg_confidence = (
        round(sum(confidences) / len(confidences), 3) if confidences else 0.0
    )
    return out, summary
