"""05_model_saving.py

This file is intentionally simple because the project already saves the best
model in:
- Notebook/03_model_training_and_comparison.py

Here we just verify the model exists and print the path.

Run:
python Notebook/05_model_saving.py
"""

import os


def main():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(root_dir, "Model", "house_price_model.pkl")

    if os.path.exists(model_path):
        print("Model saved successfully at:")
        print(model_path)
    else:
        print("Model file not found. Run 03_model_training_and_comparison.py first.")


if __name__ == "__main__":
    main()

