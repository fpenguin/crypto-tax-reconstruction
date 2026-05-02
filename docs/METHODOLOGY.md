# Methodology

This document describes how the toolkit reconstructs cryptocurrency tax
events. It is written for someone who needs to understand or defend the
output to an auditor — not as a marketing overview.

## Adjusted Cost Base (ACB) — global pooling per asset

Canada's Income Tax Act treats each cryptocurrency as a fungible "identical
property". When you dispose of part of a holding, the ACB drawn is the
weighted average of every prior buy of that asset, regardless of which
exchange or wallet held it.

The toolkit pools ACB **globally per asset across all portfolios**. A buy
of 1 BTC on Exchange A and a later buy of 1 BTC on Exchange B sit in the
same pool. A subsequent sale of 1.5 BTC from Wallet C draws 1.5 BTC of
weighted-average cost from that pool, regardless of which physical buy
funded which physical wallet.

### Bridged and wrapped equivalents

The parser treats certain pairs as the same economic asset for ACB
purposes:

- ETH ↔ WETH
- BTC ↔ WBTC
- MATIC ↔ POL ↔ WMATIC
- BNB ↔ WBNB
- AVAX ↔ WAVAX
- FTM ↔ WFTM
- SOL ↔ WSOL
- USDT ↔ BSC-USD

This is conservative — only well-known wraps where the economic exposure
is identical. It is not exhaustive; if you bridge an asset that isn't on
the list, you may need a manual reconstruction entry.

## Transfer matching

A `Sent` row in one portfolio and a `Received` row in another for the same
(or canonically equivalent) asset within the configured time window and
amount tolerance is matched as a transfer pair. Transfer pairs are removed
from disposal calculations because they represent the taxpayer moving an
asset between their own wallets — not a taxable disposition.

Defaults: 10-minute window, 0.01 fractional amount tolerance.

## DeFi swap detection

A same-timestamp `Sell` + `Buy` pair on the same wallet (or wallet group)
is interpreted as a DeFi swap. Both legs are taxable, but they are linked
in the output so it is clear they are two halves of one economic event.

## Missing ACB

When a `Sell` or `Sent` row would draw from a pool that has no — or
insufficient — prior buy, the toolkit treats this as a "missing ACB"
event. Two strategies are offered:

**Zero mode (default).** Imputed ACB is $0. Conservative: produces the
maximum possible reported gain. Use this when you have no documentation at
all and want to over-report rather than risk being assessed as
under-reporting.

**FMV mode.** Imputed ACB equals the proceeds of the disposal at FMV. Net
result: the missing portion produces a near-zero gain. This relies on
CRA's *Guide for Cryptocurrency Users and Tax Professionals* permitting a
"reasonable approximation" when records cannot be retrieved. Each
imputation is logged in `missing_purchase_history.csv` with a documented
cause label.

When you have partial documentation (e.g. you know you bought 5 ETH in
2021 even though the exchange has since gone bankrupt), the right move is
not to flip a global flag — it is to add a manual reconstruction entry to
your supplemental CSV with a `Notes` column that explains what evidence
supports it.

## Worthless write-offs

Tokens that have lost all value — issuer insolvency, on-chain death,
delisting — can be disposed at $0 proceeds with documented ACB. The
disposition narrative (`Notes` column on the manual entry) should
reference the supporting evidence: announcement URL, on-chain transaction
showing the contract being burned, exchange delisting notice, etc.

For Section 50(1) abandonment of a property the taxpayer can no longer
dispose of (often the case with NFTs from issuers who have rugpulled),
file a manual `Sell` row at $0 proceeds in the year of abandonment.

## Airdrops, staking rewards, and lending interest

The CRA classifies these as ordinary income at FMV on the date of receipt
(reported on T1 line 13000), with the same FMV becoming the asset's ACB
for any future disposition.

The toolkit does not auto-aggregate Other Income because the
business-vs-hobby classification depends on the taxpayer's overall fact
pattern. Review the `Notes` column of your manual entries for receipts
flagged airdrop / staking / interest, and discuss with your CPA before
filing.

## Year-end balance forward-fill

Closing positions are computed per asset per year. Years with no activity
forward-fill the prior year's closing balance, so the year-end inventory
table is dense across the full reporting range — useful for catching
positions that disappeared without a documented disposal.

## Dust filtering

Year-end positions valued below `--dust-threshold-cad` (default $1) AND
below 1 unit are flagged as dust. By default dust is hidden from the
balances output to keep the year-end inventory readable. Use
`--include-dust-balances` if you need the raw view.

## Output documents

A clean run produces (in the `--outdir`):

- `clean_transactions.csv` — every row after parsing, with engine-added
  columns: `engine_acb_used_cad`, `engine_running_acb_cad`, swap pair IDs,
  transfer pair IDs, missing-ACB flags
- `cra_yearly_totals.csv` — per-year proceeds / ACB / fees / gain-loss /
  50%-inclusion taxable amounts
- `cra_asset_year_report.csv` — the same but broken out by asset
- `missing_purchase_history.csv` — every missing-ACB event with cause
- `priority_fix_ranking.csv` — events ranked by tax impact
- `anchor_buy_entries.csv` — paste-ready manual rows
- `matched_transfers.csv` — wallet-to-wallet pairings
- `defi_swaps.csv` — Sell+Buy swap pairs
- `year_end_balances.csv` — closing positions, post-dust-filter
- `review_required_transactions.csv` — rows flagged for review
- `audit_memo.md` — text-format audit memo

`generate_tax_filing.py` then reads these and produces the human-readable
tax-filing package in its own output directory.

## Limitations

This toolkit is opinionated and conservative. It will not:

- Compute Bank of Canada noon-rate FX conversions per-row. USD prices are
  converted using year-average rates. If an auditor wants per-day
  precision, you supply a more precise FX file via the manual CSV's
  `Price CAD` column.
- Substitute for a CPA's review of business-vs-hobby classification,
  Section 50(1) eligibility, mining-income treatment, or tax-residency
  questions.
- Handle margin / perpetuals / futures that settle in cash. Those need
  custom handling.
- Verify on-chain that a wallet you list as your own actually is. The
  evidence trail (your manual entries' Notes) is your responsibility.

## Provenance and reproducibility

Every transaction in the engine output has a `source_file` column tracing
it back to the input CSV that produced it. Every override has a
`Supersedes` fingerprint that ties it to the row it replaced. The audit
memo records the exact CLI flags used. This is intentional: the goal is
that an auditor with the same input files and the same CLI invocation can
reproduce the numbers byte-for-byte.
