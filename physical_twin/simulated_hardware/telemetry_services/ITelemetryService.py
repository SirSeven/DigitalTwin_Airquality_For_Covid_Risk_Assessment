import json
from datetime import datetime


class ITelemetryService:

    def send_data(self, device_id: str, sensor_id: str, sensor_property_name: str, data_timestamp: datetime, sensor_data: str):
        pass
