import os
import pandas as pd
from config import DEVICES_DATA_PATH, EXCLUDE_COLUMNS

def get_model_name(device_type, state):
    """
    Generate the LSTM model filename based on device type and state.
    """
    if device_type == 'bale_counter':
        return f"lstm_{state}_bale_counter.h5"
    elif device_type == 'temperature_sensor':
        return f"lstm_{state}_temperature_sensor.h5"
    elif device_type == 'output_sensor':
        return f"lstm_{state}.h5"
    else:
        return f"lstm_{state}.h5"

def get_rf_model_name(device_type):
    """
    Generate the Random Forest model filename based on device type.
    """
    if device_type == 'bale_counter':
        return "random_forest_bale_counter.pkl"
    elif device_type == 'output_sensor':
        return "random_forest_output_sensor.pkl"
    elif device_type == 'temperature_sensor':
        return "random_forest_temperature_sensor.pkl"
    elif device_type == 'motor_monitor':
        return "random_forest_motor_monitor.pkl"
    return None

def get_device_files():
    """
    Fetch all device CSV files from the data directory.
    """
    device_files = []
    for file in os.listdir(DEVICES_DATA_PATH):
        if file.endswith("_unified.csv"):
            device_type = file.split('_')[0] + '_' + file.split('_')[1]
            if device_type == "hatch_status":
                continue
            device_files.append((device_type, file))
    return device_files

def get_numerical_features(df):
    """
    Identify numerical sensor columns in a DataFrame.
    """
    return [col for col in df.columns if col not in EXCLUDE_COLUMNS and pd.api.types.is_numeric_dtype(df[col])]
    