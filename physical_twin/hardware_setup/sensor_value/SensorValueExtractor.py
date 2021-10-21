from sensors import ISensor
from . import SensorValueType

class SensorValueExtractor:

    def __init__(self, sensor:ISensor, propertyName: str, propertyValueType: SensorValueType):
        self.sensor = sensor
        self.propertyName = propertyName
        self.propertyValueType = propertyValueType

    def get_value(self):
        return {
            'sensor_id': self.sensor.get_name(),
            'property_name': self.propertyName,
            'property_value': self.sensor.get_data(self.propertyValueType)
        }