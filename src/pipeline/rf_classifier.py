import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from config import SAVED_MODELS_PATH
from device_utils import get_rf_model_name, get_numerical_features

def apply_random_forest(df, device_type):
    """
    Apply trained Random Forest classifier to classify time steps.
    """
    model_name = get_rf_model_name(device_type)
    if not model_name:
        print(f"⚠️ No RF model name defined for {device_type}. Skipping classification.")
        return df

    model_path = os.path.join(SAVED_MODELS_PATH, model_name)
    if not os.path.exists(model_path):
        print(f"⚠️ Random Forest model not found for {device_type}. Skipping classification.")
        return df

    rf = joblib.load(model_path)
    feature_cols = get_numerical_features(df)

    if not feature_cols:
        print(f"⚠️ No features found for {device_type}. Cannot classify.")
        return df

    X = df[feature_cols]
    df['rf_prediction'] = rf.predict(X)
    return df

def train_rf_for_device(device_name, df):
    """
    Train and save Random Forest model using is_anomaly or label column.
    """
    feature_cols = get_numerical_features(df)
    if not feature_cols:
        print(f"⚠️ No features available to train RF for {device_name}.")
        return

    X = df[feature_cols]
    y = df['is_anomaly'].astype(int) if 'is_anomaly' in df.columns else df['label']

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)

    model_filename = f"random_forest_{device_name}.pkl"
    save_path = os.path.join(SAVED_MODELS_PATH, model_filename)
    joblib.dump(rf, save_path)

    print(f"✅ RF model saved at {save_path} for {device_name}")
