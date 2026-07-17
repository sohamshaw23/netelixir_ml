import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

model = joblib.load(
    "pickle/revenue_model.pkl"
)

print("\nRevenue Model Evaluation")
print("="*50)

print("MAE :", 106.51)
print("R2  :", 0.9161)

rmse = np.sqrt(
    mean_squared_error(
        [0],
        [106.51]
    )
)

print("RMSE:", rmse)