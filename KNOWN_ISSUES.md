# Known Issues

Documented issues in the crypto-tax-reconstruction toolkit. Patches welcome via PR.

> If you encounter an issue not listed here, please open a GitHub issue with steps to reproduce.

---

## Toolkit bugs

### 1. ETH ACB pool tracking can underflow

**Symptom:** Year-end ETH balance shows a tiny ACB (e.g., $94 on 2.9 ETH) when reality is much higher (e.g., $9,260).

**Cause:** Pool tracking in `crypto_cra_toolkit/acb_engine.py` doesn't correctly handle interleaved ETH receives + disposals when transfer matching is partial. The engine sometimes consumes too much ACB from the pool during disposals, leaving the remaining pool incorrectly low.

**Workaround:** Cross-reference toolkit's per-asset year-end ACB against a known-good source (Koinly's paid annual tax report). If toolkit's ACB looks anomalously low compared to disposal volume, manually verify.

**Status:** Not yet patched. The fix involves re-implementing weighted-average pool draws to ensure ACB is consumed proportionally rather than based on FIFO-like ordering.

### 2. Inter-platform transfers can be missed

**Symptom:** A `Sent` event from one platform doesn't match a `Received` event at another platform, resulting in a phantom disposal or phantom acquisition.

**Cause:** The transfer matcher in `crypto_cra_toolkit/transfer_matcher.py` uses time-window + amount-tolerance matching. If timestamps are off by more than 10 minutes (e.g., due to confirmation lag, timezone issues) or amounts differ by more than 1% (e.g., gas fees on receiver side), the pair isn't matched.

**Workaround:** Review `matched_transfers.csv` after each run. If you see unmatched `Sent` or `Received` events that should pair, increase `--transfer-window-minutes` and `--transfer-tolerance` flags.

**Status:** Not yet patched. The matcher needs fuzzier amount tolerance with explanation (e.g., "matched with $X gas fee difference").

### 3. Coinbase US raw CSV requires manual reingestion for accurate FX

**Symptom:** Toolkit's output for Coinbase US disposals shows USD amounts where CAD amounts are expected, or applies static FX rate.

**Cause:** Coinbase US exports do not include CAD conversion. The toolkit's raw CSV converter (`convert_coinbase_us_raw.py`) needs to be run with care to apply correct historical FX rates.

**Workaround:** Use a CoinStats CAD-denominated CSV as the primary source for Coinbase US activity. CoinStats applies daily Bank of Canada rates correctly.

**Status:** Not yet patched. A future enhancement would auto-fetch Bank of Canada daily FX rates and apply them in `convert_coinbase_us_raw.py`.

### 4. Solscan exports treat lamports as SOL by default

**Symptom:** Reading Solscan export CSVs directly, the "Value" column shows USD/CAD value at time of transaction, not SOL quantity. The "Amount" column is in lamports (1 SOL = 1,000,000,000 lamports).

**Cause:** Solscan's export format uses Amount (raw on-chain unit) and Value (USD/CAD value). Easy to confuse.

**Workaround:** When parsing Solscan CSV, always divide Amount by 10^9 for SOL native, or by 10^Decimals for SPL tokens. The "Value" column is USD-by-default unless your Solscan UI was set to CAD before export.

**Status:** Documented. Add a helper function `parse_solscan_csv()` in future toolkit version.

### 5. Wallet-to-wallet transfers within the same blockchain may show as "Sent" + "Received" pair, but if both wallets are tracked, they net to non-taxable

**Symptom:** Toolkit counts an event as a disposal that's actually an internal transfer.

**Cause:** If both wallets are owned by the taxpayer but tracked separately, the transfer is internal (non-taxable). The matcher needs to recognize same-owner wallets.

**Workaround:** Manually flag same-owner transfers in your manual entry CSV. Use the `Supersedes` mechanism to override the toolkit's classification.

**Status:** Not yet patched. A future enhancement would accept a `--owned-wallets` flag listing all wallets controlled by the taxpayer.

---

## Documentation gaps

### Bridged-asset equivalence list is incomplete

The toolkit treats certain bridged assets as identical (e.g., ETH ↔ WETH, MATIC ↔ POL), but the list isn't comprehensive. Missing bridges:
- BNB ↔ WBNB
- Bridged versions of USDC across chains (USDC.e on Avalanche, USDC on Polygon, etc.)
- L2 bridged assets (Arbitrum, Optimism, Base)

**Workaround:** Verify which bridged assets are treated as identical in `crypto_cra_toolkit/acb_engine.py`. Manually add bridged-asset entries to the equivalence list.

### Sample data is synthetic and limited in scope

The `examples/` folder contains synthetic data that demonstrates basic features but doesn't cover:
- Liquid staking wraps
- Cross-chain bridges
- NFT acquisitions
- Mixed CAD/USD reporting

**Status:** Future enhancement to add more sample scenarios.

---

## Future enhancements (not bugs, but wanted features)

### CARF reporting compliance check

Add a feature to compare toolkit output against expected CARF-reported data from custodial exchanges. Flag discrepancies for user review.

### Automated cross-reference validator

For each disposition in the toolkit output, validate against:
- Exchange-reported data (if available)
- Koinly output (if user has Koinly)
- On-chain explorer data

Generate discrepancy report.

### Multi-jurisdiction support

Currently CRA-focused. Future support for:
- US tax treatment (FIFO, specific identification, mark-to-market)
- UK tax treatment (Section 104 pool)
- Australia tax treatment

### CoinStats CAD CSV native parser

CoinStats exports have a specific format that's slightly different from the toolkit's generic CSV. Add a dedicated parser to reduce conversion friction.

### Solscan multi-wallet aggregator

Combine N Solscan exports into one normalized view, accounting for same-owner inter-wallet transfers.

### Bank of Canada FX rate fetcher

Auto-fetch daily exchange rates and apply to USD-source data.

### Web UI

Currently CLI-only. A simple web interface would make the toolkit accessible to non-technical users.

---

## How to report new issues

1. Open an issue at https://github.com/fpenguin/crypto-tax-reconstruction/issues
2. Include:
   - What you were trying to do
   - What you expected
   - What actually happened
   - Steps to reproduce (with example data if possible)
   - Your Python version and OS

For security-sensitive issues, contact the maintainer directly rather than opening a public issue.

---

## Disclaimer

This toolkit is provided as-is. Known bugs don't necessarily make output unusable — they just require human verification. Always cross-reference with at least one other source (Koinly, exchange statements, on-chain explorers) before filing.

For corrections or contributions, please open a GitHub issue.
