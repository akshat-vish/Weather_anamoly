import meteostat as ms
from datetime import datetime

station = ms.Station("42182")

start = datetime(2025, 1, 1)
end = datetime(2025, 2, 1)

print("Downloading hourly data...")

data = ms.hourly(
    station,
    start,
    end
)

df = data.fetch()
df.to_csv("safdarjung_2025_01.csv")

print("\nRows:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst rows:")
print(df.head(10))

print("\nLast rows:")
print(df.tail(10))

print("\nMissing values:")
print(df.isna().sum())