"""Unit-level verification suite for the toolkit.

Synthetic fixtures that prove each module behaves correctly in isolation:
parser dedupe + supersedes, transfer match, DeFi swap detect, ACB pooling
under FMV/zero modes, classifier rules, anchor close-the-gap, year-end
balance forward-fill.
"""

from __future__ import annotations

import io
import os
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Tests write throwaway CSVs to a per-platform temp directory.
TMP = Path(tempfile.gettempdir()) / "cra_toolkit_tests"
TMP.mkdir(exist_ok=True, parents=True)

from crypto_cra_toolkit.parser import load_coinstats_csv, load_sources
from crypto_cra_toolkit.transfer_matcher import match_transfers
from crypto_cra_toolkit.defi_detector import detect_defi_swaps
from crypto_cra_toolkit.acb_engine import run_acb
from crypto_cra_toolkit.classifier import classify_missing
from crypto_cra_toolkit.reconstruction import build_anchor_entries, rank_priority
from crypto_cra_toolkit.balances import compute_year_end_balances, latest_year_summary


def _csv(rows: list[dict]) -> Path:
    """Write a tiny CoinStats-shaped CSV to a temp path and return it."""
    cols = ["Portfolio", "Coin Name", "Coin Symbol", "Exchange", "Pair",
            "Type", "Amount", "Price", "Price CAD",
            "Fee Percent", "Fee Amount", "Fee Currency", "Date", "Notes"]
    df = pd.DataFrame(rows)
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    df = df[cols]
    p = TMP / f"fixture_{uuid.uuid4().hex}.csv"
    df.to_csv(p, index=False)
    return p


