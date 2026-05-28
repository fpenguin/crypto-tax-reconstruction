# CARF Preparation Checklist for Canadian Crypto Filers (2026)

The Crypto-Asset Reporting Framework (CARF) takes effect in Canada on January 1, 2026. This document outlines what changes for individual Canadian filers and how to prepare.

> **This is not professional tax advice.** Engage a qualified Canadian tax professional or CPA for your specific situation. CARF implementation details are evolving; check CRA's website for the latest information.

---

## TL;DR

Starting in 2026, Canadian-regulated crypto custodians (Wealthsimple Crypto, Newton, NDAX, Bull Bitcoin, etc.) and foreign exchanges with Canadian users (Coinbase, Binance, Crypto.com, etc.) are required to **report your year-end balances and annual transaction summaries directly to CRA**.

CRA will use this data to:
- Auto-populate parts of your T1 filing
- Cross-check what you report against what exchanges reported
- Flag discrepancies for review or audit

**Implication for you:** If your prior-year filings under-reported crypto activity, CARF will eventually expose it. Voluntary amendment **now** is much cheaper than reactive defense **later**.

---

## What CARF actually requires (high level)

CARF is an OECD-led framework adopted by Canada via Bill C-59. It mirrors the Common Reporting Standard (CRS) for traditional banking, but for crypto.

Custodians (called "Crypto-Asset Service Providers" or CASPs) must collect:
- **Account holder identification** (name, address, TIN, date of birth)
- **Tax residency** (CAD vs USA vs other jurisdiction)
- **Year-end balances** of every crypto asset
- **Annual transaction summaries** including:
  - Sales/disposals (proceeds in CAD)
  - Buys/acquisitions (cost in CAD)
  - Crypto-to-crypto trades (taxable dispositions)
  - Withdrawals/deposits (transfers in or out)
  - Staking rewards, airdrops, mining income

CASPs report this annually to CRA, and CRA shares with foreign tax authorities under the OECD framework.

### First reporting cycle

- **Tax year covered:** 2026 (January 1 - December 31)
- **CASP report due to CRA:** mid-2027
- **CRA cross-checks against 2026 T1 filings:** late 2027 - mid-2028
- **First wave of CARF-triggered audits:** late 2028 - 2029

---

## What changes for you as a Canadian crypto filer

### Before CARF (2024 and prior tax years)

- CRA had no direct visibility into your crypto activity
- Audits were rare and usually triggered by specific events (large deposits, unrelated tax issues)
- Many users under-reported crypto income with little risk

### After CARF (2026 onwards)

- CRA receives detailed records from every Canadian-regulated CASP you use
- Foreign CASPs share with CRA via OECD tax treaty if you're a Canadian resident
- Your T1 filing **must reconcile** to what CASPs report, or expect a query
- Audit triggers become automated and predictable

### Auto-Fill My Return improvements

Expect CRA's Auto-Fill My Return (used by tax software like Wealthsimple Tax, TurboTax, etc.) to start including:
- Crypto disposition summary (Schedule 3 line 15301 totals)
- Crypto income (line 13000 / 12100)
- Year-end crypto balances for verification

If you can't match the CRA-auto-filled numbers, you have a reconciliation problem to solve.

---

## What CARF does NOT cover

Important gaps that remain:

