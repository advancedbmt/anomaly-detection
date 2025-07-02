from fastapi import FastAPI, HTTPException, Query
import paho.mqtt.client as mqtt
import json
import postgres_connection as pg_conn
from processing.prediction import process_device_query  # your updated logic

app = FastAPI(title="Anomaly Prediction API")

MQTT_BROKER = "hivemq"
MQTT_PORT = 1883

@app.get("/predict")
def predict_motor(motor: str = Query(..., description="Motor name (e.g., Motor29)")):
    """
    Run anomaly detection for a given motor and publish results via MQTT.
    """
    try:
        # Connect to PostgreSQL
        conn = pg_conn.get_postgres_connection()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

    try:
        # Load motor time-series data
        df = pg_conn.get_motor_timeseries(conn, motor)
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Motor timeseries not found: {e}")

    try:
        # Run anomaly detection
        result_df = process_device_query("motor_monitor", df)
        if result_df is None:
            raise ValueError("Prediction result is empty or invalid")

        # Serialize result
        payload = json.dumps({
            "motor": motor,
            "result": json.loads(result_df.to_json(orient='records', date_format="iso"))
        })

        # Publish to MQTT
        mqtt_client = mqtt.Client(client_id="prediction-publisher")
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        topic = f"prediction/anomaly/{motor}"
        mqtt_client.publish(topic, payload)
        mqtt_client.disconnect()

        print(f"📤 Published to topic: {topic} | payload: {payload}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction or MQTT failed: {e}")
    finally:
        conn.close()

    return {"status": "success", "motor": motor, "topic": topic}
