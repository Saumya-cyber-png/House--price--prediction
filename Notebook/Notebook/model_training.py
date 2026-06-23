import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load Dataset
df = pd.read_csv("Dataset/kc_house_data.csv")

# Features
X = df[['bedrooms', 'bathrooms', 'sqft_living', 'floors']]

# Target
y = df['price']

# Split Data
# Train Model
model = LinearRegression()

model.fit(X_train, y_train)

# Prediction
predictions