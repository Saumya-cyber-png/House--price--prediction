import pandas as pd

# Load Dataset
df = pd.read_csv("Dataset/kc_house_data.csv")

# Show first 5 rows
print(df.head())

# Show dataset shape
print("\nDataset Shape:")
print(df.shape)
print("\nColumn Names:")
print(df.columns)

print("\nDataset Information:")
print(df.info())
print("Before:", df.shape)

df = df.drop_duplicates()

print("After:", df.shape)