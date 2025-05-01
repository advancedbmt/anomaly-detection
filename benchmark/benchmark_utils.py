# benchmark/benchmark_utils.py

import time
import psutil
import csv
import os
from datetime import datetime

BENCHMARK_CSV_PATH = os.path.join(os.path.dirname(__file__), "benchmark_metrics.csv")

def benchmark_device(device_type, csv_file, process_fn, dry_run=False, test_case_id=None):
    """
    Benchmark the time, CPU, memory, disk usage for processing a device.

    Parameters:
        device_type (str): Name of the device type.
        csv_file (str): Path to the CSV file.
        process_fn (function): Function that processes the device.
        dry_run (bool): If True, skips processing to simulate speed.
        test_case_id (int): ID of the test case for traceability.
    """
    start_time = time.time()

    # Capture memory and CPU before
    cpu_before = psutil.cpu_percent(interval=None)
    mem_before = psutil.virtual_memory().used / (1024 * 1024)  # in MB
    io_before = psutil.disk_io_counters()

    # Run model processing unless dry run
    if not dry_run:
        process_fn(device_type, csv_file)

    # Capture memory and CPU after
    end_time = time.time()
    cpu_after = psutil.cpu_percent(interval=None)
    mem_after = psutil.virtual_memory().used / (1024 * 1024)
    io_after = psutil.disk_io_counters()

    inference_time_ms = (end_time - start_time) * 1000
    avg_cpu = (cpu_before + cpu_after) / 2
    mem_used = mem_after

    disk_read_mb = (io_after.read_bytes - io_before.read_bytes) / (1024 * 1024)
    disk_write_mb = (io_after.write_bytes - io_before.write_bytes) / (1024 * 1024)

    print(f"✅ Finished {device_type} | {inference_time_ms:.2f} ms | CPU: {avg_cpu:.1f}% | Mem: {mem_used:.2f} MB")

    # Save to CSV
    log_benchmark_metric({
        "timestamp": datetime.now().isoformat(),
        "test_case_id": test_case_id,
        "device_type": device_type,
        "csv_file": csv_file,
        "inference_time_ms": round(inference_time_ms, 2),
        "cpu_percent": round(avg_cpu, 2),
        "memory_mb": round(mem_used, 2),
        "disk_read_mb": round(disk_read_mb, 4),
        "disk_write_mb": round(disk_write_mb, 4)
    })

def log_benchmark_metric(metric_row):
    file_exists = os.path.exists(BENCHMARK_CSV_PATH)
    with open(BENCHMARK_CSV_PATH, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=metric_row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(metric_row)
