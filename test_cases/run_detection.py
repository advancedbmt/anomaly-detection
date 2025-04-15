import pandas as pd
from sklearn.ensemble import IsolationForest

# Load synthetic data
df = pd.read_csv("motor_monitor_synthetic.csv")

# === Preprocessing ===
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.dropna()

# Convert states to numeric if needed
if "state" in df.columns:
    df["state_code"] = df["state"].astype("category").cat.codes
else:
    df["state_code"] = 0

# === Prepare features ===
features = df[["feature_0", "state_code"]]

# === Anomaly Detection Model ===
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
df["predicted_anomaly"] = model.fit_predict(features)

# Convert -1 to 1 (anomaly), 1 to 0 (normal)
df["predicted_anomaly"] = df["predicted_anomaly"].map({-1: 1, 1: 0})

# === Save output for evaluation ===
predicted_anomalies = df[["timestamp", "predicted_anomaly"]]
