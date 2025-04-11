import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from funcs.IoTDevice import IoTDevice
import funcs.json_process as json_process


def parse_entry(entry):
    time_part, state_part = entry.split(" ", 1)
    if ":" in time_part:
        time_obj = datetime.strptime(time_part.lower(), "%I:%M%p").time()
    else:
        time_obj = datetime.strptime(time_part.lower(), "%I%p").time()
    time_str = time_obj.strftime("%H:%M")
    state_clean = state_part.replace("\\", " ")
    return (time_str, state_clean)


def inject_anomaly_by_time(df, anomaly, sensor_name, time_column="timestamp", target_column="feature_0"):
    if anomaly["tag"] != sensor_name:
        return df
    
    df[time_column] = pd.to_datetime(df[time_column])

    # Strip timezone if present
    happen_time = pd.to_datetime(anomaly["HappenTime"]).tz_localize(None)

    duration_minutes = int(anomaly["length"].replace("min", ""))
    anomaly_value = float(anomaly["Value"])

    time_diff = (df[time_column] - happen_time).abs()
    start_idx = time_diff.idxmin()

    end_time = happen_time + timedelta(minutes=duration_minutes)
    mask = (df[time_column] >= happen_time) & (df[time_column] < end_time)

    noise = np.random.uniform(-0.5, 0.5, size=mask.sum()) * 5
    df.loc[mask, target_column] = anomaly_value + noise
    df.loc[mask, "is_anomaly"] = True

    return df


def parse_state_timeline(state_entries, date="2025-04-07"):
    parsed_states = []
    for entry in state_entries:
        try:
            time_str, state_str = entry.split()
            try:
                time_obj = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %I:%M%p")
            except ValueError:
                time_obj = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %I%p")
            state = state_str.split("\\")[0].lower()
            parsed_states.append((time_obj, state))
        except Exception as e:
            print(f"Error parsing entry '{entry}': {e}")
    return sorted(parsed_states, key=lambda x: x[0])



def generate_state_based_data(state_schedule, state_ranges, ambient_temp, freq="1min"):
    df_parts = []
    for i in range(len(state_schedule) - 1):
        start_time, state = state_schedule[i]
        end_time, _ = state_schedule[i + 1]
        if state not in state_ranges:
            print(f"⚠️ Skipping unknown state: {state}")
            continue
        time_range = pd.date_range(
            start=start_time, end=end_time - timedelta(minutes=1), freq=freq
        )
        temp_min, temp_max = state_ranges[state]
        temps = (
            np.random.uniform(temp_min, temp_max, size=len(time_range)) + ambient_temp
        )
        df_part = pd.DataFrame(
            {
                "timestamp": time_range,
                "feature_0": temps,
                "state": state,
                "is_anomaly": False,
            }
        )
        df_parts.append(df_part)
    return pd.concat(df_parts, ignore_index=True)

def device_data_generation(generated_device, synth_id):

    #loading the configs
    ambient_temp = generated_device.get_device_attribute("ambientTemperature")
    tag_list = generated_device.get_device_attribute("tag_list")
    synth_schedule = generated_device.get_synthesis_parameter("batch")
    parsed_schedule = parse_state_timeline(synth_schedule)

    anomoly_list = generated_device.get_synthesis_parameter("customAnomaly")
    dfs = []

    for sensor_name, config in tag_list.items():
        state_ranges = {
            state.lower(): (val["minIncrease"], val["maxIncrease"])
            for state, val in config["states"].items()
        }
        if "temperature" in sensor_name.lower():
            df = generate_state_based_data(parsed_schedule, state_ranges, ambient_temp)
        else:
            df = generate_state_based_data(parsed_schedule, state_ranges, 0)
        for anomaly in anomoly_list:
            if "sensor" in anomaly:
                if anomaly["sensor"]==synth_id:
                    print(f"Injecting anomaly for {sensor_name} with ID {synth_id}")
                    inject_anomaly_by_time(df, anomaly, sensor_name)
            else:
                inject_anomaly_by_time(df, anomaly, sensor_name)
        df["sensor"] = sensor_name
        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)

    return dfs, combined_df





if __name__ == "__main__":

    test_temp_device = IoTDevice()
    test_json_path = "../json_file/basic_config.json"
    test_temp_device.load_json(test_json_path)

    ambient_temp = test_temp_device.get_device_attribute("ambientTemperature")
    state_entries = test_temp_device.get_synthesis_parameter("batch")
    anomaly_injection = test_temp_device.get_synthesis_parameter("customAnomaly")
    states_config = test_temp_device.get_device_attribute("tag_list")["temperatureSensor1"][
        "states"
    ]
    try:
        state_ranges = {
            state.lower(): (val["minIncrease"], val["maxIncrease"])
            for state, val in states_config.items()
        }
    except:
        state_ranges = {
            state["state"].lower(): (state["tagValueMin"], state["tagValueMax"])
            for state in states_config
        }

    parsed_schedule = parse_state_timeline(state_entries)
    df = generate_state_based_data(parsed_schedule, state_ranges)

    for anom in anomaly_injection:
        df = json_process.inject_anomaly_by_time(df, anom)

    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"].to_numpy(), df["feature_0"].to_numpy(), label="Temperature", color="royalblue")
    plt.title("State-Based Motor Temperature with Anomalies")
    plt.xlabel("Timestamp")
    plt.ylabel("Temperature (\u00b0C)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    df.to_csv("test_temp.csv", index=False)
    print("✅ State-based data exported to test_temp.csv")
