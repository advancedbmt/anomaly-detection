import os
import time
import pandas as pd
from benchmark_utils import benchmark_device
from multi_device_pipeline_final_updated_with_rf_plot import process_device

# ⚙️ Updated test cases with temperature sensor included
TEST_CASES = [
    {"test_id": 1, "motor": 1, "bale": 1, "pump": 1, "temp": 1, "interval": 0.1, "duration_min": 0.1},
    {"test_id": 2, "motor": 3, "bale": 1, "pump": 3, "temp": 3, "interval": 0.1, "duration_min": 0.1}
]

# 📂 Unified CSV filenames
DEVICE_FILE_MAP = {
    "motor_monitor": "motor_monitor_0_unified.csv",
    "bale_counter": "bale_counter_0_unified.csv",
    "output_sensor": "output_sensor_0_unified.csv",
    "temperature_sensor": "temperature_sensor_0_unified.csv"
}

# 🧠 Caches
CSV_CACHE = {}
MODEL_CACHE = {}

BASE_DIR = os.path.dirname(__file__)
DEVICES_DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, "../src/devices_data"))

def process_device_with_cache(device_type, csv_file):
    # ✅ Load and cache CSV once
    if csv_file not in CSV_CACHE:
        full_path = os.path.join(DEVICES_DATA_PATH, csv_file)
        print(f"📄 Loading CSV: {full_path}")
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"❌ File not found: {full_path}")
        df = pd.read_csv(full_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        CSV_CACHE[csv_file] = df

    # ✅ Placeholder for future model preloading
    if device_type not in MODEL_CACHE:
        MODEL_CACHE[device_type] = {}

    return process_device(device_type, csv_file, suppress_plot=True)

def run_test_case(test):
    print(f"\n=== Running Test Case #{test['test_id']} ===")
    total_ticks = int((test["duration_min"] * 60) / test["interval"])

    for tick in range(total_ticks):
        print(f"\n⏱️ Tick {tick + 1}/{total_ticks}")
        tick_start = time.time()

        for device_type in DEVICE_FILE_MAP:
            # Map device_type to test dictionary key (motor, bale, pump, temp)
            short_key = {
                "motor_monitor": "motor",
                "bale_counter": "bale",
                "output_sensor": "pump",
                "temperature_sensor": "temp"
            }[device_type]

            count = test.get(short_key, 0)
            csv_file = DEVICE_FILE_MAP[device_type]

            for i in range(count):
                start = time.time()

                benchmark_device(
                    device_type=device_type,
                    csv_file=csv_file,
                    process_fn=process_device_with_cache,
                    dry_run=False,
                    test_case_id=test["test_id"]
                )

                elapsed = time.time() - start
                print(f"⏳ {device_type} call {i + 1}/{count} took {elapsed:.2f} sec")

        # ⏱️ Keep tick interval constant
        tick_elapsed = time.time() - tick_start
        if tick_elapsed < test["interval"]:
            time.sleep(test["interval"] - tick_elapsed)

    print(f"\n✅ Test Case #{test['test_id']} completed.\n")

def main():
    for test in TEST_CASES:
        run_test_case(test)

if __name__ == "__main__":
    main()
