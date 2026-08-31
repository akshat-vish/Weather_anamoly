import pandas as pd


def engineer_features(df):
    df = df.copy()
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values(["station_id", "time"])

    df["hour"] = df["time"].dt.hour
    df["month"] = df["time"].dt.month

    for col in ["temp", "pres", "rhum", "wspd", "prcp"]:
        shifted = df.groupby("station_id")[col].shift(1)

        roll_mean = shifted.groupby(df["station_id"]).transform(
            lambda x: x.rolling(6, min_periods=1).mean()
        )
        roll_std = shifted.groupby(df["station_id"]).transform(
            lambda x: x.rolling(6, min_periods=1).std().fillna(0)
        )
        df[f"{col}_roll_mean"] = roll_mean
        df[f"{col}_roll_std"] = roll_std
        df[f"{col}_zscore"] = (df[col] - roll_mean) / (roll_std + 1e-6)

    return df