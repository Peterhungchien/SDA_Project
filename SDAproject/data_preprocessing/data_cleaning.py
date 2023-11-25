import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform comprehensive cleaning on financial data.

    :param df: Input DataFrame with financial data.
    :return: Cleaned DataFrame.
    """
    # Fill missing values
    df_cleaned = df.ffill()

    # Remove duplicates
    df_cleaned = df_cleaned.drop_duplicates()

    # Handle outliers, e.g., prices or volumes that are several standard deviations away from the mean
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        upper_limit = df_cleaned[col].mean() + 3 * df_cleaned[col].std()
        lower_limit = df_cleaned[col].mean() - 3 * df_cleaned[col].std()
        df_cleaned = df_cleaned[(df_cleaned[col] < upper_limit) & (df_cleaned[col] > lower_limit)]

    # Convert data types if necessary, e.g., dates to datetime objects
    df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'])

    return df_cleaned

def add_date_parts(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy[date_column] = pd.to_datetime(df_copy[date_column])
    df_copy['Year'] = df_copy[date_column].dt.year
    df_copy['Month'] = df_copy[date_column].dt.month
    df_copy['Day'] = df_copy[date_column].dt.day
    df_copy['DayOfWeek'] = df_copy[date_column].dt.dayofweek
    df_copy = df_copy.drop(columns=[date_column])
    return df_copy