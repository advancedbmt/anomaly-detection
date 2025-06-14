import os
import pandas as pd
from config import DEVICES_DATA_PATH, EXCLUDE_COLUMNS


def get_model_name(device_type, state):
    """
    Generate the LSTM model filename based on device type and state.
    """
    if device_type == "bale_counter":
        return f"lstm_{state}_bale_counter.h5"
    elif device_type == "temperature_sensor":
        return f"lstm_{state}_temperature_sensor.h5"
    elif device_type == "output_sensor":
        return f"lstm_{state}.h5"
    else:
        return f"lstm_{state}.h5"


# Removed get_rf_model_name as RF classifier is being removed
# def get_rf_model_name(device_type):
#     """
#     Generate the Random Forest model filename based on device type.
#     """
#     if device_type == "bale_counter":
#         return "random_forest_bale_counter.pkl"
#     elif device_type == "output_sensor":
#         return "random_forest_output_sensor.pkl"
#     elif device_type == "temperature_sensor":
#         return "random_forest_temperature_sensor.pkl"
#     elif device_type == "motor_monitor":
#         return "random_forest_motor_monitor.pkl"
#     return None


def get_device_files():
    """
    Fetch all device CSV files from the data directory, returning full paths.
    """
    device_files = []
    for file in os.listdir(DEVICES_DATA_PATH):
        if file.endswith("_unified.csv"):
            # Ensure device_type extraction is robust
            parts = file.split("_")
            if len(parts) >= 2: # handle cases like "hatch_status_0_unified.csv"
                device_type = "_".join(parts[:2]) # e.g., "bale_counter", "hatch_status"
            else:
                device_type = parts[0] # Fallback for single word names

            if device_type == "hatch_status": # Still exclude if desired
                continue
            full_path = os.path.join(DEVICES_DATA_PATH, file)
            device_files.append((device_type, full_path))
    return device_files


def get_numerical_features(df):
    # 'rf_prediction' is no longer generated, 'is_anomaly' is an output/label, not a feature.
    # 'reconstruction_error' is also an output/score.
    exclude = EXCLUDE_COLUMNS + ["label", "rf_prediction", "is_anomaly", "reconstruction_error"]
    return [
        col
        for col in df.columns
        if col not in exclude and pd.api.types.is_numeric_dtype(df[col])
    ]