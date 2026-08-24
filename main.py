from fastapi import FastAPI , Response , HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd



CSV_FILE = "india_weather_2025_january.csv"

app = FastAPI()

#frontend allowed to run on these origins to call API from browser
app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_methods=["*"],
     allow_headers=["*"],
)

#loads CSV once the server starts
df = pd.read_csv(CSV_FILE)

#to delete exact duplicate rows
df = df.drop_duplicates()

df["time"] = pd.to_datetime(df["time"])


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