"""crypto_cra_toolkit — forensic ACB reconstruction for Canadian crypto tax filings.

Pipeline:
    parser            -> normalize + dedupe CoinStats CSV(s)
    transfer_matcher  -> match Sent <-> Received (non-taxable transfers)
    defi_detector     -> detect implicit DEX swaps (Sell A + Buy B same instant)
    acb_engine        -> CRA-style global ACB pooling + gain/loss
    classifier        -> root-cause label for each missing-ACB event
    reconstruction    -> emit anchor Buy entries that close the gaps
    reporting         -> CSV outputs + Markdown audit memo
"""

__all__ = [
    "parser",
    "transfer_matcher",
    "defi_detector",
    "acb_engine",
    "classifier",
    "reconstruction",
    "reporting",
]

__version__ = "0.2.0"
