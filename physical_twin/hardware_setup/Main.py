import sys
import json
import importlib
from .DeviceSensorsService import DeviceSensorsService
from sensor_value.SensorValueExtractor import SensorValueExtractor
from sensor_value.SensorValueType import SensorValueType
from telemetry_services import AzureIoTHubService
from sensors import ISensor

def readJsonFromFile(file_path: str) -> object:
    file = open(file_path)
    file_content = file.read()
    file.close()
    data = json.loads(file_content)
    return data

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

    config = readJsonFromFile(configFilePath)
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

    DeviceSensorsService.send_device_telemetry(azureIoTHub_telemetry_service, device_id, sensorCollection)
