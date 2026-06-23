"""03_model_training_and_comparison.py

Trains and compares three regressors on kc_house_data.csv (or engineered clean_house_data.csv):
1) Linear Regression
2) Decision Tree Regressor
3) Random Forest Regressor

We compute and print:
- MAE
- MSE
- RMSE
- R2

We also save the best model into:
Model/house_price_model.pkl

Run:
python Notebook/03_model_training_and_comparison.py
"""

import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


def build_preprocessor(df: pd.DataFrame) -> ColumnTransformer:
    X = df.drop(columns=["price"], errors="ignore")

    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_cols),
            ("cat", categorical_pipeline, categorical_cols),
        ],
        remainder="drop",
    )


def evaluate(y_true, y_pred) -> dict:
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = float(np.sqrt(mse))
    r2 = r2_score(y_true, y_pred)
    return {"MAE": mae, "MSE": mse, "RMSE": rmse, "R2": r2}


def main():
    root_dir = os.path.dirname(os.path.dirname(__file__))

    # Prefer engineered file if it exists
    engineered_path = os.path.join(root_dir, "Dataset", "clean_house_data.csv")
    raw_path = os.path.join(root_dir, "Dataset", "kc_house_data.csv")

    data_path = engineered_path if os.path.exists(engineered_path) else raw_path

    df = pd.read_csv(data_path)

    if "price" not in df.columns:
        raise ValueError("Expected target column 'price'.")

    X = df.drop(columns=["price"])
    y = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    preprocessor = build_preprocessor(df)

    candidates = {
        "LinearRegression": LinearRegression(),
        "DecisionTreeRegressor": DecisionTreeRegressor(random_state=42),
        "RandomForestRegressor": RandomForestRegressor(
            n_estimators=250, random_state=42, n_jobs=-1
        ),
    }

    metrics_table = []
    best_model_name = None
    best_r2 = -float("inf")
    best_pipeline = None

    for name, estimator in candidates.items():
        # For trees, scaling doesn't hurt, but we keep one consistent pipeline.
        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", estimator)])
        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        m = evaluate(y_test, y_pred)
        metrics_table.append({"Model": name, **m})

        print("\n==", name, "==")
        print(f"MAE : {m['MAE']:.4f}")
        print(f"MSE : {m['MSE']:.4f}")
        print(f"RMSE: {m['RMSE']:.4f}")
        print(f"R2  : {m['R2']:.4f}")

        if m["R2"] > best_r2:
            best_r2 = m["R2"]
            best_model_name = name
            best_pipeline = pipeline

    metrics_df = pd.DataFrame(metrics_table).sort_values(by="R2", ascending=False)
    print("\n=== Model Comparison (sorted by R2) ===")
    print(metrics_df.to_string(index=False))

    # Save best model
    model_dir = os.path.join(root_dir, "Model")
    os.makedirs(model_dir, exist_ok=True)
    out_model_path = os.path.join(model_dir, "house_price_model.pkl")

    joblib.dump(best_pipeline, out_model_path)

    print("\nBest model:", best_model_name)
    print("Saved best model to:", out_model_path)


if __name__ == "__main__":
    main()

