import pandas as pd

def normalize_data(df: pd.DataFrame, cols=None) -> pd.DataFrame:
    """
    Normalize the input DataFrame.

    :param df: Input DataFrame with financial data.
    :return: Normalized DataFrame.
    """
    new_df = df.copy()
    if not cols:
        cols = new_df.columns
    for column in cols:
        new_df[column] = (new_df[column] - new_df[column].min()) / (new_df[column].max() - new_df[column].min())
    return new_df
