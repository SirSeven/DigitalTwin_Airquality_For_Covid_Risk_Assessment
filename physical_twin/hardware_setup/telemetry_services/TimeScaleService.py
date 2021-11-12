import requests
from datetime import datetime
from . import ITelemetryService


class TimeScaleService(ITelemetryService):
    # url="http://140.78.155.6:5000/api/sensordata"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self, targetUrl):
        self.url = targetUrl

    def send_data(self, device_id: str, sensor_id: str, sensor_property_name: str, data_timestamp: datetime, sensor_data):
        jsonObjects = sensor_data
        jsonObjects['roomnumber'] = device_id
        jsonObjects['sensorname'] = sensor_id

        json_object = json.dumps(jsonObjects)
        postdata = requests.post(
            self.url, headers=self.headers, data=json_object)     # SENDING THE DATA
        if postdata.status_code == 201:
            print('Sensor data sending successfully....')
        else:
            print(postdata.text+'Failed to post Sensor data to server!')
