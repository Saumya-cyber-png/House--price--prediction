"""00_data_preprocessing.py

Loads kc_house_data.csv and performs basic preprocessing:
- Select numeric features
- Handle missing values (median for numeric)
- Split train/test
- Scale features (optional but helpful for Linear Regression)

Outputs:
- X_train, X_test, y_train, y_test as numpy arrays
- A preprocessor/scaler pipeline that can be reused for inference

This is written as a script so you can run it directly:
python Notebook/00_data_preprocessing.py
"""

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_dataset(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    return df


def build_preprocessor(df: pd.DataFrame) -> ColumnTransformer:
    """Builds a preprocessing pipeline.

    - Numeric: fill missing with median + scale
    - Categorical: fill missing with most_frequent + one-hot encode

    Even if your dataset has few categorical columns, this is safe and general.
    """
    X = df.drop(columns=["price"], errors="ignore")

    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", __import__("sklearn").impute.SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", __import__("sklearn").impute.SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_cols),
            ("cat", categorical_pipeline, categorical_cols),
        ],
        remainder="drop",
    )

    return preprocessor


def main():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(root_dir, "Dataset", "kc_house_data.csv")
    model_dir = os.path.join(root_dir, "Model")
    os.makedirs(model_dir, exist_ok=True)

    df = load_dataset(data_path)

    if "price" not in df.columns:
        raise ValueError("Expected target column 'price' in kc_house_data.csv")

    # Build preprocessing pipeline
    preprocessor = build_preprocessor(df)

    X = df.drop(columns=["price"])
    y = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Save the preprocessing object (reusable for training/inference)
    preprocessor_path = os.path.join(model_dir, "preprocessor.joblib")
    joblib.dump(preprocessor, preprocessor_path)

    print("Preprocessing completed successfully.")
    print(f"Train size: {len(X_train)} | Test size: {len(X_test)}")
    print(f"Saved preprocessing pipeline to: {preprocessor_path}")

    # Also save split arrays for convenience
    joblib.dump(
        {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test},
        os.path.join(model_dir, "train_test_split.joblib"),
    )


if __name__ == "__main__":
    main()

