# Combined-Pool ACB for Canadian Crypto Filers

How to apply Section 47 of the Income Tax Act (Adjusted Cost Base, identical properties) to cryptocurrency holdings spread across multiple wallets, exchanges, and custodians.

> **This is not professional tax advice.** Engage a qualified Canadian tax professional or CPA for your specific situation.

---

## TL;DR

Under Canadian tax law, **all your holdings of the same cryptocurrency** — across every wallet, every exchange, every custodian — form **a single pool** for ACB calculation purposes. When you dispose of any unit of that crypto, the ACB used is the **weighted average of the entire combined pool**, not the cost of the specific unit being sold.

This is the same rule that applies to publicly-traded stocks held in multiple brokerage accounts.

For active crypto users with holdings split between self-custody and centralized exchanges, this commonly **reduces your capital gain** on disposals (and reduces your tax) because your custodial exchange's separately-tracked ACB is usually higher than the global pool weighted average.

---

## The legal basis

### Section 47 of the Income Tax Act (ITA)

> "Where, at any time after 1971, a taxpayer has acquired a property (in this section referred to as the 'newly-acquired property') that is identical to another property (in this section referred to as the 'previously-acquired property') owned by the taxpayer immediately before that time, the **adjusted cost base** to the taxpayer of each such property owned by the taxpayer at that time shall... be deemed to be the amount **equal to the quotient obtained when the aggregate adjusted cost base** to the taxpayer immediately before that time of the previously-acquired property and **the cost** to the taxpayer of the newly-acquired property is divided by the **number of properties** that are identical to the newly-acquired property and that are owned by the taxpayer at that time."

In plain English: when you acquire more of the same crypto, the ACB of every unit you hold becomes the **weighted average** of (existing pool ACB + new acquisition cost) divided by total units.

### Why this matters for crypto

CRA confirmed in technical interpretation that cryptocurrency is "property" for tax purposes. Section 47 applies to crypto.

**Important:** "Identical" for crypto means "same token/coin," regardless of where it's held. Your BTC at Coinbase and your BTC at Wealthsimple and your BTC in a hardware wallet are all the same identical property.

---

## What this means in practice

### Scenario A: Single pool ACB

You have:
- 1 BTC in self-custody, acquired in 2017 for $1,000 CAD
- 1 BTC at Coinbase, acquired in 2024 for $80,000 CAD
- Total: 2 BTC, total ACB $81,000, weighted-average ACB = $40,500 per BTC

You sell 1 BTC from Coinbase for $100,000 CAD.

| Calculation method | ACB used | Gain |
|---|---|---|
| ❌ Specific identification (Coinbase records only) | $80,000 | $20,000 |
| ❌ FIFO (oldest first, the $1K one) | $1,000 | $99,000 |
| ✅ Weighted average (Section 47, correct) | $40,500 | $59,500 |

Whether you use the right method matters for your tax calculation.

### Scenario B: Custodian-prepared ACB is "wrong" by Section 47 standards

Many custodial exchanges (Wealthsimple Crypto, Coinbase, Newton, etc.) prepare a year-end "Realized Gain/Loss" report. Their calculations use **only the assets held in your account at that exchange** — they don't know about your other holdings.

Wealthsimple Crypto explicitly states this in their disclaimer:

> "For transferred in crypto assets, the starting book cost is set in our system to the fair market value of the assets at the time of transfer. Book cost values for clients that have transferred in crypto assets may therefore be inaccurate, and clients should do their own book cost calculations in order to ensure accurate tax reporting."

If you accept the exchange-prepared ACB at face value, you're typically **NOT** applying Section 47 correctly.

---

## When combined-pool ACB helps vs. hurts

### Helps (lower tax)

Your self-custody holdings have a **lower per-unit ACB** than the assets you have on a centralized exchange. Common when:
- You bought crypto cheaply early on (2015-2020)
- You accumulated some through low-cost methods (mining, gameplay rewards, airdrops at $0 ACB)
- You then later bought more at higher prices on a custodial exchange

When you sell from the custodial exchange, combined pool **blends down** the per-unit ACB → **lower gain** → less tax.

### Hurts (higher tax)

Your self-custody holdings have a **higher per-unit ACB** than your custodial holdings. Less common, but possible when:
- You bought heavily at peak prices via self-custody (e.g., DeFi/NFT-related purchases at 2021 prices)
- You acquired custodial holdings cheaply (e.g., via dollar-cost-averaging at lower prices)

