import pandas as pd
from engineer_features import engineer_features

df = pd.read_csv("india_weather_2025_january.csv")
df = df.drop_duplicates()

df = engineer_features(df)

print("Shape:", df.shape)
print()
print("Columns:", list(df.columns))
print()
print(df.head(3))