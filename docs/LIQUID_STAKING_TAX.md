# Liquid Staking Tax Treatment for Canadian Crypto Filers

How to handle liquid staking derivatives (Lido stETH, Sanctum LST, Marinade mSOL, Rocket Pool rETH, etc.) under Canadian tax law.

> **This is not professional tax advice.** Engage a qualified Canadian tax professional or CPA for your specific situation. Liquid staking is an evolving area in crypto tax law.

---

## TL;DR

Liquid staking lets you stake a crypto-asset (typically ETH or SOL) while receiving a tradeable derivative token representing your stake. Examples: ETH → stETH (Lido), SOL → LST (Sanctum), SOL → mSOL (Marinade), ETH → rETH (Rocket Pool).

**Two defensible Canadian tax treatments:**

1. **Non-taxable wrap** (most common, used by Koinly and similar tools): the wrap and unwrap are non-taxable events. Pool ACB is unchanged. Tax recognized only when you actually dispose of the derivative or unstaked asset.

2. **Taxable swap** (strict CRA reading, less common in practice): the wrap is a disposition of the underlying asset; the derivative is acquired at FMV. Pool ACB recalculated.

**Pick one and apply consistently.** Most practitioners use #1 (non-taxable wrap) because:
- It mirrors how most tax software treats it
- It matches the economic reality (you can unwrap at any time)
- CRA hasn't issued definitive guidance otherwise

---

## What liquid staking is

Liquid staking solves a problem: traditional staking locks up your asset, and you can't trade or use it elsewhere. Liquid staking gives you a tradeable receipt token (the "liquid staking derivative" or LSD) that represents your stake + accumulated rewards.

Mechanics:
1. You deposit 1 ETH into Lido smart contract
2. Lido stakes the ETH on an Ethereum validator
3. Lido mints 1 stETH (representing your stake)
4. stETH accumulates value over time as the underlying ETH earns staking rewards
5. You can unstake at any time, returning your original ETH plus any yield

Many liquid staking protocols use **rebasing** (your balance of stETH grows over time) or **value-accumulating** (your balance is constant but the redemption rate vs ETH increases).

### Common liquid staking protocols and tokens

| Protocol | Underlying | Derivative | Notes |
|---|---|---|---|
| Lido (Ethereum) | ETH | stETH | Largest LSD, rebases daily |
| Rocket Pool (Ethereum) | ETH | rETH | Value-accumulating |
| Coinbase (centralized) | ETH | cbETH | Value-accumulating |
| Marinade (Solana) | SOL | mSOL | Value-accumulating |
| Sanctum / Various (Solana) | SOL | LST, JitoSOL, bSOL, etc. | Multiple variants |
| Frax (Multi-chain) | ETH | sfrxETH | Rebasing |

---

## Treatment 1: Non-taxable wrap (most common)

### Theory

The wrap (depositing ETH for stETH) and unwrap (redeeming stETH for ETH) are treated as **non-taxable transactions** — like wrapping ETH as WETH, or moving between your own wallets.

The reasoning:
- Same economic ownership (you can unwrap any time)
- Same beneficial interest in the underlying asset
- The derivative is a "receipt" for the underlying, not a different asset

### Tax mechanics

| Event | Treatment |
|---|---|
| Wrap (ETH → stETH) | Non-taxable. Pool ACB unchanged. |
| Hold stETH (rebasing) | Daily rebases are NOT income at FMV. Treated as natural appreciation of pool value. |
| Unwrap (stETH → ETH) | Non-taxable. Pool ACB unchanged. |
| Sell stETH or unwrapped ETH | Taxable disposition at FMV. ACB = pool ACB. Capital gain = proceeds − ACB. |

### Practical example

You wrap 4.5 ETH into stETH on May 20, 2023. At that time:
- Your ETH pool: 33.73 ETH at $107,823 ACB → $3,197/ETH
- Pool ACB unchanged: 33.73 ETH at $107,823

You hold for 2 years. By May 2025:
- stETH has rebased to ~5 ETH worth (4.5 original + ~0.5 yield)
- Pool ACB still: 33.73 ETH at $107,823 (no income recognized)

You unwrap and sell 5 ETH for $15,000 CAD in June 2025:
- Sale proceeds: $15,000
- ACB used (weighted-average pool): 5 × $3,197 = $15,985
- Capital loss: -$985

Note: under this treatment, the 0.5 ETH of accumulated yield is NOT separately taxed as income. Its FMV becomes part of the disposition proceeds at sale time.

### Documentation

To support non-taxable wrap treatment:
- Note: "Liquid staking wrap treated as non-taxable per consistent treatment in tax software [Koinly / Cointracker / etc.] and per general practice that derivative represents same underlying asset"
- Keep records of wrap/unwrap transactions for verification
- Track underlying asset pool ACB unchanged through wrap/unwrap events

### Pros

