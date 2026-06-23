"""04_model_evaluation.py

Evaluates the saved best model (Model/house_price_model.pkl) on a fresh
train/test split.

This script prints MAE, MSE, RMSE, and R2.

Run:
python Notebook/04_model_evaluation.py
"""

import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate(y_true, y_pred) -> dict:
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = float(np.sqrt(mse))
    r2 = r2_score(y_true, y_pred)
    return {"MAE": mae, "MSE": mse, "RMSE": rmse, "R2": r2}


def main():
    root_dir = os.path.dirname(os.path.dirname(__file__))

    model_path = os.path.join(root_dir, "Model", "house_price_model.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Saved model not found at {model_path}. Run 03_model_training_and_comparison.py first."
        )

    engineered_path = os.path.join(root_dir, "Dataset", "clean_house_data.csv")
    raw_path = os.path.join(root_dir, "Dataset", "kc_house_data.csv")
    data_path = engineered_path if os.path.exists(engineered_path) else raw_path

    df = pd.read_csv(data_path)

    X = df.drop(columns=["price"])
    y = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = joblib.load(model_path)

    y_pred = pipeline.predict(X_test)

    m = evaluate(y_test, y_pred)
    print("Saved best model evaluation on test split:")
    print(f"MAE : {m['MAE']:.4f}")
    print(f"MSE : {m['MSE']:.4f}")
    print(f"RMSE: {m['RMSE']:.4f}")
    print(f"R2  : {m['R2']:.4f}")


if __name__ == "__main__":
    main()

