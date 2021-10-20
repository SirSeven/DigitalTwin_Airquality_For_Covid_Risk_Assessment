import csv

from sensor_value.SensorValueType import SensorValueType
from . import ISensor


class CsvValuesSensor(ISensor):

    def __init__(self, configObject):
        self.name = configObject['Name']
        self.sensorData = self.__parse_csv(configObject['CsvFilePath'])
        self.index = 0

    def refresh_data(self):
        if(self.index > len(self.sensorData)):
            self.index = 0

        data = self.sensorData[self.index]
        self.currentSensorData = data

        self.index += 1

    def get_data(self, sensorProperty : SensorValueType):
        if(sensorProperty == SensorValueType['TEMPERATURE']):
            return self.currentSensorData['temperature']
        elif(sensorProperty == SensorValueType['CO2']):
            return self.currentSensorData['co2']
        elif(sensorProperty == SensorValueType['HUMIDITY']):
            return self.currentSensorData['humidity']
        
        raise Exception('unsupported sensor value type')

    def get_name(self):
        return self.name

    def __parse_csv(self, csvFilePath):
        # read csv file
        with open(csvFilePath, encoding='utf-8') as csvFile:
            # load csv file data using csv library's dictionary reader
            csvReader = csv.DictReader(csvFile)
            data = []
            for rows in csvReader:
                data.append(rows)

            return data
