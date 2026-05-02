"""Parser — load + normalize CoinStats / NDAX / Klay / manual CSVs into one frame.

Design notes
------------
* CoinStats exports duplicate many rows (the same trade appears twice with the
  same timestamp + amount + portfolio). We dedupe at parse time, otherwise the
  ACB pool gets double-funded and transfers match against ghost partners.
* "Fill" rows are CoinStats balance-reconciliation fakes — never count them.
* A common bridge/wrap relationship table lets the transfer matcher recognise
  that ETH ↔ WETH, MATIC ↔ POL, BSC-USD ↔ USDT etc. are the same economic asset.
* All sources flow through `load_sources()` which concatenates them and tags a
  `source_file` column for traceability.

Public surface
--------------
load_coinstats_csv(path, exclude_text=None) -> pd.DataFrame
load_manual_csv(path) -> pd.DataFrame
load_sources(coinstats_paths, manual_paths=None, exclude_text=None) -> pd.DataFrame
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd

# Symbol equivalence groups. Each set is treated as the same economic asset for
# transfer matching and ACB pooling. Conservative — only well-known wraps/bridges.
SYMBOL_EQUIVALENCE: List[set[str]] = [
    {"ETH", "WETH"},
    {"MATIC", "POL", "WMATIC"},
    {"BTC", "WBTC"},
    {"BNB", "WBNB"},
    {"AVAX", "WAVAX"},
    {"FTM", "WFTM"},
    {"SOL", "WSOL"},
    {"USDT", "BSC-USD"},
]

STABLECOINS = {"USDT", "USDC", "DAI", "BUSD", "TUSD", "USDP", "FRAX", "BSC-USD", "USDC.E"}

# Major fiat-funded coins that are virtually never a "first acquisition via airdrop".
MAJOR_COINS = {"BTC", "ETH", "BNB", "SOL", "AVAX", "MATIC", "ADA", "DOT", "XRP", "LTC"}

TAXABLE_DISPOSAL_TYPES = {"sell"}
ACQUISITION_TYPES = {"buy"}
TRANSFER_TYPES = {"sent", "received"}
FEE_TYPES = {"fee"}
IGNORED_SYSTEM_TYPES = {"fill", "approve", "fail"}

REVIEW_TYPES = {
    "earn lock",
    "earn unlock",
    "interest earn",
    "dust convert",
    "add liquidity",
    "remove liquidity",
    "subscribe",
    "unsubscribe",
    "roll in",
    "roll out",
}


def _equivalence_key(symbol: str) -> str:
    """Map a symbol to its canonical bucket for cross-symbol matching."""
    for group in SYMBOL_EQUIVALENCE:
        if symbol in group:
            return min(group)  # deterministic representative
    return symbol


def clean_symbol(symbol: object) -> str:
    if pd.isna(symbol):
        return "UNKNOWN"
    s = str(symbol).strip()
    if len(s) > 80:  # ERC721 contract addresses
        return s[:77] + "..."
    return s


def normalize_type(t: object) -> str:
    if pd.isna(t):
        return "unknown"
    return str(t).strip().lower()


def parse_money(x: object) -> float:
    if pd.isna(x):
        return 0.0
    if isinstance(x, (int, float)):
        return 0.0 if math.isnan(x) else float(x)
    s = str(x).replace("$", "").replace(",", "").strip()
    # Some CoinStats exports leak "[object Object]" into Fee Percent, Price CAD etc.
    if not s or "object" in s.lower():
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


def _estimate_fee_cad(row: pd.Series) -> float:
    """Only price the fee in CAD when the fee currency matches the traded asset.

    When fees are quoted in a different currency (very common: ETH gas on a
    non-ETH trade) we set the CAD value to zero and flag the row for manual
    pricing — it's safer to under-deduct than to multiply ETH gas by a token
    price as the prototype did.
    """
    fee_amt = row["fee_amount"]
    if fee_amt == 0.0:
        return 0.0
    fee_cur = row["fee_currency"]
    asset = str(row["asset"]).strip()
    if fee_cur == "" or fee_cur.upper() == asset.upper():
        return fee_amt * row["price_cad"]
    return 0.0


def _normalize_coinstats(df: pd.DataFrame, source_file: str) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["year"] = df["date"].dt.year

    df["type_norm"] = df["Type"].apply(normalize_type)
    df["asset"] = df["Coin Symbol"].apply(clean_symbol)
    df["asset_canonical"] = df["asset"].apply(_equivalence_key)
    df["amount_abs"] = pd.to_numeric(df["Amount"], errors="coerce").abs().fillna(0.0)

    # Handle CoinStats column-name variants. Older exports have "Price CAD";
    # 2026 exports switched to "Price USD". For tax-in-CAD, USD→CAD requires
    # the Bank of Canada noon rate per date — but as a first-order
    # approximation we apply a flat factor based on the average of the
    # date range. The exact rates can be refined per-row by the user later.
    if "Price CAD" in df.columns:
        df["price_cad"] = df["Price CAD"].apply(parse_money)
    elif "Price USD" in df.columns:
        # Per-date USD/CAD would be ideal; flat 1.36 is reasonable for 2025-2026,
        # 1.27 for 2021-2022. Use date-weighted approximation.
        usd = df["Price USD"].apply(parse_money)
        # USD/CAD by year (Bank of Canada annual averages):
        # 2020: 1.341, 2021: 1.254, 2022: 1.302, 2023: 1.350, 2024: 1.369, 2025: 1.385, 2026: 1.395
        usdcad = df["year"].map({
            2015: 1.279, 2016: 1.325, 2017: 1.298, 2018: 1.295, 2019: 1.327,
            2020: 1.341, 2021: 1.254, 2022: 1.302, 2023: 1.350,
            2024: 1.369, 2025: 1.385, 2026: 1.395,
        }).fillna(1.30)
        df["price_cad"] = usd * usdcad
        df.attrs["price_column"] = "Price USD (converted to CAD using year-average BoC rate)"
    else:
        df["price_cad"] = 0.0
    df["value_cad"] = df["amount_abs"] * df["price_cad"]

    if "Fee Amount" in df.columns:
        df["fee_amount"] = df["Fee Amount"].apply(parse_money)
    else:
        df["fee_amount"] = 0.0

    if "Fee Currency" in df.columns:
        df["fee_currency"] = df["Fee Currency"].fillna("").astype(str).str.strip()
    else:
        df["fee_currency"] = ""

    df["fee_value_cad_est"] = df.apply(_estimate_fee_cad, axis=1)
    df["fee_currency_mismatch"] = (
        (df["fee_amount"] > 0)
        & (df["fee_currency"] != "")
        & (df["fee_currency"].str.upper() != df["asset"].str.upper())
    )

    df["source_file"] = source_file
    return df


def _dedupe_coinstats(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Remove the duplicate rows that CoinStats sometimes emits for the same event.

    Two rows are treated as the same transaction when (Portfolio, Date, Type,
    Coin Symbol, Amount) all match. Note this is only safe because CoinStats
    timestamps are second-precision; two genuinely separate but identical
    transactions in the same second on the same wallet would also collapse,
    but that's far rarer than the duplication issue.
    """
    key_cols = ["Portfolio", "Date", "Type", "Coin Symbol", "Amount"]
    before = len(df)
    df = df.drop_duplicates(subset=key_cols, keep="first").reset_index(drop=True)
    return df, before - len(df)


