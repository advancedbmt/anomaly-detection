import os
import pandas as pd
from core.config import BASE_DIR, SAVED_MODELS_PATH
from core.device_utils import get_model_name, get_numerical_features
from core.ad_logic import detect_state_anomalies
from core.plotting import plot_reconstruction_error
from core.export_json import export_incident_json

def process_device(device_type: str, csv_path: str):
    print(f"\n🔍 Processing {device_type} from CSV: {csv_path}")
    df_all = pd.DataFrame()

    try:
        abs_path = os.path.join(BASE_DIR, csv_path)
        df = pd.read_csv(abs_path)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        features = get_numerical_features(df)
        if not features:
            raise ValueError(f"No numeric features for {device_type}")

        for state in df['state'].unique():
            model_path = os.path.join(SAVED_MODELS_PATH, get_model_name(device_type, state))
            if not os.path.exists(model_path):
                print(f"⚠️ Model missing for state: {state}")
                continue
            df_state = df[df['state'] == state].copy()
            df_processed = detect_state_anomalies(df_state, model_path, features)
            if 'reconstruction_error' in df_processed.columns:
                df_all = pd.concat([df_all, df_processed], ignore_index=True)

        if df_all.empty:
            raise ValueError("No state segments were processed")

        df_all.sort_values("timestamp", inplace=True)
        df_all.reset_index(drop=True, inplace=True)

        plot_reconstruction_error(df_all, device_type)
        export_incident_json(df_all, device_type)
        return df_all

    except Exception as e:
        print(f"❌ Error: {e}")
        raise
