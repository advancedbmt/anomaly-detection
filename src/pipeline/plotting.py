import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates # Import mdates for date formatting
from config import ANOMALY_PERCENTILE # Assuming this is used for thresholding

# Removed plot_lstm_vs_rf as it's no longer needed
# def plot_lstm_vs_rf(df, device_type):
#    ... (removed code) ...


def plot_reconstruction_error(df_processed, device_type, state_label=""): # state_label can be "All States" now
    """
    Plot reconstruction error for a given state/device and highlight anomalies.
    """
    plt.figure(figsize=(14, 6)) # Increased figure size for consistency

    if 'timestamp' not in df_processed.columns or 'reconstruction_error' not in df_processed.columns:
        print(f"❌ Cannot plot reconstruction error for {device_type}: Missing 'timestamp' or 'reconstruction_error' column.")
        return

    plt.plot(df_processed['timestamp'], df_processed['reconstruction_error'],
             label='Reconstruction Error', color='blue', alpha=0.7)

    # Ensure threshold calculation handles NaNs and is robust
    # If ANOMALY_PERCENTILE is 99.5, this will make anomalies very sparse.
    # Adjust ANOMALY_PERCENTILE in config.py if you want more/fewer anomalies.
    if not df_processed['reconstruction_error'].empty:
        threshold = df_processed['reconstruction_error'].dropna().quantile(ANOMALY_PERCENTILE / 100)
        plt.axhline(y=threshold, color='orange', linestyle='--',
                    label=f'Threshold ({ANOMALY_PERCENTILE}th percentile)')
    else:
        print(f"⚠️ No reconstruction error data to calculate threshold for {device_type}.")
        threshold = None


    # Plot 'is_anomaly' points if available
    if 'is_anomaly' in df_processed.columns and threshold is not None:
        # Use the actual reconstruction_error value for the scatter point, not a fixed value
        anomalies = df_processed[df_processed['is_anomaly'] == True] # Filter for True
        if not anomalies.empty:
            # Only plot scatter points where the error actually exceeds the threshold, for clarity
            anomalies_to_plot = anomalies[anomalies['reconstruction_error'] > threshold]
            plt.scatter(anomalies_to_plot['timestamp'], anomalies_to_plot['reconstruction_error'],
                        color='red', label='LSTM Detected Anomalies', marker='o', s=50, zorder=5) # Changed marker/label for clarity
        else:
             print(f"ℹ️ No LSTM detected anomalies to plot for {device_type}.")
    elif 'is_anomaly' in df_processed.columns:
        print(f"ℹ️ 'is_anomaly' column exists but no threshold to compare against for plotting points for {device_type}.")


    plt.title(f"{device_type} - {state_label} Reconstruction Error & Anomalies")
    plt.xlabel("Timestamp")
    plt.ylabel("Error")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # Format x-axis for dates
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M'))
    plt.xticks(rotation=45)
    plt.show()