def _apply_excludes(df: pd.DataFrame, exclude_text: Iterable[str]) -> pd.DataFrame:
    if not exclude_text:
        return df
    mask = pd.Series(False, index=df.index)
    searchable_cols = [
        c for c in ["Portfolio", "Coin Name", "Coin Symbol", "Exchange", "Pair", "Notes"]
        if c in df.columns
    ]
    if not searchable_cols:
        return df
    combined = df[searchable_cols].fillna("").astype(str).agg(" ".join, axis=1).str.lower()
    for term in exclude_text:
        if term:
            mask |= combined.str.contains(re.escape(term.lower()), regex=True, na=False)
    return df.loc[~mask].copy()


def load_coinstats_csv(
    path: Path,
    exclude_text: Optional[Iterable[str]] = None,
) -> pd.DataFrame:
    """Load and normalize a single CoinStats CSV. Returns sort-by-date frame."""
    df = pd.read_csv(path)
    required = {"Portfolio", "Coin Name", "Coin Symbol", "Type", "Amount", "Date"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path.name}: missing expected columns {sorted(missing)}")
    if "Price CAD" not in df.columns and "Price USD" not in df.columns:
        raise ValueError(f"{path.name}: needs either 'Price CAD' or 'Price USD' column")

    df, dropped = _dedupe_coinstats(df)
    df = _normalize_coinstats(df, source_file=path.name)
    df = _apply_excludes(df, exclude_text or [])
    df = df.sort_values("date").reset_index(drop=True)
    df.attrs["dedup_drops"] = dropped
    return df


