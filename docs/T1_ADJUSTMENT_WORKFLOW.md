# T1 Adjustment Workflow for Canadian Crypto Filers

A practical guide to amending a previously-filed Canadian T1 return when you discover unreported cryptocurrency activity or need to correct ACB.

> **This is not professional tax advice.** Engage a qualified Canadian tax professional or CPA for your specific situation. This document reflects real-world experience as of 2026 but CRA rules and tooling change.

---

## When you need this guide

You filed your T1 by the deadline. Later you discover:

- Self-custody wallet activity you didn't report
- A capital loss carryforward that increased after a Notice of Reassessment for a prior year
- Crypto rewards or staking income you forgot to disclose
- Additional business expenses or deductions you missed
- An ACB methodology error (e.g., used separate pools when global pooling per Section 47 ITA was required)
- An exchange's prepared cost basis was wrong and needs correction

You need to file a **T1 Adjustment**. There are three methods, with very different practical characteristics.

---

## The three amendment methods

### Method A — ReFILE via NETFILE (through certified tax software)

**Speed:** Fastest. 1-3 weeks processing after submission.
**Best for:** Simple corrections where your tax software still has your filed return open.

How:
1. Open your filed return in Wealthsimple Tax, TurboTax, StudioTax, etc.
2. Find the "ReFILE" or "Amend" function (often hidden behind a gear icon or "Make changes")
3. Edit the lines that need correction
4. Submit electronically through NETFILE

**Limitations:**
- Some return types aren't supported by ReFILE (e.g., bankruptcy, marital change, certain credits)
- Cannot be used until your **original return has been assessed** (NOA issued)
- Maximum 9 ReFILE submissions per return per year

### Method B — Change My Return (CRA My Account)

**Speed:** Medium. 4-6 weeks processing.
**Best for:** Most amendments when software ReFILE fails or you want direct CRA interaction.

How:
1. Log into CRA My Account
2. Tax returns → Change My Return → select the year
3. Add the line changes one at a time
4. Use the comment box to explain your reasons
5. Upload supporting documents via "Submit documents"

**Limitations:**
- Requires NOA on file
- Has line-by-line maximums (some lines can only be changed certain ways)
- Cannot include complex schedule changes; references to "see attached" require Submit documents flow

### Method C — Paper T1-ADJ (mailed form)

**Speed:** Slowest. 8-12 weeks processing.
**Best for:** Last resort when A and B both fail. Or when you have many supporting documents to attach.

How:
1. Download Form T1-ADJ (T1 Adjustment Request) from CRA
2. Fill in identifying info, lines being changed, reasons
3. Attach all supporting documents
4. Mail (tracked) to your tax centre

**Limitations:**
- Slowest processing
- Higher error rate (manual handling at CRA)
- Risk of mail loss without tracking

---

## ⚠️ The critical rule: wait for your NOA first

**All three methods require your original return to be assessed first.**

CRA's official guidance: https://www.canada.ca/en/services/taxes/income-tax/personal-income-tax/after-you-file/change-return.html

> "To request a change to your return, wait until you receive your notice of assessment (NOA) before submitting your request."

If you try to amend before the NOA arrives, expect rejection. The most common error you'll see is:

### NETFILE Result Code 686

> "The Canada Revenue Agency cannot process this ReFILE due to system constraints. If the entries are correct, please send a paper T1 Adjustment form and attach all pertinent slips and receipts."

**Don't be misled by the "send paper T1-ADJ" message.** Paper T1-ADJ has the same NOA-first requirement. The system message is generic. The actual fix: **wait for your NOA**.

Typical NOA timing:
- **Simple returns filed by April 30:** NOA in 2-4 weeks
- **Returns with rental/business income (June 15 filers):** NOA in 4-12 weeks
- **Complex returns flagged for review:** longer

---

## Recommended decision tree

