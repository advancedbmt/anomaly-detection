# Anomaly Detection

The Anomaly Detection algorithm for detecting abnormal data in the batch data

## Getting Started

The following software should be installed prior to spinning up the development environment

  * [Git](https://git-scm.com/downloads)
  * [Visual Studio Code](https://code.visualstudio.com/download)
  * [Anaconda](https://www.anaconda.com/)



## Usage

For Conda envionment setup, please use the environment.yml file. The environment.yml file contains the required packages for the project.
The code for setting up the conda environment is as follows:


```
conda env create -f test_cases/environment.yml
```

### Folder Overview
* `json_folder` contains the config files for different devices.
  - device_config*.json are the config files containing basic device info
  - The synthetic_config.json file contains the config for generating synthetic data. It includes the following:
    - Each device type's state schedule
    - the range for each sensor's synthetic data generation rules
    - All names appearing in the designated device_config file should also appear in synthetic_config.json

  - The pipeline_config.json file is for integration purposes. However, it is not used in the current version of the code.

* `src` contains the original data used by anomaly detection
* `test_cases` contains the modelized anomaly detection for benchmarking
* `benchmark` contains the files for the anomaly detection benchmark test
* `test_csv` contains reshaped data for anomaly detection

### How To Run
The `test_cases/multi_device_pipeline_final_updated_with_rf_plot.ipynb` file contains the code for multi-device detection

if in step 6, the random forest cannot be used, run the next block of code to retrain the random forest model. After getting the new random forest model, run the previous block of code to plot anomaly classification results.

The `test_cases/state_lstm_inference_and_rf_classification.ipynb` contains the code for single-device anomaly detection

Run the corresponding Jupyter files in the conda environment for anomaly detection

The default configuration is as follows
```
DEVICES_DATA_PATH = "../src/devices_data/"
SAVED_MODELS_PATH = "../test_cases/saved_models/"
EXCLUDE_COLUMNS = ['timestamp', 'state', 'reconstruction_error', 'is_anomaly', 'label']
SEQUENCE_LENGTH = 30
ANOMALY_PERCENTILE = 99.5
MIN_ANOMALY_DURATION = 3
ERROR_SMOOTHING_SPAN = 5
```

- `DEVICES_DATA_PATH` should be the device config file
- `SAVED_MODELS_PATH` is the folder storing all trained models
- `EXCLUDE_COLUMNS ` data columns need to be excluded for anomaly detection
- `SEQUENCE_LENGTH ` reconstruction window length for LSTM decoder
- `ANOMALY_PERCENTILE ` percentile for anomaly classification
- `MIN_ANOMALY_DURATION ` minimum length for anomaly to be considered as a true anomaly
- `ERROR_SMOOTHING_SPAN ` smoothing window for anomaly detection threshold 
