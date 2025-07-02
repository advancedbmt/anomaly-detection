# Anomaly Detection Pipeline

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

A lightweight time–series anomaly detection system using LSTM autoencoders. It processes sensor CSVs or PostgreSQL data and exports JSON results.

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

Python 3.10+ is required. Clone the repository and install dependencies with `pip` or `conda`. Docker files are provided for a fully reproducible setup.

```bash
# optional: create a virtual environment
python -m venv .venv && source .venv/bin/activate

# install
pip install -r requirements.txt
```

Or start everything in Docker:

```bash
docker compose -f docker-compose.anomaly.yml up --build
```

## Usage

Start Jupyter inside Docker or your local environment and run `src/pipeline/main.ipynb`. To run as a script:

```bash
python src/pipeline/main.py
```

The script loads data, performs anomaly detection, and writes `data/anomalies_output.json`.

## Configuration

Database settings live in [`src/pipeline/config.py`](src/pipeline/config.py):

```python
DB_NAME = "db"
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "db"  # Docker service name
DB_PORT = "5432"
```

Modify these values or set environment variables so the pipeline can connect to your PostgreSQL instance. Paths for input CSVs and saved models are also defined in this file.

## Development

Use `python -m venv` or `conda` to create an environment. We recommend running `flake8` and `black` before submitting pull requests. Unit tests (under `benchmark/`) can be executed with `pytest`.

```bash
pytest
```

## Project Structure

```
archive/                Previous notebooks and scripts
benchmark/              Benchmark utilities and tests
json_folder/            Example configuration JSON files
src/                    Core pipeline code
storage/saved_models/   Pre-trained LSTM models
```

See the repository for additional data and example CSVs.

## Contributing

Issues and pull requests are welcome! Please follow standard [PEP 8](https://peps.python.org/pep-0008/) style and run linters before submitting. Opening an issue to discuss new features is encouraged.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Credits

Built with help from LLM Agents and the open-source community.

## FAQ

- **File or model not found** – check paths in `config.py`.
- **No anomalies detected** – lower `ANOMALY_PERCENTILE` or retrain models.
- **Plotting issues** – ensure the DataFrame has the required columns.
