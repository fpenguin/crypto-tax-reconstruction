# Crypto-Asset Tax Reconstruction — Cover Letter

**Taxpayer**: [TAXPAYER FULL NAME]
**SIN (last 4)**: [XXXX]
**Tax years covered**: {years_covered}
**Reconstruction date**: {today}
**Filing currency**: Canadian Dollars (CAD)
**Prepared by**: [PREPARER NAME — taxpayer or CPA]
**Reviewed by**: [CPA NAME, designation, firm]

---

## Purpose of this Document

This package is a defensive reconstruction of cryptocurrency activity for the
Canada Revenue Agency. It is provided alongside the taxpayer's T1 General
Income Tax and Benefit Return for the relevant years, and is intended to
demonstrate good-faith compliance with CRA's *Guide for Cryptocurrency Users
and Tax Professionals* and the underlying provisions of the **Income Tax Act**
governing the disposition of capital property.

A reconstruction was necessary because:

1. The taxpayer used **[N] distinct exchanges, wallets, and DeFi protocols**
   between [START YEAR] and [END YEAR]. Where applicable, list the venues:
   [LIST OF EXCHANGES, WALLETS, DEFI PROTOCOLS].

2. **No single tracking tool captures all activity correctly.** [Name the
   primary aggregator used and any others tested.] Reconstruction was
   completed manually using [list evidence sources: bank statements, exchange
   CSV exports, on-chain explorers, contemporaneous investment journals,
   platform support correspondence].

## Methodology

**ACB pooling.** Adjusted Cost Base is pooled globally per asset across all
wallets and exchanges, including bridged/wrapped equivalents (e.g., ETH ↔ WETH;
MATIC ↔ POL; USDT ↔ BSC-USD). This complies with CRA's identical-property
rule.

**Missing ACB.** Where original purchase records cannot be retrieved [name
the specific situations: e.g., "for the cold-storage wallet at [ADDRESS]";
"for the [EXCHANGE] account whose mid-period transaction history was destroyed
in the [DATE] bankruptcy"; "for staking rewards from [PROTOCOL] which were
wiped in the [DATE] collapse"], the taxpayer has used **Fair Market Value at
sale date as a reasonable approximation per CRA's official Guide for
Cryptocurrency Users and Tax Professionals**. This produces a near-zero gain
on the missing portion — neither claiming a fictitious loss nor conceding a
fictitious gain.

**Transfer matching.** [N] transfer pairs between the taxpayer's own
wallets and exchanges have been identified and excluded from disposition
calculations as non-taxable wallet-to-wallet movements.

**DeFi swap detection.** [N] same-timestamp Sell+Buy pairs on the
taxpayer's DeFi-compatible wallets are detected as swaps and treated as
linked dispositive events on each side.

**Worthless write-offs.** Tokens that have lost all value [list the
specific tokens and the supporting evidence: e.g., "BUSD post-Binance
discontinuation", "[TOKEN] after issuer insolvency on [DATE]"] have been
disposed at $0 proceeds with documented ACB.

**Airdrop and staking treatment.** [List the airdrop and staking events]
have been booked at FMV at receipt as ACB on the asset side, with the
matching FMV declared as **Other Income on T1 line 13000**.

**Section 50(1) abandonment.** [If applicable] [INVESTMENT NAME] for which
[REASON] was abandoned at year-end [YEAR] for **[$AMOUNT] CAD** capital
loss; supporting documentation includes [list].

## Materiality and Caveats

- All amounts are CAD. USD/USDT/stablecoin values are converted using Bank
  of Canada noon rates where retrievable, or year-average rates [list
  specific rates used per year].
- Several positions on platforms with sub-[$THRESHOLD] CAD activity have
  been acknowledged in the audit memo but not integrated as line items
  due to immateriality.
- The reconstruction relies on FMV approximations where original purchase
  records could not be retrieved. Every such instance is flagged in the
  audit memo's missing-purchase-history section with a documented cause
  and confidence level.
- This reconstruction is the taxpayer's good-faith effort. A Canadian
  crypto-tax-specialist CPA reviewed the methodology before filing.

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
   - `missing_purchase_history.csv` — missing-ACB events
   - `matched_transfers.csv` — wallet-to-wallet transfer pairings
   - `year_end_balances.csv` — closing positions per year per asset

Supplementary on-chain and exchange evidence:
- [List on-chain explorers used: Etherscan / Solscan / etc.] transaction-
  history CSVs for the taxpayer's primary wallets
- [List exchanges] "All Operations" CSV exports
- [Bankruptcy claim portal screenshots, where applicable]
- Investment journal exported from [PLATFORM] (preserved as PDF +
  markdown archives), containing contemporaneous purchase prices, dates,
  and rationale

If CRA requires additional substantiation for any specific transaction, the
taxpayer can provide on-chain transaction hashes within 14 days of request.

---

This is a tax reconstruction prepared by the taxpayer with reference to
publicly documented CRA guidance. **It is not professional tax advice.** It
has been reviewed by [CPA NAME, FIRM, designation].

Signed: ____________________________  Date: ____________

Reviewed by CPA: ____________________________  Date: ____________
