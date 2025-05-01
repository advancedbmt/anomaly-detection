# benchmark/generate_benchmark_summary.py

import pandas as pd
import os

# Adjust path if needed
BASE_DIR = os.path.dirname(__file__)
input_path = os.path.join(BASE_DIR, "benchmark_metrics_clean.csv")
output_path = os.path.join(BASE_DIR, "benchmark_summary.csv")

# Load cleaned metrics
df = pd.read_csv(input_path)

# Convert types
df['test_case_id'] = pd.to_numeric(df['test_case_id'], errors='coerce')
df['inference_time_ms'] = pd.to_numeric(df['inference_time_ms'], errors='coerce')
df['cpu_percent'] = pd.to_numeric(df['cpu_percent'], errors='coerce')
df['memory_mb'] = pd.to_numeric(df['memory_mb'], errors='coerce')
df['disk_read_mb'] = pd.to_numeric(df['disk_read_mb'], errors='coerce')
df['disk_write_mb'] = pd.to_numeric(df['disk_write_mb'], errors='coerce')

# Group and summarize
summary = df.groupby(['test_case_id', 'device_type']).agg({
    'inference_time_ms': ['mean', 'median', 'max', 'min', 'std'],
    'cpu_percent': ['mean', 'median', 'max', 'min', 'std'],
    'memory_mb': ['mean', 'median', 'max', 'min', 'std'],
    'disk_read_mb': ['mean', 'median', 'max', 'min', 'std'],
    'disk_write_mb': ['mean', 'median', 'max', 'min', 'std']
}).reset_index()

# Flatten column names
summary.columns = ['_'.join(col).strip('_') for col in summary.columns.values]

# Save to CSV
summary.to_csv(output_path, index=False)
print(f"✅ Benchmark summary saved to: {output_path}")
