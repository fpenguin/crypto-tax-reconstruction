# Abandonment Claims for Worthless Crypto-Assets

How to claim a capital loss in Canada when crypto-assets become permanently inaccessible, worthless, or stranded due to platform shutdowns, failed migrations, or dead blockchains.

> **This is not professional tax advice.** Engage a qualified Canadian tax professional or CPA for your specific situation. Abandonment treatment is a developing area in Canadian crypto tax law.

---

## TL;DR

You can claim a **deemed disposition at $0 proceeds** for crypto-assets that have become permanently unrecoverable, generating a capital loss equal to the asset's adjusted cost base. This is sometimes called an "abandonment claim."

CRA has not issued a definitive position on crypto abandonment. The position is supported by:
- Section 50(1) ITA logic (deemed disposition of worthless property), even though the section technically applies to debts and shares
- General CRA practice of accepting documented worthless dispositions
- Consistency with how similar non-crypto property losses are treated

To claim defensibly, you need: (1) a clear shutdown / loss event, (2) documented date and evidence, (3) good-faith determination that recovery is impossible, (4) consistent treatment with prior filings.

---

## What "abandonment" means in this context

In Canadian tax, abandonment is not a formal disposition category. The principle is:

> Property that has become permanently inaccessible or worthless **should** be treated as if disposed of at $0 proceeds, generating a capital loss equal to its adjusted cost base.

For crypto-assets specifically, this can apply when:
- A platform shuts down and you cannot withdraw
- A blockchain migrates and you missed the migration window
- A token contract is paused/dead and trades at $0
- An NFT marketplace is defunct and tokens can't be listed
- A wallet was compromised (hacked / stolen) — though CRA treats theft differently
- A protocol was hacked, funds drained, and recovery is impossible

For each, you must determine: "Could a reasonable person believe these assets will never be recovered?"

---

## Five categories of defensible abandonment claims

### Category 1: Platform shutdown with no asset return

**Trigger event:** Centralized platform announces shutdown; users cannot withdraw.

**Examples (publicly documented):**
- Mt. Gox (2014) — most users never got assets back
- Voyager Digital (2022 bankruptcy) — partial returns over years
- Celsius Network (2022 bankruptcy) — protracted Chapter 11
- BlockFi (2022 bankruptcy)
- Various smaller exchanges that simply closed (e.g., Cred, Coinflex)

**Defensibility:** STRONG when shutdown is publicly documented and you have records showing your account at the platform.

**Documentation required:**
- Platform's shutdown announcement (URL, screenshot, archive.org link)
- Your account statement showing balance at time of shutdown
- Any correspondence with platform attempting recovery
- Bankruptcy filings if applicable

**Timing:** Claim in the year the shutdown becomes effectively permanent (often the year of bankruptcy filing or "last hope of recovery" event).

### Category 2: Failed blockchain migration

**Trigger event:** A blockchain migrates to a new network and requires users to opt-in to receive new tokens. You missed the window.

**Examples:**
- Fantom → Sonic migration (FTM holders had to swap to S; some missed deadline)
- Klaytn → Kaia migration (KLAY → KAIA conversion)
- Various ICO-era tokens migrating from one chain to another
- Pre-merge Ethereum forks (some old contracts on ETC, EthereumPoW)

**Defensibility:** STRONG when the migration window publicly closed and you didn't act.

**Documentation required:**
- Migration announcement with deadline date
- Evidence that you didn't migrate (your wallet still showing old tokens)
- Date of "no longer accessible" determination

**Timing:** Claim in the year the migration window closed (or the year you confirmed unrecoverability).

### Category 3: Dead token contract / project collapse

**Trigger event:** Token contract has zero trading volume, project team disbanded, no liquidity available.

**Examples:**
- Many 2017 ICO tokens (paused or de-listed by all exchanges)
- Failed DeFi protocols (where the token has no purpose left)
- Pre-FTX collapse Solana ecosystem tokens (StepN GST/GMT after game collapsed)
- BUSD on BEP-20 chain after Paxos discontinuation
- Various rug-pulled meme tokens

**Defensibility:** MEDIUM-STRONG when the project's death is documentable.

**Documentation required:**
- Trading volume showing $0 on major exchanges
- Project's social media silence / discontinuation announcement
- Failed redemption attempts
- Token contract status (paused, abandoned developer)

**Timing:** Claim in the year you confirmed unrecoverability. Best practice: take a screenshot of CoinGecko / CoinMarketCap showing $0 or no listing.

### Category 4: Game/platform NFTs after game shutdown

**Trigger event:** Web3 game collapses or shuts down. In-game NFTs become orphan assets with no marketplace activity.

**Examples:**
- Aglet (sneaker collection app, NFTs trapped in iOS app after platform shutdown March 2024)
- 5KM (move-to-earn, project collapsed post-FTX)
- Various play-to-earn projects from 2021-2022 era
- Defunct NFT marketplaces (some lost user access entirely)

**Defensibility:** MEDIUM. Stronger when there's a public shutdown announcement; weaker when the NFTs technically still exist on-chain with minimal market.

