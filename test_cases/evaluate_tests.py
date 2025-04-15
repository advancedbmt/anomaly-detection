# This script compares the actual detected anomalies with expected ones.
# It evaluates precision, recall, F1-score and shows a confusion matrix for each sensor.

import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report

# Import expected and actual results from the other test case files
from test_cases import expected_outputs, run_detection

# List of synthetic files to evaluate
CSV_FILES = [
    "motor_monitor_synthetic.csv",
    "bale_counter_synthetic.csv",
    "temperature_bank_synthetic.csv"
]

# Load expected and actual results
actual_results = run_detection.actual_results
expected_results = expected_outputs.expected_results

# This dictionary will store evaluation report for each device and sensor
evaluation_summary = {}

# Iterate through each file and compare actual vs expected
for file_name in CSV_FILES:
    # Skip files missing from either dict
    if file_name not in expected_results or file_name not in actual_results:
        continue

    expected = expected_results[file_name]
    actual = actual_results[file_name]

    file_report = {}

    for sensor_name in expected:
        # Convert timestamps to datetime objects and round to minute
        expected_times = expected.get(sensor_name, [])
        actual_times = actual.get(sensor_name, [])

        expected_set = set(pd.to_datetime(expected_times).round("min"))
        actual_set = set(pd.to_datetime(actual_times).round("min"))

        # Create a unified list of timestamps
        all_times = sorted(expected_set.union(actual_set))

        # Create binary vectors: 1 = anomaly, 0 = normal
        y_true = [1 if t in expected_set else 0 for t in all_times]
        y_pred = [1 if t in actual_set else 0 for t in all_times]

        if not y_true:
            continue

        # Compute confusion matrix and classification report
        cm = confusion_matrix(y_true, y_pred)
        report = classification_report(y_true, y_pred, output_dict=True)

        file_report[sensor_name] = {
            "confusion_matrix": cm.tolist(),
            "precision": round(report['1']['precision'], 2),
            "recall": round(report['1']['recall'], 2),
            "f1_score": round(report['1']['f1-score'], 2)
        }

    # Store per file
    evaluation_summary[file_name] = file_report

# Pretty print the results
import json
print(json.dumps(evaluation_summary, indent=4))


#timestamp
#feature_0
#sensor
#state