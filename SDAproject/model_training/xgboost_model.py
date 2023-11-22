from sklearn.model_selection import train_test_split, GridSearchCV
from SDAproject.utils.common_utils import load_config
from pathlib import Path
from typing import Union

def train_xgboost_model(df: pd.DataFrame, target_column: str, params: Union[dict, None] = None) -> xgb.XGBRegressor:
    """
    Train an XGBoost model with hyperparameter tuning and cross-validation.

    :param df: DataFrame with training data.
    :param target_column: Name of the column to be predicted.
    :param params: Dictionary of hyperparameters for tuning. If None, uses default settings.
    :return: Best trained XGBoost model from GridSearchCV.
    """
    current_file_path = Path(__file__)
    config_path = current_file_path.parent.parent / "config" / "settings.yaml"

    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if not params:
        params = load_config(config_path)['model_training']['xgboost']

    model = xgb.XGBRegressor(**params)
    param_grid = {
        'n_estimators': [100, 200],
        'learning_rate': [0.05, 0.1],
        # Add more parameters as needed
    }

    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    best_model.fit(X_train, y_train)

    return best_model

