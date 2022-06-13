import DeviceSensorsService
from conditions.JsonPathConditionService import JsonPathConditionService
from sensor_value import SensorValueExtractor, SensorValueType
from telemetry_services import AzureIoTHubService
from sensors import CsvValuesSensor

if __name__ == '__main__':
    sensor = CsvValuesSensor({
        'Name': 'Sensor',
        'CsvFilePath': 'sensorData.csv'
    })

    sensorCollection = [{
        'sensor': sensor,
        'valueExtractors': [
            #SensorValueExtractor(sensor, 'temp', SensorValueType['TEMPERATURE']),
            SensorValueExtractor(sensor, 'co2Value', SensorValueType['CO2']),
            #SensorValueExtractor(sensor, 'humid', SensorValueType['HUMIDITY'])
        ]
    }]
    azureIoTHub_telemetry_service = AzureIoTHubService('HostName=at-davemar-dipl.azure-devices.net;DeviceId=Raspberry_Floor;SharedAccessKey=rSRtoppf2TfMrE8+VvbHjTaKQeUShqX6VWh048nUT4g=')
    jsonPathConditionService = JsonPathConditionService('path-to-config-file.json')

    DeviceSensorsService.send_device_telemetry(azureIoTHub_telemetry_service, jsonPathConditionService, 'Raspberry_Floor', sensorCollection)