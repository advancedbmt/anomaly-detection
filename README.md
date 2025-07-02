
# Anomaly Detection FastAPI Service

This FastAPI-based service runs anomaly detection on IoT device CSV data using an LSTM Autoencoder model and exports the results in JSON format for further analysis (e.g., incident classification).

## 🚀 How to Run

1. **Build and Run the Docker Container:**

```bash
docker-compose -f docker-compose.ad.yml up --build
```

2. **Access the Swagger UI:**

Open your browser and go to:  
[http://localhost:8001/docs](http://localhost:8001/docs)

This brings up the interactive **Swagger UI** where you can test the `/run_ad` endpoint.

## 🧪 Example Requests for `/run_ad`

### Example 1: Motor Monitor
```json
{
  "csv_path": "train_data/devices_data/motor_monitor_0_unified.csv",
  "device_type": "motor_monitor"
}
```

### Example 2: Bale Counter
```json
{
  "csv_path": "train_data/devices_data/bale_counter_0_unified.csv",
  "device_type": "bale_counter"
}
```

### Example 3: Temperature Sensor
```json
{
  "csv_path": "train_data/devices_data/temperature_sensor_0_unified.csv",
  "device_type": "temperature_sensor"
}
```

### Example 4: Output Sensor
```json
{
  "csv_path": "train_data/devices_data/output_sensor_0_unified.csv",
  "device_type": "output_sensor"
}
```

## 📂 Output

The output will be saved as:

```
outputs/{device_type}_anomalies_output.json
```

For example:

```
outputs/motor_monitor_anomalies_output.json
```

Each JSON contains anomaly results for the device, including timestamp, reconstruction error, state, anomaly flags, and extracted feature values.

## 📞 Health Check

You can test if the service is up by calling:

```
GET http://localhost:8001/health
```

Expected response:

```json
{"status": "Anomaly Detection Service is running"}
```

---

© 2025 Advanced BMT | FastAPI Microservice for Anomaly Detection
