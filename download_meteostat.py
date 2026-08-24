import meteostat as ms
from datetime import datetime
import pandas as pd

# ---------------------------------------
# Stations
# ---------------------------------------

stations = {
    "42182": "Safdarjung",
    "42181": "Palam",
    "42139": "Meerut",
    "42176": "Rohtak",
    "42262": "Aligarh",
    "42137": "Karnal",
    "42140": "Roorkee"
}

# ---------------------------------------
# Date range
# ---------------------------------------

start = datetime(2025, 1, 1)
end = datetime(2025, 2, 1)

all_data = []

# ---------------------------------------
# Download each station
# ---------------------------------------

for station_id, station_name in stations.items():

    print(f"\nDownloading {station_name} ({station_id})...")

    try:
        station = ms.Station(station_id)

        data = ms.hourly(
            station,
            start,
            end
        )

        df = data.fetch()

        # Check if Meteostat returned nothing
        if df is None or df.empty:
            print("No data found - skipping.")
            continue

        # Add station information
        df["station_id"] = station_id
        df["station_name"] = station_name

        all_data.append(df)

        print("Rows:", len(df))

    except Exception as e:
        print(f"ERROR for {station_name}: {e}")
        continue

    df = data.fetch()

    if df is None or df.empty:
        print("No data found.")
        continue

    # Add station information
    df["station_id"] = station_id
    df["station_name"] = station_name

    all_data.append(df)

    print("Rows:", len(df))


# ---------------------------------------
# Combine all stations
# ---------------------------------------

if all_data:

    combined = pd.concat(all_data)

    combined = combined.reset_index()

    # Sort
    combined = combined.sort_values(
        ["station_id", "time"]
    )

    # Save
    combined.to_csv(
        "india_weather_2025_january.csv",
        index=False
    )

    print("\n==============================")
    print("DOWNLOAD COMPLETE")
    print("==============================")

    print("Total rows:", len(combined))
    print("Stations:", combined["station_id"].nunique())

    print("\nRows per station:")
    print(combined["station_name"].value_counts())

    print("\nSaved as:")
    print("india_weather_2025_january.csv")

else:

    print("No station data was downloaded.")