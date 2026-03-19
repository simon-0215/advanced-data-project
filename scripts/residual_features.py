import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, root_mean_squared_error


def create_lagged_features(
    residuals: pd.Series,
    n_lags: int,
    target_name: str = "target",
) -> pd.DataFrame:
    if not isinstance(residuals, pd.Series):
        raise TypeError("residuals must be a pandas Series.")
    if n_lags < 1:
        raise ValueError("n_lags must be >= 1.")

    df = pd.DataFrame({target_name: residuals})

    for lag in range(1, n_lags + 1):
        df[f"lag_{lag}"] = residuals.shift(lag)

    lag_cols = [f"lag_{lag}" for lag in range(1, n_lags + 1)]
    df = df[lag_cols + [target_name]]

    return df.dropna().copy()


def train_test_split_time_series(
    data: pd.DataFrame,
    target_col: str = "target",
    test_size: float = 0.2,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    if target_col not in data.columns:
        raise ValueError(f"target_col '{target_col}' not found in data.")
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")

    split_idx = int(len(data) * (1 - test_size))
    if split_idx <= 0 or split_idx >= len(data):
        raise ValueError("Split results in empty train/test set. Check test_size.")

    X = data.drop(columns=[target_col])
    y = data[target_col]

    X_train = X.iloc[:split_idx]
    X_test = X.iloc[split_idx:]
    y_train = y.iloc[:split_idx]
    y_test = y.iloc[split_idx:]

    return X_train, X_test, y_train, y_test


def train_evaluate_random_forest(
    lagged_data: pd.DataFrame,
    target_col: str = "target",
    test_size: float = 0.2,
    n_estimators: int = 300,
    random_state: int = 42,
) -> dict:
    X_train, X_test, y_train, y_test = train_test_split_time_series(
        lagged_data, target_col=target_col, test_size=test_size
    )

    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)

    return {
        "model": model,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "y_pred": pd.Series(y_pred, index=y_test.index, name="prediction"),
        "r2": float(r2),
        "rmse": float(rmse),
    }


def combine_arima_and_ml_residual_predictions(
    arima_prediction: pd.Series,
    ml_residual_prediction: pd.Series,
    arima_name: str = "arima_prediction",
    residual_name: str = "ml_residual_prediction",
    final_name: str = "final_prediction",
) -> pd.DataFrame:
    if not isinstance(arima_prediction, pd.Series):
        raise TypeError("arima_prediction must be a pandas Series.")
    if not isinstance(ml_residual_prediction, pd.Series):
        raise TypeError("ml_residual_prediction must be a pandas Series.")

    arima_prediction = arima_prediction.sort_index()
    ml_residual_prediction = ml_residual_prediction.sort_index()

    common_index = arima_prediction.index.intersection(ml_residual_prediction.index)
    if len(common_index) == 0:
        raise ValueError(
            "No overlapping timestamps between ARIMA and ML residual predictions."
        )

    arima_aligned = arima_prediction.loc[common_index].rename(arima_name)
    residual_aligned = ml_residual_prediction.loc[common_index].rename(residual_name)

    combined = pd.concat([arima_aligned, residual_aligned], axis=1)
    combined[final_name] = combined[arima_name] + combined[residual_name]

    return combined


