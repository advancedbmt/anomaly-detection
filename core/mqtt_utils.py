import json
import paho.mqtt.client as mqtt

def default_handle_msg(topic, payload):
    print(f"📥 {topic}: {payload}")

def start_mqtt_receiver(on_msg_callback=None, broker_host="localhost", broker_port=1883, client_id="ad_receiver"):
    if on_msg_callback is None:
        on_msg_callback = default_handle_msg

    def on_connect(client, userdata, flags, rc):
        print("✅ MQTT Connected" if rc == 0 else f"❌ MQTT Connect failed: {rc}")
        client.subscribe("#")

    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
        except Exception:
            payload = msg.payload.decode()
        on_msg_callback(msg.topic, payload)

    client = mqtt.Client(client_id=client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_host, broker_port, 60)
    client.loop_start()
    return client
