import json


class IoTDevice:
    def __init__(self):
        self.IoT_attributes = {}
        self.Network_attributes = {}
        self.sync_param = {}

    def load_json(self, json_file):
        with open(json_file, "r") as file:
            config_full = json.load(file)
            for key, value in config_full["device_info"].items():
                self.IoT_attributes[key] = value
            for key, value in config_full["network_info"].items():
                self.Network_attributes[key] = value
            for key, value in config_full["synth_detial"].items():
                self.sync_param[key] = value

    def get_device_attribute(self, attribute):
        return self.IoT_attributes.get(attribute, None)

    def get_network_attribute(self, attribute):
        return self.Network_attributes.get(attribute, None)

    def get_synthesis_parameter(self, attribute):
        return self.sync_param.get(attribute, None)