def compare_arima_ml_hybrid_rmse(
    returns: pd.Series,
    n_lags: int = 5,
    test_size: float = 0.2,
    arima_order: tuple[int, int, int] = (1, 0, 1),
    n_estimators: int = 300,
    random_state: int = 42,
) -> dict:
    from statsmodels.tsa.arima.model import ARIMA

    if not isinstance(returns, pd.Series):
        raise TypeError("returns must be a pandas Series.")
    if n_lags < 1:
        raise ValueError("n_lags must be >= 1.")
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")

    y = returns.dropna().sort_index()
    split_idx = int(len(y) * (1 - test_size))
    if split_idx <= n_lags or split_idx >= len(y):
        raise ValueError("Not enough samples for the requested n_lags/test_size.")

    y_train = y.iloc[:split_idx]
    y_test = y.iloc[split_idx:]

    arima_model = ARIMA(y_train, order=arima_order)
    arima_fitted = arima_model.fit()
    arima_pred_test = arima_fitted.get_forecast(steps=len(y_test)).predicted_mean
    arima_pred_test = pd.Series(
        np.asarray(arima_pred_test),
        index=y_test.index,
        name="arima_prediction",
    )

    lagged_returns = create_lagged_features(y, n_lags=n_lags, target_name="target")
    X_all = lagged_returns.drop(columns=["target"])
    y_all = lagged_returns["target"]

    train_mask = X_all.index < y_test.index[0]
    X_train_ml = X_all.loc[train_mask]
    y_train_ml = y_all.loc[train_mask]
    X_test_ml = X_all.loc[~train_mask]
    y_test_ml = y_all.loc[~train_mask]

    rf_direct = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
    )
    rf_direct.fit(X_train_ml, y_train_ml)
    ml_direct_pred_test = pd.Series(
        rf_direct.predict(X_test_ml), index=X_test_ml.index, name="ml_direct_prediction"
    )

    train_residuals = (y_train - arima_fitted.fittedvalues).dropna()

    lagged_resid_train = create_lagged_features(
        train_residuals, n_lags=n_lags, target_name="target"
    )
    X_resid_train = lagged_resid_train.drop(columns=["target"])
    y_resid_train = lagged_resid_train["target"]

    rf_resid = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
    )
    rf_resid.fit(X_resid_train, y_resid_train)

    arima_aligned, y_test_aligned = arima_pred_test.align(y_test, join="inner")
    residual_test_realized = (y_test_aligned - arima_aligned).rename("residual")
    residual_for_features = pd.concat([train_residuals, residual_test_realized]).sort_index()

    lagged_resid_all = create_lagged_features(
        residual_for_features, n_lags=n_lags, target_name="target"
    )
    X_resid_test = lagged_resid_all.drop(columns=["target"]).reindex(y_test_aligned.index).dropna()
    if X_resid_test.empty:
        raise ValueError(
            "Residual test feature matrix is empty after alignment. "
            "Try smaller n_lags or larger training window."
        )
    ml_resid_pred_test = pd.Series(
        rf_resid.predict(X_resid_test), index=X_resid_test.index, name="ml_residual_prediction"
    )

    hybrid_df = combine_arima_and_ml_residual_predictions(
        arima_prediction=arima_aligned,
        ml_residual_prediction=ml_resid_pred_test,
    )
    hybrid_pred_test = hybrid_df["final_prediction"]

    arima_eval = pd.concat([y_test, arima_pred_test], axis=1).dropna()
    ml_eval = pd.concat([y_test_ml, ml_direct_pred_test], axis=1).dropna()
    hybrid_eval = pd.concat([y_test, hybrid_pred_test], axis=1).dropna()

    rmse_arima = root_mean_squared_error(arima_eval.iloc[:, 0], arima_eval.iloc[:, 1])
    rmse_ml = root_mean_squared_error(ml_eval.iloc[:, 0], ml_eval.iloc[:, 1])
    rmse_hybrid = root_mean_squared_error(hybrid_eval.iloc[:, 0], hybrid_eval.iloc[:, 1])

    print("\nModel RMSE comparison (lower is better)")
    print("-" * 45)
    print(f"1) ARIMA only : {rmse_arima:.8f}")
    print(f"2) ML only    : {rmse_ml:.8f}")
    print(f"3) Hybrid     : {rmse_hybrid:.8f}")

    return {
        "rmse": {
            "arima_only": float(rmse_arima),
            "ml_only": float(rmse_ml),
            "hybrid": float(rmse_hybrid),
        },
        "predictions": {
            "arima": arima_pred_test,
            "ml_only": ml_direct_pred_test,
            "ml_residual": ml_resid_pred_test,
            "hybrid": hybrid_pred_test,
        },
        "series": {
            "y_test_arima": arima_eval.iloc[:, 0],
            "y_test_ml": ml_eval.iloc[:, 0],
            "y_test_hybrid": hybrid_eval.iloc[:, 0],
        },
    }

