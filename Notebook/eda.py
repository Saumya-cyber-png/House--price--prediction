import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def main() -> None:
    root_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(root_dir, "Dataset", "kc_house_data.csv")

    screenshots_dir = os.path.join(root_dir, "Documentation", "Screenshots")
    ensure_dir(screenshots_dir)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at: {data_path}")

    df = pd.read_csv(data_path)

    # ===============
    # 1) Histogram
    # ===============
    plt.figure(figsize=(8, 5))
    sns.histplot(df["price"], bins=30, kde=False, color="steelblue")
    plt.title("House Prices - Histogram")
    plt.xlabel("price")
    plt.ylabel("count")
    plt.show()

    plt.figure(figsize=(8, 5))
    sns.histplot(df["price"], bins=30, kde=False, color="steelblue")
    plt.title("House Prices - Histogram")
    plt.xlabel("price")
    plt.ylabel("count")
    plt.savefig(os.path.join(screenshots_dir, "histogram.png"), dpi=200, bbox_inches="tight")
    plt.close()

    # ===============
    # 2) Boxplot
    # ===============
    plt.figure(figsize=(6, 5))
    sns.boxplot(y=df["price"], color="orange")
    plt.title("House Prices - Boxplot")
    plt.ylabel("price")
    plt.show()

    plt.figure(figsize=(6, 5))
    sns.boxplot(y=df["price"], color="orange")
    plt.title("House Prices - Boxplot")
    plt.ylabel("price")
    plt.savefig(os.path.join(screenshots_dir, "boxplot.png"), dpi=200, bbox_inches="tight")
    plt.close()

    # =====================
    # 3) Scatter sqft_living
    # =====================
    if "sqft_living" not in df.columns:
        raise KeyError("Column 'sqft_living' not found in dataset.")

    plt.figure(figsize=(7, 5))
    plt.scatter(df["sqft_living"], df["price"], s=10, alpha=0.4, color="seagreen")
    plt.title("Price vs Sqft Living")
    plt.xlabel("sqft_living")
    plt.ylabel("price")
    plt.show()

    plt.figure(figsize=(7, 5))
    plt.scatter(df["sqft_living"], df["price"], s=10, alpha=0.4, color="seagreen")
    plt.title("Price vs Sqft Living")
    plt.xlabel("sqft_living")
    plt.ylabel("price")
    plt.savefig(os.path.join(screenshots_dir, "scatterplot.png"), dpi=200, bbox_inches="tight")
    plt.close()

    # =====================
    # 4) Correlation Heatmap
    # =====================
    numeric_df = df.select_dtypes(include=["int64", "float64"]).copy()

    plt.figure(figsize=(10, 8))
    if "price" in numeric_df.columns and numeric_df.shape[1] > 1:
        corr = numeric_df.corr(numeric_only=True)
        sns.heatmap(corr, cmap="viridis", square=False)
        plt.title("Correlation Heatmap (Numeric Features)")
    else:
        plt.text(0.5, 0.5, "Not enough numeric columns for correlation heatmap.", ha="center")

    plt.show()

    plt.figure(figsize=(10, 8))
    if "price" in numeric_df.columns and numeric_df.shape[1] > 1:
        corr = numeric_df.corr(numeric_only=True)
        sns.heatmap(corr, cmap="viridis", square=False)
        plt.title("Correlation Heatmap (Numeric Features)")
    else:
        plt.text(0.5, 0.5, "Not enough numeric columns for correlation heatmap.", ha="center")

    plt.savefig(os.path.join(screenshots_dir, "heatmap.png"), dpi=200, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()