| Activity | CARF status | Your responsibility |
|---|---|---|
| **Self-custody wallets** (MetaMask, hardware wallets) | NOT reported (no custodian) | Track and report yourself |
| **DEX trades** (Uniswap, Jupiter, etc.) | NOT reported | Track from on-chain explorers |
| **DeFi protocols** (Aave, Compound, Lido) | NOT reported (non-custodial) | Track yourself; treat per CRA guidance |
| **Peer-to-peer transfers** (Wallet-to-wallet) | NOT reported | Track to demonstrate they're transfers, not disposals |
| **Foreign exchanges not implementing CARF** | Unreported (for now) | Voluntary disclosure or expect future risk |
| **Self-hosted nodes / mining** | NOT reported | Track yourself |
| **NFTs** | Variable (some CASPs report, some don't) | Verify per platform |

For Canadian crypto users with significant self-custody activity, **CARF doesn't eliminate the reconciliation work** — it just adds another data source you must match.

---

## Reconciliation imperative

Going forward, your annual tax workflow must include:

### Step 1: Gather CASP reports

Each year by end of February:
- Wealthsimple Crypto: Year-end Realized Gain/Loss + Staking Rewards reports
- Coinbase Canada / US: Statements and 1099-DA (US) or equivalent (CA)
- Newton: Year-end transaction history
- NDAX: Year-end ledger
- Bull Bitcoin, Shakepay, Coinsmart: equivalent statements
- Each report shows what the CASP has reported (or will report) to CRA

### Step 2: Cross-reference each report

For each asset, sum your CASP-reported gains/income and compare against:
- Your tax software's calculation (Koinly, Cointracker, etc.)
- Your own spreadsheet
- On-chain explorer data for transfers in/out

Discrepancies indicate:
- Missing transactions in one source
- Different ACB methodologies
- Timing differences (FX rate, transaction date interpretation)

### Step 3: Reconcile to CRA's expected numbers

When CRA's Auto-Fill My Return pulls CARF data:
- Your Schedule 3 line 15301 should match (or exceed, with self-custody addition) the CASP-reported gains
- Your line 13000 should match CASP-reported staking/rewards income
- Your year-end balance section (if added to T1) should match

### Step 4: Document your reconciliation

Keep working papers showing:
- CASP-reported numbers (per source)
- Your own calculations (per asset, per year)
- Reconciliation differences and explanations
- Any self-custody additions not in CASP reports

If CRA queries any line, you can produce reconciliation work paper immediately.

---

## Pre-CARF preparation checklist (do BEFORE first CARF cycle in 2027)

### Inventory your crypto presence (1-2 hours)

- [ ] List every centralized exchange you've ever used (active + inactive)
- [ ] List every wallet you control (self-custody, hardware, software)
- [ ] List every DeFi protocol where you have positions (Aave, Lido, Sanctum, etc.)
- [ ] List every NFT collection you've participated in
- [ ] Note any exchanges that went bankrupt or shut down (FTX, Voyager, BlockFi, etc.)

### Reconstruct prior-year activity (10-40 hours)

- [ ] Download all available tax reports from each CASP (typically 5-10 years of history)
- [ ] Export transaction history from each self-custody wallet via blockchain explorer
- [ ] Use a tax tool (Koinly, Cointracker, this toolkit) to consolidate and calculate per-year tax
- [ ] Cross-reference each tool's output against the CASP reports
- [ ] Identify any years where filed T1 amounts don't match reconstruction

### Voluntary amendments where needed

For each year where your filed T1 differs from your reconstruction by a material amount:

- [ ] File a T1 Adjustment (see `docs/T1_ADJUSTMENT_WORKFLOW.md`)
- [ ] Include cover letter explaining the methodology
- [ ] Attach supporting transaction records
- [ ] Pay any additional tax owed; carry forward any losses identified
- [ ] Note: amendments are subject to statute of limitations (typically 3 years from NOA)

### Update going-forward processes (1-2 hours)

- [ ] Set up CoinStats / Koinly / equivalent for 2026+ tracking from day 1
- [ ] Enable Auto-Fill My Return for your 2026 filing (will start pulling CARF data)
- [ ] Configure direct deposit with CRA to speed refunds
- [ ] Set calendar reminders for January 2027 to gather CASP reports
- [ ] Subscribe to CRA notices via My Account email alerts
- [ ] Verify your CRA profile has current address, banking info, etc.

---

## Common reconciliation pitfalls

### Pitfall 1: FX rate differences

CASPs may use different FX rate sources (real-time vs daily average vs end-of-day). Two reports of the "same" transaction can show slightly different CAD amounts.

**Tolerance:** Reconcile to within 1-2% per transaction. Document the source you used.

### Pitfall 2: Timing differences

A transaction at 11:55 PM UTC on December 31 might be reported in different tax years depending on the CASP's timezone convention.

**Tolerance:** If a transaction is at the year boundary, document which year you chose and why.

### Pitfall 3: Crypto-to-crypto swaps

Custodial swap (e.g., USDC → BTC at Coinbase) appears as one transaction. But for CRA, it's two events: dispose USDC, acquire BTC.

**Action:** Verify your tax software is splitting these correctly.

### Pitfall 4: Self-custody transfers misclassified as disposals

If you transfer crypto from MetaMask to Coinbase and your tax software doesn't recognize the matching pair, it may treat the transfer as a sale.

**Action:** Use transfer-matching features in your tax software. Verify pairs are matched.

### Pitfall 5: Missing staking/airdrop income

CARF requires CASPs to report staking rewards and reward income. If you forgot to report this on prior T1s, the discrepancy will be obvious to CRA.

**Action:** Add forgotten income on the most recent year's T1 (or amend prior years if material).

### Pitfall 6: Different ACB methodology

Your CASP uses separate-pool ACB. You should be using combined-pool weighted-average per Section 47 ITA.

**Action:** Apply combined-pool consistently. See `docs/COMBINED_POOL_ACB.md`.

---

## Voluntary Disclosures Program (VDP) consideration

If your prior-year under-reporting is **significant** (typically > $25,000 in unreported income or > $5,000 in unpaid tax), you may qualify for CRA's Voluntary Disclosures Program (VDP).

VDP benefits:
- Penalty relief (typically 50% reduction)
- Interest relief (typically 50% reduction)
- Protection from criminal prosecution

VDP requirements:
- Disclosure must be **voluntary** (filed before CRA contacts you)
- Disclosure must be **complete** (all relevant years and details)
- Disclosure must include payment (full unpaid tax)
- Must be filed at least one year past the original return deadline

If you're considering large amendments due to CARF risk, consult a CPA about VDP eligibility BEFORE filing the amendments.

---

## Timing strategy

### Optimal sequence

1. **2026 Q2-Q3:** Complete prior-year reconstruction (2021-2024)
2. **2026 Q3-Q4:** File T1 Adjustments for any material prior-year discrepancies
3. **2027 Q1:** Receive CASP reports for 2026
4. **2027 Q2-Q3:** File 2026 T1, reconciling to CASP reports + your own records
5. **2027 Q4+:** Monitor CRA queries; respond with reconciliation documentation

### Why this sequence

Filing 2026 T1 first without amending prior years creates risk: CRA sees clean 2026 reporting but discrepancies with prior-year filed amounts. Amending prior years first establishes a consistent historical track record before the first CARF reporting cycle.

---

## Tools and resources

### Canadian-specific tax software

- **Wealthsimple Tax** (free, with paid premium for crypto auto-import from Wealthsimple Crypto)
- **TurboTax** (commercial, supports crypto via Koinly integration)
- **StudioTax** (free, manual crypto entry)
- **UFile** (commercial)

### Crypto tax tracking tools

- **Koinly** ($49-279/year): comprehensive, paid Pro tier supports Canada specifically
- **Cointracker** ($79+/year): broad exchange support
- **Cointracking.info** ($150+/year): power-user features
- **This toolkit** (free, open-source): for users wanting transparent ACB calculation

### CRA resources

- CRA cryptocurrency guidance: https://www.canada.ca/en/revenue-agency/programs/about-canada-revenue-agency-cra/compliance/digital-currency/cryptocurrency-guide.html
- T1 Adjustment process: https://www.canada.ca/en/services/taxes/income-tax/personal-income-tax/after-you-file/change-return.html
- Voluntary Disclosures Program: https://www.canada.ca/en/revenue-agency/programs/about-canada-revenue-agency-cra/voluntary-disclosures-program-overview.html
- Income Tax Folio S3-F11-C1 (Cryptocurrency): https://www.canada.ca/en/revenue-agency/services/tax/technical-information/income-tax/income-tax-folios-index.html

### Government of Canada CARF announcement

- https://www.canada.ca/en/revenue-agency.html (search "CARF" or "Crypto-Asset Reporting Framework")

---

## Summary

CARF starts January 1, 2026. CRA will receive detailed crypto activity reports from custodial exchanges starting in 2027.

**Your priorities:**
1. **Reconstruct prior years** (2021-2024) to verify your filed T1s match reality
2. **Amend any years** with material discrepancies BEFORE the first CARF cycle exposes them
3. **Reconcile your 2026 T1** carefully against expected CASP-reported data
4. **Document your reconciliation** for potential audit defense

**Don't:**
- Assume CRA won't notice — they will
- Wait until 2028 to amend prior years — by then, CRA has CARF data and amendments become reactive (no VDP protection)
- File 2026 T1 without first reconciling to CASP reports

---

## Disclaimer

This guide is based on publicly-available information about CARF implementation as of 2026. CRA's specific implementation details and timing may evolve. Consult a qualified Canadian tax professional or CPA for your specific situation.

For corrections or contributions, please open a GitHub issue.
