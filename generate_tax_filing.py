#!/usr/bin/env python3
"""Generate a tax-filing deliverable package from the toolkit's engine output.

Produces (in --outdir):
- cover_letter_for_cra.md   — master cover letter (methodology + caveats)
- line_mapping_summary.md   — which numbers go on which T1/Schedule 3 line
- {year}_transactions.md    — per-year disposal & income detail
- INDEX.md                  — index of generated files

Run AFTER the pipeline (analyze.py) has produced engine outputs. Reads:
- cra_yearly_totals.csv
- cra_asset_year_report.csv
- clean_transactions.csv
- missing_purchase_history.csv

The cover letter is a generic template. If you have a customised cover letter
at docs/COVER_LETTER_TEMPLATE.md (relative to this script's parent dir), that
file is used instead and {today} / {years_covered} placeholders are filled in.

Disclaimer: this output is a working paper. It is NOT professional tax advice.
Have a qualified tax professional review before filing.
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
DEFAULT_ENGINE_OUT = ROOT / "out"
DEFAULT_TAX_OUT = ROOT / "tax_filing"


# ─── Formatting helpers ────────────────────────────────────────────────────

def _money(x) -> str:
    if pd.isna(x) or x is None:
        return "$0.00"
    val = float(x)
    if val == 0:  # avoid "$-0.00"
        val = 0.0
    return f"${val:,.2f}"


def _qty(x) -> str:
    if pd.isna(x) or x is None:
        return "0"
    s = f"{float(x):.8f}".rstrip("0").rstrip(".")
    return s or "0"


# ─── Cover letter (generic template) ───────────────────────────────────────

DEFAULT_COVER_LETTER = """\
# Crypto-Asset Tax Reconstruction — Cover Letter

**Tax years covered**: {years_covered}
**Reconstruction date**: {today}
**Filing currency**: Canadian Dollars (CAD)

---

## Purpose of this Document

This package is a defensive reconstruction of cryptocurrency activity for the
Canada Revenue Agency. It is provided alongside the taxpayer's T1 General
Income Tax and Benefit Return for the relevant years, and is intended to
demonstrate good-faith compliance with CRA's *Guide for Cryptocurrency Users
and Tax Professionals* and the underlying provisions of the **Income Tax Act**
governing the disposition of capital property.

A reconstruction is necessary when the taxpayer used multiple exchanges,
self-custody wallets, and DeFi protocols, and no single tracking tool
captures all activity correctly. Reconstruction is performed manually using
exchange CSV exports, on-chain explorers, contemporaneous investment journals,
and direct platform support correspondence.

## Methodology

**ACB pooling.** Adjusted Cost Base is pooled globally per asset across all
wallets and exchanges, including bridged/wrapped equivalents. This complies
with CRA's identical-property rule.

**Missing ACB.** Where original purchase records cannot be retrieved, the
taxpayer uses **Fair Market Value at sale date as a reasonable approximation
per CRA's Guide for Cryptocurrency Users**. This produces a near-zero gain on
the missing portion — neither claiming a fictitious loss nor conceding a
fictitious gain. Each instance is flagged in the audit memo's
missing-purchase-history section with a documented cause.

**Transfer matching.** Transfer pairs between the taxpayer's own wallets and
exchanges have been identified and excluded from disposition calculations as
non-taxable wallet-to-wallet movements.

**DeFi swap detection.** Same-timestamp Sell+Buy pairs on DeFi-compatible
wallets are detected as swaps and treated as a single dispositive event for
each side, preserving the relationship between the asset given up and the
asset received.

**Worthless write-offs.** Tokens that have lost all value are disposed at $0
proceeds with documented ACB. Where supporting evidence exists (issuer
insolvency, on-chain death, regulatory delisting), the disposition narrative
references the evidence.

**Airdrops, staking, and lending.** Receipts of these types are booked at FMV
at receipt as ACB on the asset side, with the matching FMV declared as
**Other Income on T1 line 13000** for the year of receipt.

## Caveats

- All amounts are CAD. USD/USDT/stablecoin values are converted using Bank of
  Canada noon rates where retrievable, year-average rates otherwise.
- Sub-material activity below a published threshold may be acknowledged in the
  audit memo but not integrated as line items.
- This reconstruction relies on FMV approximations where original records could
  not be retrieved. All such instances are flagged.
