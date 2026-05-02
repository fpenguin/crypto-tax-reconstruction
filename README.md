# crypto-tax-reconstruction

A Python toolkit for reconstructing multi-year, multi-venue cryptocurrency
activity into a defensible tax-filing record. Built originally for Canadian
filers (CRA Schedule 3 / T1 line 12700 / line 13000), but the underlying
ACB engine and detectors are jurisdiction-agnostic.

> **This is not professional tax advice.** It is a working-paper generator.
> Have a qualified tax professional review the output before filing.

## Why this exists

If you have used more than a handful of exchanges, self-custody wallets, or
DeFi protocols across several tax years, no single tracking tool will get
your numbers right. CoinStats and Koinly each miss things; both struggle with
DeFi swaps, bridged assets, NFTs, airdrops with no on-chain prior receive,
and exchanges that have since been delisted, gone bankrupt, or renamed
themselves.

This toolkit takes a primary-aggregator CSV (CoinStats-format), lets you
layer in any number of supplemental CSVs (manual reconstructions, exchange
exports, on-chain explorer downloads), and produces:

- a clean transaction frame with deduped, normalized rows
- transfer-pair matching across portfolios (so wallet-to-wallet movements
  don't get miscounted as disposals)
- DeFi swap detection (same-timestamp Sell+Buy pairs)
- Adjusted Cost Base (ACB) pooling per asset, globally, with bridged-asset
  equivalence (ETH↔WETH, MATIC↔POL, etc.)
- a missing-purchase-history classifier with documented FMV imputation when
  records cannot be retrieved
- year-end balance snapshots with dust filtering
- per-asset and per-year capital-gain/loss reports
- a complete tax-filing package (cover letter, line-mapping summary, per-year
  transaction reports)

## Install

```bash
git clone https://github.com/<your-username>/crypto-tax-reconstruction.git
cd crypto-tax-reconstruction
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Tested on Python 3.10+. Only runtime dependency is `pandas`.

## Quickstart against the example data

```bash
# Run the full pipeline against the synthetic sample data:
python3 analyze.py examples/sample_transactions.csv \
    --manual examples/sample_manual_entries.csv \
    --outdir out_example

# Then generate the human-readable tax-filing package:
python3 generate_tax_filing.py --engine-out out_example --outdir tax_filing_example

# Inspect the output:
ls out_example/                 # CSVs and audit_memo.md
ls tax_filing_example/          # cover letter, line mapping, per-year reports
```

The full file layout produced by a successful run is described in
`docs/METHODOLOGY.md`.

## Using your own data

Two input CSV formats are accepted:

**Primary CoinStats CSV** — required columns: `Portfolio`, `Coin Name`,
`Coin Symbol`, `Type`, `Amount`, `Date`, plus one of `Price CAD` or
`Price USD`. Optional: `Pair`, `Exchange`, `Fee Amount`, `Fee Currency`,
`Fee Percent`, `Notes`. See `examples/sample_transactions.csv` for shape.

**Manual / supplemental CSV** — required columns: `Date`, `Type`,
`Coin Symbol`, `Amount`, `Price CAD`, `Portfolio`. Optional: `Coin Name`,
`Notes`, `Supersedes` (powerful — see below). See
`examples/sample_manual_entries.csv`.

### Supported `Type` values

`Buy`, `Sell`, `Sent`, `Received`, `Fee`, `Fill`, `Approve`, `Fail`. The
parser is also lenient with synonyms (case-insensitive, lowercased).

### The `Supersedes` mechanism

A row in your manual CSV can declare itself an authoritative override of a
specific row in the primary CSV. The fingerprint format is:

```
Date|Type|Coin Symbol|Amount|Portfolio
```

For example, a CoinStats row that should really be classified as a `Sell`
instead of `Sent` (e.g. an off-ramp to a since-defunct exchange) can be
overridden:

```csv
Portfolio,Coin Symbol,Type,Amount,Price CAD,Date,Notes,Supersedes
Maple Crypto,BTC,Sell,0.5,90000,2024-04-10 11:00:00,Off-ramp sale,2024-04-10 11:00:00|Sent|BTC|0.5|Maple Crypto
```

This survives future CoinStats CSV refreshes. If a refresh changes the
underlying row, the fingerprint stops matching and you'll see a warning
during pipeline runs — at which point you re-verify and update.

## Pipeline stages

```
sample_transactions.csv ──┐
sample_manual_entries.csv ─┤
                           ├─► parser  (dedupe, normalize, supersedes)
                           │
                           ├─► transfer matcher  (Sent ↔ Received pairs)
                           │
                           ├─► DeFi swap detector  (same-timestamp Sell+Buy)
                           │
                           ├─► ACB engine  (global per-asset pool, FMV/zero
                           │              imputation for missing ACB)
                           │
                           ├─► classifier  (label missing-ACB causes)
                           │
                           ├─► reconstruction  (anchor-buy suggestions,
                           │                     priority ranking)
                           │
                           ├─► balances  (year-end snapshots, dust filter)
                           │
                           └─► reporting  (CSVs + audit memo)
                                  │
                                  └─► generate_tax_filing.py
                                         (cover letter, line mapping,
                                          per-year transaction reports)
```

## Output files

A run produces, in `--outdir`:

| File | What it contains |
|---|---|
| `clean_transactions.csv` | every row after dedupe, normalize, supersedes, transfer-pairing, DeFi swap labels, and ACB annotations |
| `cra_yearly_totals.csv` | proceeds / ACB / fees / gain-loss / 50%-inclusion taxable amounts per year |
| `cra_asset_year_report.csv` | the same but broken out per asset per year |
| `missing_purchase_history.csv` | every disposal where ACB could not be sourced from a documented buy, with classifier label and remediation suggestion |
| `priority_fix_ranking.csv` | the missing-ACB events ranked by tax impact so you know which gaps to chase first |
| `anchor_buy_entries.csv` | template rows you can paste into your manual CSV as anchor buys |
| `matched_transfers.csv` | every Sent↔Received pair the matcher found |
| `defi_swaps.csv` | every Sell+Buy DeFi swap pair |
| `year_end_balances.csv` | non-dust closing positions per year per asset |
| `review_required_transactions.csv` | rows the engine flagged for human review |
| `transaction_type_summary.csv` | type-by-year row counts |
| `fee_currency_mismatch.csv` | rows where fee was paid in a different asset (often gas in ETH for non-ETH trades) |
| `audit_memo.md` | full text-format audit memo describing every stage |

Then `generate_tax_filing.py` produces, in its own `--outdir`:

| File | What it is |
|---|---|
| `cover_letter_for_cra.md` | methodology explanation suitable for handing to your CPA or attaching to a return |
| `line_mapping_summary.md` | which dollar amount goes on which T1 / Schedule 3 line, year by year |
| `<year>_transactions.md` | per-year deep dive: every disposal, asset-year aggregate, missing-ACB events, carryforward note |
| `INDEX.md` | links to all the above |

## Configuration

`analyze.py` accepts these flags:

| Flag | Default | What it does |
|---|---|---|
| `--manual <path>` | (none) | Add a supplemental CSV. Repeatable. |
| `--outdir <path>` | `coinstats_tax_output` | Where to write outputs. |
| `--exclude <substr>` | (none) | Drop rows whose searchable fields contain this. Repeatable. |
| `--assume-missing-acb {zero,fmv}` | `zero` | How to value the cost basis of disposals with no documented buy. |
| `--use-received-as-provisional-acb` | off | Treat unmatched `Received` rows as anchor buys at FMV. |
| `--transfer-window-minutes` | `10` | Time window for matching `Sent` ↔ `Received`. |
| `--transfer-tolerance` | `0.01` | Allowed amount mismatch (fraction). |
| `--swap-window-seconds` | `120` | Time window for matching DeFi `Sell` + `Buy` pairs. |
| `--suspicious-gain-cad` | (engine default) | Single-disposal gain above which a row is flagged for review. |
| `--dust-threshold-cad` | `1.00` | Year-end positions valued below this and below 1 unit are flagged dust. |
| `--include-dust-balances` | off | Keep dust in the balances output. |
| `--earliest-date <YYYY-MM-DD>` | (none) | Drop rows dated before this. Useful for backfill noise. |

## Testing

```bash
pytest tests/
```

The test suite (`tests/test_pipeline.py`) covers parser dedupe, supersedes
matching, transfer pairing, DeFi swap detection, ACB pool draws, FMV-mode
imputation, year-end balance forward-fill, and several edge cases.

## Methodology

For a deeper write-up of the design choices and trade-offs, see
[`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

For a CRA-targeted cover letter template you can adapt, see
[`docs/COVER_LETTER_TEMPLATE.md`](docs/COVER_LETTER_TEMPLATE.md).

## Disclaimer

This software is provided as-is, with no warranty of fitness for any
particular purpose, including correctness of tax computations. Tax law is
complex and jurisdiction-specific; **engage a qualified tax professional
before filing**. The maintainer is not a CPA and the project is not legal
or tax advice.

## License

MIT — see `LICENSE`.