```
Did your original return get its NOA?
│
├── NO → STOP. Pre-pay any expected amendment liability to your tax account
│        (via online banking, payee "CRA Revenue — current year")
│        to neutralize interest exposure. Then wait.
│
└── YES → Try Method A (ReFILE) first
         │
         ├── ReFILE succeeded → Done. Upload supporting docs to My Account.
         │
         ├── ReFILE rejected → Try Method B (Change My Return)
         │                    │
         │                    ├── Change My Return succeeded → Done.
         │                    │
         │                    └── Change My Return failed → Method C (paper)
         │
         └── ReFILE not available (return type unsupported) → Method B → Method C
```

---

## The "wait for NOA" trap and how to handle it

You file your original return owing money. You pay it. **Then** you realize you have an amendment to make that will increase your liability. The amendment can't be submitted until the NOA arrives.

**Common worry**: "Will my overpayment be refunded before I can amend? Will I owe penalties / interest?"

**Honest answer:** Yes, the refund will likely happen. CRA processes returns sequentially and refunds overpayments after assessment. You'll receive the refund within 1-2 weeks (direct deposit) or 3-4 weeks (cheque).

**Interest exposure is minimal because:**
1. Interest accrues on **arrears** (negative balance), not transient gaps
2. During the refund period, your tax account balance is $0 (no arrears)
3. Interest only starts after the reassessment is processed and new tax assessed
4. If you pay immediately upon reassessment notice, you owe maybe $30-100 in interest

### Pre-payment strategy

Even though you'll receive a refund, you can **pre-pay the expected additional tax** anyway:

1. Log into CRA My Account → Accounts and payments → Make a payment
2. Select: "Pay personal tax owing or by instalment"
3. Tax year: current year
4. Amount: original filed amount **plus** expected amendment increase
5. Submit via online banking

After amendment is processed:
- Total payable: (original filed) + (amendment increase)
- Less: your pre-payment
- Result: small refund or zero

This keeps interest exposure at $0 and avoids the refund-then-rebill cycle entirely.

---

## Preparation checklist (do BEFORE NOA arrives)

While you wait, prepare everything so submission is fast:

- [ ] Draft your line-by-line changes (line number, original, revised, reason)
- [ ] Calculate the revised tax payable
- [ ] Write a cover letter explaining the amendment
- [ ] Assemble supporting documents (transaction records, exchange reports, NORA for any updated carryforward, etc.)
- [ ] Decide which method (A, B, or C) you'll try first
- [ ] Pre-pay expected additional liability to neutralize interest
- [ ] Set a calendar reminder to check CRA My Account for NOA arrival
- [ ] Save the cover letter and supporting docs in a clearly-labeled folder

When the NOA arrives, you submit within minutes — not days.

---

## Cover letter content (recommended structure)

A good amendment cover letter includes:

1. **Subject line**: "T1 Adjustment Request — [Tax Year] — [Your Name]"
2. **Summary table**: Filed line → Revised line, with delta
3. **Reason for amendment**: Why each change is being made (3-5 sentences per line)
4. **Methodology section**: How you calculated revised numbers (e.g., "applied weighted-average ACB across all wallets per Section 47 ITA")
5. **Voluntary disclosure context**: Note that the amendment is filed proactively before any CRA inquiry
6. **Supporting documents list**: What you're attaching
7. **Signature**

See `docs/COVER_LETTER_TEMPLATE.md` in this repo for a starter template.

---

## Penalty exposure (usually minimal for voluntary disclosure)

CRA distinguishes between:
- **Innocent mistake**: amendment filed before CRA detection → no penalty
- **Failure to file**: filed return omitted obvious income → small penalty possible
- **Repeated failure**: previously assessed for failure to report → larger penalty
- **Gross negligence**: intentional omission → significant penalty + interest

For most crypto amendments where you're voluntarily disclosing previously-unreported activity:
- No penalty if it's your first such amendment
- Interest at CRA's prescribed rate (~10% annualized in 2025-2026) on the unpaid balance
- VDP (Voluntary Disclosures Program) protection if the amount is large enough to qualify

If you're worried about penalty exposure on a large amendment, consult a CPA about VDP eligibility before filing.

---

## CARF context (2026 onwards)

Canada's Crypto-Asset Reporting Framework takes effect January 1, 2026. Custodial exchanges (Coinbase, Wealthsimple Crypto, Binance, etc.) report year-end balances AND annual transaction summaries directly to CRA.

