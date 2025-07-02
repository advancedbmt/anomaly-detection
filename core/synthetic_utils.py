import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

def parse_state_timeline(entries, date="2025-04-07"):
    result = []
    for entry in entries:
        try:
            time_str, state = entry.split()
            dt = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %I:%M%p")
            result.append((dt, state.lower()))
        except Exception:
            continue
    return sorted(result, key=lambda x: x[0])

def generate_state_based_data(schedule, ranges, ambient=0.0, freq="1min"):
    df_all = []
    for i in range(len(schedule) - 1):
        start, state = schedule[i]
        end, _ = schedule[i + 1]
        if state not in ranges:
            continue
        times = pd.date_range(start=start, end=end - timedelta(minutes=1), freq=freq)
        values = np.random.uniform(*ranges[state], len(times)) + ambient
        df = pd.DataFrame({
            "timestamp": times,
            "feature_0": values,
            "state": state,
            "is_anomaly": False
        })
        df_all.append(df)
    return pd.concat(df_all, ignore_index=True)

def inject_anomaly_by_time(df, anomaly, sensor, time_col="timestamp", target="feature_0"):
    if anomaly["tag"] != sensor:
        return df
    happen_time = pd.to_datetime(anomaly["HappenTime"]).tz_localize(None)
    duration = int(anomaly["length"].replace("min", ""))
    value = float(anomaly["Value"])
    end_time = happen_time + timedelta(minutes=duration)
    mask = (df[time_col] >= happen_time) & (df[time_col] < end_time)
    noise = np.random.uniform(-0.5, 0.5, size=mask.sum()) * 5
    if 1.2 <= value <= 2.0:
        df.loc[mask, target] *= value + noise
    else:
        df.loc[mask, target] = value + noise
    df.loc[mask, "is_anomaly"] = True
    return df
