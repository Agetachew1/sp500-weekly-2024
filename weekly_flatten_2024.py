import pandas as pd
import yfinance as yf
from pathlib import Path

# --------------------------
# CONFIG
# --------------------------
TICKERS = [
    "AAPL", "NVDA", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "NFLX", "AVGO",
    "UNH", "JPM", "V", "XOM", "PEP", "BRK-B", "WMT", "LLY", "MA", "ORCL", "COST",
    "PG", "HD", "JNJ", "BAC", "CRM", "ABBV", "KO", "TMUS", "CVX", "MRK", "WFC",
    "CSCO", "ACN", "NOW", "AXP", "MCD", "BX", "IBM", "DIS", "LIN", "TMO", "MS",
    "ABT", "ADBE", "AMD", "PM", "ISRG", "PLTR", "GE", "INTU", "GS", "CAT", "TXN",
    "QCOM", "VZ", "BKNG", "DHR", "T", "BLK", "RTX", "SPGI", "PFE", "HON", "NEE",
    "CMCSA", "ANET", "AMGN", "PGR", "LOW", "SYK", "UNP", "TJX", "KKR", "SCHW", "ETN",
    "AMAT", "BA", "BSX", "C", "UBER", "COP", "PANW", "ADP", "DE", "FI", "BMY", "LMT",
    "GILD", "NKE", "CB", "UPS", "ADI", "MMC", "MDT", "VRTX", "MU", "SBUX", "PLD",
    "GEV", "LRCX", "MO", "SO", "EQIX", "CRWD", "PYPL", "SHW", "ICE", "CME", "AMT",
    "APH", "ELV", "TT", "MCO", "CMG", "INTC", "KLAC", "ABNB", "DUK", "PH", "CDNS",
    "WM", "DELL", "MDLZ", "MAR", "MSI", "WELL", "AON", "REGN", "CI", "HCA", "PNC",
    "ITW", "SNPS", "CTAS", "CL", "USB", "FTNT", "ZTS", "MCK", "GD", "TDG", "CEG",
    "AJG", "EMR", "MMM", "ORLY", "NOC", "COF", "ECL", "EOG", "FDX", "BDX", "APD",
    "WMB", "SPG", "ADSK", "RCL", "RSG", "CARR", "CSX", "HLT", "DLR", "TGT", "KMI",
    "OKE", "TFC", "AFL", "GM", "BK", "ROP", "MET", "CPRT", "FCX", "CVS", "PCAR",
    "SRE", "AZO", "TRV", "NXPI", "JCI", "GWW", "NSC", "PSA", "SLB", "AMP", "ALL",
    "FICO", "MNST", "PAYX", "CHTR", "AEP", "ROST", "PWR", "CMI", "AXON", "VST", "URI",
    "MSCI", "LULU", "O", "PSX", "AIG", "FANG", "D", "HWM", "DHI", "KR", "NDAQ", "OXY",
    "EW", "COR", "KDP", "FIS", "KMB", "NEM", "DFS", "PCG", "TEL", "MPC", "FAST", "AME",
    "PEG", "PRU", "KVUE", "STZ", "GLW", "LHX", "GRMN", "BKR", "CBRE", "CTVA", "HES",
    "CCI", "DAL", "CTSH", "F", "VRSK", "EA", "ODFL", "XEL", "TRGP", "A", "IT", "LVS",
    "SYY", "VLO", "OTIS", "LEN", "EXC", "IR", "YUM", "KHC", "GEHC", "IQV", "GIS",
    "CCL", "RMD", "VMC", "HSY", "ACGL", "IDXX", "WAB", "ROK", "MLM", "EXR", "DD",
    "ETR", "DECK", "EFX", "UAL", "WTW", "TTWO", "HIG", "RJF", "AVB", "MTB", "DXCM",
    "ED", "EBAY", "HPQ", "IRM", "EIX", "LYV", "VICI", "CNC", "WEC", "MCHP", "HUM",
    "ANSS", "BRO", "CSGP", "MPWR", "GDDY", "TSCO", "STT", "CAH", "GPN", "FITB", "XYL",
    "HPE", "KEYS", "DOW", "EQR", "ON", "PPG", "K", "SW", "NUE", "EL", "BR", "WBD",
    "TPL", "CHD", "MTD", "DOV", "TYL", "FTV", "TROW", "VLTO", "EQT", "SYF", "NVR",
    "DTE", "VTR", "AWK", "ADM", "NTAP", "WST", "CPAY", "PPL", "LYB", "AEE", "EXPE",
    "HBAN", "CDW", "FE", "HUBB", "HAL", "ROL", "PHM", "CINF", "PTC", "WRB", "DRI",
    "FOXA", "FOX", "IFF", "SBAC", "WAT", "ERIE", "TDY", "ATO", "RF", "BIIB", "ZBH",
    "CNP", "MKC", "ES", "WDC", "TSN", "TER", "STE", "PKG", "CLX", "NTRS", "ZBRA",
    "DVN", "CBOE", "WY", "LUV", "ULTA", "CMS", "INVH", "FSLR", "BF-B", "LDOS", "CFG",
    "LH", "VRSN", "IP", "ESS", "PODD", "COO", "SMCI", "STX", "MAA", "FDS", "NRG",
    "BBY", "SNA", "L", "PFG", "STLD", "TRMB", "OMC", "CTRA", "HRL", "ARE", "BLDR",
    "JBHT", "GEN", "DGX", "KEY", "NI", "MOH", "PNR", "J", "DG", "BALL", "NWS",
    "NWSA", "UDR", "HOLX", "JBL", "GPC", "IEX", "MAS", "KIM", "ALGN", "DLTR", "EXPD",
    "EG", "MRNA", "LNT", "AVY", "BAX", "TPR", "VTRS", "CF", "FFIV", "DPZ", "AKAM",
    "RL", "TXT", "SWKS", "EVRG", "EPAM", "DOC", "APTV", "RVTY", "AMCR", "REG",
    "POOL", "INCY", "BXP", "KMX", "CAG", "HST", "JKHY", "SWK", "DVA", "CPB", "CHRW",
    "JNPR", "CPT", "TAP", "NDSN", "PAYC", "UHS", "NCLH", "DAY", "SJM", "TECH", "SOLV",
    "ALLE", "BG", "AIZ", "IPG", "BEN", "EMN", "ALB", "MGM", "AOS", "WYNN", "PNW",
    "ENPH", "LKQ", "FRT", "CRL", "GNRC", "AES", "GL", "LW", "HSIC", "MKTX", "MTCH",
    "TFX", "WBA", "HAS", "IVZ", "APA", "MOS", "PARA", "MHK", "CE", "HII", "CZR",
    "BWA", "QRVO", "FMC", "AMTM"
]

