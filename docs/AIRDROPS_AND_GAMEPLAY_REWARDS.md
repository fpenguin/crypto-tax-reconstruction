# Airdrops and Gameplay Rewards for Canadian Crypto Filers

How to handle airdropped tokens, play-to-earn rewards, mining income, and other "received without payment" crypto events.

> **This is not professional tax advice.** Engage a qualified Canadian tax professional or CPA for your specific situation. CRA's position on airdrop income is not fully formalized.

---

## TL;DR

When you receive cryptocurrency without paying for it (airdrops, play-to-earn rewards, staking rewards, mining, faucets, etc.), Canadian tax practice has converged on **two acceptable treatments**:

1. **$0 ACB at receipt; full sale proceeds as capital gain** — simpler, deferred recognition
2. **FMV at receipt as income (line 13000); ACB = FMV; subsequent disposal is capital gain** — proper but more complex

Both are defensible. **Pick one and apply consistently across years and across all "received without payment" events.**

Most individual filers use Treatment 1 because it's simpler and CRA hasn't issued definitive guidance against it.

---

## What counts as "received without payment"

This category includes:

| Type | Examples |
|---|---|
| **Airdrops** | JUP (Jupiter), PENGU (Pudgy Penguins), BONK (Solana), WIF, various memecoin drops |
| **Play-to-earn rewards** | StepN (GST, GMT), Walken (WLKN), various P2E games |
| **Mining income** | Block rewards (Bitcoin, Ethereum classic, Monero, etc.) |
| **Staking rewards** | ETH staking, ATOM, ADA, SOL native staking (not liquid staking — see separate doc) |
| **Liquidity provider rewards** | Uniswap LP fees, Sushiswap rewards |
| **DeFi yield** | Aave deposits, Compound supplies |
| **Faucets / promotional drops** | New chain launches with promotional distributions |
| **Reward income from exchanges** | Coinbase USDC rewards, Wealthsimple cashback, exchange subscription rebates |

All of these have one characteristic: you received crypto without giving anything tangible in exchange (other than perhaps time, gas fees, or active participation).

---

## The two treatments

### Treatment 1: $0 ACB convention (most common in practice)

**Theory:** No FMV recognized at receipt. The token enters your inventory with $0 ACB. When you eventually dispose of it, the full sale proceeds become a capital gain.

**Mechanics:**
| Event | Treatment |
|---|---|
| Receive 1,000 tokens of XYZ via airdrop | Receipt at $0 ACB. No income recognized. |
| Hold XYZ for 6 months | No tax events. |
| Sell 1,000 XYZ for $5,000 CAD | Capital gain $5,000 (proceeds − $0 ACB). |

**Pros:**
- Simple
- Defers tax recognition
- 50% capital gain inclusion is favorable (vs 100% income inclusion)
- Avoids the FMV-at-receipt valuation problem for thin-market tokens
- Common practice; CRA hasn't actively challenged

**Cons:**
- Aggressive position; CRA could theoretically require income recognition at receipt
- Sale event may be in a high-tax year vs lower-tax year
- Doesn't reflect economic reality (you DID receive value)

### Treatment 2: Income at FMV (proper)

**Theory:** When you receive an airdrop / reward, you have ordinary income equal to FMV at the time of receipt. The token's ACB becomes the FMV. Subsequent disposal is a capital event vs the ACB.

**Mechanics:**
| Event | Treatment |
|---|---|
| Receive 1,000 tokens of XYZ via airdrop (FMV $3/token at receipt = $3,000 total) | $3,000 ordinary income on T1 line 13000. ACB = $3,000. |
| Hold XYZ for 6 months | No tax events. |
| Sell 1,000 XYZ for $5,000 CAD | Capital gain $2,000 (proceeds $5,000 − ACB $3,000). |

**Pros:**
- Methodologically pure
- Matches business income / mining-as-business treatment
- Aligns with CRA's general "receipt of value = income" principle

**Cons:**
- More complex (need FMV at receipt for every drop)
- Income recognized at receipt (no deferral)
- FMV at receipt is often unclear for new tokens
- Higher tax rate (ordinary income 100% vs capital gain 50%)