When you sell from the custodial exchange, combined pool **blends up** the per-unit ACB → **higher gain** → more tax.

**You don't get to pick.** Section 47 is mandatory. You must apply it consistently.

---

## How to calculate combined-pool ACB

### Step 1: Establish per-asset pools

For each crypto you hold, list every acquisition across every wallet/exchange:

| Date | Quantity | Cost (CAD) | Source |
|---|---|---|---|
| 2017-05-10 | 1.0 BTC | $1,000 | Coinbase original buy |
| 2024-02-15 | 0.5 BTC | $35,000 | Wealthsimple Crypto |
| 2024-08-20 | 0.5 BTC | $45,000 | Wealthsimple Crypto |
| ... | ... | ... | ... |

### Step 2: Track running weighted average

After each acquisition, recalculate per-unit ACB:

| After | Total Qty | Total ACB | Per-unit ACB |
|---|---|---|---|
| 2017-05-10 buy | 1.0 BTC | $1,000 | $1,000 |
| 2024-02-15 buy | 1.5 BTC | $36,000 | $24,000 |
| 2024-08-20 buy | 2.0 BTC | $81,000 | $40,500 |

### Step 3: For each disposal, use pool ACB at that moment

If you sell 0.5 BTC after the 2024-08-20 buy:
- ACB used: 0.5 × $40,500 = **$20,250**
- Remaining pool: 1.5 BTC × $40,500 = $60,750 ACB

### Step 4: Continue forward

Each disposal removes proportional ACB. Each acquisition adds and rebalances.

---

## Tools

### Manual approach

A spreadsheet works for simple cases. For each asset, maintain a ledger with columns:
- Date
- Type (Buy/Sell/Receive/Send)
- Quantity (signed +/-)
- Cost (CAD, for buys/receives) or Proceeds (CAD, for sells)
- Running Quantity
- Running ACB
- Per-unit ACB after this transaction

### Automated approach

Tax software like Koinly, Cointracker, Accointing handle this if all your wallets are connected. Make sure each asset's pool spans ALL your wallets.

