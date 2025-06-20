import matplotlib.pyplot as plt
import pandas as pd
from config import ANOMALY_PERCENTILE

def plot_lstm_vs_rf(df, device_type):
    """
    Improved plot showing LSTM and RF predictions with black dots for anomalies.
    """
    plt.figure(figsize=(14, 6))

    if "is_anomaly" in df.columns:
        plt.step(df['timestamp'], df['is_anomaly'], where='post', label='LSTM Anomaly Detection', alpha=0.7)

    if "rf_prediction" in df.columns:
        rf_pred = pd.to_numeric(df["rf_prediction"], errors="coerce").fillna(0)
        plt.step(df['timestamp'], rf_pred + 0.05, where='post', label='RF Classification (shifted)', alpha=0.7)

    if "is_anomaly" in df.columns:
        anomalies_lstm = df[df['is_anomaly'] == 1]
        plt.scatter(anomalies_lstm['timestamp'], anomalies_lstm['is_anomaly'], color='black',
                    label='LSTM Anomaly Points', marker='o', s=50)

    if "rf_prediction" in df.columns:
        anomalies_rf = df[df['rf_prediction'] == 1]
        plt.scatter(anomalies_rf['timestamp'], [1.05] * len(anomalies_rf), color='black',
                    label='RF Anomaly Points', marker='x', s=50)

    plt.title(f"{device_type} - LSTM vs RF Anomaly Detection")
    plt.xlabel("Timestamp")
    plt.ylabel("Anomaly (1=True, 0=False)")
    plt.yticks([0, 1, 1.05])
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_reconstruction_error(df_state_processed, device_type, state):
    """
    Plot reconstruction error for a given state and highlight anomalies.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df_state_processed['timestamp'], df_state_processed['reconstruction_error'],
             label='Reconstruction Error', color='blue', alpha=0.7)

    threshold = df_state_processed['reconstruction_error'].dropna().quantile(ANOMALY_PERCENTILE / 100)
    plt.axhline(y=threshold, color='orange', linestyle='--',
                label=f'Threshold ({ANOMALY_PERCENTILE}th percentile)')

    anomalies = df_state_processed[df_state_processed['is_anomaly']]
    if not anomalies.empty:
        plt.scatter(anomalies['timestamp'], anomalies['reconstruction_error'],
                    color='red', label='Anomalies', marker='x', s=100)

    plt.title(f"{device_type} - State: {state}\nReconstruction Error & Anomalies")
    plt.xlabel("Timestamp")
    plt.ylabel("Error")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
