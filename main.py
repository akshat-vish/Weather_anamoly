from fastapi import FastAPI , Response , HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import json
from engineer_features import engineer_features



CSV_FILE = "india_weather_2025_january.csv"
MODEL_FILE = "anomaly_model.joblib"
FEATURES_FILE = "features.json"

#ASSUMPTION (UNCONFIERMED MAY CHANGE): 1 = anomaly, 0 = normal
ANOMALY_LABEL = 1# single value  will get if it gets confirmed the opposite

app = FastAPI()

#frontend allowed to run on these origins to call API from browser
app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_methods=["*"],
     allow_headers=["*"],
)

# ---- Load weather data ----
df = pd.read_csv(CSV_FILE)
df = df.drop_duplicates()
df["time"] = pd.to_datetime(df["time"])

# ---- Loaded anomaly model + expected features ----
model = joblib.load(MODEL_FILE)
with open(FEATURES_FILE) as f:
    feature_columns = json.load(f)

#---- Build a renamed copy for feature engineering (model expects these names) ----
model_input = df.rename(columns={
    "time": "timestamp_utc",
    "temp": "raw_temp_c",
    "pres": "raw_pressure_mbar",
    "rhum": "raw_humidity_pct",
})
model_input = engineer_features(model_input)
model_input["dayofweek"] = model_input["timestamp_utc"].dt.dayofweek

X = model_input[feature_columns]

# ---- Run predictions once, store results back onto the main df ----
predictions = model.predict(X)
probabilities = model.predict_proba(X)

print(f"Total rows: {len(predictions)}")
print(f"Predicted as class 1: {(predictions == 1).sum()}")
print(f"Predicted as class 0: {(predictions == 0).sum()}")

df["is_anomaly"] = predictions == ANOMALY_LABEL
df["anomaly_probability"] = probabilities[:, ANOMALY_LABEL]


@app.get("/")
def read_root():
    return {"message" : "Weather anomaly backend is running"}

@app.get("/weather")
def get_weather(
    station_id: int = None,
    station_name: str = None,
    start: str = None,
    end: str = None,
):
    result = df

    if station_id is not None:
        result = result[result["station_id"] == station_id]

    if station_name is not None:
        result = result[result["station_name"] == station_name]

    if start is not None:
        try:
            start_date = pd.to_datetime(start)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid 'start' date. Use format YYYY-MM-DD.")
        result = result[result["time"] >= start_date]

    if end is not None:
        try:
            end_date = pd.to_datetime(end)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid 'end' date. Use format YYYY-MM-DD.")
        end_of_day = end_date + pd.Timedelta(days=1)
        result = result[result["time"] < end_of_day]

    json_data = result.to_json(orient="records", date_format="iso")
    return Response(content=json_data, media_type="application/json")

@app.get("/stations")
def get_stations():
    stations = df[["station_id","station_name"]].drop_duplicates()
    json_data = stations.to_json(orient="records")
    return Response(content=json_data, media_type="application/json")

@app.get("/anomalies")
def get_anomalies(
    station_id: int = None,
    station_name: str = None,
    start: str = None,
    end: str = None,
    only_anomalies: bool = True,
):
    result = df

    if station_id is not None:
        result = result[result["station_id"] == station_id]
    if station_name is not None:
        result = result[result["station_name"] == station_name]

    if start is not None:
        try:
            start_date = pd.to_datetime(start)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid 'start' date. Use format YYYY-MM-DD.")
        result = result[result["time"] >= start_date]

    if end is not None:
        try:
            end_date = pd.to_datetime(end)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid 'end' date. Use format YYYY-MM-DD.")
        end_of_day = end_date + pd.Timedelta(days=1)
        result = result[result["time"] < end_of_day]

    if only_anomalies:
        result = result[result["is_anomaly"] == True]

    json_data = result.to_json(orient="records", date_format="iso")
    return Response(content=json_data, media_type="application/json")
    