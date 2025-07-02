import json

class IoTDevice:
    def __init__(self):
        self.iot = {}
        self.sync = {}
        self.incidents = []

    def load_json(self, device_file, synth_file, device_name):
        with open(device_file) as f:
            self.iot = json.load(f)["devices"][device_name]
        with open(synth_file) as f:
            conf = json.load(f)
            self.sync = conf["synthesis"][device_name]
            self.incidents = conf.get("incidents", [])

    def get_device_attribute(self, key):
        return self.iot.get(key)

    def get_synthesis_parameter(self, key):
        return self.sync.get(key)

    def get_incident_list(self):
        return self.incidents
