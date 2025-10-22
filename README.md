# S&P 500 Weekly Dataset (2024)

This dataset contains **weekly open and close prices** for all S&P 500 companies in 2024, fetched from Yahoo Finance using Python.

## Files
- `weekly_openclose_2024.csv` — For Excel or pandas
- `weekly_openclose_2024.tsv` — Tab-separated version
- `weekly_flatten_2024.py` — Script to regenerate data
- `tickers.txt` — List of all S&P 500 symbols

## How to use
''' python
import pandas as pd
df = pd.read_csv("weekly_openclose_2024.csv")
print(df.head())


## Data Source
Yahoo Finance public API via yfinance Python library. 


## License
Shared for education and research use only under CC BY-NC 4.0


## About
Created by Agetachew1
Goal:Provide an easy-to-use open dataset for stock analysis, ML experiments, and financial modeling.

