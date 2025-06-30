import os
import json
import pandas as pd
from datetime import datetime
from config import BASE_DIR, EXCLUDE_COLUMNS

EXPORT_PATH = os.path.join(BASE_DIR, "data/anomalies_output.json")

def export_incident_json(df, device_type):
    """
    Export all processed records per device, including sensor features,
    reconstruction error, is_anomaly flags, and error percentile for use by
    downstream systems (Incident Classification).
    """
    if 'timestamp' not in df.columns:
        print(f"❌ Cannot export JSON for {device_type}: Missing 'timestamp' column.")
        return

    # Ensure required columns exist for export
    error_col_name = None
    if 'reconstruction_error' in df.columns:
        error_col_name = 'reconstruction_error'
    elif 'error' in df.columns: # Fallback if col name changed
        error_col_name = 'error'
    else:
        print(f"⚠️ Warning: Neither 'error' nor 'reconstruction_error' column found in df for {device_type}. Exporting without error scores.")

    if 'is_anomaly' not in df.columns:
        print(f"⚠️ Warning: 'is_anomaly' column not found in df for {device_type}. Exporting without LSTM anomaly flags.")
    
    # ✅ NEW: Check for error_percentile column
    if 'error_percentile' not in df.columns:
        print(f"⚠️ Warning: 'error_percentile' column not found in df for {device_type}. Exporting without anomaly probability.")


    incidents = []
    for _, row in df.iterrows(): # Iterate over ALL rows
        # Dynamically determine features to export, excluding those in EXCLUDE_COLUMNS
        actual_exclude_cols = [col for col in EXCLUDE_COLUMNS if col in df.columns]

        features = {
            col: row[col]
            for col in df.columns
            if col not in actual_exclude_cols and pd.api.types.is_numeric_dtype(df[col])
            and col not in [error_col_name, 'is_anomaly', 'error_percentile'] # Exclude new percentile from features
        }

        incidents.append({
            "device": device_type,
            "timestamp": row['timestamp'].isoformat() if isinstance(row['timestamp'], pd.Timestamp) else str(row['timestamp']),
            "error": row.get(error_col_name) if error_col_name else None,
            "state": row.get('state'),
            "is_anomaly": row.get('is_anomaly', False),
            "error_percentile": row.get('error_percentile', 0.0), # ✅ NEW: Export error percentile
            "features": features
        })

    export_data = {device_type: incidents}

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