import os
import pandas as pd
from config import SAVED_MODELS_PATH
from device_utils import get_model_name, get_numerical_features
from state_anomaly import detect_state_anomalies
from export_json import export_incident_json


def process_device_query(device_type: str, df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Process a device's time-series DataFrame and apply anomaly detection.

    Parameters:
    - device_type: device name (used for model naming, etc.)
    - df_raw: time-series DataFrame (e.g., from get_motor_timeseries)
    """
    print(f"\n{'=' * 50}")
    print(f"Processing device: {device_type}")
    print(f"{'=' * 50}\n")

    device_start_time = pd.Timestamp.now()
    df_all = pd.DataFrame()

    try:
        df = df_raw.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        available_features = get_numerical_features(df)

        if not available_features:
            print(f"⚠️ {device_type} - No numeric features detected.")
            return None

        print(f"{device_type} - Auto-detected features: {available_features}")

        for state in df['state'].unique():
            model_name = get_model_name(device_type, state)
            model_path = os.path.join(SAVED_MODELS_PATH, model_name)

            if not os.path.exists(model_path):
                print(f"⚠️ Missing model for {device_type} state: {state}")
                continue

            df_state = df[df['state'] == state].copy()
            df_processed = detect_state_anomalies(df_state, model_path, available_features)

            if 'reconstruction_error' in df_processed.columns:
                df_all = pd.concat([df_all, df_processed], ignore_index=True)
            else:
                print(f"⚠️ {device_type} - State {state} processed, but 'reconstruction_error' column is missing.")

        if df_all.empty:
            print(f"⚠️ {device_type} - No data processed for any state.")
            return None

        df_all.sort_values('timestamp', inplace=True)
        df_all.reset_index(drop=True, inplace=True)

        print(f"\n--- DEBUG: {device_type} is_anomaly counts BEFORE JSON export ---")
        if 'is_anomaly' in df_all.columns:
            print(df_all['is_anomaly'].value_counts())
        else:
            print("'is_anomaly' column not found in df_all!")

        export_incident_json(df_all, device_type)

        print(f"✅ Finished {device_type} in {(pd.Timestamp.now() - device_start_time).total_seconds():.2f} sec")
        return df_all

    except Exception as e:
        print(f"❌ Error processing {device_type}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
