from sensor_value import SensorValueType

class ISensor:

    def refresh_data():
        pass

    def get_data(self, sensorValueType : SensorValueType):
        pass

    def get_name(self):
        pass

    def get_data_timestamp(self):
        pass