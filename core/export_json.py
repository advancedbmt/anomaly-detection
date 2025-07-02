import os
import json
import pandas as pd
from core.config import BASE_DIR, EXCLUDE_COLUMNS   


def export_incident_json(df, device_type):
    if 'timestamp' not in df.columns:
        print(f"❌ Missing 'timestamp' column in {device_type}")
        return

    export_path = os.path.join(BASE_DIR, "outputs", f"{device_type}_anomalies_output.json")

    error_col = 'reconstruction_error' if 'reconstruction_error' in df.columns else 'error'

    incidents = []
    for _, row in df.iterrows():
        features = {
            col: row[col]
            for col in df.columns
            if col not in EXCLUDE_COLUMNS and pd.api.types.is_numeric_dtype(df[col])
        }
        incidents.append({
            "device": device_type,
            "timestamp": row['timestamp'].isoformat() if isinstance(row['timestamp'], pd.Timestamp) else str(row['timestamp']),
            "error": row.get(error_col),
            "state": row.get('state'),
            "is_anomaly": row.get('is_anomaly', False),
            "error_percentile": row.get('error_percentile', 0.0),
            "features": features
        })

    if os.path.exists(export_path):
        with open(export_path, 'r') as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = {}
    else:
        existing = {}

    existing[device_type] = incidents
    with open(export_path, 'w') as f:
        json.dump(existing, f, indent=2)

    print(f"📤 Exported {len(incidents)} records for {device_type} to {export_path}")
