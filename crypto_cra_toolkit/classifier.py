"""Root-cause classifier for missing-ACB events.

Each missing event is labelled with one of:

* ``transfer_in_unmatched``    — unmatched Received row exists for this asset
                                 *before* the sale on a *different* portfolio.
                                 Fix: extend the matcher window or import the
                                 source wallet's history.
* ``fiat_origin_missing``      — major coin (BTC, ETH, ...) sold in early years
                                 with no prior Buy. Fix: import fiat-onramp
                                 records (NDAX, Coinbase, KRW exchange).
* ``defi_swap_missing``        — DeFi/altcoin sold without a prior Buy and
                                 the wallet has many other swap rows. Fix:
                                 import the DEX history or trace the swap.
* ``stablecoin_redeem``        — sale of USDC/USDT/DAI/etc. → ACB ≈ proceeds,
                                 no real gain. Fix: stamp $1 ≈ par as ACB.
* ``airdrop_or_income``        — only Received rows for this asset appear in
                                 history; no Buy and no Sent counter-party.
                                 Fix: book FMV at receipt as Other Income.
* ``unknown``                  — none of the above.

A confidence in [0,1] is attached to each label so the priority ranker can
weight them.
"""

from __future__ import annotations

from typing import Iterable, List

import pandas as pd

from .parser import MAJOR_COINS, STABLECOINS


EARLY_FIAT_CUTOFF_YEAR = 2022  # Sales of major coins before this are likely fiat-origin.


def _has_prior_unmatched_received(df: pd.DataFrame, asset_canon: str, before_date) -> bool:
    cand = df[
        (df["asset_canonical"] == asset_canon)
        & (df["type_norm"] == "received")
        & (df["date"] < before_date)
        & (~df["is_matched_transfer"].fillna(False))
    ]
    return len(cand) > 0


def _has_only_received(df: pd.DataFrame, asset_canon: str, before_date) -> bool:
    cand = df[(df["asset_canonical"] == asset_canon) & (df["date"] < before_date)]
    if cand.empty:
        return False
    types = set(cand["type_norm"].unique())
    return ("received" in types) and not (types & {"buy", "sent"})


def _is_defi_token(asset: str) -> bool:
    if asset in MAJOR_COINS or asset in STABLECOINS:
        return False
    if len(asset) > 25:  # raw contract address — definitely DeFi
        return True
    return True  # everything else: treat as DeFi-ish for now


def classify_missing(
    annotated_df: pd.DataFrame,
    missing_events: pd.DataFrame,
) -> pd.DataFrame:
    """Add cause + confidence columns to the missing-events frame.

    annotated_df is the post-engine frame; missing_events comes from ACBResult.
    """
    if missing_events.empty:
        return missing_events.assign(cause=[], cause_confidence=[], suggestion=[])

    causes: List[str] = []
    confidences: List[float] = []
    suggestions: List[str] = []

    for _, ev in missing_events.iterrows():
        asset = ev["asset"]
        asset_canon = ev["asset_canonical"]
        date = ev["date"]
        year = ev["year"]
        portfolio = ev.get("portfolio", "")

        # Order matters: check the most specific signals first.
        if asset_canon in STABLECOINS:
            causes.append("stablecoin_redeem")
            confidences.append(0.95)
            suggestions.append(
                "Stamp ACB ≈ 1 USD/CAD per unit (par). Add a Buy at $1 CAD per unit "
                "for the missing quantity, dated ≥1 day before the sale."
            )
            continue

        # Only-ever-Received before this sale and no Sent counterparty is a much
        # stronger airdrop signal than the generic "prior unmatched Received"
        # check below, so it must run first.
        if _has_only_received(annotated_df, asset_canon, date):
            causes.append("airdrop_or_income")
            confidences.append(0.7)
            suggestions.append(
                "All prior history for this asset is Received — likely an airdrop, "
                "staking reward, or game reward. Book FMV at receipt as Other Income; "
                "that becomes the ACB."
            )
            continue

        if _has_prior_unmatched_received(annotated_df, asset_canon, date):
            causes.append("transfer_in_unmatched")
            confidences.append(0.85)
            suggestions.append(
                "Widen the transfer-match window or import the source wallet/exchange "
                "where this asset was originally bought. Likely a real transfer, not a buy."
            )
            continue

        if asset_canon in MAJOR_COINS and year <= EARLY_FIAT_CUTOFF_YEAR:
            causes.append("fiat_origin_missing")
            confidences.append(0.8)
            suggestions.append(
                "Add the fiat-onramp purchase that funded this asset (NDAX, Coinbase, "
                "or local fiat exchange). Use the fiat statement amount as ACB."
            )
            continue

        if _is_defi_token(asset):
            causes.append("defi_swap_missing")
            confidences.append(0.6)
            suggestions.append(
                "Likely acquired via DEX swap (Uniswap, PancakeSwap, …) that wasn't "
                "captured. Trace the swap on the explorer; the CAD value of the asset "
                "you spent on that swap is the ACB."
            )
            continue

        causes.append("unknown")
        confidences.append(0.3)
        suggestions.append("No automatic classification — review on-chain history.")

    out = missing_events.copy()
    out["cause"] = causes
    out["cause_confidence"] = confidences
    out["suggestion"] = suggestions
    return out
