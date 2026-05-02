# Example data

This folder contains a synthetic dataset for trying out the toolkit. **All
people, exchanges, wallets, and transactions are fictional.**

## Files

- `sample_transactions.csv` — primary aggregator export (CoinStats-format).
  Two fictional years (2024 and 2025) of activity across three made-up venues:
  "Maple Crypto" (a Canadian CEX), "Polar Wallet" (self-custody), and
  "Skyport" (a foreign CEX/NFT marketplace), plus a "Vault Wallet" cold-storage
  destination.

- `sample_manual_entries.csv` — supplemental file demonstrating the override
  mechanisms: an anchor `Buy` to provide ACB for a missing-purchase event,
  and a `Supersedes` row that reclassifies a primary-aggregator row.

## What the data exercises

The sample is intentionally varied so a quick run lights up most of the
pipeline:

| Scenario | Where it is | What it tests |
|---|---|---|
| Plain Buy / Sell on a CEX | Maple Crypto BTC + ETH + SOL | ACB pooling, basic gain/loss |
| Send → Receive transfer pair | BTC, ETH, USDC moves between portfolios | transfer matcher (excludes from disposals) |
| DeFi swap (same-timestamp Sell + Buy) | Polar Wallet BTC↔ETH (2024-07-04), ETH↔NEW (2025-08-01) | DeFi swap detector |
| Airdrop receipt + later disposal | GOOD token (2024-06 → 2024-08), BUMP (2024-12 → 2025-07) | Other Income on receipt; capital gain on disposal |
| Stablecoin position | USDC, USDT positions | near-zero-gain disposals |
| Missing-ACB event | 2 ETH `Received` 2025-01-15 with no matching `Send` | classifier + FMV-mode imputation |
| NFT primary + secondary sale | MoonGuy #423 (Skyport) | non-fungible asset handling |
| Profit-taking and loss-taking sales | Various BTC, NEW disposals | gain and loss legs both populate |

## How to run it

From the repo root:

```bash
# 1. ZERO-mode pipeline (default — fastest, conservative)
python3 analyze.py examples/sample_transactions.csv \
    --manual examples/sample_manual_entries.csv \
    --outdir out_example

# 2. Then generate the tax-filing deliverable package
python3 generate_tax_filing.py --engine-out out_example --outdir tax_filing_example

# 3. Inspect:
ls out_example/
ls tax_filing_example/
```

Try `--assume-missing-acb fmv` to see how the engine substitutes Fair Market
Value for the missing-ACB ETH event:

```bash
python3 analyze.py examples/sample_transactions.csv \
    --manual examples/sample_manual_entries.csv \
    --assume-missing-acb fmv \
    --outdir out_example_fmv
```

## A note on prices

Prices in the sample are CAD-denominated and chosen to be illustrative, not
correct for any particular date. They roughly match the order of magnitude
of real prices in the relevant period but should not be used for any actual
research or back-testing.
