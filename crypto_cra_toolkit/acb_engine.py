"""ACB engine — Canadian-style Adjusted Cost Base pooling, with audit lineage.

Key design decisions
--------------------
1. **Global pool per asset.** The CRA requires identical-property pooling
   across *all* wallets and exchanges. The pool is keyed by canonical asset
   (so ETH and WETH share a pool — see parser.SYMBOL_EQUIVALENCE).
2. **Matched transfers are skipped.** The transfer matcher tags Sent/Received
   pairs that are wallet-to-wallet hops; those are not taxable events and
   don't move the ACB pool.
3. **Unmatched Received = optional provisional ACB.** When a Received row
   couldn't be matched and the caller has set ``use_received_as_provisional_acb``,
   we treat it as a fresh acquisition at the row's CAD price. Otherwise we
   skip it (so it can be flagged elsewhere as a possible airdrop/income event).
4. **Suspicious gain detector.** Whenever a sale draws on missing ACB and the
   imputed gain is large, we flag it so the priority-fix rank can surface it.
5. **Audit lineage.** Every disposal records the running pool state both
   pre- and post-trade plus the assumption used for any missing portion. The
   reconstruction module reads this to draft anchor entries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import pandas as pd

from .parser import (
    ACQUISITION_TYPES,
    FEE_TYPES,
    REVIEW_TYPES,
    TAXABLE_DISPOSAL_TYPES,
)


SUSPICIOUS_GAIN_CAD_DEFAULT = 1000.0  # gains above this on a missing-ACB sale are flagged


@dataclass
class LotState:
    qty: float = 0.0
    acb: float = 0.0

    def average_cost(self) -> float:
        return 0.0 if self.qty <= 0 else self.acb / self.qty


@dataclass
class AssetYearSummary:
    year: int
    asset: str
    proceeds_cad: float = 0.0
    acb_used_cad: float = 0.0
    disposition_fees_cad: float = 0.0
    gain_loss_cad: float = 0.0
    buys_cad: float = 0.0
    buys_qty: float = 0.0
    sells_qty: float = 0.0
    missing_qty: float = 0.0
    missing_acb_assumed_cad: float = 0.0
    suspicious_gain_events: int = 0
    warnings: List[str] = field(default_factory=list)


@dataclass
class ACBResult:
    report: pd.DataFrame
    yearly_totals: pd.DataFrame
    missing_events: pd.DataFrame
    review_events: pd.DataFrame
    type_summary: pd.DataFrame
    annotated: pd.DataFrame  # input frame plus per-row engine columns


def _summary_for(
    summaries: Dict[tuple[int, str], AssetYearSummary], year: int, asset: str
) -> AssetYearSummary:
    key = (year, asset)
    if key not in summaries:
        summaries[key] = AssetYearSummary(year=year, asset=asset)
    return summaries[key]


def run_acb(
    df: pd.DataFrame,
    assume_missing_acb: str = "zero",
    use_received_as_provisional_acb: bool = False,
    suspicious_gain_threshold_cad: float = SUSPICIOUS_GAIN_CAD_DEFAULT,
) -> ACBResult:
    """Compute global ACB and yearly gain/loss.

    df must already be:
      * deduped + normalized (parser)
      * annotated with transfer_match_id (transfer_matcher)
      * optionally annotated with swap_id (defi_detector)
    """
    out = df.copy()
    # Engine annotations on the source frame.
    for col in (
        "engine_acb_qty_before", "engine_acb_qty_after",
        "engine_acb_cad_before", "engine_acb_cad_after",
        "engine_acb_used_cad", "engine_missing_qty",
        "engine_assumed_acb_cad", "engine_role", "engine_suspicious_gain",
    ):
        out[col] = pd.NA

    states: Dict[str, LotState] = {}
    summaries: Dict[tuple[int, str], AssetYearSummary] = {}
    missing_events: List[dict] = []
    review_events: List[dict] = []

    for idx, row in out.iterrows():
        asset_canon = row["asset_canonical"]
        asset = row["asset"]
        typ = row["type_norm"]
        try:
            year = int(row["year"])
        except (TypeError, ValueError):
            continue
        qty = float(row["amount_abs"])
        value = float(row["value_cad"])
        date = row["date"]
        fee_cad = float(row["fee_value_cad_est"])
        is_matched_transfer = bool(row.get("is_matched_transfer", False))

        if qty <= 0:
            continue

        state = states.setdefault(asset_canon, LotState())
        summ = _summary_for(summaries, year, asset_canon)

        out.at[idx, "engine_acb_qty_before"] = state.qty
        out.at[idx, "engine_acb_cad_before"] = state.acb

        if typ in ACQUISITION_TYPES:
            state.qty += qty
            state.acb += value + fee_cad
            summ.buys_qty += qty
            summ.buys_cad += value + fee_cad
            out.at[idx, "engine_role"] = "buy"

        elif typ == "received":
            if is_matched_transfer:
                # Wallet-to-wallet receive: no economic change.
                out.at[idx, "engine_role"] = "transfer_in"
            elif use_received_as_provisional_acb and value > 0:
                state.qty += qty
                state.acb += value
                summ.buys_qty += qty
                summ.buys_cad += value
                summ.warnings.append("Provisional ACB from unmatched Received row.")
                out.at[idx, "engine_role"] = "provisional_buy"
            else:
                out.at[idx, "engine_role"] = "unmatched_receive"

        elif typ == "sent":
            if is_matched_transfer:
                out.at[idx, "engine_role"] = "transfer_out"
            else:
                # An unmatched Send is usually a token spend / NFT mint / external
                # gift. We don't book it as a disposal automatically because we
                # often don't know proceeds; classifier flags it for review.
                out.at[idx, "engine_role"] = "unmatched_send"

        elif typ in TAXABLE_DISPOSAL_TYPES:
            proceeds = value
            sell_qty = qty
            summ.disposition_fees_cad += fee_cad
            summ.proceeds_cad += proceeds
            summ.sells_qty += sell_qty

            if state.qty >= sell_qty and state.qty > 0:
                avg_acb = state.average_cost()
                acb_used = avg_acb * sell_qty
                state.qty -= sell_qty
                state.acb -= acb_used
                missing_qty = 0.0
                assumed = 0.0
            else:
                available = max(state.qty, 0.0)
                avg_acb = state.average_cost()
                acb_used = avg_acb * available if available > 0 else 0.0
                missing_qty = sell_qty - available
                if assume_missing_acb == "fmv":
                    assumed = proceeds * (missing_qty / sell_qty) if sell_qty else 0.0
                else:
                    assumed = 0.0
                acb_used += assumed
                summ.missing_qty += missing_qty
                summ.missing_acb_assumed_cad += assumed
                state.qty = 0.0
                state.acb = 0.0
                summ.warnings.append("Missing purchase history detected.")

                gain_on_missing = proceeds - acb_used
                suspicious = (
                    missing_qty > 0
                    and gain_on_missing > suspicious_gain_threshold_cad
                )
                if suspicious:
                    summ.suspicious_gain_events += 1
                out.at[idx, "engine_suspicious_gain"] = bool(suspicious)

                missing_events.append({
                    "date": date,
                    "year": year,
                    "asset": asset,
                    "asset_canonical": asset_canon,
                    "portfolio": row.get("Portfolio", ""),
                    "type": row.get("Type", ""),
                    "qty_sold": sell_qty,
                    "qty_available_before_sale": available,
                    "missing_qty": missing_qty,
                    "proceeds_cad": proceeds,
                    "assumed_missing_acb_cad": assumed,
                    "gain_on_missing_cad": round(gain_on_missing, 2),
                    "suspicious": suspicious,
                    "row_index": idx,
                })

            summ.acb_used_cad += acb_used
            summ.gain_loss_cad += proceeds - acb_used
            out.at[idx, "engine_role"] = "sell"
            out.at[idx, "engine_acb_used_cad"] = acb_used
            out.at[idx, "engine_missing_qty"] = missing_qty
            out.at[idx, "engine_assumed_acb_cad"] = assumed

        elif typ in FEE_TYPES:
            out.at[idx, "engine_role"] = "fee"

        elif typ in REVIEW_TYPES:
            out.at[idx, "engine_role"] = "review"
            review_events.append({
                "date": date,
                "year": year,
                "asset": asset,
                "portfolio": row.get("Portfolio", ""),
                "type": row.get("Type", ""),
                "qty": qty,
                "value_cad": round(value, 2),
                "note": _review_note(typ),
                "row_index": idx,
            })

        out.at[idx, "engine_acb_qty_after"] = state.qty
        out.at[idx, "engine_acb_cad_after"] = state.acb

    # ----- Build outputs -----
    report_rows = []
    for s in summaries.values():
        if any([s.proceeds_cad, s.acb_used_cad, s.buys_cad, s.sells_qty, s.missing_qty]):
            net = s.gain_loss_cad - s.disposition_fees_cad
            report_rows.append({
                "year": s.year,
                "asset": s.asset,
                "proceeds_cad": round(s.proceeds_cad, 2),
                "acb_used_cad": round(s.acb_used_cad, 2),
                "disposition_fees_cad": round(s.disposition_fees_cad, 2),
                "gain_loss_cad": round(net, 2),
                "taxable_capital_gain_50pct_cad": round(max(net, 0) * 0.5, 2),
                "allowable_capital_loss_50pct_cad": round(min(net, 0) * 0.5, 2),
                "buys_qty": s.buys_qty,
                "buys_cad": round(s.buys_cad, 2),
                "sells_qty": s.sells_qty,
                "missing_qty": s.missing_qty,
                "missing_acb_assumed_cad": round(s.missing_acb_assumed_cad, 2),
                "suspicious_gain_events": s.suspicious_gain_events,
                "warnings": " | ".join(sorted(set(s.warnings))),
            })

    report = (
        pd.DataFrame(report_rows).sort_values(["year", "asset"]).reset_index(drop=True)
        if report_rows else pd.DataFrame()
    )

    yearly = _yearly_totals(report)

    missing_df = pd.DataFrame(missing_events)
    review_df = pd.DataFrame(review_events)

    type_summary = (
        out.groupby(["year", "type_norm"], dropna=False)
        .agg(rows=("type_norm", "size"), value_cad=("value_cad", "sum"))
        .reset_index()
        .sort_values(["year", "type_norm"])
    )
    type_summary["value_cad"] = type_summary["value_cad"].round(2)

    return ACBResult(
        report=report,
        yearly_totals=yearly,
        missing_events=missing_df,
        review_events=review_df,
        type_summary=type_summary,
        annotated=out,
    )


def _yearly_totals(report: pd.DataFrame) -> pd.DataFrame:
    if report.empty:
        return pd.DataFrame()
    return report.groupby("year").agg(
        proceeds_cad=("proceeds_cad", "sum"),
        acb_used_cad=("acb_used_cad", "sum"),
        disposition_fees_cad=("disposition_fees_cad", "sum"),
        gain_loss_cad=("gain_loss_cad", "sum"),
        taxable_capital_gain_50pct_cad=("taxable_capital_gain_50pct_cad", "sum"),
        allowable_capital_loss_50pct_cad=("allowable_capital_loss_50pct_cad", "sum"),
        missing_qty_events=("missing_qty", lambda s: (s > 0).sum()),
        missing_acb_assumed_cad=("missing_acb_assumed_cad", "sum"),
        suspicious_gain_events=("suspicious_gain_events", "sum"),
    ).reset_index().round(2)


def _review_note(typ: str) -> str:
    if typ in {"earn unlock", "earn lock", "interest earn"}:
        return "Likely taxable income at FMV under CRA — book as Other Income."
    if typ in {"dust convert", "add liquidity", "remove liquidity"}:
        return "Potential disposal — verify with on-chain receipt."
    return "Subscription / roll event — confirm whether a disposition occurred."