- Simpler accounting
- Matches most tax software defaults
- Defers tax recognition to actual disposal
- Mirrors economic reality (you didn't really "trade" assets)

### Cons

- Aggressive position; CRA could theoretically challenge
- Yield accumulates without periodic income recognition
- All yield realized as capital gain (vs ordinary income), which is actually favorable

---

## Treatment 2: Taxable swap (strict CRA reading)

### Theory

The wrap is a disposition of the underlying (you give up ETH, receive stETH). Two different assets. Two different tokens. Two different chains-of-custody. Both are taxable events under CRA's general crypto-to-crypto swap principle.

### Tax mechanics

| Event | Treatment |
|---|---|
| Wrap (ETH → stETH) | TAXABLE. ETH disposed at FMV; stETH acquired at same FMV. |
| Hold stETH (rebasing) | Each rebase = received tokens at $0 ACB (or FMV-as-income). |
| Unwrap (stETH → ETH) | TAXABLE. stETH disposed at FMV; ETH acquired at same FMV. |
| Sell ETH | Taxable. ACB = FMV at unwrap. |

### Practical example

You wrap 4.5 ETH into stETH on May 20, 2023. ETH FMV: $2,000/ETH.

- Wrap event: disposition of 4.5 ETH at $9,000 FMV
- ACB used (weighted-avg, suppose $3,197/ETH): 4.5 × $3,197 = $14,387
- **Capital loss on wrap: $5,387**
- stETH acquired: 4.5 stETH at $9,000 ACB ($2,000/stETH)

You hold and unwrap May 2025. ETH FMV: $3,000/ETH. stETH redeems to 5 ETH (incl. yield).

- Unwrap event: disposition of 4.5 stETH at $13,500 FMV (5 ETH × $2,700 / 1)
- Actually wait — stETH redeems to 5 ETH at $3,000/ETH = $15,000
- Disposition of 4.5 stETH at $15,000 FMV
- ACB used: 4.5 × $2,000 = $9,000
- **Capital gain on unwrap: $6,000**
- ETH acquired: 5 ETH at $15,000 ACB ($3,000/ETH)

You sell 5 ETH for $15,000:
- ACB: $15,000
- Proceeds: $15,000
- Gain: $0

Cumulative tax recognition: -$5,387 + $6,000 + $0 = +$613 capital gain

### Documentation

To support taxable swap treatment:
- Record each wrap/unwrap as separate Schedule 3 entries
- Cross-reference each with on-chain transaction hash
- Note: "Liquid staking wrap treated as taxable disposition per Section 47 weighted-average ACB applied to each event"

### Pros

- Methodologically pure
- Matches strict crypto-to-crypto swap doctrine
- Crystallizes tax events as they happen (vs deferring)

### Cons

- More complex accounting
- More tax events to track
- Periodic income recognition for rebasing tokens

---

## Which treatment to choose?

### Factors favoring Treatment 1 (non-taxable wrap)

- You hold the LSD for >1 year (deferral benefit)
- Your tax software (Koinly, Cointracker) defaults to this
- You've used this treatment for prior years (consistency)
- The wrap activity is purely for staking yield (not trading)

### Factors favoring Treatment 2 (taxable swap)

- You actively trade LSDs (frequent buy/sell)
- You use LSDs as collateral in DeFi (where they're treated as different asset)
- You wrap large amounts at low ACB (Treatment 2 triggers losses that could offset other gains)
- You expect CRA to issue guidance preferring this method

### Practical recommendation

**Default to Treatment 1 (non-taxable wrap)** unless you have a specific reason to choose otherwise. It's simpler, matches tool defaults, and aligns with most current practice.

**Be consistent.** If you use Treatment 1 for ETH → stETH, use it for SOL → mSOL too. Don't pick the treatment that's most favorable for each asset individually.

---

## Worked examples (both treatments)

### Example: Sanctum LST roundtrip

You stake 647 SOL on Sanctum on Feb 4, 2024. You receive 507.87 LST (ratio reflects accumulated yield). You unwind 18 months later (Jun 18, 2025) for ~723.56 SOL.

| Event | Treatment 1 (non-taxable) | Treatment 2 (taxable) |
|---|---|---|
| Stake 647 SOL → 507.87 LST | Non-taxable. Pool unchanged. | Disposition of 647 SOL at FMV (say $85,064). Acquisition of 507.87 LST at $85,064 ACB. Capital gain/loss on SOL disposal. |
| Hold LST 18 months | No tax events. | If LST rebased, periodic income at FMV. If value-accumulated (LST didn't rebase), no events. |
| Unstake 507.87 LST → 723.56 SOL | Non-taxable. Pool unchanged. | Disposition of 507.87 LST at FMV (say $146,211). Acquisition of 723.56 SOL at $146,211 ACB. Capital gain/loss on LST disposal. |
| Sell 723.56 SOL for $200,000 | Taxable. ACB = original SOL pool weighted avg × 647 (original) − some adjustment for yield realized at sale. | Taxable. ACB = $146,211 (from unwrap). Gain = $200,000 − $146,211 = $53,789. |

The end-state cumulative tax is similar under both treatments. Treatment 2 triggers more intermediate tax events but doesn't fundamentally change the total tax.

---

## Yield treatment

### Under Treatment 1 (non-taxable wrap)

The yield is implicit in the derivative's accumulated value. When you unwrap or sell, the additional value (compared to original ACB) is realized as **capital gain**, not income.

### Under Treatment 2 (taxable swap)

Two sub-options for yield:
- **(a)** Rebases / accumulations recognized as **income at FMV** when received → reduces future capital gain
- **(b)** Rebases recognized as $0 ACB token acquisitions → all gain realized as capital gain on sale

In practice, most tax software uses (b) — treats yield as $0 ACB additions to the pool. This is functionally similar to Treatment 1 for tax outcome.

---

## Special considerations

### When the derivative depegs from the underlying

stETH famously depegged from ETH in 2022, trading at a discount. If you sold stETH during depeg:
- Treatment 1: capital loss recognized at the time of stETH sale (vs your ETH pool ACB)
- Treatment 2: capital loss on stETH (vs stETH ACB at wrap time)

Both treatments can recognize losses; the specific number differs slightly.

### Using LSD as DeFi collateral

If you deposit stETH into Aave as collateral, the question of whether you've "disposed of" your stETH arises. Under Treatment 1, collateral deposit is non-taxable (you retain economic ownership). Under Treatment 2, you may need to evaluate.

Generally, depositing into a lending protocol where you retain withdrawal rights = non-taxable. Trading away the rights = taxable.

### LSD-to-LSD swaps

If you swap stETH for rETH (both ETH derivatives), this is more clearly a taxable swap (two different protocols' tokens, not the same underlying).

### Solana LST ecosystem (multiple derivatives)

Solana has many LSD options (mSOL, LST, JitoSOL, bSOL, etc.). Each is a separate token. Swapping between them is a taxable swap; staking and unstaking with the same protocol can use non-taxable treatment.

---

## Consistency across tax years

Once you choose a treatment, document it and apply consistently going forward:

| Year | Treatment | Notes |
|---|---|---|
| 2022 | Non-taxable wrap | Lido stETH event; Koinly's default; documented in tax records |
| 2023 | Non-taxable wrap | Continued; no LSD disposals |
| 2024 | Non-taxable wrap | Added Sanctum LST; same treatment |
| 2025 | Non-taxable wrap | LSDs disposed; capital gain recognized at sale only |

If you change treatment, document why and apply going forward only (don't retroactively re-do prior years).

---

## Documentation per LSD position

For each liquid staking position, retain:

1. **Stake/wrap transaction**
   - Date
   - On-chain transaction hash
   - Amount wrapped
   - Derivative received
   - Treatment applied (1 or 2)

2. **Periodic snapshots**
   - Year-end derivative balance
   - Implied underlying value
   - Any reward / yield accrual

3. **Unstake/unwrap transaction**
   - Date, hash, amounts
   - Treatment

4. **Final disposition**
   - Sale date, proceeds, ACB
   - Capital gain/loss calculation

---

## What CRA might ask

In a review, CRA could query:

- "Why didn't you report the stETH wrap as a disposition?"
- Response: "Treated as non-taxable wrap consistent with [tax software] default and general practice. Documented in records."

- "How did you calculate ACB on the LSD?"
- Response: "Same as the underlying asset pool. No separate ACB tracking since wrap was non-taxable."

- "Why is your yield not on Line 13000?"
- Response: "Yield captured at disposal as part of capital gain on sale of the derivative/underlying."

If pressed harder (e.g., CRA insists on Treatment 2), you can either:
- Accept reassessment and adjust prior years
- Object via Notice of Objection

For most filers, Treatment 1 is unchallenged.

---

## Summary

| Aspect | Treatment 1 (Non-taxable Wrap) | Treatment 2 (Taxable Swap) |
|---|---|---|
| Wrap event | No tax | Capital gain/loss on underlying |
| Hold (rebase) | No tax | Either income at FMV or $0 ACB additions |
| Unwrap event | No tax | Capital gain/loss on derivative |
| Final sale | Capital gain/loss vs original pool | Capital gain/loss vs current pool |
| Defensibility | Strong (matches practice) | Strong (matches doctrine) |
| Complexity | Low | High |
| Tax software default | Treatment 1 | Manual |

**Default choice for most users: Treatment 1 (non-taxable wrap).** Consistency across years is more important than which treatment you pick.

---

## Disclaimer

This guide is based on real-world Canadian crypto tax practice as of 2026. CRA has not issued specific guidance on liquid staking derivatives. The two treatments described are both defensible. Consult a qualified Canadian tax professional or CPA for your specific situation.

For corrections or contributions, please open a GitHub issue.
