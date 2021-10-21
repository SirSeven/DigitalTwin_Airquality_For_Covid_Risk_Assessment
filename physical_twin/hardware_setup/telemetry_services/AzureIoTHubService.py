from azure.iot.device.iothub.sync_clients import IoTHubDeviceClient, Message
from . import ITelemetryService

class AzureIoTHubService(ITelemetryService):
    
    def __init__(self, connectionString):
        self.iotHubConnection = IoTHubDeviceClient.create_from_connection_string(connectionString)

    def send_data(self, device_id, sensor_id, sensor_data):
        iotMessage = Message(sensor_data)
        self.iotHubConnection.send_message(iotMessage)
        pass