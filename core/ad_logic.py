import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from core.config import SEQUENCE_LENGTH, ANOMALY_PERCENTILE, ERROR_SMOOTHING_SPAN
from core.device_utils import get_numerical_features

def create_sequences(data, seq_length=SEQUENCE_LENGTH):
    return np.array([data.iloc[i:i + seq_length].values for i in range(len(data) - seq_length)])

def detect_state_anomalies(df_state, model_path, feature_cols):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df_state[feature_cols])

    model = load_model(model_path, compile=False)
    if scaled.shape[1] != model.input_shape[-1]:
        print(f"⚠️ Model expects {model.input_shape[-1]} features, got {scaled.shape[1]}")
        return df_state

    sequences = create_sequences(pd.DataFrame(scaled))
    reconstructions = model.predict(sequences, verbose=0)
    errors = np.mean((reconstructions - sequences[:, -reconstructions.shape[1]:, :]) ** 2, axis=(1, 2))
    errors = pd.Series(errors).ewm(span=ERROR_SMOOTHING_SPAN).mean().values

    threshold = np.percentile(errors, ANOMALY_PERCENTILE)
    anomaly_flags = errors > threshold
    flags = np.array([False] * len(df_state))
    flags[SEQUENCE_LENGTH:len(errors) + SEQUENCE_LENGTH] = anomaly_flags

    df_state['reconstruction_error'] = [0.0] * SEQUENCE_LENGTH + errors.tolist()
    df_state['is_anomaly'] = flags

    error_percentiles = (
        pd.Series(errors).rank(pct=True).values * 100
        if len(errors) > 0 and np.max(errors) > 0
        else np.zeros(len(errors))
    )
    df_state['error_percentile'] = [0.0] * SEQUENCE_LENGTH + error_percentiles.tolist()

    return df_state
