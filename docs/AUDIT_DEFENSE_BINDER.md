# Audit Defense Binder Template

A 7-year document organization framework for Canadian crypto filers preparing for potential CRA review.

> **This is not professional tax advice.** Engage a qualified Canadian tax professional or CPA for your specific situation.

---

## Why you need an audit defense binder

CRA can request supporting documentation for any tax return for at least **6 years** (per ITA Section 230 record retention requirement, often safer to keep 7 years). For crypto-asset holdings specifically:

- ACB calculations span many years; you need every acquisition documented
- Disposition events require proof of proceeds and ACB
- Abandonment claims need shutdown event evidence
- Cross-references between exchanges, wallets, and tax software must be reproducible

A well-organized binder turns a stressful CRA query into a 30-minute exercise: pull file X, attach, respond.

---

## Categorization framework (recommended A-J structure)

Organize digital files into 10 categories:

### A. Custodial exchange records
Per-exchange, per-year:
- Annual tax statements (Realized Gain/Loss reports, 1099 forms)
- Account activity exports (full CSV downloads)
- Account balance statements
- KYC documents (if requested by CRA)

Examples:
- `A1_Wealthsimple_2025_RealizedGainLoss.pdf`
- `A2_Wealthsimple_ActivityExport_2021-2025.csv`
- `A3_Coinbase_Canada_2024_TaxReport.pdf`
- `A4_NDAX_FullLedger_2021-2026.csv`

### B. Self-custody on-chain exports
Per-wallet, per-blockchain:
- Etherscan exports (Ethereum, Polygon, Optimism, etc.)
- BSC Scan exports
- Solscan exports (one per wallet)
- Bitcoin block explorer exports
- Hardware wallet records (Ledger Live, Trezor Suite)

Examples:
- `B1_Etherscan_0xABC1234..._Transactions.csv`
- `B2_BSC_0xABC1234..._Transactions.csv`
- `B3_Solscan_WalletName_Transfers.csv`

### C. Tax software outputs
Per-year, per-tool:
- Koinly annual tax reports (full PDF)
- Cointracker tax statements
- Your reconstruction toolkit output (CSV + audit memo)

Examples:
- `C1_Koinly_2024_CompleteTaxReport.pdf`
- `C2_Toolkit_clean_transactions_2025.csv`
- `C3_Toolkit_audit_memo_2025.md`

### D. Blockchain explorer detail
For each material transaction (large amounts, complex swaps):
- Etherscan / BSC Scan / Solscan transaction page (printed or screenshotted)
- Smart contract interaction details
- Approval transactions

Examples:
- `D1_LargeETHSale_Etherscan_TxHash_xxx.pdf`
- `D2_DeFiSwap_TxHash_yyy.pdf`

### E. Acquisition receipts (establishing ACB)
- Bank statements showing fiat purchases
- Wire transfer confirmations
- Cash purchase receipts (rare, retain)
- P2P purchase records (Bisq, LocalBitcoins, etc.)

Examples:
- `E1_RBC_Statement_2021-Q4_BTCPurchase.pdf`
- `E2_WireTransfer_to_NDAX_2022-03.pdf`
- `E3_P2P_BTCPurchase_Bisq_Receipt.pdf`

### F. Shutdown / abandonment evidence
For each abandonment claim:
- Platform shutdown announcement (archived link via archive.org)
- Migration deadline announcements
- Project death announcements
- Court / bankruptcy filings if applicable

Examples:
- `F1_AgletShutdown_Mar2024_blogpost.pdf` (archive.org snapshot)
- `F2_BUSD_PaxosDiscontinuation_Feb2023.pdf`
- `F3_Sonic_FTM_Migration_Announcement.pdf`
- `F4_FTX_Bankruptcy_Filing.pdf`

### G. Prior-year tax records
Per-year, the complete filed return + supporting:
- T1 General PDF (as filed)
- All Schedules
- Notice of Assessment (NOA)
- Any Notice of Reassessment (NORA)
- Cover letters submitted

Examples:
- `G1_T1_2024_Filed.pdf`
- `G2_NOA_2024_dated_2025-05-08.pdf`
- `G3_NORA_2022_dated_2026-05-14.pdf`
- `G4_CoverLetter_2024_Amendment.pdf`

### H. Specific transaction documentation
For transactions that need explanation:
- Etherscan tx for NFT purchases / sales
- DeFi protocol interaction logs
- Bridge transactions (cross-chain)
- Manual reconstruction notes

