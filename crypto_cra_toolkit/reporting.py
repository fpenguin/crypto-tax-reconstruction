"""Reporting — write CSV outputs and the Markdown audit memo."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Optional

import pandas as pd  # noqa: F401  (used in type annotations)

from .acb_engine import ACBResult
from .transfer_matcher import TransferMatchSummary
from .defi_detector import SwapDetectorSummary


CSV_FILES = {
    "clean_transactions":     "clean_transactions.csv",
    "report":                 "cra_asset_year_report.csv",
    "yearly_totals":          "cra_yearly_totals.csv",
    "missing":                "missing_purchase_history.csv",
    "type_summary":           "transaction_type_summary.csv",
    "review":                 "review_required_transactions.csv",
    "fee_mismatch":           "fee_currency_mismatch.csv",
    "transfers":              "matched_transfers.csv",
    "swaps":                  "defi_swaps.csv",
    "anchors":                "anchor_buy_entries.csv",
    "priority":               "priority_fix_ranking.csv",
    "balances":               "year_end_balances.csv",
}


def write_outputs(
    outdir: Path,
    annotated_df: pd.DataFrame,
    acb: ACBResult,
    classified_missing: pd.DataFrame,
    priority: pd.DataFrame,
    anchors: pd.DataFrame,
    transfer_summary: TransferMatchSummary,
    swap_summary: SwapDetectorSummary,
    settings: dict,
    balances: Optional[pd.DataFrame] = None,
) -> dict[str, Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    paths = {key: outdir / name for key, name in CSV_FILES.items()}

    annotated_df.to_csv(paths["clean_transactions"], index=False)
    acb.report.to_csv(paths["report"], index=False)
    acb.yearly_totals.to_csv(paths["yearly_totals"], index=False)
    classified_missing.to_csv(paths["missing"], index=False)
    acb.type_summary.to_csv(paths["type_summary"], index=False)
    acb.review_events.to_csv(paths["review"], index=False)

    fee_mm = annotated_df[annotated_df["fee_currency_mismatch"]].copy()
    fee_mm[["date", "asset", "fee_amount", "fee_currency", "Portfolio", "Notes"]].to_csv(
        paths["fee_mismatch"], index=False
    )

    transfers = annotated_df[annotated_df["is_matched_transfer"]].copy()
    transfers = transfers[[
        "transfer_match_id", "transfer_role", "transfer_confidence",
        "asset", "amount_abs", "date", "Portfolio", "value_cad",
    ]].sort_values(["transfer_match_id", "transfer_role"])
    transfers.to_csv(paths["transfers"], index=False)

    swaps = annotated_df[annotated_df["swap_id"].notna()].copy()
    swaps = swaps[[
        "swap_id", "swap_role", "asset", "amount_abs", "value_cad",
        "date", "Portfolio",
    ]].sort_values(["swap_id", "swap_role"])
    swaps.to_csv(paths["swaps"], index=False)

    anchors.to_csv(paths["anchors"], index=False)
    priority.to_csv(paths["priority"], index=False)

    if balances is not None and not balances.empty:
        if settings.get("include_dust_in_balances", False):
            balances.to_csv(paths["balances"], index=False)
        else:
            # Default: hide dust from year-end balances output. The dust is
            # still computed (we know exactly what's flagged), it's just
            # withheld from the CSV the user opens to reduce noise. They can
            # opt back in with --include-dust-balances.
            balances[~balances["is_dust"]].to_csv(paths["balances"], index=False)
    else:
        # Always create the file, even if empty, so downstream tools don't break.
        pd.DataFrame().to_csv(paths["balances"], index=False)

    memo_path = outdir / "audit_memo.md"
    memo_path.write_text(_render_memo(
        acb=acb,
        classified_missing=classified_missing,
        priority=priority,
        anchors=anchors,
        transfer_summary=transfer_summary,
        swap_summary=swap_summary,
        settings=settings,
        balances=balances,
    ))
    paths["memo"] = memo_path
    return paths


def _render_memo(
    acb: ACBResult,
    classified_missing: pd.DataFrame,
    priority: pd.DataFrame,
    anchors: pd.DataFrame,
    transfer_summary: TransferMatchSummary,
    swap_summary: SwapDetectorSummary,
    settings: dict,
    balances: Optional[pd.DataFrame] = None,
) -> str:
    lines: list[str] = []
    lines.append("# CRA Crypto Reconstruction — Audit Memo")
    lines.append("")
    lines.append(f"_Generated: {pd.Timestamp.utcnow():%Y-%m-%d %H:%M UTC}_")
    lines.append("")

    lines.append("## Methodology")
    lines.append("")
    lines.append(
        "This reconstruction follows the Canada Revenue Agency's identical-property "
        "(adjusted cost base) rule. ACB is pooled **globally per asset across all "
        "wallets and exchanges**, including bridged/wrapped equivalents (e.g. "
        "ETH ↔ WETH). The pipeline is forensic, not bookkeeping: it detects "
        "transfers between the user's own wallets, separates them from real "
        "dispositions, classifies the root cause of any missing acquisition "
        "history, and proposes the smallest defensible set of anchor entries "
        "needed to close the gaps."
    )
    lines.append("")

    lines.append("## Pipeline configuration")
    lines.append("")
    for k, v in settings.items():
        lines.append(f"- **{k}**: `{v}`")
    lines.append("")

    lines.append("## Stage 1 — Transfer matching")
    lines.append("")
    lines.append(
        f"Sent rows considered: {transfer_summary.total_sent}. "
        f"Received rows considered: {transfer_summary.total_received}. "
        f"Pairs matched: **{transfer_summary.matched_pairs}** at average "
        f"confidence **{transfer_summary.avg_confidence}**, of which "
        f"{transfer_summary.cross_symbol_matches} crossed wrapped/bridged symbols. "
        "Matched pairs are excluded from ACB calculations as non-taxable "
        "wallet-to-wallet movements."
    )
    lines.append("")

    lines.append("## Stage 2 — DeFi swap detection")
    lines.append("")
    lines.append(
        f"Sell rows: {swap_summary.sell_rows}. Buy rows: {swap_summary.buy_rows}. "
        f"Swap pairs detected: **{swap_summary.swaps_detected}**. "
        f"Sells without a paired Buy: {swap_summary.sells_unpaired}. "
        "Detected pairs let the engine see Sell→Buy swaps as one economic event "
        "and surface unpaired Sells as candidates for missing acquisition history."
    )
    lines.append("")

    lines.append("## Stage 3 — Yearly capital gains")
    lines.append("")
    if acb.yearly_totals.empty:
        lines.append("_No taxable activity computed._")
    else:
        lines.append("```")
        lines.append(acb.yearly_totals.to_string(index=False))
        lines.append("```")
    lines.append("")

    lines.append("## Stage 4 — Missing-ACB analysis")
    lines.append("")
    if classified_missing.empty:
        lines.append("_No missing-ACB events under the chosen assumptions._")
    else:
        cause_counts = classified_missing["cause"].value_counts()
        lines.append(f"Total missing-ACB events: **{len(classified_missing)}**")
        lines.append("")
        lines.append("| Root cause | Events |")
        lines.append("|---|---|")
        for cause, n in cause_counts.items():
            lines.append(f"| {cause} | {n} |")
        lines.append("")
        suspicious = int(classified_missing.get("suspicious", pd.Series(dtype=bool)).sum())
        lines.append(
            f"Suspicious-gain flags (gain > threshold on a missing-ACB sale): **{suspicious}**."
        )
    lines.append("")

    lines.append("## Stage 5 — Priority fix ranking (top 10)")
    lines.append("")
    if priority.empty:
        lines.append("_Nothing to rank._")
    else:
        cols = [
            "priority_rank", "date", "asset", "qty_sold", "missing_qty",
            "proceeds_cad", "gain_on_missing_cad", "cause", "cause_confidence",
        ]
        cols = [c for c in cols if c in priority.columns]
        top = priority.head(10)[cols].copy()
        if "date" in top.columns:
            top["date"] = pd.to_datetime(top["date"]).dt.strftime("%Y-%m-%d")
        lines.append("```")
        lines.append(top.to_string(index=False))
        lines.append("```")
    lines.append("")

    lines.append("## Stage 6 — Anchor entries proposed")
    lines.append("")
    if anchors.empty:
        lines.append("_No anchor entries needed._")
    else:
        lines.append(
            f"Generated **{len(anchors)}** anchor Buy rows in `anchor_buy_entries.csv`. "
            "Re-run the pipeline with that file as a manual source to confirm the gaps "
            "close. Replace placeholder prices with real fiat-onramp / FMV records "
            "before filing."
        )
        cause_breakdown = anchors["anchor_cause"].value_counts()
        lines.append("")
        lines.append("| Anchor cause | Count | Total CAD value |")
        lines.append("|---|---|---|")
        for cause, n in cause_breakdown.items():
            total = anchors.loc[anchors["anchor_cause"] == cause, "anchor_value_cad"].sum()
            lines.append(f"| {cause} | {n} | {total:,.2f} |")
    lines.append("")

    lines.append("## Stage 7 — Year-end balances")
    lines.append("")
    if balances is None or balances.empty:
        lines.append("_Year-end balances not computed._")
    else:
        non_dust = balances[~balances["is_dust"]]
        last_year = int(balances["year"].max())
        last_year_view = non_dust[non_dust["year"] == last_year].head(15)
        lines.append(
            f"Closing positions per asset are written to `year_end_balances.csv`. "
            f"Filter applied: dust positions worth less than "
            f"`{settings.get('dust_threshold_cad', 0.05)}` CAD AND under 1 unit "
            f"are tagged but kept (set `is_dust=True`) so you can audit them. "
            f"Top {len(last_year_view)} non-dust positions for {last_year}:"
        )
        lines.append("")
        if not last_year_view.empty:
            cols = ["asset", "qty", "acb_cad", "price_cad", "value_cad"]
            view = last_year_view[cols].copy()
            view["qty"] = view["qty"].map(lambda x: f"{x:.6f}".rstrip("0").rstrip(".") or "0")
            lines.append("```")
            lines.append(view.to_string(index=False))
            lines.append("```")
    lines.append("")

    lines.append("## Stage 8 — Platforms acknowledged but not integrated (immateriality)")
    lines.append("")
    lines.append(
        "Platforms with activity below the integration materiality threshold "
        "should be documented here for transparency but need not be added as "
        "line items in the engine. Document the platform, the period of use, "
        "the supporting evidence on file, the estimated total tax impact, and "
        "the reason the user chose not to integrate (typically: residual "
        "balance is dust, or interest income is below filer's chosen materiality "
        "threshold). Update this section when adding new manual entries."
    )
    lines.append("")
    lines.append("## Assumptions and caveats")
    lines.append("")
    lines.append(
        "- Symbol equivalence groups (parser.SYMBOL_EQUIVALENCE) are conservative; "
        "less-common wraps/bridges may not match and would surface as missing ACB."
    )
    lines.append(
        "- The transfer matcher uses a ±10-minute window and 1% amount tolerance "
        "by default; bridges with longer settlement may need a wider window."
    )
    lines.append(
        "- Fees in a currency different from the traded asset are set to 0 CAD "
        "and surfaced in `fee_currency_mismatch.csv` for manual pricing."
    )
    lines.append(
        "- Anchor entries are placeholders, not facts: they are sized to close the "
        "ACB gap mathematically. Replace with documented fiat / FMV records before "
        "filing. The CRA expects best-evidence reconstruction, not perfection."
    )
    lines.append(
        "- This tool is a reconstruction aid, not tax advice. Have a Canadian "
        "CPA or crypto-tax specialist review before filing."
    )
    lines.append("")

    return "\n".join(lines)
