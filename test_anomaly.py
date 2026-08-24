import pandas as pd
import joblib
from engineer_features import engineer_features


#Loaded the trained model
model = joblib.load("anomaly_model.joblib")

#Loaded the weather data
df = pd.read_csv("india_weather_2025_january.csv")
df = df.drop_duplicates()

#Renaming
df = df.rename(columns={
    "time": "timestamp_utc",
    "temp": "raw_temp_c",
    "pres": "raw_pressure_mbar",
    "rhum": "raw_humidity_pct",
})

#Generated the engineered features
df = engineer_features(df)

# 'dayofweek' column
df["dayofweek"] = df["timestamp_utc"].dt.dayofweek

# Loaded exact features list the model expects
import json
with open("features.json") as f:
    feature_columns = json.load(f)

# Select only those columns, in the exact order the model expects
X = df[feature_columns]

# Run predictions
predictions = model.predict(X)
probabilities = model.predict_proba(X)

print("First 10 predictions:", predictions[:10])
print("First 10 probabilities:", probabilities[:10])