START = "2024-01-01"
END   = "2024-12-31"
INTERVAL = "1wk"      # weekly
AUTO_ADJUST = False

# Save to Desktop so you can see the files immediately
OUTDIR = Path.home() / "Desktop"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPUT_TSV = OUTDIR / "weekly_openclose_2024.tsv"
OUTPUT_CSV = OUTDIR / "weekly_openclose_2024.csv"

def get_name_sector(t):
    try:
        info = yf.Ticker(t).get_info()
        name = info.get("longName") or info.get("shortName") or t
        sector = info.get("sector") or info.get("industry") or ""
        return name, sector
    except Exception as e:
        print(f"[{t}] name/sector lookup failed: {e}")
        return t, ""

print("Downloading…", TICKERS)
data = yf.download(
    TICKERS,
    start=START,
    end=END,
    interval=INTERVAL,
    auto_adjust=AUTO_ADJUST,
    group_by="ticker",
    threads=True,
    progress=False
)

if data is None or len(data) == 0:
    print("No data returned. Check internet connection and try again.")
    raise SystemExit(1)

# If only one ticker, yfinance returns single-level columns; otherwise MultiIndex
rows = []
for t in TICKERS:
    print(f"Processing {t}…")
    if hasattr(data.columns, "levels") and t in data.columns.get_level_values(0):
        df = data[t].copy()
    else:
        # Fallback for single-ticker shape or if MultiIndex missing this ticker
        cols = set(map(str, data.columns))
        if {"Open","Close"}.issubset(cols):
            df = data.copy()
        else:
            print(f"  ⚠️  No columns for {t}; skipping.")
            continue

    keep = [c for c in ["Open","Close"] if c in df.columns]
    if len(keep) < 2:
        print(f"  ⚠️  Missing Open/Close for {t}; skipping.")
        continue

    df = df[keep].dropna().sort_index()
    df = df.loc[(df.index >= pd.Timestamp(START)) & (df.index <= pd.Timestamp(END))]

    name, sector = get_name_sector(t)
    flat = [t, name, sector]
    for _, r in df.iterrows():
        flat.append(round(float(r["Open"]), 2))
        flat.append(round(float(r["Close"]), 2))

    print(f"  → weeks: {len(df)}  → values appended: {len(flat)-3}")
    rows.append(flat)

if not rows:
    print("No rows built; nothing to write.")
    raise SystemExit(1)

# pad to same width
max_len = max(len(r) for r in rows)
for r in rows:
    r += [""] * (max_len - len(r))

out_df = pd.DataFrame(rows)

out_df.to_csv(OUTPUT_TSV, sep="\t", index=False, header=False)
out_df.to_csv(OUTPUT_CSV, index=False, header=False)

print("✅ Done.")
print(f"  • {OUTPUT_TSV}")
print(f"  • {OUTPUT_CSV}")
