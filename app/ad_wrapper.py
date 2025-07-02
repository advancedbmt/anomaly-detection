import os
from core.ad_processor import process_device

def run_anomaly_detection(csv_path: str, device_type: str) -> str:
    """
    FastAPI wrapper to run anomaly detection using core pipeline logic.
    Returns name of the exported anomaly JSON file.
    """
    print(f"🔍 Running Anomaly Detection on {csv_path} for device type: {device_type}")

    # Run pipeline – includes plotting and export_json inside
    df_result = process_device(device_type, csv_path)

    # We don't save another output here – it's already handled in export_incident_json
    print(f"✅ Anomaly detection completed for {device_type}")
    return f"{device_type}_anomalies_output.json"
