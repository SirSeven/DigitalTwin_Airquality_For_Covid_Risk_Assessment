import time
import json
from sensor_value.SensorValueExtractor import SensorValueExtractor
from sensors.ISensor import ISensor
from telemetry_services.AzureIoTHubService import AzureIoTHubService


def send_device_telemetry(connection_string: str, device_id: str, sensorCollection):

    try:
        service = AzureIoTHubService(connection_string)

        print("IoT Hub device sending periodic messages, press Ctrl-C to exit")

        while True:
            for sensorObj in sensorCollection:
                sensor: ISensor = sensorObj['sensor']
                sensor.refresh_data()

                sensorValueExtractor: SensorValueExtractor
                for sensorValueExtractor in sensorObj['valueExtractors']:
                    sensor_data = sensorValueExtractor.get_value()

                    sensor_data_str = json.dumps({sensor_data['property_name']: sensor_data['property_value']})
                    print(f"Sending message: {sensor_data_str}")
                    service.send_data(device_id, sensor_data['sensor_id'], sensor_data_str)
                    print("Message successfully sent")

            time.sleep(1)

    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")