**Special consideration:** If NFTs still have any market (even floor of $5), CRA may argue they're not abandoned. Solution: actually sell on OpenSea for the floor price (real disposition with real proceeds, even if small).

**Documentation required:**
- Platform shutdown announcement / app store removal
- Inability to access wallet (for app-locked NFTs)
- Or proof of attempted sale at zero/near-zero (e.g., sold to Unsellable.com for $0.01)

### Category 5: Lost / forgotten access (not abandonment per CRA)

⚠️ **NOT a valid abandonment claim** per CRA's typical position:

- Lost private keys
- Forgotten passwords
- Hardware wallet destroyed without backup
- Self-induced "ragequit" where you sent assets to dead address

CRA's reasoning: lost-key losses are typically considered **personal carelessness**, not deemed disposition. The asset still exists; you just can't access it. (Compare to losing cash — not a tax-deductible loss.)

**Workaround:** If you can document the access loss in a way that's beyond your control (theft, fire, etc.), it may qualify. Consult a CPA.

---

## Defensibility framework

For each abandonment claim, ask:

### Question 1: Is the loss event documented?

Strong evidence = public announcement with date.
Medium evidence = market data showing $0 / illiquidity.
Weak evidence = your subjective belief.

### Question 2: Is recovery objectively impossible?

Strong: contract paused, platform bankrupt, migration window expired.
Medium: practical inability (e.g., no exchanges list the token).
Weak: you "gave up trying."

### Question 3: Have you tried alternative dispositions?

Strong: documented attempt to sell at any price (even $0.01).
Medium: market shows no orders for months.
Weak: you assumed it was worthless without testing.

### Question 4: Are you treating similar assets consistently?

If you have other dead positions, claim all of them or none. Don't cherry-pick.

### Question 5: Is the ACB justifiable?

You must have evidence of what you paid for the asset (or how its ACB was established via prior transactions).

---

## Documentation requirements

For each abandonment claim, retain in your audit defense binder for at least 7 years:

