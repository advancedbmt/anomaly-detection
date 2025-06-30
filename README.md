# Anomaly Detection Pipeline

This project implements a time–series anomaly detection workflow built with LSTM Autoencoders. It processes sensor data from CSV files or a PostgreSQL database and exports the results to a structured JSON file. A Docker environment is provided for a reproducible setup.

## Project Structure

The repository assumes a set of directories located at the project root:

- `data/` &ndash; output location for generated files such as `anomalies_output.json`
- `src/devices_data/` &ndash; raw sensor CSV files (`*_unified.csv`)
- `storage/saved_models/` &ndash; directory containing pre-trained LSTM model files (`.h5`)

If these folders live outside of the repository, ensure they are mounted or linked so the code can locate them.

## Environment

The recommended way to run the pipeline is inside Docker. A `Dockerfile` and `docker-compose.anomaly.yml` are included.

```bash
docker compose -f docker-compose.anomaly.yml up --build
```

This launches a container running Jupyter Notebook on port `8891` with all Python dependencies installed.

For local development without Docker, create a Python 3.10+ environment and install dependencies from `requirements.txt` or `environment.yml`:

```bash
# Using conda
env_name=anomaly_env
conda create -n $env_name python=3.12
conda activate $env_name
pip install -r requirements.txt
```

The main libraries used are:

- `pandas`, `numpy`, `scikit-learn`
- `tensorflow` and `keras`
- `matplotlib`, `seaborn`
- `psycopg2-binary` for PostgreSQL access
- `paho-mqtt`, `psutil`, and other utilities

## Database Configuration

The pipeline now requires access to a PostgreSQL database to load historical sensor values. Connection parameters are defined in `src/pipeline/config.py`:

```python
DB_NAME = "db"
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "db"  # Docker service name
DB_PORT = "5432"
```

These can be adjusted through environment variables or by editing `config.py`. Ensure the database is running and reachable from the Docker container (the compose file expects a service named `db`).

## Running the Pipeline

1. Start the Docker environment or activate your Python environment.
2. Open Jupyter Notebook (automatically started inside Docker) and navigate to `src/pipeline/main.ipynb`. **This notebook handles all database communication.**
3. Execute the notebook cells or convert it to a Python script and run:

   ```bash
   python src/pipeline/main.py
   ```

   Note that `main.py` does not connect to PostgreSQL. It expects CSV data only.

The script loads data, performs anomaly detection per device, plots reconstruction errors, and writes results to `data/anomalies_output.json`.

## Output

`anomalies_output.json` contains a record for each timestamp with keys such as `device`, `timestamp`, `error`, `state`, `is_anomaly`, and `error_percentile`. Plots illustrating reconstruction error vs. the anomaly threshold are also generated for each device.

## Troubleshooting

- **File or model not found** &ndash; verify the directory paths in `config.py`.
- **No anomalies detected** &ndash; lower `ANOMALY_PERCENTILE` or review model training.
- **Plotting issues** &ndash; ensure the DataFrame passed to `plot_reconstruction_error` has the required columns.

---
