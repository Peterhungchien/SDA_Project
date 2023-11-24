import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from numpy.typing import ArrayLike
def evaluate_classification_model(model, X_test: pd.DataFrame, y_test: ArrayLike) -> dict:
    """
    Evaluate a classification model with standard and financial metrics.

    :param model: Trained model to evaluate.
    :param X_test: Test features DataFrame.
    :param y_test: Test target DataFrame.
    :return: Dictionary of evaluation metrics.
    """
    predictions = model.predict(X_test)

    metrics = {
        'accuracy': accuracy_score(y_test, predictions),
        'precision': precision_score(y_test, predictions),
        'recall': recall_score(y_test, predictions),
        'f1_score': f1_score(y_test, predictions),
        'sharpe_ratio': calculate_sharpe_ratio(predictions)
    }

    return metrics

def evaluate_continuous_model(model, X_test: pd.DataFrame, y_test: ArrayLike) -> dict:
    """
    Evaluate a continuous model with standard and financial metrics.

    :param model: Trained model to evaluate.
    :param X_test: Test features DataFrame.
    :param y_test: Test target DataFrame.
    :return: Dictionary of evaluation metrics.
    """
    predictions = model.predict(X_test)

    metrics = {
        'mse': mean_squared_error(y_test, predictions),
        'mae': mean_absolute_error(y_test, predictions),
        'rmse': np.sqrt(mean_squared_error(y_test, predictions)),
        'mape': mean_absolute_percentage_error(y_test, predictions),
        'sharpe_ratio': calculate_sharpe_ratio(predictions)
    }

    return metrics


def calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.0) -> np.floating:
    """
    Calculate the Sharpe Ratio for the given returns.

    :param returns: Array of returns.
    :param risk_free_rate: Risk-free rate, default is 0.
    :return: Sharpe Ratio.
    """
    excess_returns = returns - risk_free_rate
    if np.std(excess_returns) == 0:
        return np.floating(0.0)
    else:
        return np.mean(excess_returns) / np.std(excess_returns)