- This is the taxpayer's good-faith effort. A Canadian crypto-tax-specialist
  CPA should review the methodology before filing.

## Supporting Evidence Index

The following files form the complete evidence package:

1. `cover_letter_for_cra.md` — this document
2. `line_mapping_summary.md` — which numbers go on which T1 / Schedule 3 line
3. `<year>_transactions.md` — per-year disposal detail
4. `manual_entries.csv` — every override and reconstruction entry with
   per-line documentation in the Notes column
5. Engine outputs:
   - `audit_memo.md` — full pipeline audit memo (methodology, all stages)
   - `cra_yearly_totals.csv` — yearly summary totals
   - `cra_asset_year_report.csv` — asset-by-year disposal detail
   - `missing_purchase_history.csv` — missing-ACB events with classifier labels
   - `matched_transfers.csv` — wallet-to-wallet transfer pairings
   - `year_end_balances.csv` — closing positions per year per asset

Supplementary on-chain and exchange evidence (taxpayer to attach as needed):
- On-chain explorer transaction-history CSVs for primary wallets
- Exchange "All Operations" CSV exports
- Bankruptcy claim portal screenshots (where applicable)
- Investment journal exports

If CRA requires additional substantiation for any specific transaction, the
taxpayer can provide on-chain transaction hashes within 14 days of request.

---

This is a tax reconstruction prepared by the taxpayer with reference to
publicly documented CRA guidance. **It is not professional tax advice.** It
should be reviewed by a Canadian crypto-tax-specialist CPA before filing.
"""


def load_cover_letter_template() -> str:
    """Use docs/COVER_LETTER_TEMPLATE.md if present; fall back to default."""
    candidate = ROOT / "docs" / "COVER_LETTER_TEMPLATE.md"
    if candidate.exists():
        return candidate.read_text()
    return DEFAULT_COVER_LETTER


# ─── Line mapping ──────────────────────────────────────────────────────────

LINE_MAPPING_TEMPLATE = """\
# T1 / Schedule 3 Line Mapping

**Note**: For tax years 2024 and later, CRA's Schedule 3 has a dedicated
**Part 5 — Bonds, debentures, promissory notes, crypto-assets, and other
similar properties**. For 2023 and earlier, crypto was typically reported
under Part 3 (Publicly traded shares) or Part 4 (Other property). Your CPA
will know the exact line numbers for the year being filed; the conceptual
mapping below is identical across years.

## Schedule 3 — Capital Gains (Losses) — Crypto Section

| Schedule 3 line | Conceptually | Reference in our reports |
|---|---|---|
| Proceeds of disposition | Total CAD received from all crypto sales | `cra_yearly_totals.csv` → `proceeds_cad` |
| Adjusted cost base | Total CAD ACB drawn | `cra_yearly_totals.csv` → `acb_used_cad` |
| Outlays and expenses | Disposition fees | `cra_yearly_totals.csv` → `disposition_fees_cad` |
| Gain (loss) | Net per-asset gain/loss | `cra_yearly_totals.csv` → `gain_loss_cad` |

## Schedule 3 — Aggregation Lines

| Schedule 3 line | Conceptually | What goes here |
|---|---|---|
| Line 19700 | Total capital gains | sum of all positive `gain_loss_cad` |
| Line 19800 | Total capital losses | sum of all negative `gain_loss_cad` (as positive) |
| Line 19900 | **Taxable capital gains (50%)** | (gains − losses) × 50% |
| Line 25300 | Net capital losses of other years (carryforward applied) | Loss carryforward from prior years |

## T1 General — Where the Schedule 3 number flows

| T1 line | What | From |
|---|---|---|
| **Line 12700** | **Taxable capital gains** | Schedule 3 line 19900 |
| **Line 13000** | **Other income** | Crypto airdrops + staking rewards + lending interest |
| Line 22100 | Carrying charges (if applicable) | Investment-related interest paid + investment-management fees |

---

## Year-by-Year Filing Summary

The following table tells you **exactly which dollar amounts go on which line
of which year's Schedule 3 / T1**. All amounts are in CAD.

{yearly_table}

---

## Loss Carryforward / Carryback Plan (mechanical)

{carryforward_plan}

Loss carrybacks (max 3 prior years) are claimed via **Form T1A — Request for
Loss Carryback**, filed alongside the loss-year return. Loss carryforwards
are claimed on **Schedule 3 line 25300** in the year you wish to apply them.

