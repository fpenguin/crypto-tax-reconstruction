# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] — 2026-05-28

### Added — Battle-tested Canadian crypto tax guidance

Six new documents distilled from real-world multi-year T1 reconstruction and 2025 T1 amendment experience:

- **`docs/T1_ADJUSTMENT_WORKFLOW.md`** — Comprehensive guide to amending Canadian T1 returns. Covers ReFILE via NETFILE vs Change My Return vs paper T1-ADJ, the "wait for NOA" rule, NETFILE error code 686, pre-payment strategy, cover letter structure, 5 common amendment scenarios, CRA query defense.

- **`docs/COMBINED_POOL_ACB.md`** — Section 47 ITA application to cryptocurrency. Weighted-average ACB across all holdings of the same asset (self-custody + custodial). Worked examples showing when this saves vs costs tax. Common mistakes to avoid.

- **`docs/CARF_PREPARATION_2026.md`** — Crypto-Asset Reporting Framework readiness checklist. What CARF requires, what it doesn't cover, reconciliation imperative for 2026+ filings, VDP timing strategy.

- **`docs/ABANDONMENT_CLAIMS_GUIDE.md`** — Five categories of defensible abandonment claims (platform shutdown, failed migration, dead contract, defunct NFT marketplace, post-hack failed recovery). Documentation requirements. Section 50(1) ITA gap and workarounds. Real-world examples (StepN, Aglet, BUSD, FTM, Klaytn migration, 5KM, etc.).

- **`docs/LIQUID_STAKING_TAX.md`** — Liquid staking derivatives (Lido stETH, Sanctum LST, Marinade mSOL, Rocket Pool rETH, etc.). Two treatments: non-taxable wrap vs taxable swap. Worked examples and decision factors.

- **`docs/AIRDROPS_AND_GAMEPLAY_REWARDS.md`** — $0 ACB at receipt vs FMV-as-income treatment for "received without payment" crypto events. Examples covering JUP, PENGU, StepN GST/GMT, Walken WLKN, Coinbase rewards, Wealthsimple staking. Consistency requirements across years.

### Added — Reference documentation

- **`docs/NETFILE_ERROR_CODES.md`** — Quick reference for common NETFILE rejection codes encountered by Canadian crypto filers. Detailed treatment of error 686 (the most common one).

- **`docs/AUDIT_DEFENSE_BINDER.md`** — 7-year document organization framework. A-J category structure. Naming conventions. CRA query response procedures.

- **`HANDOFF_TEMPLATE.md`** — Template for multi-year AI-assisted crypto tax projects. Self-contained handoff structure (16 sections) that any AI agent (Claude, Codex, GPT, etc.) can use to pick up work without prior memory.

- **`KNOWN_ISSUES.md`** — Documented toolkit bugs and workarounds. Pull requests welcome.

### Changed

- **README.md** — Added section linking to all new guides.

### Notes

This release adds substantial documentation (~25,000+ words) but no code changes. The toolkit logic is unchanged. All new content is sanitized and contains no personally-identifying information.

---

## [1.0.0] — 2026-05-02

### Added — Initial public release

- Python toolkit for reconstructing multi-year, multi-venue cryptocurrency activity into a defensible tax-filing record
- Built originally for Canadian filers (CRA Schedule 3 / T1 line 12700 / line 13000), but the underlying ACB engine and detectors are jurisdiction-agnostic

### Core components

- **`crypto_cra_toolkit/`** — Python package with all reconstruction logic:
  - Parser module (dedupe, normalize, supersedes)
  - Transfer matcher (Sent ↔ Received pairs)
  - DeFi swap detector (same-timestamp Sell + Buy pairs)
  - ACB engine (global per-asset pool, weighted-average)
  - Root-cause classifier (missing-ACB labels)
  - Reconstruction (anchor buy suggestions, priority ranking)
  - Year-end balances (snapshot, dust filter)
  - Reporting (CSVs + audit memo)

- **`analyze.py`** — CLI entry point
- **`generate_tax_filing.py`** — Tax filing package generator
- **`tests/`** — Pytest suite covering parser, transfer matching, DeFi swap detection, ACB pool draws, FMV imputation, balance forward-fill

### Documentation

- **`README.md`** — Overview, install, quickstart, configuration
- **`docs/METHODOLOGY.md`** — Design choices and trade-offs
- **`docs/COVER_LETTER_TEMPLATE.md`** — CRA-targeted cover letter template

### Sample data

- **`examples/sample_transactions.csv`** — Synthetic primary CSV
- **`examples/sample_manual_entries.csv`** — Synthetic supplemental CSV

### Project files

- **`LICENSE`** — MIT
- **`.gitignore`** — Standard Python + project-specific exclusions
- **`requirements.txt`** — Runtime dependencies (just `pandas`)
- **`requirements-dev.txt`** — Test dependencies

---

[1.1.0]: https://github.com/fpenguin/crypto-tax-reconstruction/releases/tag/v1.1.0
[1.0.0]: https://github.com/fpenguin/crypto-tax-reconstruction/releases/tag/v1.0.0
