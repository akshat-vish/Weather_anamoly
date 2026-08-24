import json
import pandas as pd

# -----------------------------------------
# 1. Load the JSON downloaded from IMD
# -----------------------------------------

with open("raw_imd.json", "r", encoding="utf-8") as f:
    data = json.load(f)

features = data.get("features", [])

print("Total raw records:", len(features))


# -----------------------------------------
# 2. Extract each observation
# -----------------------------------------

rows = []

for feature in features:

    properties = feature.get("properties", {})
    geometry = feature.get("geometry", {})

    coordinates = geometry.get("coordinates", [None, None])

    longitude = coordinates[0]
    latitude = coordinates[1]

    rows.append({
        "station_id": properties.get("wigos_station_identifier"),
        "timestamp": properties.get("phenomenonTime"),
        "parameter": properties.get("name"),
        "value": properties.get("value"),
        "units": properties.get("units"),
        "latitude": latitude,
        "longitude": longitude
    })


df = pd.DataFrame(rows)


# -----------------------------------------
# 3. Show basic information
# -----------------------------------------

print("\nParameters found:")
print(df["parameter"].value_counts())

print("\nStations found:")
print(df["station_id"].nunique())

print("\nTimestamps found:")
print(df["timestamp"].nunique())


# -----------------------------------------
# 4. Convert from LONG format
#    to WIDE format
# -----------------------------------------

weather = df.pivot_table(
    index=[
        "station_id",
        "timestamp",
        "latitude",
        "longitude"
    ],
    columns="parameter",
    values="value",
    aggfunc="first"
).reset_index()


# -----------------------------------------
# 5. Rename columns
# -----------------------------------------

weather = weather.rename(columns={
    "air_temperature": "temperature_c",
    "relative_humidity": "humidity_pct",
    "dewpoint_temperature": "dewpoint_c",
    "wind_speed": "wind_speed_ms",
    "wind_direction": "wind_direction_deg",
    "pressure_reduced_to_mean_sea_level": "pressure_hpa",
    "total_precipitation_or_total_water_equivalent":
        "precipitation"
})


# -----------------------------------------
# 6. Sort chronologically
# -----------------------------------------

weather["timestamp"] = pd.to_datetime(
    weather["timestamp"],
    errors="coerce",
    utc = True
)

#Remove obsevation that dont have timestamp
weather = weather.dropna(subset=["timestamp"])

df=pd.DataFrame(rows)

# Remove records without a timestamp
df = df.dropna(subset=["timestamp"])

print("\nParameters found:")
print(df["parameter"].value_counts())

print("\nStations found:")
print(df["station_id"].nunique())

print("\nTimestamps found:")
print(df["timestamp"].nunique())

weather = weather.sort_values(
    ["station_id", "timestamp"]
)


# -----------------------------------------
# 7. Display the result
# -----------------------------------------

print("\nClean dataset:")
print(weather.head(20).to_string())

print("\nDataset shape:")
print(weather.shape)


# -----------------------------------------
# 8. Check missing values
# -----------------------------------------

print("\nMissing values:")
print(weather.isna().sum())


# -----------------------------------------
# 9. Save clean dataset
# -----------------------------------------

weather.to_csv(
    "imd_weather_clean.csv",
    index=False
)

print("\nSaved successfully:")
print("imd_weather_clean.csv")