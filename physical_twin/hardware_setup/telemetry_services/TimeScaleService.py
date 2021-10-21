import json
import requests
from . import ITelemetryService

class TimeScaleService(ITelemetryService):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self, targetUrl):
        self.url = targetUrl

    def send_data(self, device_id, sensor_id, sensor_data):

        jsonObjects = {
            'roomnumber': device_id,
            'sensorname': sensor_id,
            sensor_data['property_name']: sensor_data['property_value']
        }

        json_object = json.dumps(jsonObjects)
        postdata = requests.post(
            self.url, headers=self.headers, data=json_object)     # SENDING THE DATA
        if postdata.status_code == 201:
            print('Sensor data sending successfully....')
        else:
            print(postdata.text+'Failed to post Sensor data to server!')
