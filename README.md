# Anomaly Detection Pipeline

An extensible framework for identifying anomalies in time-series sensor data using LSTM autoencoders. The project includes a FastAPI service for real-time predictions, a Jupyter workflow for exploration, and Docker recipes for a reproducible setup.

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development](#development)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)
- [FAQ](#faq)

## Installation

The pipeline requires **Python 3.10+**. You can install dependencies with pip or conda, or run everything in Docker.

```bash
# clone the repository
git clone https://github.com/yourorg/anomaly-detection.git
cd anomaly-detection

# optional: create a virtual environment
python -m venv venv
source venv/bin/activate

# install requirements
pip install -r requirements.txt
```

Conda users may create an environment with the provided `environment.yml`:

```bash
conda env create -f environment.yml
conda activate python3.12
```

To start a completely reproducible stack, build and run the Docker compose setup:

```bash
docker compose -f docker-compose.anomaly.yml up --build
```

This exposes the FastAPI service on **localhost:8002** and mounts the project source code inside the container.

## Usage

Run the Jupyter notebook for exploratory work:

```bash
jupyter notebook src/pipeline/main.ipynb
```

Or execute the pipeline as a script:

```bash
python src/pipeline/main.py
```

The FastAPI service can be launched manually from `src/pipeline`:

```bash
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

After processing, results are written to `data/anomalies_output.json` and plots are generated for each device.

## Configuration

All paths and model parameters live in [`src/pipeline/config.py`](src/pipeline/config.py). Edit this file or set the following environment variables to override defaults:

- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` – PostgreSQL connection
- `SEQUENCE_LENGTH`, `ANOMALY_PERCENTILE` – LSTM settings
- `DEVICES_DATA_PATH` – location of input CSV files
- `SAVED_MODELS_PATH` – directory containing `.h5` models

Ensure these folders exist or are mounted when running in Docker.

## Development

Install development tools and run the tests:

```bash
pip install -r requirements.txt
pip install pytest black flake8 pre-commit
pre-commit install
pytest
```

Formatting is enforced with **Black** and **flake8** via pre‑commit hooks. Benchmark scripts live in the `benchmark/` folder.

## Project Structure

```
├── src/                 # pipeline code
│   ├── devices_data/    # example CSVs
│   └── pipeline/        # FastAPI server and utilities
├── storage/saved_models # pretrained LSTM models
├── data/                # output JSON and plots
└── benchmark/           # performance tests
```

## Contributing

Contributions are welcome! Please open an issue or pull request. Make sure to format your code with **Black** and run `pre-commit` before submitting.

## License

This project is licensed under the [MIT](LICENSE) license.

## Credits

Built with help from **LLM Agents** and numerous open‑source libraries including TensorFlow, Pandas and FastAPI.

## FAQ

- **File or model not found** – verify the paths in `config.py`.
- **No anomalies detected** – lower `ANOMALY_PERCENTILE` or retrain your models.
- **Plotting issues** – ensure the DataFrame passed to plotting functions contains the required columns.

