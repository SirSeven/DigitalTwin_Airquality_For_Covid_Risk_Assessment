import DeviceSensorsService
from sensor_value import SensorValueExtractor, SensorValueType
from telemetry_services import AzureIoTHubService
from sensors import CsvValuesSensor

if __name__ == '__main__':
    sensor = CsvValuesSensor({
        'Name': 'test-sensor',
        'CsvFilePath': 'sensorData.csv'
    })

    sensorCollection = [{
        'sensor': sensor,
        'valueExtractors': [
            SensorValueExtractor(sensor, 'temp', SensorValueType['TEMPERATURE']),
            SensorValueExtractor(sensor, 'co2', SensorValueType['CO2']),
            SensorValueExtractor(sensor, 'humid', SensorValueType['HUMIDITY'])
        ]
    }]
    azureIoTHub_telemetry_service = AzureIoTHubService('HostName=at-davemar-dipl.azure-devices.net;DeviceId=Arduino321;SharedAccessKey=W+OkySOxpziDTVPyWg5xmFDGQ1gUSxVovIUfejOglhI=')

    DeviceSensorsService.send_device_telemetry(azureIoTHub_telemetry_service, 'test-device', sensorCollection)