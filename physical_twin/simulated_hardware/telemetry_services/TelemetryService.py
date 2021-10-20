import json

class TelemetryService:
    
    def send_data(self, device_id, sensor_id, sensor_data):
        pass

    def __sensor_data_to_json(self, sensor_data):
        data_object = {}
        for sensor_data_entry in sensor_data:
            data_object[sensor_data_entry['property_name']] = sensor_data_entry['value']

        json_object = json.dumps(data_object)
        return json_object