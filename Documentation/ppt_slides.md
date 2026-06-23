# PPT Slide Content (House Price Prediction)

## Slide 1: Title
**House Price Prediction**
- Using Machine Learning Regression
- Dataset: kc_house_data.csv

## Slide 2: Problem Statement
- Predict house prices based on features (bedrooms, bathrooms, size, floors, etc.)
- Help estimate selling price using data-driven approach

## Slide 3: Dataset Overview
- Source dataset: `kc_house_data.csv`
- Target variable: `price`
- Features: mix of numeric + possible categorical columns

## Slide 4: Workflow (High Level)
1. Data preprocessing
2. EDA & Visualization
3. Feature engineering
4. Train multiple models
5. Evaluate & compare models
6. Save the best model
7. Deploy using Streamlit

## Slide 5: Data Preprocessing
- Handle missing values
  - Numeric: median
  - Categorical: most frequent
- Encoding categorical variables
- Feature scaling (important for Linear Regression)
- Pipeline ensures consistent preprocessing

## Slide 6: EDA & Plots
Saved plots in `Documentation/`:
- Histogram (price distribution)
- Boxplot (outliers)
- Scatter plot (sqft_living vs price)
- Heatmap (correlations)

## Slide 7: Feature Engineering
- Create interaction feature: `bedrooms * bathrooms`
- Create per-floor living area: `sqft_living / floors`
- Save engineered dataset to `Dataset/clean_house_data.csv`

## Slide 8: Models Compared
1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor

## Slide 9: Evaluation Metrics
- MAE: average absolute prediction error
- MSE: squared error (penalizes large mistakes)
- RMSE: sqrt of MSE (in same units as price)
- R2 Score: explains variance (higher is better)

## Slide 10: Results (Explain in your run)
- Show table of metrics sorted by R2
- Highlight which model performed best

## Slide 11: Best Model Saving
- Best pipeline saved as:
  - `Model/house_price_model.pkl`
- Pipeline includes preprocessing + trained model

## Slide 12: Streamlit Deployment
- Web app where user enters features
- App loads saved pipeline and predicts price instantly
- Location: `Streamlit_App/app.py`

## Slide 13: Demo Flow
- User opens app
- Enters inputs
- Clicks Predict
- Shows predicted price + input summary

## Slide 14: Conclusion
- End-to-end ML project built
- Model comparison completed
- Deployment done with Streamlit

## Slide 15: Future Work
- Hyperparameter tuning (GridSearchCV)
- Add more feature engineering
- Explainability (feature importance / SHAP)
- Improved input UI and validation

