import pandas as pd
import joblib
from engineer_features import engineer_features

# Load clean data (no injected faults)
df = pd.read_csv("india_weather_2025_january.csv")
df = df.drop_duplicates()
df = df.sort_values(["station_id", "time"]).reset_index(drop=True)

# Engineer features
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

# Load the model (trained with contamination=0.50)
model = joblib.load("isolation_forest_model.joblib")

# Predict on CLEAN data (no injected faults)
predictions = model.predict(X)
scores = model.decision_function(X)

# Count false positives
total = len(predictions)
flagged_as_anomaly = (predictions == -1).sum()
flagged_as_normal = (predictions == 1).sum()

print("=" * 60)
print("FALSE POSITIVE CHECK")
print("=" * 60)
print(f"Total clean weather records: {total}")
print(f"Flagged as ANOMALY (-1): {flagged_as_anomaly} ({flagged_as_anomaly/total*100:.1f}%)")
print(f"Flagged as normal (+1): {flagged_as_normal} ({flagged_as_normal/total*100:.1f}%)")
print()

if flagged_as_anomaly > 0:
    print(f"⚠️  WARNING: {flagged_as_anomaly} normal data points flagged as anomalies!")
    print(f"   This means {flagged_as_anomaly/total*100:.1f}% FALSE POSITIVE RATE")
    print()

    # Show some examples
    anomaly_indices = df[predictions == -1].index[:10]
    print("First 10 false positives:")
    print("-" * 60)
    for idx in anomaly_indices:
        row = df.loc[idx]
        print(f"Row {idx}: station={row['station_name']}, time={row['time']}, "
              f"temp={row['temp']:.1f}°C, score={scores[idx]:.4f}")
else:
    print("✅ No false positives! (But this might mean contamination is too low)")

print()
print("=" * 60)
print("SCORE DISTRIBUTION")
print("=" * 60)
print(f"Min score: {scores.min():.4f}")
print(f"Max score: {scores.max():.4f}")
print(f"Mean score: {scores.mean():.4f}")
print(f"Threshold (0.0): scores below 0 are flagged as anomalies")