### Comparison for total tax

Same example as above (receive 1,000 XYZ; eventually sell for $5,000):

| Treatment | Total reported | Tax (assume 53% MTR) |
|---|---|---|
| **1: $0 ACB** | $5,000 capital gain × 50% inclusion = $2,500 taxable | $1,325 |
| **2: FMV income** | $3,000 income + ($2,000 cap gain × 50%) = $4,000 taxable | $2,120 |

**Treatment 1 results in LOWER total tax** in most scenarios. This is why most individual filers prefer it.

---

## CRA's position (such as it is)

CRA has issued limited formal guidance on airdrops. Their general principles include:

- **Mining income**: If conducted as a business, recognize income at FMV at receipt (per CRA Folio S3-F11-C1)
- **Staking rewards**: Generally treated as income at FMV (when in a custodial setting that issues T-slips like Wealthsimple ETH staking)
- **Airdrops**: No formal position. Could argue either way.
- **Play-to-earn**: No formal position. Often treated similarly to mining if active participation required.

The "no formal position" gap is what allows Treatment 1 ($0 ACB) to be defended. The argument:

> "I received tokens without active participation or service rendered. The fair market value at receipt was negligible or undeterminable. I am treating disposition proceeds as full capital gain, consistent with general practice in the Canadian crypto community."

This argument is weakest when:
- The tokens had a clear, liquid market at receipt
- You actively participated (e.g., DeFi liquidity provision)
- The dollar amounts are large

---

## Decision tree for treatment

```
Did you actively engage to earn this asset?
│
├── YES (active mining, business-like staking, LP'ing, P2E with effort)
│   │
│   └── Recognize as INCOME at FMV at receipt (Treatment 2)
│       Use Line 13500 (business income) if a business operation
│       Use Line 13000 (other income) if not a business
│
└── NO (passive airdrop, faucet drop, promotional)
    │
    └── Choose Treatment 1 ($0 ACB) or Treatment 2 (income at FMV)
        Apply consistently across all such receipts
```

For most individuals receiving passive airdrops (JUP, PENGU, BONK, etc.) with no active participation, Treatment 1 is widely accepted.

For Wealthsimple ETH staking rewards, Treatment 2 is the practice because Wealthsimple reports FMV at receipt on their tax statements (Line 12100 or 13000).

For Coinbase US rewards (USDC rewards, subscription rebates), Treatment 2 is the practice because Coinbase issues 1099-MISC forms with FMV income.

---

## Examples (sanitized)

### Example A: Major airdrop (Treatment 1)

You receive 1,000 JUP tokens on January 31, 2024. FMV ~$1.50 USD = ~$2.00 CAD per JUP.

**Treatment 1 (chosen):**
- Receipt: 1,000 JUP at $0 ACB. No income recognition.
- December 2024 sale of 1,000 JUP for $1,500 CAD.
- Capital gain: $1,500 − $0 = $1,500.
- Taxable: $750 (50% inclusion). At 53% MTR: $397 tax.

**Treatment 2 (alternative):**
- Receipt: 1,000 JUP at FMV $2.00/JUP = $2,000 income.
- ACB: $2,000 ($2.00/JUP).
- December 2024 sale of 1,000 JUP for $1,500.
- Capital loss: $1,500 − $2,000 = -$500.
- Taxable income: $2,000 − $250 (50% of capital loss) = $1,750. At 53% MTR: $928 tax.

In this case, Treatment 1 saves $531 in tax because the token price fell after the airdrop.

### Example B: Multiple small airdrops (Treatment 1 wins)

You receive various Solana ecosystem airdrops totaling 50+ different tokens through 2024-2025. Most are worthless or thinly traded.

**Treatment 1 (chosen):**
- Each airdrop: $0 ACB.
- When you eventually swap/sell any of these via Jupiter aggregator, capital gain = proceeds.
- Simple to track in Koinly (defaults to this).

