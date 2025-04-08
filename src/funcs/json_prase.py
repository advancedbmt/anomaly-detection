import json
from datetime import datetime

class IoTDevice:
    def __init__(self):
        #For storing the device attributes of the device
        self.IoT_attributes = {} 

        self.Network_attributes = {}

        #For storing the synthetic generated data
        self.sync_param = {}

    ### Function to load the JSON file and parse the data
    # @param json_file: Path to the JSON file
    # @return: None
    # This function loads the JSON file and parses the data into the class attributes.
    # It reads the device information, network information, and synthesis details from the JSON file. 
    def load_json(self, json_file):
        with open(json_file, 'r') as file:
            config_full = json.load(file)
            for key, value in config_full["device_info"].items():
                self.IoT_attributes[key] = value
            
            for key, value in config_full["network_info"].items():
                self.Network_attributes[key] = value
            
            for key, value in config_full["synth_detial"].items():
                self.sync_param[key] = value

    ### Function to get the device attributes
    # @return: Dictionary containing the device attributes
    # This function returns the device attributes stored in the class.
    def get_device_attributes_all(self):
        return self.IoT_attributes
    
    ### Function to get the network attributes
    # @return: Dictionary containing the network attributes
    # This function returns the network attributes stored in the class.
    def get_network_attributes_all(self):
        return self.Network_attributes
    
    ### Function to get the synthesis parameters
    # @return: Dictionary containing the synthesis parameters
    # This function returns the synthesis parameters stored in the class.
    def get_synthesis_parameters_all(self):
        return self.sync_param

    ### function to get specific attribute of the device
    # @param attribute: Attribute to be retrieved
    # @return: Value of the specified attribute or None if not found
    # This function retrieves the value of a specific attribute from the device attributes.
    # It returns the value if found, otherwise None.
    def get_device_attribute(self, attribute):
        return self.IoT_attributes.get(attribute, None)
    
    ### function to get specific attribute of the network
    # @param attribute: Attribute to be retrieved
    # @return: Value of the specified attribute or None if not found
    # This function retrieves the value of a specific attribute from the network attributes.
    # It returns the value if found, otherwise None.
    def get_network_attribute(self, attribute):
        return self.Network_attributes.get(attribute, None)
    
    ### function to get specific synthesis parameter
    # @param attribute: Attribute to be retrieved
    # @return: Value of the specified attribute or None if not found
    # This function retrieves the value of a specific synthesis parameter.
    # It returns the value if found, otherwise None.
    def get_synthesis_parameter(self, attribute):
        return self.sync_param.get(attribute, None)
    
    ### Function to modify a specific attribute of the device
    # @param attribute: Attribute to be modified
    # @param value: New value for the attribute
    # @return: bool indicating success or failure
    # This function modifies a specific attribute of the device with the provided value.
    # It returns True if the attribute is modified successfully, otherwise False.
    def modify_attribute(self, attribute, value):
        if attribute in self.IoT_attributes:
            self.IoT_attributes[attribute] = value
            return True
        else:
            return False
        
    ### Function to modify a specific attribute of the network
    # @param attribute: Attribute to be modified
    # @param value: New value for the attribute
    # @return: bool indicating success or failure
    # This function modifies a specific attribute of the network with the provided value.
    # It returns True if the attribute is modified successfully, otherwise False.
    def modify_network_attribute(self, attribute, value):
        if attribute in self.Network_attributes:
            self.Network_attributes[attribute] = value
            return True
        else:
            return False
        
    ### Function to modify a specific synthesis parameter
    # @param attribute: Attribute to be modified
    # @param value: New value for the attribute
    # @return: bool indicating success or failure
    # This function modifies a specific synthesis parameter with the provided value.
    # It returns True if the parameter is modified successfully, otherwise False.
    def modify_synthesis_parameter(self, attribute, value):
        if attribute in self.sync_param:
            self.sync_param[attribute] = value
            return True
        else:
            return False


if __name__ == "__main__":
    # Example usage of the IoTDevice class
    device = IoTDevice()
    device.load_json("../../json_file/basic_config.json")
    
    print("Device Attributes:", device.get_device_attribute("ambientTemperature"))

    # Modify an attribute
    if device.modify_attribute("topic", "factory/line1/device123/temperatureSensor_test"):
        print("Attribute modified successfully.")
    else:
        print("Failed to modify attribute.")
