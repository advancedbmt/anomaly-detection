# This dictionary holds the expected anomaly timestamps for each sensor in each file.
# It is manually created based on the known injected anomalies from synthetic_config.json.

expected_results = {
    "motor_monitor_synthetic.csv": {
        "temperature": ["2025-04-07 10:15", "2025-04-07 10:16"],
        "rpm": ["2025-04-07 15:00", "2025-04-07 15:01"]
    },
    "bale_counter_synthetic.csv": {
        "total_weight": ["2025-04-07 14:00"],
        "bales": ["2025-04-07 20:30"]
    },
    "temperature_bank_synthetic.csv": {
        "temperatureSensor1": ["2025-04-07 13:00", "2025-04-07 16:45"]
    }
}
