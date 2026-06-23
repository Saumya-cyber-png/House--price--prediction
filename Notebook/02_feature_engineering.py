"""02_feature_engineering.py

Feature engineering for kc_house_data.csv.

To keep this project simple for beginners, we do lightweight engineering:
- Create interaction features (e.g., bedrooms*bathrooms)
- Create per-floor living area proxy if floors and sqft_living exist

Then we save an engineered CSV to Dataset/clean_house_data.csv.

Run:
python Notebook/02_feature_engineering.py
"""

import os
import pandas as pd


def main():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(root_dir, "Dataset", "kc_house_data.csv")
    out_path = os.path.join(root_dir, "Dataset", "clean_house_data.csv")

    df = pd.read_csv(data_path)

    # Create engineered features only if columns exist
    if {"bedrooms", "bathrooms"}.issubset(df.columns):
        df["bed_bath_interaction"] = df["bedrooms"] * df["bathrooms"]

    if {"sqft_living", "floors"}.issubset(df.columns):
        # Avoid division by zero
        df["sqft_living_per_floor"] = df["sqft_living"] / df["floors"].replace(0, pd.NA)

    # Basic sanity: keep original columns + engineered ones
    df.to_csv(out_path, index=False)

    print("Feature engineering completed.")
    print("Saved engineered dataset to:", out_path)


if __name__ == "__main__":
    main()

