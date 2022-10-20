from datetime import datetime
import os
import sys
from threading import Timer
from DeviceSensorsService import DeviceSensorsService
from conditions.JsonPathConditionService import JsonPathConditionService
from telemetry_services import DelayedTelemetryService
from sensor_value import SensorValueExtractor, SensorValueType
from sensors import CsvValuesSensor

telemetryService = DeviceSensorsService()

def stopTelemetrySending():
    telemetryService.stop()

if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print("No execution time or no conditions file given. Aborting.")
        sys.exit()

    executionTimeStr = sys.argv[1]
    if not executionTimeStr.isnumeric():
        print("Invalid execution time given. Use only ints. Aborting.")
        sys.exit()

    conditionsJson = sys.argv[2]   
    
    timer = Timer(int(executionTimeStr), stopTelemetrySending)
    timer.start()

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
    telemetry_service = DelayedTelemetryService(10)
    jsonPathConditionService = JsonPathConditionService(conditionsJson)
    
    telemetryService.send_device_telemetry(telemetry_service, jsonPathConditionService, 'Raspberry_Floor', sensorCollection)

    timer.cancel()

    stoppingTime = datetime.utcnow()
    #print(f"Stopping time: {stoppingTime}.")
    processingTimeSec = (stoppingTime-startingTime).total_seconds()
    print(f"Processed {DelayedTelemetryService.messagesProcessed} msg in {processingTimeSec} sec. {round(DelayedTelemetryService.messagesProcessed/processingTimeSec,2)} msg/sec")