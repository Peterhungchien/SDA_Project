import yfinance as yf
import pandas as pd
from typing import List

def fetch_yahoo_finance_data(tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch financial data from Yahoo Finance.

    :param tickers: List of ticker symbols.
    :param start_date: Start date in 'YYYY-MM-DD' format.
    :param end_date: End date in 'YYYY-MM-DD' format.
    :return: DataFrame with financial data.
    """
    data = yf.download(tickers, start=start_date, end=end_date)
    return data
