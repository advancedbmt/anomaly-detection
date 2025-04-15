import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report

def evaluate_device(device_name):
    expected_path = f"TESTCASE/expected/{device_name}_expected.csv"
    predicted_path = f"TESTCASE/results/{device_name}_predicted.csv"

    expected = pd.read_csv(expected_path)
    predicted = pd.read_csv(predicted_path)

    # Merge on timestamp and sensor
    merged = pd.merge(expected, predicted, on=["timestamp", "sensor"])

    y_true = merged["is_anomaly"]
    y_pred = merged["is_anomaly_pred"]

    print(f"\n📊 Evaluation for device: {device_name}")
    print(confusion_matrix(y_true, y_pred))
    print(classification_report(y_true, y_pred, digits=3))

# Example usage
if __name__ == "__main__":
    evaluate_device("motor_monitor")