**Treatment 2 would require:**
- Determining FMV at each receipt (often impossible for thin-market tokens)
- Income recognition on dozens of receipts (potentially small amounts each but cumulatively significant)
- Tracking ACB per receipt

Treatment 1 is the only practical option for high-volume small airdrops.

### Example C: Wealthsimple ETH staking (Treatment 2, mandatory)

You stake ETH at Wealthsimple Crypto. Each week, Wealthsimple credits you with a small amount of ETH as staking yield. Wealthsimple's annual tax statement shows $632.47 CAD of staking rewards.

**Treatment 2 (mandated by Wealthsimple's reporting):**
- Receipt: each weekly reward at FMV (Wealthsimple captures this).
- Line 13000 income: $632.47 (total annual).
- ACB of the staked-back ETH: $632.47.

You cannot use Treatment 1 here because Wealthsimple has already reported FMV income to CRA (via T-slip equivalent or 1099-MISC for cross-border accounts).

### Example D: StepN/Walken gameplay rewards (Treatment 1, conventional)

You play StepN and earn GST tokens through walking activity. You play for months and accumulate thousands of GST.

**Treatment 1 (chosen):**
- Each GST received: $0 ACB at the time.
- When you eventually swap GST for SOL or USDC, the full proceeds become capital gain.
- This treatment is consistent with how Koinly handles in-game rewards (typically classified as receives without cost basis).

**Treatment 2 alternative:**
- Each GST received: FMV at receipt = income (could be hundreds of small income events).
- Cumulative income could be substantial ($5,000-$20,000+ for active players).
- But ACB then matches FMV, so subsequent disposal might be near-zero gain.

In this case, Treatment 1 is simpler but Treatment 2 might be MORE tax-efficient IF the user was in a low tax bracket during the accumulation years (income at low rate) vs high tax bracket at sale (gain at high rate). Choose based on your situation.

### Example E: Coinbase US rewards (Treatment 2, mandatory)

Coinbase US credits you with $263.66 USD of USDC rewards in 2025 (from holding USDC) plus $120.36 USD of subscription rebates (from Coinbase One). Total: $384 USD ≈ $518 CAD.

**Treatment 2 (mandated):**
- Line 13000 income: $518 CAD.
- ACB of the USDC received: $518 CAD.
- Subsequent disposal: no gain (USDC is stable; ACB = proceeds).

Coinbase issues 1099-MISC to the IRS for US recipients; CRA gets this data via tax treaty. You can't hide this as $0 ACB.

---

## Consistency requirements

Once you choose a treatment for a category, **apply consistently**:

| Category | Your treatment | Year-1 | Year-2 | Year-3 |
|---|---|---|---|---|
| Airdrops (JUP, BONK, etc.) | Treatment 1 ($0 ACB) | ✓ | ✓ | ✓ |
| Wealthsimple ETH staking | Treatment 2 (income at FMV) | ✓ | ✓ | ✓ |
| Coinbase US rewards | Treatment 2 (income at FMV) | ✓ | ✓ | ✓ |
| StepN gameplay rewards | Treatment 1 ($0 ACB) | ✓ | ✓ | ✓ |
| Mining (if applicable) | Treatment 2 (business income, FMV) | ✓ | ✓ | ✓ |
| Mining (hobby, if applicable) | Treatment 1 or 2 | choose | apply same | apply same |

**Switching treatment retrospectively requires CRA notification.** Switching prospectively (new tax year) is acceptable but should be documented.

---

## Special cases

### Hard forks

A blockchain forks (e.g., Ethereum Classic split from Ethereum, Bitcoin Cash from Bitcoin). You hold the original; you receive the new asset for free.

**Treatment:** Same as airdrop. Treatment 1 ($0 ACB) or Treatment 2 (income at FMV). Most filers use Treatment 1.

### NFT airdrops

You receive an NFT for free (e.g., from holding a certain collection or interacting with a protocol).

**Treatment:** NFTs are tricky because FMV is often unclear (no liquid market). Treatment 1 ($0 ACB) is the default.

### Wrapped/synthetic tokens received for participating in a protocol

You provide liquidity to Uniswap and receive UNI tokens as a reward. You stake in Aave and receive AAVE tokens as a reward.

**Treatment:** Generally Treatment 2 (income at FMV) because there's active participation and the FMV is clearly determinable. Less defensible to use Treatment 1.

### Tax-loss harvesting via airdrop-to-zero

You receive worthless airdropped tokens (FMV truly $0). No tax event under either treatment.

If later the token gains value: Treatment 1 ($0 ACB) means full proceeds become gain. Treatment 2 (income at FMV $0 = $0 income; ACB $0) gives same result.

For receive-then-immediately-worthless cases, both treatments converge.

### Airdrops to wallets you don't control

Some airdrops are sent to your "Solana wallet" but you don't recognize them — could be spam, scam, or legitimate. If you never engage with the tokens, are they income?

**Practical answer:** Most filers don't recognize "received but not claimed" tokens as income. If you never swap them, no tax event occurs. If you do eventually swap them, Treatment 1 (capital gain on proceeds) is the simplest.

---

## Documentation requirements

For each "received without payment" event, maintain:

1. **Source** (which protocol, project, exchange)
2. **Date** of receipt
3. **Quantity** received
4. **FMV at receipt** (even if using Treatment 1, document FMV for safety)
5. **Treatment applied** (Treatment 1 or 2)
6. **ACB recorded** (either $0 or FMV)
7. **Source documentation** (Etherscan tx, exchange statement, etc.)

In your tax software (Koinly, Cointracker), tag each receipt with the appropriate category for consistent processing.

---

## Cross-border considerations

### US-source airdrops (Coinbase US rewards, etc.)

These are reported to IRS via 1099-MISC. The IRS shares with CRA under the tax treaty. **You cannot hide US-source rewards** — they appear in CRA's records.

For US-source crypto rewards, Treatment 2 (income at FMV) is mandatory because the institution has already reported income to the IRS.

### Foreign (non-US) airdrops to Canadian-resident wallets

CRA doesn't automatically receive foreign-source airdrop data. Treatment 1 is more defensible here, but you must report all worldwide income as a Canadian resident.

---

## Summary table

| Type | Recommended treatment | Reasoning |
|---|---|---|
| Major exchange staking rewards (WS, Coinbase) | Treatment 2 (income at FMV) | Institution reports FMV to tax authority |
| Major exchange reward income (Coinbase USDC rewards) | Treatment 2 (income at FMV) | Same |
| Airdrops to self-custody wallets | Treatment 1 ($0 ACB) | Common practice; deferral benefit |
| Play-to-earn gameplay rewards | Treatment 1 ($0 ACB) | Common practice; FMV often unclear |
| Mining (business) | Treatment 2 (business income line 13500) | CRA position |
| Mining (hobby) | Either treatment | Choose based on consistency |
| Hard fork tokens | Treatment 1 ($0 ACB) | Common practice |
| NFT airdrops | Treatment 1 ($0 ACB) | FMV unclear for most |
| Active DeFi reward tokens (UNI, AAVE) | Treatment 2 (income at FMV) | Active participation |

---

## What CRA might ask

Common queries:
- "Did you receive any cryptocurrency without payment in [year]?"
- Response: List all such receipts with treatment applied.

- "How did you value these for tax purposes?"
- Response: "Treatment 1: $0 ACB at receipt, full proceeds as capital gain on sale. Documented in tax records."

- "Why didn't you report this as income?"
- Response: "Treatment based on common Canadian crypto practice for [category]. Applied consistently across [years]. CRA has not issued formal guidance against this treatment for [category]."

Most filers using Treatment 1 for airdrops/gameplay rewards have not been challenged by CRA, but it remains an area of potential audit risk for large amounts.

---

## Disclaimer

This guide is based on real-world Canadian crypto tax practice as of 2026. CRA's position on airdrops and gameplay rewards is not fully formalized. Both treatments described are defensible. Consult a qualified Canadian tax professional or CPA for your specific situation.

For corrections or contributions, please open a GitHub issue.
