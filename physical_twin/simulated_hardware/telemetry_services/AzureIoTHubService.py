from datetime import datetime
import json
from azure.iot.device.iothub.sync_clients import IoTHubDeviceClient, Message
from . import ITelemetryService

class AzureIoTHubService(ITelemetryService):

    def __init__(self, connectionString):
        self.iotHubConnection = IoTHubDeviceClient.create_from_connection_string(
            connectionString)

    def send_data(self, device_id: str, sensor_id: str, sensor_property_name: str, data_timestamp: datetime, sensor_data):

        sensor_data_str = json.dumps({'component_id': sensor_id,
                                      'component_property_name': sensor_property_name,
                                      'component_property_value': sensor_data,
                                      'is_telemetry': True,
                                      'timestamp': data_timestamp.isoformat()})
        iotMessage = Message(sensor_data_str.encode('utf-8'), None, 'utf-8', 'application/json')
        self.iotHubConnection.send_message(iotMessage)
        pass
