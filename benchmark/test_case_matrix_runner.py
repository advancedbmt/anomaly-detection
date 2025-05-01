
import time
from benchmark_utils import benchmark_device
from multi_device_pipeline_final_updated_with_rf_plot import process_device

# Mapping test cases from the streaming benchmark table
TEST_CASES = [
    {"test_id": 1, "motor": 1, "bale": 1, "pump": 1, "interval": 1, "duration_min": 5},
    {"test_id": 2, "motor": 10, "bale": 1, "pump": 10, "interval": 1, "duration_min": 5},
    {"test_id": 3, "motor": 25, "bale": 1, "pump": 25, "interval": 1, "duration_min": 5},
    {"test_id": 4, "motor": 50, "bale": 1, "pump": 50, "interval": 1, "duration_min": 5},
    {"test_id": 5, "motor": 75, "bale": 1, "pump": 75, "interval": 1, "duration_min": 5},
    {"test_id": 6, "motor": 100, "bale": 1, "pump": 100, "interval": 1, "duration_min": 5},
    {"test_id": 7, "motor": 50, "bale": 1, "pump": 50, "interval": 5, "duration_min": 10},
    {"test_id": 8, "motor": 50, "bale": 1, "pump": 50, "interval": 10, "duration_min": 15},
    {"test_id": 9, "motor": 50, "bale": 1, "pump": 50, "interval": 15, "duration_min": 20},
]

# These filenames must exist in your src/devices_data folder
MOTOR_FILE = "motor_monitor_0_unified.csv"
BALE_FILE = "bale_counter_0_unified.csv"
PUMP_FILE = "output_sensor_0_unified.csv"

def run_test_case(test):
    print(f"\n=== Running Test Case #{test['test_id']} ===")
    device_map = {
        "motor_monitor": (MOTOR_FILE, test["motor"]),
        "bale_counter": (BALE_FILE, test["bale"]),
        "output_sensor": (PUMP_FILE, test["pump"])
    }
    total_runs = test["duration_min"] * 60 // test["interval"]

    for tick in range(total_runs):
        print(f"⏱️ Tick {tick + 1}/{total_runs}")
        for device_type, (file, count) in device_map.items():
            for i in range(count):
                benchmark_device(device_type, file, process_device)
        time.sleep(test["interval"])

    print(f"✅ Test Case #{test['test_id']} completed.\n")

def main():
    for test in TEST_CASES:
        run_test_case(test)

if __name__ == "__main__":
    main()
