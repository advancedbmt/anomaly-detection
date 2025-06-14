import os
import json
import pandas as pd
from datetime import datetime
from config import BASE_DIR, EXCLUDE_COLUMNS # Ensure EXCLUDE_COLUMNS is the one from the new config

EXPORT_PATH = os.path.join(BASE_DIR, "data/anomalies_output.json")

def export_incident_json(df, device_type):
    """
    Export all processed records per device, including sensor features,
    reconstruction error, and is_anomaly flags for use by any downstream system
    (formerly Incident Classification).
    """
    if 'timestamp' not in df.columns:
        print(f"❌ Cannot export JSON for {device_type}: Missing 'timestamp' column.")
        return

    # Ensure 'reconstruction_error' and 'is_anomaly' columns exist.
    if 'reconstruction_error' not in df.columns:
        print(f"⚠️ Warning: 'reconstruction_error' column not found in df for {device_type}. Exporting without error scores.")
        error_col_name = None
    else:
        error_col_name = 'reconstruction_error'

    if 'is_anomaly' not in df.columns:
        print(f"⚠️ Warning: 'is_anomaly' column not found in df for {device_type}. Exporting without LSTM anomaly flags.")

    incidents = []
    for _, row in df.iterrows(): # Iterate over ALL rows to export complete time series
        # Dynamically determine features to export, excluding those in EXCLUDE_COLUMNS
        # and also outputs like error/is_anomaly
        features = {
            col: row[col]
            for col in df.columns
            if col not in EXCLUDE_COLUMNS and pd.api.types.is_numeric_dtype(df[col])
            and col not in [error_col_name, 'is_anomaly'] # Ensure error and anomaly flag are not treated as features
        }

        incidents.append({
            "device": device_type,
            "timestamp": row['timestamp'].isoformat() if isinstance(row['timestamp'], pd.Timestamp) else str(row['timestamp']),
            "error": row.get(error_col_name) if error_col_name else None, # Map 'reconstruction_error' to 'error' key
            "state": row.get('state'),
            "is_anomaly": row.get('is_anomaly', False), # Include LSTM's is_anomaly
            "features": features
        })

    export_data = {device_type: incidents}

    # Merge with existing file content if it exists
    if os.path.exists(EXPORT_PATH):
        try:
            with open(EXPORT_PATH, 'r') as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Existing JSON file at {EXPORT_PATH} is corrupted. Overwriting.")
            existing_data = {}

        existing_data[device_type] = incidents
    else:
        existing_data = export_data

    with open(EXPORT_PATH, 'w') as f:
        json.dump(existing_data, f, indent=2)

    print(f"📤 Exported {len(incidents)} records for {device_type} to JSON")