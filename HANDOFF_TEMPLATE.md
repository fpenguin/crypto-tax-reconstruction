# HANDOFF.md TEMPLATE — Multi-Year Crypto Tax Project

A template for creating a self-contained handoff document that any AI agent (Claude, Codex, GPT, successor) can use to pick up multi-year cryptocurrency tax work without prior memory of the project.

> **This is a template.** Copy to your own project folder as `HANDOFF.md`, then fill in the bracketed sections.

---

## Why use this template

Crypto tax reconstruction across multiple years often involves:
- 50+ wallets and exchanges
- 1,000+ transactions per year
- Multiple ACB methodology decisions
- Carryforward chains spanning years
- Real-world events affecting tax position (NORA, NOA, error 686, etc.)
- AI assistance across multiple sessions

Without a structured handoff, each new session requires re-explaining everything. With this template, a fresh AI agent can be productive within 10 minutes of reading.

---

## Template structure (16 sections)

Copy the content below into your `HANDOFF.md` and customize for your situation:

```markdown
# HANDOFF.md — [Your Project Name]

**Last updated:** [Date — keep updated after every session]
**Project status:** [One-line status: e.g., "2025 amendment pending NOA"]
**Next agent's first task:** Read this file. Then execute Section 4 decision tree.

---

## 🚨 START HERE — IF YOU ARE A FRESH AI AGENT

You have no memory of this project but everything you need is in this folder and its subfolders.

**Step 1:** Confirm with [taxpayer name] what's changed since this handoff was written:
- "Has [specific pending event] happened yet?"
- "Are you working on continuing [last activity] or starting [next phase]?"

**Step 2:** Based on answers, jump to the relevant section:
- [Status A] → Section [X]
- [Status B] → Section [Y]

**Critical context you must absorb before responding:**

1. Tax jurisdiction: [Canada / US / etc.]
2. Tax bracket: [marginal rate at top, e.g., 53.5% federal+BC]
3. Filing structure: [individual / joint / spouse name]
4. Filing deadline: [April 30 / June 15 / other]
5. ACB method: [Canada ACB / US FIFO / specific identification]
6. Currency: [all CAD unless marked USD]
7. Crypto venues used: [list]

**Hard "do not do" rules:**

- Do NOT [first restriction, e.g., reopen tax year XX (statute closed)]
- Do NOT [second restriction]
- Do NOT [recalculate ACB from scratch — use established choices in Section 9]
- Do NOT [other restrictions]

---

## 0. Project Summary (1-page version)

[2-3 paragraphs describing the engagement]

---

## 1. Current State (as of [date, time, timezone])

### What was just attempted/completed

- [Most recent action]
- [Result]
- [Outcome]

### Payment status (CRA / IRS tax account)

| Date | Action | Amount |
|---|---|---|
| [date] | [description] | [amount] |
| ... | ... | ... |
| **Total** | | **[total]** |
| Current owing/overpayment | | **[amount]** |

### Documents PREPARED but NOT YET SUBMITTED

Located in `/path/to/project/Refile_Kit_YYYY/`:

1. `01_Schedule3_Worksheet.xlsx`
2. `02_Transaction_Schedule.xlsx`
3. `03_Cover_Letter.docx`
4. [etc.]

### Final amendment numbers (locked)

| Line | Filed | Amended | Change |
|---|---|---|---|
| [line] | [val] | [val] | [delta] |
| ... | ... | ... | ... |

---

## 2. Why [current blocker/issue] happened

[Explanation of the most recent obstacle]

---

## 3. Timeline ahead (expected)

| Expected date | Event | Action required |
|---|---|---|
| [date] | [event] | [action] |
| ... | ... | ... |

---

## 4. DECISION TREE — When [trigger event]

**Trigger:** [description of event that initiates next action]

### Decision A: [first decision point]

[Instructions]

### Decision B: [if A succeeds]

[Instructions]

### Decision C: [fallback if A fails]

[Instructions]

### Decision D: [last resort]

[Instructions]

### Decision E: [post-action]

[Instructions]

---

## 5. Post-Submission (if already filed when next agent arrives)

[Instructions for continuing after submission]

### Verify acceptance

[Steps]

### Common queries and prepared responses

| If asked about... | Response template |
|---|---|
| [topic] | [response] |

---

## 6. Carryforward Chain Status

| Year | Net cap loss | Status as of [date] |
|---|---|---|
| [year] | [amount] | [status] |
| ... | ... | ... |

---

## 7. End-of-[year] Crypto Inventory (post-amendment)

### Active holdings (still on books)

| Asset | Quantity | Approx ACB | Location | Notes |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

### Abandoned (zeroed out, do NOT re-track)

- [Asset 1] (ACB $X) — [reason]
- [Asset 2] (ACB $Y) — [reason]
- ...

---

## 8. [Next Tax Year] — Known Events to Track

### Already known events

| Date | Event | Estimated tax impact |
|---|---|---|
| ... | ... | ... |

### Planned actions

1. [Action 1]
2. [Action 2]

### Estimated [next year] tax (rough)

[Rough projection]

---

## 9. Methodology Reference (USE FOR CONSISTENCY)

These were the methodology choices established for the [recent] amendment. Apply consistently in future years.

### Capital gains methodology

| Element | Choice | Rationale |
|---|---|---|
| Pooling method | [e.g., ACB Canada weighted-average per asset] | [reasoning] |
| [Asset] ACB pool | [e.g., combined (self-custody + WS)] | [reasoning] |
| ... | ... | ... |

### Income treatment

| Source | Treatment | T1 Line |
|---|---|---|
| Airdrops | $0 ACB at receipt | Schedule 3 |
| Staking rewards (custodial) | Income at FMV | Line 13000 |
| ... | ... | ... |

### Disposition methodology

| Event | Treatment |
|---|---|
| Crypto-to-crypto swap | Taxable disposition |
| Liquid staking wrap | Non-taxable / Taxable (pick and stick) |
| ... | ... |

---

## 10. Audit Defense Binder Index (file locations)

### Project root

`/path/to/project/folder/`

### Critical subfolders

| Folder | Contents |
|---|---|
| `Refile_Kit_YYYY/` | [description] |
| ... | ... |

### Evidence files (preserve 7 years)

**Authoritative tax records:**
- [Doc 1] — [where stored]
- [Doc 2] — [where stored]

**Acquisition receipts:**
- [Doc 1] — [where stored]
- ...

**Disposition records:**
- [Doc 1] — [where stored]
- ...

**Abandonment evidence:**
- [Doc 1] — [where stored]
- ...

**Prior year tax records:**
- [Doc 1] — [where stored]
- ...

---

## 11. Toolkit / Software Known Bugs

[List of known bugs in tools you've been using; don't trust their numbers blindly]

1. [Bug 1] — [workaround]
2. [Bug 2] — [workaround]

**Always prefer (in order):**
1. [Source 1]
2. [Source 2]
3. [Source 3]
4. [Local toolkit — use cautiously]

---

## 12. Key Contacts & References

### Government tax authority
- [Phone]
- [My Account / e-services URL]
- [Submit documents URL]
- Mailing address: [tax centre]
- [Useful guidance URLs]

### Tax software
- [Software 1] — support email
- [Account numbers]

### Reference numbers
- [Important reference 1]: [number]
- ...

---

## 13. [Family Member] (Spouse / Dependent) — Case [Status]

**Status as of [date]: [open / closed / pending]**

Key established facts (preserve for future reference):
- [Fact 1]
- [Fact 2]
- ...

---

## 14. Lessons Learned (for next agent — apply these)

[Numbered list of insights from this engagement that should inform future work]

1. [Lesson 1]
2. [Lesson 2]
3. ...

---

## 15. Quick-Start Prompt Template (for [taxpayer] to use next year)

When [taxpayer] returns and starts a new conversation, suggest this prompt:

```
I'm [taxpayer name], continuing my crypto tax work. Please read HANDOFF.md at
[full path]
before responding to anything else. After you've read it, ask me:
1. [Status question 1]
2. [Status question 2]
3. [What's the specific task you need help with today?]

Don't recalculate [thing] from scratch — use the established methodology in
HANDOFF.md Section 9. Don't [other restriction].
```

---

## 16. Files Inventory (full list at project root)

[Listing of all files in project, organized by folder]

**Project root files:**
- `HANDOFF.md` (this file)
- [file 1]
- [file 2]
- ...

**`subfolder1/` contents:**
- ...

---

## END OF HANDOFF

**Next agent: thank you for being thorough.** When you complete a session with [taxpayer], update this file to reflect new state. Append a new "Last updated" line at the top and add new sections as needed. The goal is that no matter who picks this up, they can be productive within 10 minutes of reading.
```

---

## How to use this template

1. **Copy this file** to your project root as `HANDOFF.md`
2. **Replace bracketed placeholders** with your project specifics
3. **Update after every session** with the taxpayer
4. **Keep all evidence files** referenced in Sections 10 and 16

---

## Sections that are critical for AI handoff success

### Section 0 — START HERE

Without this section, the next agent will read top-to-bottom and may take 30-60 minutes to get oriented. With it, they read this section first (2 minutes), confirm state with taxpayer (5 minutes), and jump to the relevant section.

### Section 4 — Decision Tree

Decision trees are far better than prose for AI agents. They reduce reasoning to "follow the branches based on user's situation."

### Section 9 — Methodology Reference

This is the **most important section** for consistency. AI agents will otherwise re-derive methodology from scratch (and sometimes choose differently than prior years). Pinning the choices prevents drift.

### Section 11 — Known Bugs

Without this, a new agent will trust the toolkit's output and apply incorrect numbers. Explicitly call out what NOT to trust.

### Section 15 — Quick-Start Prompt

Make it easy for the taxpayer to bootstrap a new agent session. The prompt should reference this file and demand the agent read it before responding.

---

## What to include vs exclude in HANDOFF.md

### Include (helps the agent)

- Decisions made and rationale
- Methodology choices
- Document file locations
- Carryforward state
- Pending tasks
- Known issues
- Contacts
- Decision trees
- Quick-start prompts

### Exclude (sensitive info)

- Social Insurance Numbers / Tax IDs
- Bank account numbers
- Specific dollar amounts (use rounded examples or [redacted])
- Real wallet addresses (use 0xexample...)
- Real transaction hashes (use txhash_example...)
- Phone numbers
- Email addresses (other than generic contact)
- Government correspondence reference numbers
- Family members' personal info beyond what's necessary

---

## Lifecycle: when to update HANDOFF.md

Update after EVERY significant session with the taxpayer:

- After completing a major task (e.g., submitted T1 amendment)
- After methodology decision (e.g., chose combined-pool ACB)
- After receiving CRA correspondence
- When discovering new information (e.g., found a missing wallet)
- When pivoting strategy (e.g., changed from paper T1-ADJ to ReFILE after NOA)

Update format:
1. Change "Last updated" date at top
2. Update Section 1 (Current State) with new facts
3. Add new entries to Section 4 (Decision Tree) if circumstances changed
4. Update Section 6 (Carryforward) if used or updated
5. Update Section 14 (Lessons Learned) with new insights
6. Don't delete old sections — append new info; preserve historical context

---

## AI agent compatibility

This template works across AI agents because it:
- Uses standard Markdown (universal)
- Pre-structures information for sequential reading
- Includes explicit "if-then" decision logic
- References specific file paths (clickable in most editors)
- Avoids tool-specific jargon
- Includes the bootstrap prompt for re-orientation

Tested with: Claude, GPT-4, Codex, Gemini, local LLMs.

---

## Example file lengths

For a complete crypto tax project handoff (multi-year, multi-wallet, complex):

- HANDOFF.md: 3,000-6,000 words
- 16 sections covering everything
- Linked to project files (don't duplicate content)

A larger HANDOFF.md is fine if it's well-organized. Length doesn't reduce usefulness when sections are clearly delineated.

---

## Disclaimer

This template is a working document for tax project handoffs. The legal and tax considerations remain the responsibility of the taxpayer and their qualified advisors. Use at your own risk.

For corrections or contributions, please open a GitHub issue.
