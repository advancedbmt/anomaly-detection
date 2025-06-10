import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# Paths (adjust for your system)
DATA_PATH = "C:/Users/Thomas/testCase/src/devices_data/"
MODEL_PATH = "C:/Users/Thomas/testCase/test_cases/saved_models/"

# Match the real file names
TARGET_DEVICES = [
    "motor_monitor_0",
    "output_sensor_0",
    "temperature_sensor_0",
    "bale_counter_0"
]

DROP_COLS = ['timestamp', 'state', 'reconstruction_error', 'is_anomaly', 'label', 'rf_prediction']

def get_feature_columns(df):
    return [col for col in df.columns if col not in DROP_COLS and pd.api.types.is_numeric_dtype(df[col])]

def get_rf_model_name(device_type):
    return f"random_forest_{device_type.replace('_0', '')}.pkl"  # Strip _0 for model name

def train_rf_for_device(device_type):
    file_path = os.path.join(DATA_PATH, f"{device_type}_unified.csv")
    if not os.path.exists(file_path):
        print(f"❌ File not found for {device_type}")
        return

    df = pd.read_csv(file_path)
    feature_cols = get_feature_columns(df)
    if not feature_cols:
        print(f"⚠️ No valid features for {device_type}. Skipping.")
        return

    X = df[feature_cols]
    y = df['label'] if 'label' in df.columns else df['is_anomaly']

    print(f"🔁 Training RF for {device_type} with {len(X)} samples and {len(feature_cols)} features")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)

    os.makedirs(MODEL_PATH, exist_ok=True)
    model_file = os.path.join(MODEL_PATH, get_rf_model_name(device_type))
    joblib.dump(clf, model_file)
    print(f"✅ Saved model to {model_file}")

def main():
    for device in TARGET_DEVICES:
        train_rf_for_device(device)

if __name__ == "__main__":
    main()
