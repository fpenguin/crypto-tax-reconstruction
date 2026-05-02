#!/usr/bin/env python3
"""CLI entry point for crypto_cra_toolkit.

Examples
--------
    # Single CoinStats CSV, conservative ACB assumption:
    python3 analyze.py path/to/transactions.csv --outdir out

    # Multiple sources (CoinStats + manual NDAX-style CSV):
    python3 analyze.py coinstats.csv --manual ndax_buys.csv --outdir out

    # Use FMV for missing ACB and treat unmatched Received rows as provisional buys:
    python3 analyze.py transactions.csv \
        --assume-missing-acb fmv \
        --use-received-as-provisional-acb
"""

from __future__ import annotations

import argparse
from pathlib import Path

from crypto_cra_toolkit.parser import load_sources
from crypto_cra_toolkit.transfer_matcher import match_transfers
from crypto_cra_toolkit.defi_detector import detect_defi_swaps
from crypto_cra_toolkit.acb_engine import run_acb, SUSPICIOUS_GAIN_CAD_DEFAULT
from crypto_cra_toolkit.classifier import classify_missing
from crypto_cra_toolkit.reconstruction import build_anchor_entries, rank_priority
from crypto_cra_toolkit.balances import compute_year_end_balances, latest_year_summary
from crypto_cra_toolkit.reporting import write_outputs


def main() -> None:
    p = argparse.ArgumentParser(description="CRA crypto tax reconstruction.")
    p.add_argument("csv", type=Path, nargs="+",
                   help="One or more CoinStats CSV exports.")
    p.add_argument("--manual", type=Path, action="append", default=[],
                   help="Optional manual CSV(s) — anchor buys, NDAX exports, etc.")
    p.add_argument("--outdir", type=Path, default=Path("coinstats_tax_output"))
    p.add_argument("--exclude", action="append", default=[],
                   help="Substring filter; rows matching get dropped (repeatable).")
    p.add_argument("--assume-missing-acb", choices=["zero", "fmv"], default="zero")
    p.add_argument("--use-received-as-provisional-acb", action="store_true")
    p.add_argument("--transfer-window-minutes", type=int, default=10)
    p.add_argument("--transfer-tolerance", type=float, default=0.01)
    p.add_argument("--swap-window-seconds", type=int, default=120)
    p.add_argument("--suspicious-gain-cad",
                   type=float, default=SUSPICIOUS_GAIN_CAD_DEFAULT)
    p.add_argument("--dust-threshold-cad", type=float, default=1.00,
                   help="Year-end balances below this CAD value AND below 1 unit are flagged as dust. Default $1 CAD.")
    p.add_argument("--include-dust-balances", action="store_true",
                   help="Keep dust-flagged positions in year_end_balances.csv. By default they are hidden.")
    p.add_argument("--earliest-date", default=None,
                   help="Drop rows dated before this date (e.g. 2021-01-01). Useful for scrubbing CoinStats legacy/backfill rows.")
    args = p.parse_args()

    df = load_sources(args.csv, manual_paths=args.manual, exclude_text=args.exclude,
                      earliest_date=args.earliest_date)
    print(f"Loaded {len(df):,} rows after dedupe (dropped {df.attrs.get('dedup_drops', 0)} duplicates).")
    if df.attrs.get("pre_cutoff_dropped", 0):
        print(f"Earliest-date filter: dropped {df.attrs['pre_cutoff_dropped']} pre-{args.earliest_date} row(s).")

    if df.attrs.get("superseded_rows", 0):
        print(f"Supersedes: {df.attrs['superseded_rows']} CoinStats row(s) replaced by manual overrides.")
    for w in df.attrs.get("supersede_warnings", []):
        print(f"  WARNING (supersedes): {w}")
    for w in df.attrs.get("disposal_collision_warnings", []):
        print(f"  WARNING (collision): {w}")

    df, transfer_summary = match_transfers(
        df,
        window_minutes=args.transfer_window_minutes,
        tolerance=args.transfer_tolerance,
    )
    print(
        f"Transfer matcher: {transfer_summary.matched_pairs} pairs "
        f"({transfer_summary.cross_symbol_matches} cross-symbol) "
        f"@ avg confidence {transfer_summary.avg_confidence}."
    )

    df, swap_summary = detect_defi_swaps(df, window_seconds=args.swap_window_seconds)
    print(f"DeFi swap detector: {swap_summary.swaps_detected} swap pairs "
          f"({swap_summary.sells_unpaired} sells unpaired).")

    acb = run_acb(
        df,
        assume_missing_acb=args.assume_missing_acb,
        use_received_as_provisional_acb=args.use_received_as_provisional_acb,
        suspicious_gain_threshold_cad=args.suspicious_gain_cad,
    )
    print(f"ACB engine: {len(acb.report)} asset-year rows; "
          f"{len(acb.missing_events)} missing-ACB events.")

    classified = classify_missing(acb.annotated, acb.missing_events)
    priority = rank_priority(classified)
    anchors = build_anchor_entries(classified)

    balances = compute_year_end_balances(
        acb.annotated, dust_threshold_cad=args.dust_threshold_cad
    )
    n_total = len(balances)
    n_dust = int(balances["is_dust"].sum()) if not balances.empty else 0
    print(f"Year-end balances: {n_total} (year, asset) snapshots; "
          f"{n_dust} flagged as dust (<${args.dust_threshold_cad:g} CAD).")

    settings = {
        "input_csvs": [str(c) for c in args.csv],
        "manual_csvs": [str(m) for m in args.manual],
        "assume_missing_acb": args.assume_missing_acb,
        "use_received_as_provisional_acb": args.use_received_as_provisional_acb,
        "transfer_window_minutes": args.transfer_window_minutes,
        "transfer_tolerance": args.transfer_tolerance,
        "swap_window_seconds": args.swap_window_seconds,
        "suspicious_gain_cad_threshold": args.suspicious_gain_cad,
        "dust_threshold_cad": args.dust_threshold_cad,
        "include_dust_in_balances": args.include_dust_balances,
        "earliest_date": args.earliest_date,
    }

    paths = write_outputs(
        outdir=args.outdir,
        annotated_df=acb.annotated,
        acb=acb,
        classified_missing=classified,
        priority=priority,
        anchors=anchors,
        transfer_summary=transfer_summary,
        swap_summary=swap_summary,
        settings=settings,
        balances=balances,
    )

    print("\nOutputs:")
    for label, p_ in paths.items():
        print(f"  {label:<20} {p_}")

    if not acb.yearly_totals.empty:
        print("\nYearly totals (CAD):")
        print(acb.yearly_totals.to_string(index=False))

    latest = latest_year_summary(balances)
    if not latest.empty:
        print(f"\nNon-dust holdings at end of {int(latest.iloc[0]['year'])}:")
        cols = ["asset", "qty", "acb_cad", "price_cad", "value_cad"]
        print(latest[cols].head(20).to_string(index=False))


if __name__ == "__main__":
    main()
