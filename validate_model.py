import pandas as pd
import joblib
from engineer_features import engineer_features

# Load the FULL real dataset — all stations, not just one
df = pd.read_csv("india_weather_2025_january.csv")
df = df.drop_duplicates()
df = df.sort_values(["station_id", "time"]).reset_index(drop=True)

model = joblib.load("isolation_forest_model.joblib")

# We'll inject faults into Karnal's rows specifically,
# but keep them inside the FULL dataset (all 6 stations together)
karnal_rows = df[df["station_id"] == 42137].index.tolist()

injected_rows = []

# --- Fault 1: a sudden spike ---
spike_index = karnal_rows[100]
df.loc[spike_index, "temp"] = 100.0
injected_rows.append((spike_index, "spike"))

# --- Fault 2: a frozen sensor (5 consecutive identical readings) ---
frozen_start_pos = 200
frozen_index = karnal_rows[frozen_start_pos]
frozen_value = 25.0                                                                                                                                                                
for offset in range(5):                                                                                                                                                                                                           
      idx = karnal_rows[frozen_start_pos + offset]                                                                                                                                                                                  
      df.loc[idx, "temp"] = frozen_value  
      injected_rows.append((idx, "frozen"))

# --- Fault 3: gradual drift ---
drift_start_pos = 300
for offset in range(10):                                                                                                                                                                                                          
      idx = karnal_rows[drift_start_pos + offset]                                                                                                                                                                                   
      df.loc[idx, "temp"] += offset * 5.0 

# Re-run feature engineering on the FULL corrupted dataset
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
predictions = model.predict(X)
scores = model.decision_function(X)

caught = 0
for idx, fault_type in injected_rows:
    result = "ANOMALY" if predictions[idx] == -1 else "missed"
    if predictions[idx] == -1:
        caught += 1
    print(f"Row {idx} ({fault_type}): {result}  (score={scores[idx]:.4f})")

print()
print(f"Caught {caught} out of {len(injected_rows)} injected faults")
print(f"Overall score range — min: {scores.min():.4f}, max: {scores.max():.4f}")