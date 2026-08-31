import pandas as pd

df = pd.read_csv("india_weather_2025_january.csv")
df = df.drop_duplicates()

columns_to_check = ["temp", "pres", "rhum", "wspd", "prcp"]

print(df[columns_to_check].describe())
print()

# Look at the most extreme high and low values for each column
for col in columns_to_check:
    print(f"--- {col} ---")
    print("Lowest 3 values:")
    print(df.nsmallest(3, col)[["time", "station_name", col]])
    print("Highest 3 values:")
    print(df.nlargest(3, col)[["time", "station_name", col]])
    print()