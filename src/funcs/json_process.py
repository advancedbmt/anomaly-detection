import json
from datetime import datetime
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


def inject_anomaly_by_time(
    df, anomaly, time_column="timestamp", target_column="feature_0"
):
    df[time_column] = pd.to_datetime(df[time_column])
    target_time = datetime.fromisoformat(anomaly["HappenTime"].replace("Z", "")).time()
    duration = int(anomaly["length"].replace("min", ""))
    anomaly_value = float(anomaly["Value"])
    df["__only_time"] = df[time_column].dt.time
    start_indices = df.index[df["__only_time"] == target_time].tolist()
    if start_indices:
        start_idx = start_indices[0]
        end_idx = start_idx + duration
        noise = np.random.uniform(-0.5, 0.5, size=end_idx - start_idx) * 5
        df.loc[start_idx : end_idx - 1, target_column] = anomaly_value + noise
        df.loc[start_idx : end_idx - 1, "is_anomaly"] = True
    df.drop(columns=["__only_time"], inplace=True)
    return df
