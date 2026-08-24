import requests
import json
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
URL = (
    "https://wis2boxstdby.imd.gov.in/"
    "oapi/collections/"
    "urn:wmo:md:in-imd:surface-based-observations.synop/"
    "items?f=json&sortby=-reportTime&limit=1000"
)

print("Downloading IMD data...")

response = requests.get(URL, timeout=30, verify=False)

if response.status_code != 200:
    print("Request failed!")
    print("Status code:", response.status_code)
    print(response.text[:500])
    exit()

data = response.json()

print("Download successful!")

# Save the original JSON
with open("raw_imd.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Raw data saved as raw_imd.json")

features = data.get("features", [])

print("Number of records:", len(features))


# ---------------------------------------------------
# Convert IMD observation records into rows
# ---------------------------------------------------

rows = []

for feature in features:

    properties = feature.get("properties", {})

    station = properties.get("wigos_station_identifier")
    report_time = properties.get("reportTime")
    observation_time = properties.get("phenomenonTime")

    parameter = properties.get("name")
    value = properties.get("value")
    units = properties.get("units")

    geometry = feature.get("geometry", {})
    coordinates = geometry.get("coordinates", [None, None])

    longitude = coordinates[0]
    latitude = coordinates[1]

    rows.append({
        "station_id": station,
        "report_time": report_time,
        "observation_time": observation_time,
        "parameter": parameter,
        "value": value,
        "units": units,
        "latitude": latitude,
        "longitude": longitude
    })


df = pd.DataFrame(rows)

print("\nRaw table:")
print(df.head())

print("\nParameters found:")

print(df["parameter"].value_counts())


# Save the raw standardized table
df.to_csv("imd_observations_long.csv", index=False)

print("\nSaved:")
print("imd_observations_long.csv")