class ParserTests(unittest.TestCase):
    def test_dedupes_repeated_rows(self):
        path = _csv([
            {"Portfolio": "W1", "Coin Symbol": "ETH", "Type": "Received",
             "Amount": 1.0, "Price CAD": 3000, "Date": "1/1/2025, 1:00:00 PM"},
            {"Portfolio": "W1", "Coin Symbol": "ETH", "Type": "Received",
             "Amount": 1.0, "Price CAD": 3000, "Date": "1/1/2025, 1:00:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            self.assertEqual(len(df), 1)
            self.assertEqual(df.attrs["dedup_drops"], 1)
        finally:
            path.unlink()

    def test_canonical_symbol_buckets_eth_weth(self):
        path = _csv([
            {"Portfolio": "W1", "Coin Symbol": "ETH", "Type": "Buy",
             "Amount": 1.0, "Price CAD": 3000, "Date": "1/1/2025, 1:00:00 PM"},
            {"Portfolio": "W1", "Coin Symbol": "WETH", "Type": "Buy",
             "Amount": 2.0, "Price CAD": 3000, "Date": "1/2/2025, 1:00:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            # canonical key should match for ETH and WETH
            self.assertEqual(df.iloc[0]["asset_canonical"], df.iloc[1]["asset_canonical"])
        finally:
            path.unlink()

    def test_fee_currency_mismatch_zero_priced(self):
        path = _csv([
            {"Portfolio": "W1", "Coin Symbol": "MATIC", "Type": "Sell",
             "Amount": 100, "Price CAD": 1.0, "Date": "1/1/2025, 1:00:00 PM",
             "Fee Amount": 0.001, "Fee Currency": "ethereum"},
        ])
        try:
            df = load_coinstats_csv(path)
            self.assertTrue(bool(df.iloc[0]["fee_currency_mismatch"]))
            self.assertEqual(df.iloc[0]["fee_value_cad_est"], 0.0)
        finally:
            path.unlink()


class TransferMatcherTests(unittest.TestCase):
    def test_matches_pair_within_window(self):
        path = _csv([
            {"Portfolio": "Binance", "Coin Symbol": "ETH", "Type": "Sent",
             "Amount": 1.5, "Price CAD": 3000, "Date": "1/1/2025, 1:00:00 PM"},
            {"Portfolio": "Metamask", "Coin Symbol": "ETH", "Type": "Received",
             "Amount": 1.5, "Price CAD": 3000, "Date": "1/1/2025, 1:02:30 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            df, summ = match_transfers(df)
            self.assertEqual(summ.matched_pairs, 1)
            self.assertTrue(df["is_matched_transfer"].all())
        finally:
            path.unlink()

    def test_does_not_match_same_portfolio(self):
        path = _csv([
            {"Portfolio": "Metamask", "Coin Symbol": "ETH", "Type": "Sent",
             "Amount": 1.5, "Price CAD": 3000, "Date": "1/1/2025, 1:00:00 PM"},
            {"Portfolio": "Metamask", "Coin Symbol": "OETH", "Type": "Received",
             "Amount": 1.5, "Price CAD": 3000, "Date": "1/1/2025, 1:00:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            df, summ = match_transfers(df)
            self.assertEqual(summ.matched_pairs, 0)
        finally:
            path.unlink()

    def test_matches_eth_to_weth_cross_symbol(self):
        path = _csv([
            {"Portfolio": "Binance", "Coin Symbol": "ETH", "Type": "Sent",
             "Amount": 0.5, "Price CAD": 3000, "Date": "1/1/2025, 1:00:00 PM"},
            {"Portfolio": "Metamask", "Coin Symbol": "WETH", "Type": "Received",
             "Amount": 0.5, "Price CAD": 3000, "Date": "1/1/2025, 1:01:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            df, summ = match_transfers(df)
            self.assertEqual(summ.matched_pairs, 1)
            self.assertEqual(summ.cross_symbol_matches, 1)
        finally:
            path.unlink()

    def test_amount_diff_outside_tolerance_rejected(self):
        path = _csv([
            {"Portfolio": "Binance", "Coin Symbol": "ETH", "Type": "Sent",
             "Amount": 1.0, "Price CAD": 3000, "Date": "1/1/2025, 1:00:00 PM"},
            {"Portfolio": "Metamask", "Coin Symbol": "ETH", "Type": "Received",
             "Amount": 0.9, "Price CAD": 3000, "Date": "1/1/2025, 1:01:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            df, summ = match_transfers(df)
            self.assertEqual(summ.matched_pairs, 0)
        finally:
            path.unlink()


class ACBEngineTests(unittest.TestCase):
    def test_matched_transfer_does_not_affect_acb(self):
        # Buy 1 ETH, transfer it to another wallet, sell it — gain should be 0.
        path = _csv([
            {"Portfolio": "Binance", "Coin Symbol": "ETH", "Type": "Buy",
             "Amount": 1.0, "Price CAD": 1000, "Date": "1/1/2025, 12:00:00 PM"},
            {"Portfolio": "Binance", "Coin Symbol": "ETH", "Type": "Sent",
             "Amount": 1.0, "Price CAD": 1000, "Date": "1/2/2025, 12:00:00 PM"},
            {"Portfolio": "Metamask", "Coin Symbol": "ETH", "Type": "Received",
             "Amount": 1.0, "Price CAD": 1000, "Date": "1/2/2025, 12:01:00 PM"},
            {"Portfolio": "Metamask", "Coin Symbol": "ETH", "Type": "Sell",
             "Amount": 1.0, "Price CAD": 1000, "Date": "1/3/2025, 12:00:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            df, _ = match_transfers(df)
            df, _ = detect_defi_swaps(df)
            acb = run_acb(df)
            row = acb.report[acb.report["asset"] == "ETH"].iloc[0]
            self.assertEqual(row["proceeds_cad"], 1000.0)
            self.assertEqual(row["acb_used_cad"], 1000.0)
            self.assertEqual(row["gain_loss_cad"], 0.0)
            self.assertEqual(int(row["missing_qty"]), 0)
        finally:
            path.unlink()

    def test_missing_acb_when_no_buy(self):
        path = _csv([
            {"Portfolio": "Metamask", "Coin Symbol": "PEPE", "Type": "Sell",
             "Amount": 1000, "Price CAD": 0.5, "Date": "1/1/2025, 12:00:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            df, _ = match_transfers(df)
            df, _ = detect_defi_swaps(df)
            acb = run_acb(df, assume_missing_acb="zero")
            self.assertEqual(len(acb.missing_events), 1)
            self.assertEqual(acb.missing_events.iloc[0]["missing_qty"], 1000)
            row = acb.report.iloc[0]
            self.assertEqual(row["proceeds_cad"], 500.0)
            self.assertEqual(row["acb_used_cad"], 0.0)
            self.assertEqual(row["gain_loss_cad"], 500.0)
        finally:
            path.unlink()

    def test_global_pool_across_portfolios(self):
        # Buy on Binance, sell on Metamask (with a transfer in between):
        # ACB pool must be global, not per-portfolio.
        path = _csv([
            {"Portfolio": "Binance", "Coin Symbol": "BTC", "Type": "Buy",
             "Amount": 0.1, "Price CAD": 50000, "Date": "1/1/2025, 12:00:00 PM"},
            {"Portfolio": "Binance", "Coin Symbol": "BTC", "Type": "Sent",
             "Amount": 0.1, "Price CAD": 50000, "Date": "1/2/2025, 12:00:00 PM"},
            {"Portfolio": "Metamask", "Coin Symbol": "BTC", "Type": "Received",
             "Amount": 0.1, "Price CAD": 50000, "Date": "1/2/2025, 12:01:00 PM"},
            {"Portfolio": "Metamask", "Coin Symbol": "BTC", "Type": "Sell",
             "Amount": 0.1, "Price CAD": 60000, "Date": "1/3/2025, 12:00:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            df, _ = match_transfers(df)
            df, _ = detect_defi_swaps(df)
            acb = run_acb(df)
            row = acb.report[acb.report["asset"] == "BTC"].iloc[0]
            # Buy 5000, sell 6000 -> 1000 gain
            self.assertEqual(row["acb_used_cad"], 5000.0)
            self.assertEqual(row["gain_loss_cad"], 1000.0)
        finally:
            path.unlink()


class ClassifierTests(unittest.TestCase):
    def test_stablecoin_redeem_label(self):
        path = _csv([
            {"Portfolio": "M", "Coin Symbol": "USDC", "Type": "Sell",
             "Amount": 100, "Price CAD": 1.0, "Date": "1/1/2025, 12:00:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            df, _ = match_transfers(df)
            df, _ = detect_defi_swaps(df)
            acb = run_acb(df)
            classified = classify_missing(acb.annotated, acb.missing_events)
            self.assertEqual(classified.iloc[0]["cause"], "stablecoin_redeem")
        finally:
            path.unlink()

    def test_fiat_origin_label_for_early_eth(self):
        path = _csv([
            {"Portfolio": "Binance", "Coin Symbol": "ETH", "Type": "Sell",
             "Amount": 1.0, "Price CAD": 3000, "Date": "1/1/2021, 12:00:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            df, _ = match_transfers(df)
            df, _ = detect_defi_swaps(df)
            acb = run_acb(df)
            classified = classify_missing(acb.annotated, acb.missing_events)
            self.assertEqual(classified.iloc[0]["cause"], "fiat_origin_missing")
        finally:
            path.unlink()

    def test_airdrop_or_income_when_only_received(self):
        path = _csv([
            {"Portfolio": "M", "Coin Symbol": "PEPE", "Type": "Received",
             "Amount": 1000, "Price CAD": 0.001, "Date": "1/1/2025, 11:00:00 AM"},
            {"Portfolio": "M", "Coin Symbol": "PEPE", "Type": "Sell",
             "Amount": 1000, "Price CAD": 0.5, "Date": "1/2/2025, 12:00:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            df, _ = match_transfers(df)
            df, _ = detect_defi_swaps(df)
            acb = run_acb(df)
            classified = classify_missing(acb.annotated, acb.missing_events)
            self.assertEqual(classified.iloc[0]["cause"], "airdrop_or_income")
        finally:
            path.unlink()


class ReconstructionTests(unittest.TestCase):
    def test_anchors_close_the_gap(self):
        """Anchor Buy rows fed back through the engine should eliminate
        missing-ACB events for the same assets."""
        path = _csv([
            {"Portfolio": "M", "Coin Symbol": "USDC", "Type": "Sell",
             "Amount": 100, "Price CAD": 1.0, "Date": "1/1/2025, 12:00:00 PM"},
            {"Portfolio": "M", "Coin Symbol": "PEPE", "Type": "Sell",
             "Amount": 1000, "Price CAD": 0.5, "Date": "1/3/2025, 12:00:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            df, _ = match_transfers(df)
            df, _ = detect_defi_swaps(df)
            acb = run_acb(df)
            classified = classify_missing(acb.annotated, acb.missing_events)
            anchors = build_anchor_entries(classified)
            self.assertEqual(len(anchors), 2)

            # Persist the anchors and re-run with both sources.
            anchors_path = TMP / f"anchors_{uuid.uuid4().hex}.csv"
            cols = ["Portfolio", "Coin Name", "Coin Symbol", "Exchange", "Pair",
                    "Type", "Amount", "Price", "Price CAD",
                    "Fee Percent", "Fee Amount", "Fee Currency", "Date", "Notes"]
            anchors[cols].to_csv(anchors_path, index=False)
            try:
                combined = load_sources([path], manual_paths=[anchors_path])
                combined, _ = match_transfers(combined)
                combined, _ = detect_defi_swaps(combined)
                acb2 = run_acb(combined)
                self.assertTrue(acb2.missing_events.empty,
                                f"Expected no missing events; got {len(acb2.missing_events)}")
                # The USDC sale should have ~zero gain.
                usdc = acb2.report[acb2.report["asset"] == "USDC"].iloc[0]
                self.assertAlmostEqual(usdc["gain_loss_cad"], 0.0, places=2)
            finally:
                anchors_path.unlink()
        finally:
            path.unlink()


class PrioritizationTests(unittest.TestCase):
    def test_priority_orders_by_gain(self):
        path = _csv([
            {"Portfolio": "M", "Coin Symbol": "USDC", "Type": "Sell",
             "Amount": 100, "Price CAD": 1.0, "Date": "1/1/2025, 12:00:00 PM"},
            {"Portfolio": "M", "Coin Symbol": "PEPE", "Type": "Sell",
             "Amount": 100, "Price CAD": 50, "Date": "1/2/2025, 12:00:00 PM"},
        ])
        try:
            df = load_coinstats_csv(path)
            df, _ = match_transfers(df)
            df, _ = detect_defi_swaps(df)
            acb = run_acb(df)
            classified = classify_missing(acb.annotated, acb.missing_events)
            ranked = rank_priority(classified)
            self.assertEqual(ranked.iloc[0]["asset"], "PEPE")
            self.assertEqual(ranked.iloc[1]["asset"], "USDC")
        finally:
            path.unlink()


class BalanceTests(unittest.TestCase):
    def _run(self, rows: list[dict], dust=0.05):
        path = _csv(rows)
        try:
            df = load_coinstats_csv(path)
            df, _ = match_transfers(df)
            df, _ = detect_defi_swaps(df)
            acb = run_acb(df)
            return compute_year_end_balances(acb.annotated, dust_threshold_cad=dust)
        finally:
            path.unlink()

    def test_carries_balance_forward_into_quiet_year(self):
        # Buy 1 BTC in 2023, do nothing in 2024, sell 0.5 BTC in 2025.
        # End-2023 balance = 1.0, end-2024 balance = 1.0 (forward-fill),
        # end-2025 balance = 0.5.
        bal = self._run([
            {"Portfolio": "X", "Coin Symbol": "BTC", "Type": "Buy",
             "Amount": 1.0, "Price CAD": 50000, "Date": "6/1/2023, 12:00:00 PM"},
            {"Portfolio": "X", "Coin Symbol": "BTC", "Type": "Sell",
             "Amount": 0.5, "Price CAD": 80000, "Date": "6/1/2025, 12:00:00 PM"},
        ])
        by_year = bal.set_index("year")["qty"].to_dict()
        self.assertEqual(by_year[2023], 1.0)
        self.assertEqual(by_year[2024], 1.0)  # forward-fill
        self.assertEqual(by_year[2025], 0.5)

    def test_eth_and_weth_share_balance(self):
        # Same canonical pool: ETH + WETH should aggregate.
        bal = self._run([
            {"Portfolio": "X", "Coin Symbol": "ETH", "Type": "Buy",
             "Amount": 1.0, "Price CAD": 3000, "Date": "1/1/2025, 12:00:00 PM"},
            {"Portfolio": "X", "Coin Symbol": "WETH", "Type": "Buy",
             "Amount": 2.0, "Price CAD": 3000, "Date": "1/2/2025, 12:00:00 PM"},
        ])
        eth_rows = bal[bal["asset_canonical"].isin(["ETH", "WETH"])]
        self.assertEqual(len(eth_rows), 1)  # one canonical row, not two
        self.assertEqual(eth_rows.iloc[0]["qty"], 3.0)

    def test_dust_filter_flags_micro_balances(self):
        # 0.000001 of a token worth $0.50 → $5e-7 CAD value, qty < 1 → dust
        bal = self._run([
            {"Portfolio": "X", "Coin Symbol": "DUSTY", "Type": "Buy",
             "Amount": 0.000001, "Price CAD": 0.5, "Date": "1/1/2025, 12:00:00 PM"},
        ])
        self.assertTrue(bool(bal.iloc[0]["is_dust"]))

    def test_dust_filter_keeps_small_qty_of_high_value_asset(self):
        # 0.001 BTC at $80k → $80 CAD value → NOT dust even though qty < 1.
        bal = self._run([
            {"Portfolio": "X", "Coin Symbol": "BTC", "Type": "Buy",
             "Amount": 0.001, "Price CAD": 80000, "Date": "1/1/2025, 12:00:00 PM"},
        ])
        self.assertFalse(bool(bal.iloc[0]["is_dust"]))

    def test_latest_year_summary_excludes_dust(self):
        bal = self._run([
            {"Portfolio": "X", "Coin Symbol": "BTC", "Type": "Buy",
             "Amount": 0.5, "Price CAD": 80000, "Date": "1/1/2025, 12:00:00 PM"},
            {"Portfolio": "X", "Coin Symbol": "DUSTY", "Type": "Buy",
             "Amount": 0.0001, "Price CAD": 0.001, "Date": "1/2/2025, 12:00:00 PM"},
        ])
        latest = latest_year_summary(bal)
        self.assertEqual(len(latest), 1)
        self.assertEqual(latest.iloc[0]["asset"], "BTC")


if __name__ == "__main__":
    unittest.main(verbosity=2)