1. **Shutdown event evidence**
   - Press release, blog post, social media announcement
   - Archive.org snapshot URL (use https://web.archive.org/web/<date>/<original-url>)
   - News article(s) confirming the event
   - Screenshot dated within reasonable proximity to event

2. **Your position evidence**
   - Wallet address showing the dead token / NFT
   - Exchange account statement showing the trapped balance
   - Quantity and ACB calculation

3. **Recovery attempts**
   - Emails to platform support
   - Migration attempts (even if failed)
   - Listing attempts on alternative platforms
   - Date you concluded "unrecoverable"

4. **Methodology note**
   - Brief explanation of why you're claiming abandonment in this year
   - Citation to public events that made the asset worthless
   - Statement of good-faith conclusion of unrecoverability

---

## When to claim — strict year vs flexible

### Strict year approach (purist)

Claim the loss in the year the loss event occurred (e.g., shutdown year).

**Pros:** Aligns precisely with economic reality.
**Cons:** Some tax years may be closed by statute of limitations.

### Flexible "confirmation year" approach (practical)

Claim in the year you formally confirmed unrecoverability during your tax review.

**Pros:** Allows you to claim within statute window.
**Cons:** Less precise; may face scrutiny if abused.

**Defense narrative for flexible approach:**

> "Following [event] on [date in prior year], I retained the assets in my wallet/account pending any potential recovery mechanism. During my [current tax year] comprehensive review, I confirmed permanent unrecoverability and am treating this as a deemed disposition at $0 proceeds."

This narrative is widely accepted for small-to-medium claims. For very large claims (>$50K), strict year is safer.

---

## Section 50(1) ITA — the formal mechanism (and its gap)

Section 50(1) of the Income Tax Act allows a taxpayer to elect deemed disposition at $0 for:
- Debts owed to the taxpayer that have become bad
- Shares of a corporation that has become bankrupt or insolvent

**The crypto gap:** Crypto-assets are typically property, not "debts" or "shares of a corporation." So Section 50(1) doesn't directly apply.

**However, the underlying principle (deemed disposition at $0 for worthless property) is generally accepted in practice by CPAs and CRA.** The technical mechanism is more like "I disposed of it for $0 because it became worthless" rather than a formal Section 50(1) election.

**For NFTs specifically:** Some commentators argue NFTs are "art" or "collectibles" with their own loss rules under different ITA sections. Treat carefully if the amount is large.

---

## Worked examples (sanitized)

### Example A: Failed platform shutdown

You purchased $5,000 of platform tokens on an exchange in 2022. The exchange shut down January 2024 with no asset return. You're claiming the loss on your 2024 T1.

| Element | Detail |
|---|---|
| ACB | $5,000 |
| Proceeds | $0 |
| Capital loss | $5,000 |
| Allowable capital loss (50%) | $2,500 |
| Documentation | Platform shutdown announcement; account statement; recovery attempt email |

### Example B: Missed blockchain migration

You held 1,000 OLDCHAIN tokens (ACB $3,000). NEWCHAIN migration window closed Dec 31, 2024. You didn't migrate. Tokens are now stranded.

| Element | Detail |
|---|---|
| ACB | $3,000 |
| Proceeds | $0 |
| Capital loss | $3,000 |
| Allowable capital loss (50%) | $1,500 |
| Documentation | Migration announcement with deadline; wallet showing OLDCHAIN balance still present; chain confirmation that OLDCHAIN no longer accepts transfers |

### Example C: Dead NFT after game collapse

You bought 2 game NFTs in 2022 for $1,500 each via OpenSea ($3,000 total ACB). The game project collapsed in late 2022. NFTs still technically exist on Ethereum but no buyers. You're claiming the loss on your 2025 T1.

| Element | Detail |
|---|---|
| ACB | $3,000 |
| Proceeds | $0 |
| Capital loss | $3,000 |
| Allowable capital loss (50%) | $1,500 |
| Documentation | Original Etherscan tx for NFT purchase; news articles about game collapse; OpenSea listing showing zero recent trades; statement of unrecoverability |

### Example D: When NOT to claim abandonment

You own 0.5 BTC in a hardware wallet. You forgot your PIN and have no seed phrase backup. You consider this a $30,000 loss.

**CRA's likely position:** Lost-key losses are not deductible. The BTC still exists; you just can't access it. No capital loss.

**Better approach:** Don't claim. Keep records in case CRA's position changes in future.

---

## Consistency across years

If you claim multiple abandonments in a single year, document them in a single table (with the same approach):

| Position | ACB | Loss event date | Confirmation year | Evidence |
|---|---|---|---|---|
| Aglet NFTs | $389 | March 28, 2024 (shutdown announcement) | 2025 (confirmed unrecoverable) | Apple receipts + shutdown announcement |
| BUSD on BEP-20 | $1,731 | Feb 2023 (Paxos discontinued) | 2025 (illiquid since) | Paxos announcement + on-chain dead state |
| FTM tokens | $1,256 | Migration window 2025 | 2025 (didn't migrate) | Sonic migration announcement |
| (etc.) | | | | |

Apply the same framework to each. If CRA queries one, the same defense applies to all.

---

## Claiming abandonment on a T1 amendment (T1-ADJ)

If you discover prior-year worthless assets during a current-year review:

1. Claim abandonment in the CURRENT year (using the confirmation year approach)
2. OR amend prior year's T1 to claim in the strict year (subject to statute of limitations)

Within statute limits, the strict year approach is cleaner. Past statute (e.g., 2022 closed in 2026), use confirmation year.

See `docs/T1_ADJUSTMENT_WORKFLOW.md` for the amendment mechanics.

---

## When CRA challenges your abandonment claim

If CRA reviews your return and questions an abandonment claim, you'll typically receive a query letter asking for:
- Evidence the asset is worthless
- Date of the loss event
- Your ACB calculation
- Why you couldn't dispose of the asset for any value

**How to respond:**
1. Provide all documentation from your binder
2. Reference the shutdown event, migration deadline, etc.
3. If pressed on "but couldn't you have sold it on OpenSea / wherever?", explain market conditions (zero volume, no listings, dead community)
4. If CRA disallows the claim, you can either:
   - Accept and pay the additional tax
   - Object via Notice of Objection (within 90 days of NORA)
   - Appeal to Tax Court (longer process)

For claims under ~$5,000, CRA typically accepts well-documented claims. For larger claims, expect more scrutiny.

---

## Alternative: actual sale via OpenSea or tax-loss harvesting services

For NFT positions with minimal but non-zero market value, consider an actual sale instead of abandonment claim:

1. List the NFT on OpenSea for the floor price (often a few hundred dollars or less)
2. Even if you accept a low offer, you have a documented disposition
3. Capital loss = ACB − sale proceeds

**Pros:** Unambiguous tax position; no abandonment defense needed.
**Cons:** Requires actually executing the sale; gas fees; may take time to find buyer.

**Tax-loss harvesting services** (e.g., Unsellable.com) accept worthless NFTs in exchange for nominal proceeds (often $0.01), allowing you to claim the loss cleanly. Verify the service's legitimacy and CRA's acceptance before relying on this.

---

## Summary

1. **Abandonment claim = deemed disposition at $0 proceeds** for worthless / unrecoverable crypto-assets.
2. **Five defensible categories**: platform shutdown, failed migration, dead contract, defunct NFT marketplace, post-hack failed recovery.
3. **NOT defensible**: lost keys, forgotten passwords (CRA treats as personal carelessness).
4. **Documentation matters**: keep shutdown announcements, account statements, recovery attempts.
5. **Consistency required**: same framework across all claims.
6. **Section 50(1) ITA doesn't directly apply** to crypto, but the underlying principle is accepted.
7. **For NFTs with minor market value**, consider actual sale instead of abandonment.

---

## Disclaimer

This guide is based on real-world Canadian crypto tax practice as of 2026. It is not professional tax advice. CRA's position on crypto abandonment is not fully formalized. Consult a qualified Canadian tax professional or CPA for your specific situation.

For corrections or contributions, please open a GitHub issue.
