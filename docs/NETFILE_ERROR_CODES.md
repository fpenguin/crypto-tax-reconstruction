# CRA NETFILE Error Code Reference

Real-world documentation of common CRA NETFILE rejection codes encountered by Canadian crypto filers, with explanations and remediation steps.

> **This is community-contributed documentation.** CRA's official error code list is at https://www.canada.ca/en/revenue-agency/services/e-services/digital-services-individuals/netfile-overview/error-codes.html — this document focuses on codes commonly hit by crypto filers.

---

## Quick reference

| Code | Meaning | Common cause | Fix |
|---|---|---|---|
| **686** | "CRA cannot process this ReFILE due to system constraints. Please send a paper T1 Adjustment." | Original return not yet assessed (no NOA) | **Wait for NOA**, then retry. Don't actually mail paper T1-ADJ pre-NOA. |
| **9** | Return rejected | Various — see specific message | Read specific message; usually duplicate filing or wrong year |
| **15** | Return contains errors | Validation failure | Run software's error check; usually missing fields |
| **32** | General system error | CRA system unavailable | Wait and retry; check CRA status page |
| **41** | Tax data inconsistent | Calculated values don't match | Re-run tax software; recalculate everything |
| **63** | Auto-Fill mismatch | Slips don't match CRA records | Verify T-slips against CRA Auto-Fill |
| **75** | NETFILE access code invalid | Wrong access code entered | Get current access code from latest NOA |
| **92** | Income mismatch | Reported income doesn't match slips | Cross-check T-slips, T5008, etc. |

---

## Code 686 — Most common for crypto filers

### Full message

> "The Canada Revenue Agency cannot process this ReFILE due to system constraints. If the entries are correct, please send a paper T1 Adjustment form and attach all pertinent slips and receipts. If you need assistance, please contact us. CRA NETFILE result code 686."

### Common cause

You're trying to ReFILE (amend) a previously-filed T1 return, but CRA hasn't issued the Notice of Assessment (NOA) for your original filing yet. The NETFILE ReFILE service requires the original return to be assessed first.

### Why crypto filers hit this often

The typical scenario:
1. You file your T1 by the deadline (April 30 or June 15)
2. Within days or weeks, you realize you forgot to report self-custody crypto, or you want to apply an updated carryforward from a recently-issued NORA for a prior year
3. You open your tax software and try to ReFILE
4. Rejection: code 686

### The misleading part of the message

CRA's message says "please send a paper T1 Adjustment form." This is generic fallback text and is **misleading** in this scenario.

**Reality:** Paper T1-ADJ has the same NOA-first requirement. You can't bypass it by switching to paper.

Per CRA's official guidance (https://www.canada.ca/en/services/taxes/income-tax/personal-income-tax/after-you-file/change-return.html):

> "To request a change to your return, wait until you receive your notice of assessment (NOA) before submitting your request."

### Remediation

1. **Don't mail paper T1-ADJ.** It will sit in CRA's processing queue and likely be returned unprocessed (or worse, processed in a way that conflicts with the eventual NOA).
2. **Wait for the 2025 NOA.** Typical timing: 2-12 weeks after filing depending on complexity and June-15 filer status.
3. **Pre-pay any expected additional tax** to your tax account NOW to neutralize interest exposure during the wait. Use online banking with payee "CRA Revenue — current year."
4. **Prepare amendment documents in advance** so you can submit within minutes of NOA arrival.
5. **When NOA arrives, retry ReFILE.** Should now succeed.
6. **If ReFILE still fails post-NOA**, use Change My Return in CRA My Account as your fallback.

See `docs/T1_ADJUSTMENT_WORKFLOW.md` for the full amendment workflow.

---

## Code 9 — General rejection

### Common cause

Multiple possibilities:
- Duplicate filing (you've already filed this year)
- Wrong tax year selected
- NETFILE access code mismatch
- Identity verification failure

### Remediation

Read the specific error message that accompanies code 9. CRA usually provides more detail. Common fixes:
- If duplicate: you've already filed; check CRA My Account
- If wrong year: verify the year selection in your tax software
- If access code: get current code from your most recent NOA

---

## Code 15 — Validation errors

### Common cause

Your tax software found errors during submission:
- Missing required fields
- Invalid SIN format
- Out-of-range amounts
- Missing T-slip information

### Remediation

Run your tax software's error check feature. Fix all flagged items. Re-submit.

---

## Code 32 — System error

### Common cause

CRA's NETFILE service is temporarily unavailable. This is rare but happens during:
- Peak season congestion
- Scheduled maintenance windows
- Unexpected outages

### Remediation

- Wait 1-4 hours and retry
- Check https://www.canada.ca/en/revenue-agency/news/system-status.html for known issues
- If persistent, contact CRA NETFILE help: 1-800-714-7257

---

## Code 41 — Tax data inconsistent

### Common cause

Your tax software calculated values that don't match what NETFILE expects:
- Manual override of a calculated field
- Software bug
- Outdated software version

### Remediation

- Update your tax software to the latest version
- Clear any manual overrides; let software recalculate
- If the issue persists, contact your tax software's support

---

## Code 63 — Auto-Fill mismatch

### Common cause

T-slips imported via Auto-Fill My Return don't match what you've entered manually, OR they don't match what CRA has on file.

### Remediation

- Re-run Auto-Fill My Return to pull latest slip data
- Cross-check each slip against your physical/digital copy
- Look for amendments to slips (e.g., T4 amended after initial issuance)

---

## Code 75 — Invalid NETFILE access code

### Common cause

The 8-character NETFILE access code on your most recent NOA isn't matching what you've entered. Common reasons:
- Typo
- Using prior-year's code instead of current
- Some characters look similar (O vs 0, I vs 1)

### Remediation

- Get current NETFILE access code from your most recent NOA
- Or skip it; you can NETFILE without it (it's optional)

---

## Code 92 — Income mismatch

### Common cause

Your reported income doesn't match CRA's records from employers, financial institutions, etc.

### Remediation

- Re-check T4, T4A, T5, T3 slips against CRA Auto-Fill records
- Look for slip amendments
- Verify foreign income reporting (T1135 if applicable)

For crypto filers specifically: this code rarely involves crypto data, since CRA didn't traditionally have crypto income records. Starting in 2026, with CARF, expect more code 92 errors related to crypto if your numbers don't match exchange reports.

---

## How to add new codes to this reference

If you encounter a NETFILE error code while filing crypto-related taxes:

1. Capture the full error message (screenshot recommended)
2. Note your scenario (what you were trying to do)
3. Document the resolution (what worked)
4. Submit a PR to this repo or open an issue

This document grows as the community contributes.

---

## When all else fails

If NETFILE submission is consistently rejected and you can't determine why:

1. **Call CRA NETFILE Help:** 1-800-714-7257
2. **Try Change My Return** in CRA My Account (different submission pathway)
3. **As last resort**, paper T1 or T1-ADJ via Canada Post (tracked mail to your tax centre)

For complex amendments where NETFILE rejects, the most efficient pathway is usually **wait for NOA → try Change My Return → if that fails, paper T1-ADJ**.

---

## Disclaimer

This reference is community-contributed and based on real-world experience as of 2026. CRA's official error code list may be more authoritative. Codes and their interpretations can change with CRA system updates.

For corrections or contributions, please open a GitHub issue.
