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

def inject_anomaly_by_time(df, anomaly, time_column='timestamp', target_column='feature_0'):
    """
    Injects an anomaly into a DataFrame based on time-of-day match, ignoring date.

    Parameters:
    - df: Pandas DataFrame with a datetime column
    - anomaly: Dictionary with keys "HappenTime", "Type", "length", "Value"
    - time_column: Name of the timestamp column (default "timestamp")
    - target_column: Name of the feature column to inject into (default "feature_0")

    Returns:
    - DataFrame with anomaly injected
    """
    # Ensure timestamp column is datetime
    df[time_column] = pd.to_datetime(df[time_column])

    # Extract the time part from the HappenTime
    target_time = datetime.fromisoformat(anomaly["HappenTime"].replace("Z", "")).time()
    
    # Extract anomaly parameters
    duration = int(anomaly["length"].replace("min", ""))
    anomaly_value = float(anomaly["Value"])

    # Match only the time (ignore date)
    df['__only_time'] = df[time_column].dt.time
    start_indices = df.index[df['__only_time'] == target_time].tolist()

    if start_indices:
        start_idx = start_indices[0]
        end_idx = start_idx + duration
        num_rows = end_idx - start_idx
        noise = np.random.uniform(-0.5, 0.5, size=num_rows) * 5
        df.loc[start_idx:end_idx-1, target_column] = anomaly_value + noise

    # Clean up
    df.drop(columns=['__only_time'], inplace=True)
    
    return df


if __name__ == "__main__":
    with open("config.json", "r") as file:
        config = json.load(file)


    batch_data = config["state_timeline"]["batch"]

    parsed_batch = [parse_entry(entry) for entry in batch_data]


    print("Parsed batch schedule:")
    print(parsed_batch)
