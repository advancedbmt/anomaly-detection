import json


class IoTDevice:
    def __init__(self):
        self.IoT_attributes = {}
        self.Network_attributes = {}
        self.sync_param = {}
        self.incident_list = []

    def load_json(self, device_file, synth_file, device_name, network_file = ""):
        with open(device_file, "r") as file:
            config_temp = json.load(file)
            for key, value in config_temp["devices"][device_name].items():
                self.IoT_attributes[key] = value
        
        with open(synth_file, "r") as file:
            config_temp = json.load(file)
            for key, value in config_temp["synthesis"][device_name].items():
                self.sync_param[key] = value
            self.incident_list = config_temp["incidents"]
            
            

    def get_device_attribute(self, attribute):
        return self.IoT_attributes.get(attribute, None)

    def get_network_attribute(self, attribute):
        return self.Network_attributes.get(attribute, None)

    def get_synthesis_parameter(self, attribute):
        return self.sync_param.get(attribute, None)
    
    def get_incident_list(self):
        return self.incident_list