If 2022/2023 returns were filed BEFORE this reconstruction, they may need
**T1-Adjustment forms (T1-ADJ)** so the higher loss amounts get into CRA's
records before they can be carried forward.

---

## Other Income (T1 Line 13000)

Airdrops, staking rewards, lending interest, and similar receipts are taxable
as ordinary income at FMV on the date of receipt. They are reported on
**T1 line 13000** in the year of receipt.

This package does not auto-aggregate these into the per-year amount because
the classification depends on the taxpayer's fact pattern (business vs
hobby, etc.). Review the per-year transaction reports for receipts flagged
as airdrop / staking and confirm with your CPA before filing.
"""


def render_yearly_table(yearly: pd.DataFrame) -> str:
    rows = ["| Year | Schedule 3 Proceeds | Schedule 3 ACB | Net Gain/Loss "
            "| Schedule 3 Line 19900 (taxable) | Notes |",
            "|---|---|---|---|---|---|"]
    for _, r in yearly.iterrows():
        year = int(r["year"])
        line19900 = round(r["taxable_capital_gain_50pct_cad"]
                          + r["allowable_capital_loss_50pct_cad"], 2)
        if line19900 < 0:
            note = "Net loss — carry forward (or back via T1A)"
        elif line19900 == 0:
            note = "Break-even"
        else:
            note = "Net taxable capital gain"
        rows.append(f"| {year} | {_money(r['proceeds_cad'])} "
                    f"| {_money(r['acb_used_cad'])} "
                    f"| {_money(r['gain_loss_cad'])} "
                    f"| **{_money(line19900)}** | {note} |")
    return "\n".join(rows)


def render_carryforward_plan(yearly: pd.DataFrame) -> str:
    """Mechanical narrative: which years have losses, which have gains."""
    lines = []
    for _, r in yearly.iterrows():
        year = int(r["year"])
        line19900 = round(r["taxable_capital_gain_50pct_cad"]
                          + r["allowable_capital_loss_50pct_cad"], 2)
        if line19900 < 0:
            lines.append(f"- **{year}** net allowable capital loss: "
                         f"{_money(line19900)} — carries forward indefinitely; "
                         f"may also be carried back up to 3 years via Form T1A "
                         f"if those years had taxable capital gains.")
        elif line19900 > 0:
            lines.append(f"- **{year}** net taxable capital gain: "
                         f"{_money(line19900)} — apply prior-year carryforward "
                         f"on Schedule 3 line 25300 to offset.")
        else:
            lines.append(f"- **{year}** break-even: no carryforward action.")
    return "\n".join(lines)


# ─── Per-year transaction detail ───────────────────────────────────────────

YEAR_REPORT_TEMPLATE = """\
# {year} Crypto Disposals — Detailed Transaction Record

**Tax year**: {year}
**Filing reference**: T1 General Income Tax and Benefit Return for {year}, Schedule 3
**Report generated**: {today}

---

## Year {year} Summary

| Item | Amount (CAD) |
|---|---|
| Total proceeds of disposition | {proceeds} |
| Total adjusted cost base used | {acb} |
| Disposition fees | {fees} |
| **Net capital gain (loss) before 50% inclusion** | **{gain}** |
| Total capital gains (sum of profitable disposals) | {gross_gains} |
| Total capital losses (sum of losing disposals) | {gross_losses} |
| Schedule 3 line 19700 (capital gains) | {line19700} |
| Schedule 3 line 19800 (capital losses) | {line19800} |
| **Schedule 3 line 19900 (50% net taxable capital gain)** | **{line19900}** |
| Missing-ACB events (FMV-imputed) | {missing_count} events totaling {missing_acb} CAD imputed ACB |

## Carryforward / Carryback Note

{carryforward_note}

## Disposal-by-Disposal Detail

The table below lists every taxable disposal during {year}, with proceeds,
ACB drawn, and resulting gain/loss. Disposals are ordered by transaction
date.

{disposals_table}

## Asset-Year Aggregate (one row per asset)

This table groups all disposals by asset and shows the cumulative effect for
the year. This is what gets transcribed to Schedule 3.

{asset_year_table}

## Missing-ACB Events for {year}

