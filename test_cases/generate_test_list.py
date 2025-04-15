import random
import json
from datetime import datetime, timedelta
import os

def generate_random_time(start_date, start_hour=8, end_hour=18):
    """
    Generate a random ISO timestamp between start_hour and end_hour.
    """
    random_hour = random.randint(start_hour, end_hour)
    random_minute = random.randint(0, 59)
    random_time = datetime(start_date.year, start_date.month, start_date.day, random_hour, random_minute)
    return random_time.strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_motor_monitor_tests():
    """
    Create a randomized test list for motor_monitor sensor anomalies.
    """
    today = datetime(2025, 4, 7)
    test_list = []

    # Sensor types and normal ranges for motor_monitor
    sensors = {
        "temperature": (60, 125),  # Normal range
        "vibration": (5, 105),
        "rpm": (0, 160),
        "power": (0, 150)
    }

    # Number of test cases to generate (between 5 and 10)
    num_tests = random.randint(5, 10)

    for _ in range(num_tests):
        sensor = random.choice(list(sensors.keys()))
        value_range = sensors[sensor]
        is_anomaly = random.choice([0, 1])  # Randomly label as anomaly or not

        # Generate values based on anomaly label
        if is_anomaly:
            anomaly_value = round(random.uniform(value_range[1] * 0.95, value_range[1] * 1.1), 1)
        else:
            anomaly_value = round(random.uniform(value_range[0], value_range[1] * 0.85), 1)

        test = {
            "name": f"{'Anomaly' if is_anomaly else 'Normal'} - {sensor}",
            "sensor": sensor,
            "expected_label": is_anomaly,
            "HappenTime": generate_random_time(today),
            "Value": anomaly_value
        }

        test_list.append(test)

    random.shuffle(test_list)
    return test_list


if __name__ == "__main__":
    test_list = generate_motor_monitor_tests()

    # Ensure directory exists
    output_dir = os.path.join("json_folder", "json_test_lists")
    os.makedirs(output_dir, exist_ok=True)

    # Output file path
    output_path = os.path.join(output_dir, "motor_monitor_tests.json")

    # Save to JSON
    with open(output_path, "w") as f:
        json.dump(test_list, f, indent=2)

    print(f"✅ New motor monitor test list saved to: {output_path}")
