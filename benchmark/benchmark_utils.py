import time
import psutil
import csv
import os
from datetime import datetime

BENCHMARK_CSV_PATH = os.path.join(os.path.dirname(__file__), "benchmark_metrics.csv")

def benchmark_device(device_type, csv_file, process_fn, dry_run=False):
    """
    Benchmark the time, CPU, memory usage for processing a device.
    
    Parameters:
        device_type (str): Name of the device type.
        csv_file (str): Path to the CSV file.
        process_fn (function): Function that processes the device.
        dry_run (bool): If True, skips processing for speed testing.
    """
    start_time = time.time()
    
    # Capture memory and CPU usage before
    cpu_before = psutil.cpu_percent(interval=0.1)
    mem_before = psutil.virtual_memory().used / (1024 * 1024)  # in MB

    if not dry_run:
        process_fn(device_type, csv_file)

    # Capture memory and CPU usage after
    end_time = time.time()
    cpu_after = psutil.cpu_percent(interval=0.1)
    mem_after = psutil.virtual_memory().used / (1024 * 1024)

    inference_time_ms = (end_time - start_time) * 1000
    avg_cpu = (cpu_before + cpu_after) / 2
    mem_used = mem_after

    print(f"✅ Finished {device_type} | {inference_time_ms:.2f} ms | CPU: {avg_cpu:.1f}% | Mem: {mem_used:.2f} MB")

    # Log to CSV
    log_benchmark_metric({
        "timestamp": datetime.now().isoformat(),
        "device_type": device_type,
        "csv_file": csv_file,
        "inference_time_ms": round(inference_time_ms, 2),
        "cpu_percent": round(avg_cpu, 2),
        "memory_mb": round(mem_used, 2),
        "disk_read_mb": 0.0,  # Optional: implement if needed
        "disk_write_mb": 0.0
    })

def log_benchmark_metric(metric_row):
    file_exists = os.path.exists(BENCHMARK_CSV_PATH)
    with open(BENCHMARK_CSV_PATH, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=metric_row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(metric_row)
