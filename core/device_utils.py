import os
import pandas as pd
from core.config import DEVICES_DATA_PATH, EXCLUDE_COLUMNS

def get_model_name(device_type, state):
    return f"lstm_{state}_{device_type}.h5"

def get_device_files():
    device_files = []
    for file in os.listdir(DEVICES_DATA_PATH):
        if file.endswith("_unified.csv"):
            parts = file.split("_")
            device_type = "_".join(parts[:2]) if len(parts) >= 2 else parts[0]
            if device_type == "hatch_status":
                continue
            full_path = os.path.join(DEVICES_DATA_PATH, file)
            device_files.append((device_type, full_path))
    return device_files

def get_numerical_features(df):
    exclude = EXCLUDE_COLUMNS + ["label", "rf_prediction", "is_anomaly", "reconstruction_error"]
    return [col for col in df.columns if col not in exclude and pd.api.types.is_numeric_dtype(df[col])]
