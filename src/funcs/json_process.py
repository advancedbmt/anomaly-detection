import json
from datetime import datetime, timedelta
import pandas as pd
import random
import numpy as np


def parse_entry(entry):
    time_part, state_part = entry.split(" ", 1)
    if ":" in time_part:
        time_obj = datetime.strptime(time_part.lower(), "%I:%M%p").time()
    else:
        time_obj = datetime.strptime(time_part.lower(), "%I%p").time()
    time_str = time_obj.strftime("%H:%M")
    state_clean = state_part.replace("\\", " ")
    return (time_str, state_clean)


def inject_anomaly_by_time(df, anomaly, sensor_name, time_column="timestamp", target_column="feature_0"):
    if anomaly["device"] != sensor_name:
        return df
    
    df[time_column] = pd.to_datetime(df[time_column])

    # Strip timezone if present
    happen_time = pd.to_datetime(anomaly["HappenTime"]).tz_localize(None)

    duration_minutes = int(anomaly["length"].replace("min", ""))
    anomaly_value = float(anomaly["Value"])

    time_diff = (df[time_column] - happen_time).abs()
    start_idx = time_diff.idxmin()

    end_time = happen_time + timedelta(minutes=duration_minutes)
    mask = (df[time_column] >= happen_time) & (df[time_column] < end_time)

    noise = np.random.uniform(-0.5, 0.5, size=mask.sum()) * 5
    df.loc[mask, target_column] = anomaly_value + noise
    df.loc[mask, "is_anomaly"] = True

    return df

