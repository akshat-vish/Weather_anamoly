import pandas as pd


def engineer_features(df):
    df = df.copy()
    df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'])
    df = df.sort_values(['station_id', 'timestamp_utc'])
    
    df['hour'] = df['timestamp_utc'].dt.hour
    df['month'] = df['timestamp_utc'].dt.month

    for col in ['raw_temp_c', 'raw_pressure_mbar', 'raw_humidity_pct']:
        roll_mean = df.groupby('station_id')[col].transform(
            lambda x: x.rolling(6, min_periods=1).mean()
        )
        roll_std = df.groupby('station_id')[col].transform(
            lambda x: x.rolling(6, min_periods=1).std().fillna(0)
        )
        df[f'{col}_roll_mean'] = roll_mean
        df[f'{col}_roll_std'] = roll_std
        df[f'{col}_zscore'] = (df[col] - roll_mean) / (roll_std + 1e-6)
        df[f'{col}_diff'] = df.groupby('station_id')[col].transform(
            lambda x: x.diff().abs()
        )
        df[f'{col}_frozen'] = df.groupby('station_id')[col].transform(
            lambda x: x.rolling(6, min_periods=3).std().fillna(999)
        )
        short = df.groupby('station_id')[col].transform(
            lambda x: x.rolling(6, min_periods=1).mean()
        )
        long = df.groupby('station_id')[col].transform(
            lambda x: x.rolling(72, min_periods=1).mean()
        )
        df[f'{col}_drift'] = (short - long).abs()
    
    return df

    