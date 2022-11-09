from conditions import JsonPathConditionService
from telemetry_services import ITelemetryService,DelayedTelemetryService
from sensors import ISensor
from sensor_value import SensorValueExtractor

class DeviceSensorsService:

    def __init__(self) -> None:
        self.cont = True

    def send_device_telemetry(self, telemetryService: ITelemetryService, jsonPathConditionService: JsonPathConditionService, device_id: str, sensorCollection, times: int = -1):
        i = 0
        #print("Starting sending device telemetry.")
        #print("Press Ctrl-C to exit")

        try:
            while self.cont and (times == -1 or i < times):
                for sensorObj in sensorCollection:
                    sensor: ISensor = sensorObj['sensor']
                    sensor.refresh_data()

                    sensorValueExtractor: SensorValueExtractor
                    for sensorValueExtractor in sensorObj['valueExtractors']:
                        sensor_data = sensorValueExtractor.get_value()

                        if jsonPathConditionService.validate(sensor_data['sensor_id'], sensor_data['property_name'], sensor_data['property_value']):
                            telemetryService.send_data(device_id, sensor_data['sensor_id'],sensor_data['property_name'], sensor_data['timestamp'], sensor_data['property_value'])
                i += 1

        except KeyboardInterrupt:
            print("device telemetry sending stopped")

        #print("Stopped sending device telemetry.")

    def stop(self):
        self.cont = False
        #print("Stopping sending device telemetry.")
