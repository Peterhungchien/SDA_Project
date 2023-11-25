import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from SDAproject.data_fetching.yahoo_finance import fetch_yahoo_finance_data
from SDAproject.data_preprocessing.data_cleaning import clean_data, add_date_parts
from SDAproject.data_preprocessing.feature_engineering import generate_moving_averages, calculate_volatility, calculate_RSI
from SDAproject.data_preprocessing.data_normalization import normalize_data
from SDAproject.model_training.xgboost_model import train_xgboost_model
from SDAproject.model_training.lightgbm_model import train_lightgbm_model
from SDAproject.model_evaluation import evaluate_continuous_model

def main():
    # Fetching Data
    tickers = ['AAPL']  # Example ticker
    data = fetch_yahoo_finance_data(tickers, '2020-01-01', '2021-01-01')
    data = data.reset_index()
    
    # Preprocessing Data
    cleaned_data = clean_data(data)
    with_features = generate_moving_averages(cleaned_data, [5, 10, 20])
    with_features = calculate_volatility(with_features, 10)
    with_features = calculate_RSI(with_features, 14)
    final_data = normalize_data(with_features, cols = list(filter(lambda x: x != 'Date', with_features.columns)))
    # plot Open, High, Low and Close price by date
    final_data.plot(x='Date', y=['Open', 'High', 'Low', 'Close'])
    final_data = add_date_parts(final_data, 'Date')
    # Assuming 'Close' is the target column
    target_column = 'Close'
    X = final_data.drop(columns=[target_column])
    y = final_data[target_column]

    # Splitting Data for Training and Testing (Assuming 80-20 split)
    train_size = int(len(final_data) * 0.8)
    X_train, y_train = X[:train_size], y[:train_size]
    X_test, y_test = X[train_size:], y[train_size:]

    # Training Models
    xgboost_model = train_xgboost_model(pd.concat([X_train, y_train], axis=1), target_column)
    lightgbm_model = train_lightgbm_model(pd.concat([X_train, y_train], axis=1), target_column)

    # Evaluating Models
    xgb_metrics = evaluate_continuous_model(xgboost_model, X_test, y_test)
    lgb_metrics = evaluate_continuous_model(lightgbm_model, X_test, y_test)
    exclude_sharpe_ratio = lambda d: {k: v for k, v in d.items() if k != 'sharpe_ratio'}
    xgb_metrics_without_sharpe_ratio = exclude_sharpe_ratio(xgb_metrics)
    lgb_metrics_without_sharpe_ratio = exclude_sharpe_ratio(lgb_metrics)
    # Visualization of Model Performance
    ax1: Axes
    fig, ax1 = plt.subplots()
    fig.suptitle('Model Performance')
    def plot_metrics(metrics: dict, ax, **kwargs):
        ax.scatter(list(metrics.keys()), list(metrics.values()), **kwargs)
    plot_metrics(xgb_metrics_without_sharpe_ratio, ax1, label='XGBoost', color='red')
    plot_metrics(lgb_metrics_without_sharpe_ratio, ax1, label='LightGBM', color='blue')
    ax1.set_xlabel('Metrics')
    ax1.set_ylabel('Value (for metrics other than Sharpe Ratio)')
    ax1.legend(loc='upper left')
    ax2 = ax1.twinx()
    plot_metrics({'Sharpe Ratio': xgb_metrics['sharpe_ratio']}, ax2, label='XGBoost', linestyle='dashed', color='red')
    plot_metrics({'Sharpe Ratio': lgb_metrics['sharpe_ratio']}, ax2, label='LightGBM', linestyle='dashed', color='blue')
    ax2.set_ylabel('Sharpe Ratio')
    fig.show()

    

if __name__ == "__main__":
    main()
