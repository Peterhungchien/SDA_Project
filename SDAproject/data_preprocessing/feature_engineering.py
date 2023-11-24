import pandas as pd
import numpy as np
from typing import List

def generate_moving_averages(df: pd.DataFrame, windows: List[int]) -> pd.DataFrame:
    """
    Generate moving averages.

    :param df: DataFrame with financial data.
    :param windows: Window sizes for moving averages.
    :return: DataFrame with moving average features.
    """
    for window in windows:
        df[f'moving_avg_{window}'] = df['Close'].rolling(window=window).mean()
    return df

def calculate_volatility(df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    """
    Calculate rolling volatility.

    :param df: DataFrame with financial data.
    :param window: Window size for calculating volatility.
    :return: DataFrame with volatility feature.
    """
    df[f'volatility_{window}'] = df['Close'].pct_change().rolling(window=window).std() * np.sqrt(window)
    return df

def calculate_RSI(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Calculate the Relative Strength Index (RSI).

    :param df: DataFrame with financial data.
    :param window: Window size for RSI calculation.
    :return: DataFrame with RSI feature.
    """
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    df[f'RSI_{window}'] = 100 - (100 / (1 + rs))
    return df