def load_manual_csv(path: Path) -> pd.DataFrame:
    """Load a user-curated supplemental CSV (anchor buys, NDAX exports, etc.).

    Required columns: Date, Type, Coin Symbol, Amount, Price CAD, Portfolio.
    Notes is optional. Manual rows skip the dedupe step (they are assumed to
    already be clean) but go through the same normalization.

    Optional column: ``Supersedes``. If present, this row replaces a matching
    CoinStats row keyed by Date|Type|Coin Symbol|Amount|Portfolio. The format
    is the same five fields separated by ``|`` (case-insensitive on Type).
    Whitespace around fields is ignored. Use this to mark a CoinStats ``Sent``
    as a real ``Sell`` (or any other reclassification) without editing the
    original CoinStats export — the override survives future CoinStats CSV
    refreshes.
    """
    df = pd.read_csv(path)
    required = {"Date", "Type", "Coin Symbol", "Amount", "Price CAD", "Portfolio"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path.name}: missing manual columns {sorted(missing)}")
    if "Coin Name" not in df.columns:
        df["Coin Name"] = df["Coin Symbol"]
    if "Notes" not in df.columns:
        df["Notes"] = "manual entry"
    if "Supersedes" not in df.columns:
        df["Supersedes"] = ""
    df = _normalize_coinstats(df, source_file=path.name)
    return df.sort_values("date").reset_index(drop=True)


def _parse_supersedes(value: object) -> Optional[dict]:
    """Parse a Supersedes fingerprint into a dict, or None if blank/invalid."""
    if value is None or pd.isna(value):
        return None
    s = str(value).strip()
    if not s:
        return None
    parts = [p.strip() for p in s.split("|")]
    if len(parts) != 5:
        return None
    try:
        date = pd.to_datetime(parts[0], errors="coerce")
    except Exception:
        date = pd.NaT
    if pd.isna(date):
        return None
    try:
        amount = float(parts[3])
    except ValueError:
        return None
    return {
        "date": date,
        "type": parts[1].lower(),
        "coin_symbol": parts[2],
        "amount": amount,
        "portfolio": parts[4],
    }


def _apply_supersedes(coinstats_df: pd.DataFrame, manual_df: pd.DataFrame
                      ) -> tuple[pd.DataFrame, int, list[str]]:
    """Drop CoinStats rows that match any manual row's Supersedes fingerprint.

    Returns (filtered_df, n_dropped, warnings). Each missing match emits a
    warning so the user can verify the fingerprint after CoinStats updates.
    """
    if "Supersedes" not in manual_df.columns:
        return coinstats_df, 0, []
    fingerprints = (manual_df["Supersedes"]
                    .dropna()
                    .astype(str)
                    .map(_parse_supersedes)
                    .dropna()
                    .tolist())
    if not fingerprints:
        return coinstats_df, 0, []

    keep_mask = pd.Series(True, index=coinstats_df.index)
    warnings: list[str] = []
    for fp in fingerprints:
        # Match on (date within 60s, type case-insensitive, coin symbol exact,
        # amount within tolerance, portfolio exact). The 60s slack is for tiny
        # CoinStats clock-skew between exports. Amount tolerance is the larger
        # of 1e-6 absolute or 1e-7 relative — covers float-precision drift on
        # large amounts (e.g. 10003.339199003 vs 10003.339199).
        dt = (coinstats_df["date"] - fp["date"]).abs()
        amt_tol = max(1e-6, abs(fp["amount"]) * 1e-7)
        cand = (
            (dt < pd.Timedelta(seconds=60))
            & (coinstats_df["type_norm"] == fp["type"])
            & (coinstats_df["Coin Symbol"].astype(str) == fp["coin_symbol"])
            & ((coinstats_df["amount_abs"] - abs(fp["amount"])).abs() < amt_tol)
            & (coinstats_df["Portfolio"].astype(str) == fp["portfolio"])
        )
        if not cand.any():
            warnings.append(
                f"Supersedes fingerprint did not match any CoinStats row: "
                f"{fp['date']:%Y-%m-%d %H:%M:%S}|{fp['type']}|{fp['coin_symbol']}|"
                f"{fp['amount']}|{fp['portfolio']}"
            )
        keep_mask &= ~cand

    n_dropped = int((~keep_mask).sum())
    return coinstats_df.loc[keep_mask].reset_index(drop=True), n_dropped, warnings


