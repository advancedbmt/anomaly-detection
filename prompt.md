# Prompt: Time-Series Anomaly Detection with LSTM Autoencoders

## Objective

Generate Python code for anomaly detection pipelines that process time-series data from CSV files using LSTM Autoencoders. Identify anomalies using dynamic reconstruction error thresholds and export structured results.

---

## Requirements

### Pipeline Logic

- Accept cleaned time-series CSVs
- Use LSTM Autoencoders to reconstruct signals per sensor/device
- Compute reconstruction errors and identify anomalies using dynamic thresholds
- Annotate anomalies with timestamps, device ID, and error score
- Export results to `anomalies_output.json` in structured format

### Visualization

- Plot LSTM anomaly predictions using Matplotlib
- Include visual markers and probability score overlays
- Differentiate between Normal vs Abnormal ranges

### Dockerization

- Dockerfile must install Python 3.8, TensorFlow, Pandas, and Matplotlib
- Compose file must define a service that:
  - Mounts `src/`, `data/`, `models/`
  - Exposes port 5000 for future expansion (optional)
  - Runs `multi_device_pipeline.py` as entrypoint

---

## Additional Prompt Templates

### Prompt: Generate pipeline logic for time-series anomaly detection using LSTM Autoencoders
Objective: Generate Python code that accepts time-series CSV data from IoT sensors, uses LSTM Autoencoders per device, computes reconstruction errors, and exports anomalies to JSON.

### Prompt: Generate Matplotlib plots for anomaly detection visualization
Objective: Generate a function to plot time-series data with LSTM anomaly detections. The plot should include error markers, colored anomaly regions, and overlay the anomaly probability.

### Prompt: Create a Dockerfile and docker-compose service for an LSTM anomaly detection pipeline
Objective: Generate a Dockerfile that installs Python 3.8, TensorFlow, Pandas, and Matplotlib. Generate a Docker Compose service that runs `multi_device_pipeline.py`, mounts necessary folders, and exposes port 5000.