For these dispositions, the original purchase records could not be
retrieved. The engine has used **Fair Market Value at sale date as a
reasonable approximation per CRA's Guide for Cryptocurrency Users**. The
imputed ACB approximates proceeds, producing a near-zero gain/loss on the
missing portion — a defensible neutral treatment.

{missing_table}

## Other Income (T1 Line 13000) for {year}

Review the manual_entries.csv for airdrop and staking receipts in this year,
and confirm Other Income inclusion with your CPA before filing.

---

## Methodology Reference

This report was generated from the same engine state that produced the audit
memo at `audit_memo.md`. For full methodology — including ACB pooling rules,
transfer matching, DeFi swap detection, and worthless write-off treatment —
see the audit memo and `docs/METHODOLOGY.md`.
"""


def render_disposals_table(clean: pd.DataFrame, year: int) -> str:
    sells = clean[(clean["type_norm"] == "sell")
                  & (clean["year"] == year)
                  & (clean["amount_abs"] > 0)].copy()
    if sells.empty:
        return "_No taxable disposals in this year._"
    sells = sells.sort_values("date").reset_index(drop=True)
    rows = ["| Date | Asset | Qty disposed | Proceeds | ACB used | Gain/Loss "
            "| Portfolio | Notes |",
            "|---|---|---|---|---|---|---|---|"]
    for _, r in sells.iterrows():
        d = pd.to_datetime(r["date"]).strftime("%Y-%m-%d")
        asset = str(r["asset"])[:35]
        if len(str(r["asset"])) > 35:
            asset += "..."
        qty = _qty(r["amount_abs"])
        proceeds = float(r.get("value_cad", 0) or 0)
        acb = float(r.get("engine_acb_used_cad", 0) or 0)
        gain = proceeds - acb
        portfolio = str(r["Portfolio"])[:25]
        notes = str(r.get("Notes", "") or "")[:60]
        if pd.isna(r.get("Notes")) or notes == "nan":
            notes = ""
        rows.append(f"| {d} | {asset} | {qty} | {_money(proceeds)} "
                    f"| {_money(acb)} | {_money(gain)} | {portfolio} | {notes} |")
    return "\n".join(rows)


def render_asset_year_table(report: pd.DataFrame, year: int) -> str:
    sub = report[report["year"] == year].copy()
    if sub.empty:
        return "_No disposals to summarize._"
    sub = sub.sort_values("gain_loss_cad")
    rows = ["| Asset | Proceeds | ACB used | Gain/Loss | Buys qty | Sells qty |",
            "|---|---|---|---|---|---|"]
    for _, r in sub.iterrows():
        asset = str(r["asset"])
        if len(asset) > 50:
            asset = asset[:47] + "..."
        rows.append(f"| {asset} | {_money(r['proceeds_cad'])} "
                    f"| {_money(r['acb_used_cad'])} | {_money(r['gain_loss_cad'])} "
                    f"| {_qty(r.get('buys_qty', 0))} | {_qty(r.get('sells_qty', 0))} |")
    return "\n".join(rows)


def render_missing_table(missing: pd.DataFrame, year: int) -> str:
    sub = missing[missing["year"] == year].copy()
    if sub.empty:
        return ("_No missing-ACB events for this year — all dispositions have "
                "documented cost basis._")
    sub = sub.sort_values("proceeds_cad", ascending=False).head(20)
    rows = ["| Date | Asset | Qty missing | Proceeds | FMV-imputed ACB | Cause |",
            "|---|---|---|---|---|---|"]
    for _, r in sub.iterrows():
        d = pd.to_datetime(r["date"]).strftime("%Y-%m-%d")
        asset = str(r["asset"])[:40]
        rows.append(f"| {d} | {asset} | {_qty(r['missing_qty'])} "
                    f"| {_money(r['proceeds_cad'])} "
                    f"| {_money(r.get('assumed_missing_acb_cad', 0))} "
                    f"| {r.get('cause', '')} |")
    return "\n".join(rows)


def carryforward_note_for(year: int, line19900: float) -> str:
    """Generic, mechanical narrative based on the gain/loss for the year."""
    if line19900 < 0:
        return (f"Year {year} produces a NET ALLOWABLE CAPITAL LOSS of "
                f"{_money(line19900)}. **Action**: this loss carries forward "
                f"indefinitely; apply on a future year's Schedule 3 line 25300. "
                f"You may also file Form T1A to carry back up to 3 prior years "
                f"if those years had taxable capital gains.")
    if line19900 > 0:
        return (f"Year {year} produces a NET TAXABLE CAPITAL GAIN of "
                f"{_money(line19900)}. **Action**: apply any unused "
                f"prior-year capital loss carryforward on Schedule 3 line 25300 "
                f"to offset. After offsetting, the remaining amount flows to "
                f"T1 line 12700.")
    return f"Year {year} is break-even; no carryforward action required."


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--engine-out", type=Path, default=DEFAULT_ENGINE_OUT,
                   help="Directory containing engine output CSVs (default: out/)")
    p.add_argument("--outdir", type=Path, default=DEFAULT_TAX_OUT,
                   help="Output directory for the deliverable package "
                        "(default: tax_filing/)")
    args = p.parse_args()

    args.outdir.mkdir(exist_ok=True, parents=True)

    today = dt.datetime.now().strftime("%B %d, %Y")
    yearly = pd.read_csv(args.engine_out / "cra_yearly_totals.csv")
    report = pd.read_csv(args.engine_out / "cra_asset_year_report.csv")
    clean = pd.read_csv(args.engine_out / "clean_transactions.csv")
    missing_path = args.engine_out / "missing_purchase_history.csv"
    missing = pd.read_csv(missing_path) if missing_path.exists() else pd.DataFrame(
        columns=["date", "asset", "year", "missing_qty", "proceeds_cad",
                 "assumed_missing_acb_cad", "cause"]
    )

    if yearly.empty:
        print("cra_yearly_totals.csv is empty — nothing to generate.")
        return

    years_covered = ", ".join(str(int(y)) for y in sorted(yearly["year"].unique()))

    # Cover letter
    cover_template = load_cover_letter_template()
    (args.outdir / "cover_letter_for_cra.md").write_text(
        cover_template.format(today=today, years_covered=years_covered)
    )

    # Line mapping
    line_mapping = LINE_MAPPING_TEMPLATE.format(
        yearly_table=render_yearly_table(yearly),
        carryforward_plan=render_carryforward_plan(yearly),
    )
    (args.outdir / "line_mapping_summary.md").write_text(line_mapping)

    # Per-year reports
    for _, r in yearly.iterrows():
        y = int(r["year"])
        sub = report[report["year"] == y]
        gross_gains = sub.loc[sub["gain_loss_cad"] > 0, "gain_loss_cad"].sum()
        gross_losses = sub.loc[sub["gain_loss_cad"] < 0, "gain_loss_cad"].sum()
        line19900 = round(r["taxable_capital_gain_50pct_cad"]
                          + r["allowable_capital_loss_50pct_cad"], 2)
        missing_sub = missing[missing["year"] == y] if not missing.empty else missing

        body = YEAR_REPORT_TEMPLATE.format(
            year=y,
            today=today,
            proceeds=_money(r["proceeds_cad"]),
            acb=_money(r["acb_used_cad"]),
            fees=_money(r["disposition_fees_cad"]),
            gain=_money(r["gain_loss_cad"]),
            gross_gains=_money(gross_gains),
            gross_losses=_money(gross_losses),
            line19700=_money(gross_gains),
            line19800=_money(-gross_losses),
            line19900=_money(line19900),
            missing_count=len(missing_sub),
            missing_acb=_money(missing_sub["assumed_missing_acb_cad"].sum()
                               if not missing_sub.empty else 0),
            carryforward_note=carryforward_note_for(y, line19900),
            disposals_table=render_disposals_table(clean, y),
            asset_year_table=render_asset_year_table(report, y),
            missing_table=render_missing_table(missing, y),
        )
        (args.outdir / f"{y}_transactions.md").write_text(body)

    # Index
    files = ["cover_letter_for_cra.md", "line_mapping_summary.md"]
    files += [f"{int(r['year'])}_transactions.md" for _, r in yearly.iterrows()]
    index = ["# Tax-Filing Package — Index", "", f"Generated: {today}", ""]
    index += [f"- [{f}]({f})" for f in files]
    (args.outdir / "INDEX.md").write_text("\n".join(index) + "\n")

    print(f"Generated tax-filing package in {args.outdir}/")
    for f in sorted(args.outdir.glob("*.md")):
        print(f"  {f.name}  ({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
