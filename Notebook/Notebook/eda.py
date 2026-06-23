import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Dataset/clean_house_data.csv")

print(df.head())

df["price"].hist()

plt.title("House Price Distribution")

plt.show()