The [crypto-tax-reconstruction toolkit](https://github.com/fpenguin/crypto-tax-reconstruction) (this repo) handles weighted-average pooling correctly with its `--engine pool` mode.

---

## Documentation for your records

CRA can request your ACB calculations during audit. Maintain:

1. **Source documents**: Exchange statements, on-chain explorer transaction lists, bank records showing fiat purchases
2. **Aggregation worksheet**: Spreadsheet showing every acquisition, the running weighted-average pool, and every disposal
3. **Cross-reference**: For each tax return line, show which transactions contributed
4. **Methodology note**: Briefly explain that you applied Section 47 weighted-average ACB across all holdings of each asset

Retain for at least 7 years (CRA's records retention requirement).

---

## Common mistakes to avoid

### Mistake 1: Trust the exchange-prepared ACB without checking

Exchange-prepared ACB only reflects what was held at that exchange. If you ever transferred crypto in from elsewhere, the exchange usually values the transferred-in amount at **FMV at transfer time**, not at your actual carryover ACB.

Always do your own calculation if you have multi-venue holdings.

### Mistake 2: Inconsistent methodology across assets

If you apply combined-pool to ETH but use exchange-prepared ACB for BTC (just because BTC's exchange-prepared number is more favorable to you), CRA could challenge the inconsistency.

**Pick one approach and apply it uniformly.** If you apply combined-pool to one asset, apply it to all assets where you have multi-venue holdings.

### Mistake 3: Forgetting to include WS Crypto (or other custodial) in the pool

A common pattern: someone has detailed records of their on-chain wallets, calculates careful weighted-average ACB on those, then "forgets" their Wealthsimple Crypto holdings in the same asset.

The custodial holdings ARE part of the same pool. Include them.

### Mistake 4: Forgetting to include hardware wallets, lost-key wallets

Even if you can't access a wallet, its contents are still part of your ACB pool (until you formally treat them as lost — see `docs/ABANDONMENT_CLAIMS_GUIDE.md` forthcoming).

### Mistake 5: Treating staking yield or rewards inconsistently

If you classify gameplay rewards as $0 ACB receipts in one year, do the same the next year. If you classify them as income at FMV one year, continue that treatment.

---

## A worked example: BTC combined pool with custodial transfers

Setup:
- 2020-01-15: Bought 0.5 BTC for $5,000 CAD via Newton (self-custody after withdrawal)
- 2021-04-10: Bought 1 BTC for $60,000 CAD via Wealthsimple Crypto (held at WS)
- 2023-02-22: Transferred 0.5 BTC from self-custody to Wealthsimple
- 2024-05-15: Bought 0.2 BTC for $20,000 CAD via Wealthsimple Crypto
- 2024-12-31: Sold 0.5 BTC from Wealthsimple for $40,000 CAD

### Wealthsimple's prepared "Realized Gain/Loss" report

Wealthsimple sees:
- 1 BTC bought April 2021 for $60,000
- 0.5 BTC transferred in Feb 2023, **valued at FMV at transfer = ~$22,000**
- 0.2 BTC bought May 2024 for $20,000
- 0.5 BTC sold Dec 2024 for $40,000

WS-prepared gain: $40,000 − ($60,000 × 0.5/1.7 + $22,000 × 0.5/1.7 + $20,000 × 0.5/1.7)... using WS's separate-pool weighted average: ~$30,000 ACB used → gain = $10,000.

### Correct CRA combined-pool calculation

Your true pool at the time of sale:
- 0.5 BTC acquired 2020 for $5,000 (still part of pool, transferred-in value irrelevant)
- 1 BTC acquired 2021 for $60,000
- 0.2 BTC acquired 2024 for $20,000
- **Total: 1.7 BTC, total ACB $85,000, per-unit $50,000**

Sale of 0.5 BTC: ACB = 0.5 × $50,000 = **$25,000**.
Gain: $40,000 − $25,000 = **$15,000**.

Difference: $5,000 of gain that Wealthsimple's report missed → ~$2,650 in additional tax at 53% MTR.

In this example, the combined-pool method results in **higher** tax than the exchange's calculation. Other scenarios (especially where self-custody holdings have very low ACB) result in much lower tax.

---

## Special situations

### Tax-loss harvesting and the superficial loss rule

If you sell crypto at a loss and re-acquire identical crypto within 30 days (before or after), the **superficial loss rule** under ITA Section 54 denies the loss and adds it to the ACB of the new acquisition.

Combined-pool ACB applies normally to the new acquisition's ACB.

### Forks and airdrops

Generally treated as new acquisitions at FMV (or $0 if FMV is uncertain). These get added to the pool, weighted-averaging down (if low FMV) or up (if high FMV).

CRA's position on airdrop FMV is unsettled. Common practice: $0 ACB at receipt, full sale price as capital gain on later disposal.

### Liquid staking wraps (stETH, LST, wSTX, etc.)

Many filers (and tax software like Koinly) treat liquid staking wraps as **non-taxable** — same underlying asset, just wrapped/unwrapped. Under this treatment:
- The wrapped token (e.g., stETH) is treated as continuing the ETH pool
- No gain/loss recognized at wrap/unwrap
- Pool ACB unchanged

This is a defensible position but not the only one. Some practitioners treat wraps as taxable swaps. See `docs/LIQUID_STAKING_TAX.md` (forthcoming).

### Crypto-to-crypto swaps (DeFi)

CRA treats crypto-to-crypto swaps as **taxable dispositions**. The asset given up is disposed at FMV; the asset received is acquired with ACB equal to that FMV. Pool ACB is recalculated for both.

---

## Summary

1. **Section 47 ITA applies to crypto.** Weighted-average ACB across all holdings of each asset.
2. **Exchange-prepared ACB is usually wrong** for multi-venue holders.
3. **Combined-pool methodology** typically reduces tax for early adopters (low historical ACB) and can increase tax in other cases — you must apply it either way.
4. **Be consistent**: same methodology across all assets where you have multi-venue holdings.
5. **Document everything**: spreadsheet showing pool calculation for each asset for each year.
6. **Retain records 7 years** for potential CRA audit.

---

## Further reading

- CRA Income Tax Folio S3-F2-C1: Capital Gains
- CRA Income Tax Folio S3-F11-C1: Cryptocurrency
- Section 47 ITA: https://laws-lois.justice.gc.ca/eng/acts/i-3.3/section-47.html
- Section 54 ITA (Definitions, including superficial loss): https://laws-lois.justice.gc.ca/eng/acts/i-3.3/section-54.html

---

## Disclaimer

This guide is based on real-world Canadian crypto tax practice as of 2026. It is not professional tax advice. CRA rules and interpretations change frequently. Consult a qualified Canadian tax professional or CPA for your specific situation.

For corrections or contributions, please open a GitHub issue.
