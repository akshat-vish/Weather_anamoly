import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from engineer_features import engineer_features

df = pd.read_csv("india_weather_2025_january.csv")
df = df.drop_duplicates()

df = engineer_features(df)

feature_columns = [
     "hour", "month",
    "temp", "pres", "rhum", "wspd", "prcp",
    "temp_roll_mean", "temp_roll_std", "temp_zscore",
    "pres_roll_mean", "pres_roll_std", "pres_zscore",
    "rhum_roll_mean", "rhum_roll_std", "rhum_zscore",
    "wspd_roll_mean", "wspd_roll_std", "wspd_zscore",
    "prcp_roll_mean", "prcp_roll_std", "prcp_zscore",
]

X = df[feature_columns]

model = IsolationForest(contamination=0.10, random_state=42)
model.fit(X)

predictions = model.predict(X)


print("Total rows:", len(predictions))
print("Predicted normal (1):", (predictions == 1).sum())
print("Predicted anomaly (-1):", (predictions == -1).sum())

joblib.dump(model, "isolation_forest_model.joblib")
print("Model saved.")