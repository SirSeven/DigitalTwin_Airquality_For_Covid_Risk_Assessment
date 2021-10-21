import time
import json
from telemetry_services import ITelemetryService
from sensors import ISensor
from sensor_value import SensorValueExtractor

def send_device_telemetry(telemetryService: ITelemetryService, device_id: str, sensorCollection):
    print("Starting sending device telemetry.")
    print("Press Ctrl-C to exit")

    try:
        while True:
            for sensorObj in sensorCollection:
                sensor: ISensor = sensorObj['sensor']
                sensor.refresh_data()

                sensorValueExtractor: SensorValueExtractor
                for sensorValueExtractor in sensorObj['valueExtractors']:
                    sensor_data = sensorValueExtractor.get_value()

                    sensor_data_str = json.dumps({sensor_data['property_name']: sensor_data['property_value']})
                    print(f"Sending message: {sensor_data_str}")
                    telemetryService.send_data(device_id, sensor_data['sensor_id'], sensor_data_str)
                    print("Message successfully sent")

            time.sleep(3)

    except KeyboardInterrupt:
        print("device telemetry sending stopped")
