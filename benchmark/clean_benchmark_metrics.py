import os
import pandas as pd

# 📂 Path to the raw benchmark CSV
BASE_DIR = os.path.dirname(__file__)
csv_path = os.path.join(BASE_DIR, "benchmark_metrics.csv")

# 🧹 Step 1: Read the raw CSV and filter out malformed rows
cleaned_rows = []
expected_columns = None
malformed_count = 0

with open(csv_path, "r") as f:
    for line in f:
        parts = line.strip().split(",")
        if expected_columns is None:
            expected_columns = len(parts)
            cleaned_rows.append(parts)  # header
        elif len(parts) == expected_columns:
            cleaned_rows.append(parts)
        else:
            malformed_count += 1

print(f"⚠️ Skipped {malformed_count} malformed rows.")

# 🧱 Step 2: Create DataFrame from filtered rows
df_clean = pd.DataFrame(cleaned_rows[1:], columns=cleaned_rows[0])

# 🔢 Step 3: Convert numeric fields safely
numeric_fields = [
    "inference_time_ms",
    "cpu_percent",
    "memory_mb",
    "disk_read_mb",
    "disk_write_mb",
    "test_case_id"
]
for col in numeric_fields:
    if col in df_clean.columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

# 💾 Step 4: Save cleaned data
clean_path = os.path.join(BASE_DIR, "benchmark_metrics_clean.csv")
df_clean.to_csv(clean_path, index=False)
print(f"✅ Cleaned CSV saved as '{clean_path}'")

# 📊 Step 5: Generate summary statistics
if "test_case_id" in df_clean.columns and "device_type" in df_clean.columns:
    summary = df_clean.groupby(["test_case_id", "device_type"]).agg({
        "inference_time_ms": ["mean", "median", "max", "min", "std"],
        "cpu_percent": ["mean", "median", "max", "min", "std"],
        "memory_mb": ["mean", "median", "max", "min", "std"],
        "disk_read_mb": ["mean", "median", "max", "min", "std"],
        "disk_write_mb": ["mean", "median", "max", "min", "std"]
    }).reset_index()

    # Flatten column names
    summary.columns = ['_'.join(col).strip('_') for col in summary.columns.values]

    # Save summary
    summary_path = os.path.join(BASE_DIR, "benchmark_summary.csv")
    summary.to_csv(summary_path, index=False)
    print(f"📈 Summary saved as '{summary_path}'")

# ✅ Step 6: Check for missing device types
expected_devices = {"motor_monitor", "bale_counter", "output_sensor", "temperature_sensor"}
present_devices = set(df_clean["device_type"].dropna().unique())
missing = expected_devices - present_devices

if missing:
    print(f"⚠️ Missing device types in cleaned data: {', '.join(missing)}")
else:
    print("✅ All expected device types are present in the cleaned metrics.")
