import sys
import json
import importlib
import DeviceSensorsService
from conditions.JsonPathConditionService import JsonPathConditionService
from conditions.NullConditionService import NullConditionService
from helpers import JsonHelper
from sensor_value.SensorValueExtractor import SensorValueExtractor
from sensor_value.SensorValueType import SensorValueType
from telemetry_services import AzureIoTHubService
from sensors import ISensor

def getSensor(sensorConfigJson) -> ISensor:
    module = importlib.import_module(sensorConfigJson['Module'])
    class_ = getattr(module, sensorConfigJson['Class'])
    return class_(sensorConfigJson['Properties'])

def getSensorValueExtractor(sensor: ISensor, sensorValueConfig) -> SensorValueExtractor:
    sensorValueType = SensorValueType[sensorValueConfig['Path'].upper()]
    return SensorValueExtractor(sensor, sensorValueConfig['Name'], sensorValueType)

if __name__ == '__main__':
    configFilePath = "config.json"
    if(len(sys.argv) > 1):
        configFilePath = sys.argv[1]
        
    if(len(sys.argv) > 2):
        validationsFilePath = sys.argv[2]
        conditionService = JsonPathConditionService(validationsFilePath)
    else:
        conditionService = NullConditionService()

    config = JsonHelper.readJsonFromFile(configFilePath)
    connection_string = config['connectionStrings']['azureIoTHub']
    device_id = config['twin']['id']

    sensorsConfig = config['twin']['sensors']
    sensorCollection = []
    for sensorConfig in sensorsConfig:
        sensor = getSensor(sensorConfig)
        sensorValueExtractors = []
        for sensorValueConfig in sensorConfig['Values']:
            sensorValueExtractors.append(getSensorValueExtractor(sensor, sensorValueConfig))

        sensorCollection.append({
            'sensor': sensor,
            'valueExtractors': sensorValueExtractors
        })

    azureIoTHub_telemetry_service = AzureIoTHubService(connection_string)

    DeviceSensorsService.send_device_telemetry(azureIoTHub_telemetry_service, conditionService, device_id, sensorCollection)
