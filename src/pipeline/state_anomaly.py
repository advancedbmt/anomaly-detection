import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from config import SEQUENCE_LENGTH, ANOMALY_PERCENTILE, ERROR_SMOOTHING_SPAN, MIN_ANOMALY_DURATION
from device_utils import get_numerical_features

def create_sequences(data, seq_length=SEQUENCE_LENGTH):
    """
    Create rolling sequences of data for LSTM input.
    """
    return np.array([data.iloc[i:i + seq_length].values for i in range(len(data) - seq_length)])

def calculate_dynamic_threshold(errors, window_size=100, n_sigma=3):
    """
    Calculate dynamic threshold using rolling stats.
    (Currently not used in detect_state_anomalies, but defined here.)
    """
    errors_series = pd.Series(errors)
    rolling_mean = errors_series.rolling(window=window_size, min_periods=1).mean()
    rolling_std = errors_series.rolling(window=window_size, min_periods=1).std()
    return rolling_mean + n_sigma * rolling_std

# This function definition is intentionally commented out for current diagnosis.
# def enforce_min_anomaly_duration(anomaly_flags, min_duration=MIN_ANOMALY_DURATION):
#     """
#     Ensure anomalies persist for at least N timesteps.
#     """
#     anomaly_indices = np.where(anomaly_flags)[0]
#     if len(anomaly_indices) == 0:
#         return anomaly_flags

#     groups = np.split(anomaly_indices, np.where(np.diff(anomaly_indices) != 1)[0] + 1)
#     for group in groups:
#         if len(group) < min_duration:
#             anomaly_flags[group] = False
#     return anomaly_flags

def detect_state_anomalies(df_state, model_path, feature_cols):
    """
    Run LSTM model on a specific state segment to detect anomalies.
    """
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df_state[feature_cols])

    model = load_model(model_path, compile=False)
    if scaled.shape[1] != model.input_shape[-1]:
        print(f"⚠️ Feature count mismatch: model expects {model.input_shape[-1]}, got {scaled.shape[1]}")
        return df_state

    sequences = create_sequences(pd.DataFrame(scaled))
    reconstructions = model.predict(sequences, verbose=0)

    errors = np.mean((reconstructions - sequences[:, -reconstructions.shape[1]:, :]) ** 2, axis=(1, 2))
    errors = pd.Series(errors).ewm(span=ERROR_SMOOTHING_SPAN).mean().values

    threshold = np.percentile(errors, ANOMALY_PERCENTILE)
    print(f"Threshold for {model_path}: {threshold:.6f} ({ANOMALY_PERCENTILE}th percentile)")

    anomaly_flags = errors > threshold
    print(f"DEBUG: After thresholding, anomaly_flags unique values: {np.unique(anomaly_flags)}")
    print(f"DEBUG: After thresholding, count of True flags: {np.sum(anomaly_flags)}")

    # anomaly_flags = enforce_min_anomaly_duration(anomaly_flags) # This must remain commented out for now.

    flags = np.array([False] * len(df_state))
    flags[SEQUENCE_LENGTH:len(errors) + SEQUENCE_LENGTH] = anomaly_flags

    df_state['reconstruction_error'] = [0.0] * SEQUENCE_LENGTH + errors.tolist()
    df_state['is_anomaly'] = flags

    # ✅ NEW: Calculate error percentile for each error score
    # Normalize error for percentile calculation by using all non-zero errors.
    # We use a large number of bins for better resolution
    if len(errors) > 0 and np.max(errors) > 0:
        # Calculate percentiles relative to the distribution of errors for this state
        error_percentiles = np.array([
            pd.Series(errors).rank(pct=True)[i] * 100
            for i in range(len(errors))
        ])
    else:
        error_percentiles = np.zeros(len(errors))

    # Pad with zeros for the initial SEQUENCE_LENGTH
    padded_percentiles = [0.0] * SEQUENCE_LENGTH + error_percentiles.tolist()
    df_state['error_percentile'] = padded_percentiles[:len(df_state)] # Ensure length matches df_state

    return df_state