def _detect_disposal_collisions(merged_df: pd.DataFrame) -> list[str]:
    """Warn when a manual disposal collides with a CoinStats disposal.

    Defensive check: if a future CoinStats export reclassifies a row that the
    manual file is already overriding (e.g. Sent → Sell), both rows would draw
    down inventory and double-count. We surface a warning so the user can add
    a Supersedes override or remove the now-redundant manual row.
    """
    disposals = merged_df[
        merged_df["type_norm"].isin({"sell", "sent"})
    ].copy()
    if disposals.empty:
        return []
    disposals["__bucket"] = (
        disposals["date"].dt.floor("min").astype(str) + "|"
        + disposals["asset_canonical"].astype(str) + "|"
        + disposals["amount_abs"].round(8).astype(str) + "|"
        + disposals["Portfolio"].astype(str)
    )
    grouped = disposals.groupby("__bucket")
    warnings: list[str] = []
    for bucket, g in grouped:
        if len(g) < 2:
            continue
        sources = g["source_file"].unique()
        if len(sources) < 2:
            continue  # both from same file is normal (e.g. CoinStats Fee+Fee)
        types = set(g["type_norm"].unique())
        if not (types & {"sell"}):
            continue  # transfers can legitimately appear from multiple sources
        warnings.append(
            f"Possible duplicate disposal: {bucket} appears in {sorted(sources)}. "
            "If a CoinStats reclassification is the cause, add a Supersedes "
            "fingerprint to the manual row."
        )
    return warnings


def load_sources(
    coinstats_paths: Iterable[Path],
    manual_paths: Optional[Iterable[Path]] = None,
    exclude_text: Optional[Iterable[str]] = None,
    earliest_date: Optional[str | pd.Timestamp] = None,
) -> pd.DataFrame:
    """Load all sources and merge.

    earliest_date — drop rows dated *before* this date. Use to scrub legacy
    CoinStats balance-backfill rows (e.g. those bogus 2015-10-06 Sent/Received
    rows that some Coinbase imports leak in). Format: any string pandas can
    parse (e.g. ``"2021-01-01"``).
    """
    cs_frames: List[pd.DataFrame] = []
    total_dropped = 0
    for p in coinstats_paths:
        f = load_coinstats_csv(Path(p), exclude_text=exclude_text)
        total_dropped += f.attrs.get("dedup_drops", 0)
        cs_frames.append(f)

    manual_frames: List[pd.DataFrame] = [load_manual_csv(Path(p)) for p in manual_paths or []]

    coinstats_combined = (
        pd.concat(cs_frames, ignore_index=True) if cs_frames else pd.DataFrame()
    )
    manual_combined = (
        pd.concat(manual_frames, ignore_index=True) if manual_frames else pd.DataFrame()
    )

    pre_cutoff_dropped = 0
    if earliest_date is not None and not coinstats_combined.empty:
        cutoff = pd.to_datetime(earliest_date)
        before = len(coinstats_combined)
        coinstats_combined = coinstats_combined[coinstats_combined["date"] >= cutoff].reset_index(drop=True)
        pre_cutoff_dropped = before - len(coinstats_combined)

    superseded_count = 0
    supersede_warnings: List[str] = []
    if not coinstats_combined.empty and not manual_combined.empty:
        coinstats_combined, superseded_count, supersede_warnings = _apply_supersedes(
            coinstats_combined, manual_combined
        )

    frames = [f for f in (coinstats_combined, manual_combined) if not f.empty]
    if not frames:
        raise ValueError("No CSV sources provided")
    out = pd.concat(frames, ignore_index=True).sort_values("date").reset_index(drop=True)
    out.attrs["dedup_drops"] = total_dropped
    out.attrs["pre_cutoff_dropped"] = pre_cutoff_dropped
    out.attrs["superseded_rows"] = superseded_count
    out.attrs["supersede_warnings"] = supersede_warnings
    out.attrs["disposal_collision_warnings"] = _detect_disposal_collisions(out)
    return out
