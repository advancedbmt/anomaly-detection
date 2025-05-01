# benchmark/benchmark_runner.py

import os
from benchmark_utils import benchmark_device
from multi_device_pipeline_final_updated_with_rf_plot import process_device


# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEVICES_DATA_PATH = os.path.join(BASE_DIR, "..", "src", "devices_data")
SUPPORTED_SUFFIX = "_unified.csv"

def get_all_unified_device_files():
    """
    Scans the devices_data folder for *_unified.csv files.
    Skips 'hatch_status' because it's not modeled.
    Returns list of (device_type, filename) tuples.
    """
    device_files = []
    for filename in os.listdir(DEVICES_DATA_PATH):
        if filename.endswith(SUPPORTED_SUFFIX):
            parts = filename.split('_')
            device_type = parts[0] + '_' + parts[1]  # e.g., motor_monitor
            if device_type == "hatch_status":
                continue
            device_files.append((device_type, filename))
    return device_files

def main():
    print("🚀 Starting benchmark for anomaly detection pipeline...\n")

    device_files = get_all_unified_device_files()

    if not device_files:
        print("❌ No unified device files found in:", DEVICES_DATA_PATH)
        return

    for device_type, csv_file in device_files:
        print(f"📦 Running benchmark for: {device_type} -> {csv_file}")
        try:
            benchmark_device(
                device_type=device_type,
                csv_file=csv_file,
                process_device_func=process_device
            )
        except Exception as e:
            print(f"❌ Failed to benchmark {device_type}: {str(e)}")

    print("\n✅ Benchmark completed! Metrics saved to: benchmark_metrics.csv")

if __name__ == "__main__":
    main()