**Implication for amendments:** If you haven't been reporting your crypto activity, CARF will eventually expose it. Voluntary amendment now is significantly cheaper than reactive defense after CARF flag.

Many practitioners are recommending Canadian crypto users do a comprehensive review of past years (2021-2024) and file amendments where needed BEFORE the first CARF reporting cycle generates audit prompts.

---

## Common amendment scenarios

### Scenario 1: Forgot to report self-custody activity

You filed your T1 based on your custodial exchange's tax report. Later realized your MetaMask / Phantom / Solflare activity wasn't in that report.

**Fix:** Add Schedule 3 line 15301 entries for the self-custody dispositions. Use weighted-average ACB across all wallets. Document each disposition.

### Scenario 2: Carryforward updated by prior-year NORA

You filed claiming X in capital loss carryforward. After your prior-year reassessment, the actual carryforward is X+Y.

**Fix:** Update line 25300 to claim the full carryforward. CRA's records should reflect the updated amount; if Auto-Fill My Return still shows the old value, manually override and cite the NORA reference number.

### Scenario 3: Realized you should have used global pooling for an asset

You used your custodial exchange's separately-tracked ACB. You should have applied Section 47 ITA weighted-average across all your holdings of that asset.

**Fix:** Recalculate ACB. See `docs/COMBINED_POOL_ACB.md` for methodology. Be prepared to defend the consistency of your approach across all relevant assets (don't apply combined pool to one asset but not another without reason).

### Scenario 4: NFT or token became permanently inaccessible

A platform shut down. A migration window expired. A bridge was hacked. You can no longer access certain crypto-assets.

**Fix:** Claim deemed disposition at $0 proceeds, with documented evidence of the shutdown/loss event. See `docs/ABANDONMENT_CLAIMS_GUIDE.md` (forthcoming).

### Scenario 5: Staking income or rewards not reported

You received staking rewards, airdrop tokens, or exchange rewards that were never reported on T1.

**Fix:** Add to T1 line 13000 (Other income) at FMV at time of receipt. Be consistent year-to-year on treatment.

---

## Defending against CRA queries

After you submit, CRA may have questions. Common ones and how to respond:

| If CRA asks... | Be ready to provide |
|---|---|
| "Why did your ACB change?" | Methodology citation + spreadsheet showing recalculation |
| "Where did this disposition come from?" | Blockchain explorer transaction hash or exchange statement |
| "Why claim abandonment on this token?" | Public shutdown announcement, migration deadline date, etc. |
| "Why is your carryforward different from our records?" | Reference to specific NORA that updated it |
| "Why didn't you report this income before?" | Honest answer: oversight, complexity, didn't have the data, etc. |

Keep a defense binder organized by asset and by tax year. CRA queries typically come 6-18 months after amendment processing.

---

## Tooling tips

- **CoinStats CAD CSV** is the best source for CAD-denominated daily FX-corrected amounts (better than re-converting USD yourself)
- **Koinly** is a good cross-reference if you have a paid subscription
- **Don't trust any single source** — reconcile across at least two (exchange + on-chain explorer, or exchange + tax software)
- **Document your reconciliation work** in case CRA asks
- **NDAX and Bull Bitcoin** are Canadian exchanges that report in CAD natively
- **Coinbase 1099-DA** is issued to US IRS but CRA can request it via tax treaty

---

## Summary

| Method | Speed | When to use |
|---|---|---|
| **ReFILE (NETFILE)** | 1-3 weeks | First choice if return type supported |
| **Change My Return** | 4-6 weeks | If ReFILE fails or unavailable |
| **Paper T1-ADJ** | 8-12 weeks | Last resort |

**Always wait for the NOA first** regardless of method. Pre-pay any expected additional liability to your tax account to eliminate interest exposure. Prepare cover letter and documents in advance so submission is immediate when NOA arrives.

---

## Disclaimer

This guide is based on real-world Canadian crypto tax practice as of 2026. It is not professional tax advice. CRA rules and interpretations change frequently. Consult a qualified Canadian tax professional or CPA for your specific situation.

For corrections or contributions, please open a GitHub issue.
