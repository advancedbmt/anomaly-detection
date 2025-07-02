import os
import time
import psutil

# === BASE PROJECT ROOT (mounted as /app) ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # this will point to /app

# === FIXED PATHS ===
DEVICES_DATA_PATH = os.path.join(BASE_DIR, "train_data/devices_data/")
SAVED_MODELS_PATH = os.path.join(BASE_DIR, "storage/saved_models/")
EXPORT_PATH = os.path.join(BASE_DIR, "outputs/")

# === CONSTANTS ===
SEQUENCE_LENGTH = 30
ANOMALY_PERCENTILE = 99.5
MIN_ANOMALY_DURATION = 3
ERROR_SMOOTHING_SPAN = 5
EXCLUDE_COLUMNS = ['timestamp', 'state', 'reconstruction_error', 'is_anomaly', 'label']

# === MEMORY TRACKING ===
process = psutil.Process(os.getpid())
start_memory = process.memory_info().rss / (1024 * 1024)
global_start_time = time.time()
