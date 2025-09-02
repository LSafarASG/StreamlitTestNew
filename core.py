# core.py
from __future__ import annotations
import pandas as pd

def country_allocation() -> pd.DataFrame:
    # Replace with your real logic / data pull
    data = [
        {"country": "US", "weight": 0.42},
        {"country": "DE", "weight": 0.18},
        {"country": "JP", "weight": 0.12},
        {"country": "GB", "weight": 0.10},
        {"country": "FR", "weight": 0.08},
        {"country": "Other", "weight": 0.10},
    ]
    return pd.DataFrame(data, columns=["country", "weight"])

def sector_allocation() -> pd.DataFrame:
    data = [
        {"sector": "Technology", "weight": 0.35},
        {"sector": "Financials", "weight": 0.20},
        {"sector": "Healthcare", "weight": 0.15},
        {"sector": "Industrials", "weight": 0.12},
        {"sector": "Consumer", "weight": 0.10},
        {"sector": "Other", "weight": 0.08},
    ]
    return pd.DataFrame(data, columns=["sector", "weight"])
