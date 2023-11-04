from datetime import datetime
import sys
from threading import Timer
from DeviceSensorsService import DeviceSensorsService
from conditions.JsonPathConditionService import JsonPathConditionService
from telemetry_services import AzureIoTHubService
from sensor_value import SensorValueExtractor, SensorValueType
from sensors import CsvValuesSensor

telemetryService = DeviceSensorsService()

def stopTelemetrySending():
    telemetryService.stop()

if __name__ == '__main__':
    startingTime = datetime.utcnow()
    #print(f"Starting time: {startingTime}") 

    sensor = CsvValuesSensor({
        'Name': 'Sensor',
        'CsvFilePath': 'sensorData.csv'
    })

    sensorCollection = [{
        'sensor': sensor,
        'valueExtractors': [
            SensorValueExtractor(sensor, 'temp', SensorValueType['TEMPERATURE']),
            #SensorValueExtractor(sensor, 'co2Value', SensorValueType['CO2']),
            #SensorValueExtractor(sensor, 'humid', SensorValueType['HUMIDITY'])
        ]
    }]
    telemetry_service = AzureIoTHubService("HostName=at-davemar-master-thesis.azure-devices.net;DeviceId=Raspberry_Floor;SharedAccessKey=JTvpeBb6QXg01lZsuJ/BBEw8BqMVgrzryYxZLcCwwBU=")
    jsonPathConditionService = JsonPathConditionService("inputs/0-0-0.json")
    
    messages = 10

    telemetryService.send_device_telemetry(telemetry_service, jsonPathConditionService, 'Raspberry_Floor', sensorCollection, messages)

    stoppingTime = datetime.utcnow()
    #print(f"Stopping time: {stoppingTime}.")
    processingTimeSec = (stoppingTime-startingTime).total_seconds()
    print(f"Processed {messages} msg in {processingTimeSec} sec. {round(messages/processingTimeSec,2)} msg/sec")