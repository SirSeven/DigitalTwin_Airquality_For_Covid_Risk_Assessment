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

                    print(f"Sending message: {sensor_data['sensor_id']}, {sensor_data['property_name']}, {sensor_data['property_value']}, {sensor_data['timestamp']}")
                    telemetryService.send_data(device_id, sensor_data['sensor_id'],sensor_data['property_name'], sensor_data['timestamp'], sensor_data['property_value'])

            time.sleep(3)
            input()

    except KeyboardInterrupt:
        print("device telemetry sending stopped")