Examples:
- `H1_NFTPurchase_Etherscan_TxHash_OpenSea.pdf`
- `H2_BridgeTransaction_PolygonToEthereum.pdf`
- `H3_LiquidStakingDeposit_LidoTx.pdf`

### I. Government correspondence
All CRA correspondence:
- NOA / NORA letters (paper or PDF)
- Audit / review letters
- Your responses to queries
- Phone call notes (date, agent, what was discussed)

Examples:
- `I1_CRA_NOA_2024.pdf`
- `I2_CRA_AuditLetter_2024-09.pdf`
- `I3_MyResponse_to_CRA_AuditLetter.pdf`
- `I4_PhoneCallNotes_CRA_2025-03-15.md`

### J. Cross-reference and reconciliation notes
Working papers showing your own analysis:
- Spreadsheets reconciling different data sources
- Methodology notes
- ACB calculation worksheets
- Hand-written notes (if you keep them)

Examples:
- `J1_ETH_ACB_Reconciliation_2024.xlsx`
- `J2_SOL_PoolHistory_2022-2025.xlsx`
- `J3_NotesOnReconstruction_2025.md`

---

## Digital vs physical organization

### Recommended: Cloud-based digital with local backup

**Primary:** Cloud storage (Dropbox, OneDrive, iCloud, Google Drive)
- Folder named `Crypto_Tax_Defense_Binder_[year]`
- Subfolders A through J
- Each file consistently named per category

**Backup:** External hard drive
- Full copy of cloud folder
- Updated quarterly

**Optional:** Physical printouts of critical documents
- Original tax returns (signed)
- CRA correspondence (originals)
- Bank statements where the only copy is digital

### Why cloud-first

- Accessible from anywhere if CRA contacts you while traveling
- Survives hardware failure
- Searchable
- Auto-versioning (Dropbox keeps file history)

---

## Naming convention

Consistent file names speed up CRA query responses:

```
[CategoryPrefix]_[Year]_[Source/Asset]_[BriefDescription].ext

Examples:
A1_2024_Wealthsimple_RealizedGainLoss.pdf
A2_2024_Coinbase_TaxStatement.pdf
B1_2024_Etherscan_0xABC..._Transactions.csv
C1_2024_Koinly_FullReport.pdf
E1_2021_RBC_StatementShowing_BTCPurchase.pdf
F1_2024_Aglet_ShutdownAnnouncement.pdf
G1_2024_T1_AsFiled.pdf
G2_2024_NOA_2025-05-08.pdf
H1_2024_NFT_Sale_OpenSea_TxHash_xxxxxxx.pdf
I1_2024_CRA_Letter_2024-09-15.pdf
```

When CRA asks "do you have records for transaction X on date Y?", you can locate the file in seconds.

---

## What CRA can request

Under ITA Section 230, CRA has broad authority to request:
- All records used to prepare your return
- Supporting documents for any claim (deduction, credit, ACB, disposition)
- Records of your worldwide income (Canadian residents must report)
- Cross-references between your records and third-party data

Specifically for crypto:
- All exchange records (you have)
- All wallet records (you have via on-chain explorers)
- Records of fiat purchases (you have via bank statements)
- ACB calculations for every asset
- Substantiation for every disposition

CRA cannot demand:
- Privileged communications with your lawyer
- Information held by foreign jurisdictions (must use treaty)
- Records you don't actually have (only what exists)

---

## Common CRA queries and binder responses

### "What was your ACB for the [asset] sold on [date]?"

Response: Pull Category C tax software output for the year. Reference the running ACB calculation. Attach the relevant page.

### "Where did you acquire [quantity] of [asset]?"

Response: Pull Category E (acquisition receipts) + Category B (on-chain receive transactions). Show the full chain.

### "Why did you claim [asset] as abandoned?"

Response: Pull Category F (shutdown evidence) + Category D (your last attempted access on-chain). Provide both.

### "Can you reconcile your [exchange] activity?"

Response: Pull Category A (exchange records) + Category C (tax software showing how exchange data was incorporated) + Category J (reconciliation worksheet).

### "Did you receive any income you didn't report?"

Response: Pull Category C (tax software complete report including all received-without-payment events). Confirm treatment used (Treatment 1 vs Treatment 2 per `docs/AIRDROPS_AND_GAMEPLAY_REWARDS.md`).

### "Explain this large transaction"

Response: Pull Category D (specific transaction explorer page) + Category H (your reconstruction notes if complex). Walk through the transaction.

---

## Retention period

