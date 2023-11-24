import pandas as pd
from .evalutation_metrics import evaluate_classification_model
from numpy.typing import ArrayLike
def compare_models(models: dict, X_test: pd.DataFrame, y_test: ArrayLike) -> pd.DataFrame:
    """
    Compare multiple models based on evaluation metrics.

    :param models: Dictionary of models to compare.
    :param X_test: Test features DataFrame.
    :param y_test: Test target DataFrame.
    :return: DataFrame with comparison of models.
    """
    results = {}

    for model_name, model in models.items():
        metrics = evaluate_classification_model(model, X_test, y_test)
        results[model_name] = metrics
    return pd.DataFrame(results)
