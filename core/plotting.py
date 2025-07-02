import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from core.config import ANOMALY_PERCENTILE

def plot_reconstruction_error(df_processed, device_type, state_label="All States"):
    if 'timestamp' not in df_processed or 'reconstruction_error' not in df_processed:
        print(f"⚠️ Missing columns in {device_type}")
        return

    plt.figure(figsize=(14, 6))
    plt.plot(df_processed['timestamp'], df_processed['reconstruction_error'], label='Reconstruction Error', color='blue', alpha=0.7)

    if not df_processed['reconstruction_error'].empty:
        threshold = df_processed['reconstruction_error'].dropna().quantile(ANOMALY_PERCENTILE / 100)
        plt.axhline(y=threshold, color='orange', linestyle='--', label=f'Threshold ({ANOMALY_PERCENTILE}th)')
    else:
        return

    if 'is_anomaly' in df_processed.columns:
        anomalies = df_processed[df_processed['is_anomaly']]
        plt.scatter(anomalies['timestamp'], anomalies['reconstruction_error'], color='red', label='Anomalies', s=50)

    plt.title(f"{device_type} - {state_label} Reconstruction Error")
    plt.xlabel("Timestamp")
    plt.ylabel("Error")
    plt.legend()
    plt.grid(True)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
