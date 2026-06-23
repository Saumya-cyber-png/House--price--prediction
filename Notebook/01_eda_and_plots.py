"""01_eda_and_plots.py

Exploratory Data Analysis (EDA) for kc_house_data.csv.

This script creates and saves:
- Histogram (distribution of price)
- Boxplot (outliers in price)
- Scatter plot (price vs sqft_living, if available)
- Heatmap (correlation heatmap of numeric features)

All plots are saved into Documentation/.

Run:
python Notebook/01_eda_and_plots.py
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def savefig(path: str):
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def main():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(root_dir, "Dataset", "kc_house_data.csv")
    doc_dir = os.path.join(root_dir, "Documentation")
    os.makedirs(doc_dir, exist_ok=True)

    df = pd.read_csv(data_path)

    # 1) Histogram
    if "price" in df.columns:
        plt.figure(figsize=(8, 5))
        df["price"].hist(bins=30, color="steelblue", alpha=0.85)
        plt.title("House Price Distribution (Histogram)")
        plt.xlabel("price")
        plt.ylabel("count")
        savefig(os.path.join(doc_dir, "hist_price.png"))

        # 2) Boxplot
        plt.figure(figsize=(6, 5))
        sns.boxplot(y=df["price"], color="orange")
        plt.title("House Price Outliers (Boxplot)")
        plt.ylabel("price")
        savefig(os.path.join(doc_dir, "boxplot_price.png"))

    # 3) Scatter Plot: price vs sqft_living (common feature)
    if "price" in df.columns and "sqft_living" in df.columns:
        plt.figure(figsize=(7, 5))
        plt.scatter(df["sqft_living"], df["price"], s=10, alpha=0.4)
        plt.title("Price vs Sqft Living (Scatter)")
        plt.xlabel("sqft_living")
        plt.ylabel("price")
        savefig(os.path.join(doc_dir, "scatter_price_vs_sqft_living.png"))

    # 4) Heatmap: correlations (numeric)
    numeric_df = df.select_dtypes(include=["int64", "float64"])
    if "price" in numeric_df.columns and numeric_df.shape[1] > 1:
        corr = numeric_df.corr(numeric_only=True)

        # Keep heatmap manageable: use top correlated features with price
        top_n = 12
        corr_with_price = corr["price"].abs().sort_values(ascending=False)
        top_features = corr_with_price.head(top_n).index.tolist()

        corr_subset = corr.loc[top_features, top_features]

        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_subset, annot=False, cmap="viridis")
        plt.title("Feature Correlation Heatmap (Top vs price)")
        savefig(os.path.join(doc_dir, "heatmap_feature_correlations.png"))

    print("EDA plots saved to Documentation/:")
    for f in [
        "hist_price.png",
        "boxplot_price.png",
        "scatter_price_vs_sqft_living.png",
        "heatmap_feature_correlations.png",
    ]:
        print("-", f)


if __name__ == "__main__":
    main()

