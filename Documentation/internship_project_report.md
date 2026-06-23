# Internship Project Report: House Price Prediction

## 1. Project Overview
This project predicts house prices using machine learning regression techniques. The dataset used is **kc_house_data.csv**, which contains features such as number of bedrooms, bathrooms, living area, and more.

The project focuses on:
- Understanding the dataset with EDA
- Cleaning and preparing the data
- Creating useful features (feature engineering)
- Training multiple regression models
- Evaluating performance using standard metrics
- Saving the best model
- Building a Streamlit application for user interaction

## 2. Dataset Description
The dataset `kc_house_data.csv` includes a target column:
- **price** (house selling price)

And multiple input feature columns (e.g., `bedrooms`, `bathrooms`, `sqft_living`, `floors`, etc.).

## 3. Data Preprocessing
Because real-world datasets often have missing values and inconsistent scales, preprocessing was required.

Steps performed:
1. **Load dataset** using pandas.
2. **Split data** into training and testing sets (80/20 split).
3. **Missing value handling**:
   - Numeric columns: fill missing values with the **median**.
   - Categorical columns: fill missing values with the **most frequent** value.
4. **Encoding**:
   - Categorical features (if any) are encoded using **OneHotEncoder**.
5. **Scaling**:
   - Numeric features are scaled using **StandardScaler**.

All these preprocessing steps were included inside a reusable scikit-learn `Pipeline`.

## 4. Exploratory Data Analysis (EDA)
EDA helps in understanding patterns and relationships.

Plots generated and saved to `Documentation/`:
- Histogram of `price` (distribution)
- Boxplot of `price` (outliers)
- Scatter plot of `sqft_living` vs `price` (trend)
- Correlation heatmap of numeric features (relationships)

## 5. Feature Engineering
To improve model performance, lightweight engineered features were created:
- Interaction feature: `bedrooms * bathrooms`
- Per-floor living area proxy: `sqft_living / floors` (when floors are non-zero)

Engineered dataset saved to:
- `Dataset/clean_house_data.csv`

If the required columns are not present, the script safely skips those engineering steps.

## 6. Model Training and Comparison
Three regression models were trained and compared:

1. **Linear Regression**
2. **Decision Tree Regressor**
3. **Random Forest Regressor**

### Train/Test Strategy
- Train: 80% of data
- Test: 20% of data

Each model was trained inside a pipeline that included preprocessing.

## 7. Model Evaluation Metrics
Model quality was measured using:
- **MAE** (Mean Absolute Error)
- **MSE** (Mean Squared Error)
- **RMSE** (Root Mean Squared Error)
- **R2 Score** (how well the model explains variance)

## 8. Best Model Saving
The model with the highest **R2 Score** on the test set was selected as the best model.

Saved to:
- `Model/house_price_model.pkl`

The saved file contains the full pipeline (preprocessing + model), ensuring consistent prediction.

## 9. Streamlit Application
A Streamlit app was created to allow users to enter house features and get predicted price.

Location:
- `Streamlit_App/app.py`

## 10. Conclusion
This project demonstrates end-to-end machine learning development for house price prediction:
- Data understanding (EDA)
- Data preparation (preprocessing + feature engineering)
- Training multiple models
- Performance evaluation
- Deployment-ready prediction via Streamlit

## 11. Future Improvements
Possible next steps:
- Hyperparameter tuning using GridSearchCV/RandomizedSearchCV
- More advanced feature engineering
- Model explainability tools (feature importance, SHAP)
- Handling more complex categorical features

