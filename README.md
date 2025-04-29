# Anomaly Detection
## TODOS
- add MQTT support
- Format the proper file structure for the project
## Folder Description
 - env.yaml: the file that contains the environment for the project. It is used to create a conda environment for the project
 - test_cases: the folder contain the predicion files and all other essential files for the project
    - multi_device_pipeline_final_updated_with_rf_plot.ipynb: the jupyter notebook that contains the multi device detection version of the code for the project
    - state_lstm_inference_and_rf_classification.ipynb: the jupyter notebook that contain the single device detection version of the code for the project
 - saved_models: the folder contains the saved models for the project
    - ***.pkl: the random forest model that is used for classification of the data
    - ***.h5: the LSTM model that is used for prediction of the data
 - test_cvs: the folder contains the test data for the project