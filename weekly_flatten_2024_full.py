# weekly_flatten_2024_full.py
import os
import time
from datetime import datetime
from typing import List, Dict

import pandas as pd
import yfinance as yf

# ---------------- Settings ----------------
START = "2024-01-01"
END   = "2024-12-31"
INTERVAL = "1wk"
BATCH_SIZE = 50            # download this many tickers at once
GET_COMPANY_INFO = True    # set False if you hit rate limits on info
OUTPUT_DIR = os.path.expanduser("~/Desktop")

def load_tickers() -> List[str]:
    # Look for tickers.txt in common spots
    candidates = [
        "tickers.txt",
        os.path.expanduser("~/Desktop/sp500-weekly-2024/tickers.txt"),
        os.path.expanduser("~/tickers.txt"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            syms = [line.strip() for line in open(p, "r", encoding="utf-8") if line.strip()]
            print(f"Loaded {len(syms)} tickers from {p}")
            return syms
    raise FileNotFoundError("tickers.txt not found. Put one-per-line tickers in a file named tickers.txt.")

def mdy(ts: pd.Timestamp) -> str:
    d = ts.to_pydatetime()
    return f"{d.month}/{d.day}/{d.year}"  # portable m/d/YYYY

def fetch_batch(tickers: List[str]) -> pd.DataFrame:
    """
    Returns a DataFrame like:
      columns: MultiIndex [ ('Open', TICKER), ('Close', TICKER) ]   OR
               MultiIndex [ ('TICKER', 'Open'), ('TICKER', 'Close') ] depending on yfinance version
      index: weekly DatetimeIndex
    """
    df = yf.download(
        tickers=tickers,
        start=START,
        end=END,
        interval=INTERVAL,
        auto_adjust=False,
        group_by="ticker",   # gives per-ticker columns in most yfinance versions
        threads=True
    )
    return df

def normalize_columns(df_raw: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Turn the raw yf.download frame into per-ticker frames with just Open/Close.
    Handles both column layouts:
      1) Columns like (ticker, field)  (when group_by='ticker')
      2) Columns like (field, ticker)  (older behavior)
    Returns { 'AAPL': DataFrame(Open, Close), ... }
    """
    per = {}
    if isinstance(df_raw.columns, pd.MultiIndex):
        # detect level order
        lvl0 = df_raw.columns.levels[0].name
        cols = df_raw.columns

        # case A: ('AAPL','Open') style
        if "Open" in set(c[1] for c in cols):
            tickers = sorted(set(c[0] for c in cols))
            for t in tickers:
                sub = df_raw[t][["Open", "Close"]].copy()
                if not sub.empty:
                    per[t] = sub
        else:
            # case B: ('Open','AAPL') style
            tickers = sorted(set(c[1] for c in cols))
            for t in tickers:
                sub = df_raw.xs(t, level=1, axis=1)[["Open", "Close"]].copy()
                if not sub.empty:
                    per[t] = sub
    else:
        # Single ticker case might produce simple columns
        cols = df_raw.columns
        if "Open" in cols and "Close" in cols:
            per["SINGLE"] = df_raw[["Open", "Close"]].copy()
    return per

def get_info_map(tickers: List[str]) -> Dict[str, Dict[str, str]]:
    info_map = {}
    for sym in tickers:
        if not GET_COMPANY_INFO:
            info_map[sym] = {"Longname": "", "Sector": ""}
            contin

