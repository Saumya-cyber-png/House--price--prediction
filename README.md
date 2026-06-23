<<<<<<< HEAD
# House Price Prediction (kc_house_data)

This project predicts house prices using **machine learning regression** on the **kc_house_data.csv** dataset.

## What’s included
- Data preprocessing (missing values + scaling + encoding)
- EDA plots (saved under `Documentation/`)
- Feature engineering (lightweight engineered features)
- Model comparison:
  - Linear Regression
  - Decision Tree Regressor
  - Random Forest Regressor
- Model evaluation metrics:
  - MAE, MSE, RMSE, R2
- Best model saved to:
  - `Model/house_price_model.pkl`
- Streamlit app for interactive prediction:
  - `Streamlit_App/app.py`

## How to run (scripts)
From the project root:

```bash
python Notebook/02_feature_engineering.py
python Notebook/01_eda_and_plots.py
python Notebook/03_model_training_and_comparison.py
```

## Streamlit application
Run:

```bash
streamlit run Streamlit_App/app.py
```

## Model file
- `Model/house_price_model.pkl`

The saved file contains a full pipeline (preprocessor + model) so inference works reliably.

## Notes
- If `Dataset/clean_house_data.csv` exists, training will use it.
- Otherwise it falls back to `Dataset/kc_house_data.csv`.

=======
# House--price--prediction
Machine learning project for predicting house price using Python and Streamlit
>>>>>>> c7df29bd39b0390de91366278901b0dd91d7ecf1