| Document | Minimum retention | Recommended |
|---|---|---|
| Filed T1 return | 6 years from filing | 7 years |
| NOA / NORA | 6 years from receipt | 7 years |
| Supporting documents (slips, receipts) | 6 years | 7 years |
| Exchange tax statements | 6 years | 7-10 years |
| On-chain transaction records | Forever (unchanging blockchain) | 10+ years for safety |
| Reconciliation worksheets | 6 years | 7 years |

If CRA reassesses your return, the retention clock resets from the NORA date.

If you have an open dispute (objection or court appeal), retain until the dispute is fully resolved.

---

## What to do when CRA contacts you

### Step 1: Don't panic

CRA queries are common and most are resolved without escalation. Most queries are for clarification, not audits.

### Step 2: Read the letter carefully

CRA will state:
- Which year(s) are being reviewed
- What documents they want
- The deadline to respond (usually 30 days)
- Where to send the response

### Step 3: Pull the relevant files

Use your binder index. Locate every document referenced in the query. Make copies (digital or physical).

### Step 4: Draft a response

Include:
- CRA's reference number
- Each item they requested + your supporting document
- Your contact info
- A brief explanation of any complex items

### Step 5: Submit response

Submit via:
- CRA My Account → Submit documents (electronic, recommended)
- Or paper mail (with delivery confirmation)
- Or fax (if specified in CRA letter)

### Step 6: Track and follow up

- Save copy of your response
- Note submission date
- Set calendar reminder for 4-8 weeks (when CRA typically responds)
- If no response in 12 weeks, follow up by phone (1-800-959-8281)

### Step 7: If CRA disagrees

If CRA's response disallows a claim or assesses additional tax:
- File Notice of Objection within 90 days of NORA
- Or pay and accept (lower friction)
- For large disputes, consult a tax lawyer about Tax Court appeal

---

## Multi-year considerations

If you have crypto activity across many years, organize binder per-year but maintain cross-year master files:

### Master files (cross-year)

- `Master_ACB_History_BTC.xlsx` — all BTC acquisitions, dispositions, pool ACB through every year
- `Master_ACB_History_ETH.xlsx` — same for ETH
- `Master_ACB_History_SOL.xlsx` — same for SOL
- `Master_Wallet_Inventory.md` — list of all wallets you've ever controlled
- `Master_Exchange_Inventory.md` — list of all exchanges you've ever used

### Per-year files (yearly snapshots)

- All Category A-J files specific to that tax year's events

When CRA queries a specific year, pull both the master files (for context) and that year's binder.

---

## Special situations

### Lost wallet / can't access old records

If you can't access an old wallet but have records of past transactions:
- Document what you DO have (on-chain explorer for the address)
- Document what you DON'T have and why
- Make a good-faith reconstruction with FMV imputation if needed
- Note in your records that the asset is now inaccessible (may be abandonment candidate)

### Defunct exchange (FTX, Voyager, BlockFi, Cred, etc.)

If you can no longer access your exchange records:
- Use any pre-collapse exports you have
- Reconstruct from bank statements (deposits / withdrawals)
- Use CoinGecko / CoinMarketCap historical price data
- Note inability to retrieve full records due to platform collapse
- Cross-reference with CASP-reported data if available

### Foreign exchange (non-Canadian)

Foreign exchanges may not have year-end statements or FMV data in CAD:
- Convert all amounts to CAD using daily Bank of Canada FX rates
- Document the FX rate source used
- Be prepared for CRA to question conversions

---

## Checklist: Is your binder audit-ready?

For each prior tax year, verify:

- [ ] Filed T1 PDF saved
- [ ] NOA / NORA saved
- [ ] All custodial exchange tax statements saved
- [ ] All exchange activity exports saved (CSV)
- [ ] All on-chain wallet transaction exports saved
- [ ] Tax software complete report saved (PDF)
- [ ] All acquisition receipts (bank statements showing fiat purchases) saved
- [ ] Any abandonment evidence saved
- [ ] Any reconciliation worksheets / notes saved
- [ ] All folders named consistently
- [ ] Cloud backup verified working
- [ ] At least one offline backup

If you can answer yes to all 11 items for each year, you're audit-ready.

---

## Disclaimer

This template is based on real-world Canadian crypto tax practice as of 2026. CRA's specific requirements vary by audit; what they request for one filer may not be what they request for another. Consult a qualified Canadian tax professional or CPA for your specific situation.

For corrections or contributions, please open a GitHub issue.
