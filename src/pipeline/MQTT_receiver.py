import paho.mqtt.client as mqtt
import json

def default_handle_msg(topic, payload):
    print(f"📥 (default handler) {topic}: {payload}")

def start_mqtt_receiver(on_msg_callback=None, broker_host="localhost", broker_port=1883, client_id="ignition_receiver"):
    if on_msg_callback is None:
        on_msg_callback = default_handle_msg  # Fallback handler

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("✅ Connected to MQTT Broker")
            client.subscribe("#")
        else:
            print(f"❌ Connection failed with code {rc}")

    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
        except Exception:
            payload = msg.payload.decode()

        on_msg_callback(msg.topic, payload)

    client = mqtt.Client(client_id=client_id)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_host, broker_port, keepalive=60)
    client.loop_start()
    return client

