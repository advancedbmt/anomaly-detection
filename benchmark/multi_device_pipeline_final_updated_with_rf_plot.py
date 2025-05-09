import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
from tensorflow.keras.models import load_model  # type: ignore
import matplotlib.pyplot as plt
import time
import psutil

# ==== CONFIGURATION ====
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEVICES_DATA_PATH = os.path.join(BASE_DIR, "..", "src", "devices_data")
SAVED_MODELS_PATH = os.path.join(BASE_DIR, "..", "test_cases", "saved_models")

EXCLUDE_COLUMNS = ['timestamp', 'state', 'reconstruction_error', 'is_anomaly', 'label']
SEQUENCE_LENGTH = 30
ANOMALY_PERCENTILE = 99.5
MIN_ANOMALY_DURATION = 3
ERROR_SMOOTHING_SPAN = 5

# ==== DEVICE MODEL UTILS ====
def get_model_name(device_type, state):
    if device_type == 'bale_counter':
        return f"lstm_{state}_bale_counter.h5"
    elif device_type == 'temperature_sensor':
        return f"lstm_{state}_temperature_sensor.h5"
    elif device_type == 'output_sensor':
        return f"lstm_{state}.h5"
    else:
        return f"lstm_{state}.h5"

def get_rf_model_name(device_type):
    if device_type == 'bale_counter':
        return "random_forest_bale.pkl"
    elif device_type == 'output_sensor':
        return "random_forest_output_sensor.pkl"
    elif device_type == 'temperature_sensor':
        return "random_forest_temperature_sensor.pkl"
    elif device_type == 'motor_monitor':
        return "random_forest_motor_monitor.pkl"
    return None

def get_device_files():
    files = []
    for f in os.listdir(DEVICES_DATA_PATH):
        if f.endswith("_unified.csv"):
            device = f.split("_")[0] + "_" + f.split("_")[1]
            if device != "hatch_status":
                files.append((device, f))
    return files

def get_numerical_features(df):
    return [col for col in df.columns if col not in EXCLUDE_COLUMNS and pd.api.types.is_numeric_dtype(df[col])]

def create_sequences(data, seq_length=SEQUENCE_LENGTH):
    return np.array([data.iloc[i:i + seq_length].values for i in range(len(data) - seq_length)])

# ==== RANDOM FOREST ====
def apply_random_forest(df, device_type):
    model_name = get_rf_model_name(device_type)
    if not model_name:
        print(f"⚠️ No RF model name defined for {device_type}.")
        return df

    model_path = os.path.join(SAVED_MODELS_PATH, model_name)
    if not os.path.exists(model_path):
        print(f"⚠️ RF model not found for {device_type}.")
        return df

    rf = joblib.load(model_path)
    features = get_numerical_features(df)
    if not features:
        print(f"⚠️ No features to classify for {device_type}.")
        return df

    df['rf_prediction'] = rf.predict(df[features])
    return df

# ==== THRESHOLD + ANOMALY ====
def calculate_dynamic_threshold(errors, window_size=100, n_sigma=3):
    rolling_mean = pd.Series(errors).rolling(window=window_size, min_periods=1).mean()
    rolling_std = pd.Series(errors).rolling(window=window_size, min_periods=1).std()
    return rolling_mean + n_sigma * rolling_std

def enforce_min_anomaly_duration(flags, min_duration):
    idx = np.where(flags)[0]
    if len(idx) == 0: return flags
    groups = np.split(idx, np.where(np.diff(idx) != 1)[0] + 1)
    for g in groups:
        if len(g) < min_duration:
            flags[g] = False
    return flags

# ==== LSTM DETECTION ====
def detect_state_anomalies(df_state, model_path, feature_cols):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df_state[feature_cols])
    model = load_model(model_path, compile=False)

    if scaled.shape[1] != model.input_shape[-1]:
        print(f"⚠️ Model input mismatch for {model_path}.")
        return df_state

    sequences = create_sequences(pd.DataFrame(scaled))
    reconstructions = model.predict(sequences)

    errors = np.mean((reconstructions - sequences[:, -reconstructions.shape[1]:, :])**2, axis=(1, 2))
    errors = pd.Series(errors).ewm(span=ERROR_SMOOTHING_SPAN).mean().values

    threshold = np.percentile(errors, ANOMALY_PERCENTILE)
    flags = errors > threshold
    flags = enforce_min_anomaly_duration(flags, MIN_ANOMALY_DURATION)

    mask = np.array([False] * len(df_state))
    mask[SEQUENCE_LENGTH:len(errors) + SEQUENCE_LENGTH] = flags

    df_state['reconstruction_error'] = [0.0] * SEQUENCE_LENGTH + errors.tolist()
    df_state['is_anomaly'] = mask
    return df_state

# ==== PLOT LSTM VS RF ====
def plot_lstm_vs_rf(df, device_type, suppress_plot=False):
    if suppress_plot: return  # 👈 skip visualization
    plt.figure(figsize=(14, 6))
    plt.step(df['timestamp'], df.get('is_anomaly', 0), where='post', label='LSTM', alpha=0.7)
    if 'rf_prediction' in df:
        rf_pred = pd.to_numeric(df["rf_prediction"], errors="coerce").fillna(0)
        plt.step(df['timestamp'], rf_pred + 0.05, where='post', label='RF +0.05', alpha=0.7)
        plt.scatter(df[df['rf_prediction'] == 1]['timestamp'], [1.05]*len(df[df['rf_prediction'] == 1]),
                    color='black', marker='x', s=50, label='RF Anomaly')
    if 'is_anomaly' in df:
        plt.scatter(df[df['is_anomaly'] == 1]['timestamp'], df[df['is_anomaly'] == 1]['is_anomaly'],
                    color='black', marker='o', s=50, label='LSTM Anomaly')
    plt.title(f"{device_type} - LSTM vs RF")
    plt.xlabel("Timestamp")
    plt.ylabel("Anomaly")
    plt.yticks([0, 1, 1.05])
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    # plt.show()

# ==== MAIN PROCESS FUNCTION ====
def process_device(device_type, csv_file, suppress_plot=False):
    print(f"\n{'='*50}\nProcessing device: {device_type}\n{'='*50}")
    start = time.time()

    try:
        df = pd.read_csv(os.path.join(DEVICES_DATA_PATH, csv_file))
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        features = get_numerical_features(df)
        if not features:
            print(f"⚠️ No numeric features in {device_type}")
            return None

        df_all = pd.DataFrame()

        for state in df['state'].unique():
            model_path = os.path.join(SAVED_MODELS_PATH, get_model_name(device_type, state))
            if not os.path.exists(model_path):
                print(f"⚠️ Missing model: {model_path}")
                continue

            df_state = df[df['state'] == state].copy()
            df_state = detect_state_anomalies(df_state, model_path, features)

            if 'reconstruction_error' in df_state.columns:
                df_all = pd.concat([df_all, df_state])

        if df_all.empty:
            return None

        df_all = df_all.sort_values('timestamp').reset_index(drop=True)
        df_all = apply_random_forest(df_all, device_type)

        plot_lstm_vs_rf(df_all, device_type, suppress_plot=suppress_plot)

        print(f"⏱️ Finished {device_type} in {time.time() - start:.2f} seconds")
        return df_all

    except Exception as e:
        print(f"❌ Error in {device_type}: {str(e)}")
        return None

# Optional direct run for dev/testing
if __name__ == "__main__":
    for device_type, csv_file in get_device_files():
        process_device(device_type, csv_file, suppress_plot=True)
