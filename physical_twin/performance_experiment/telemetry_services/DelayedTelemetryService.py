from datetime import datetime
import time
from . import ITelemetryService


class DelayedTelemetryService(ITelemetryService):
    messagesProcessed = 0

    def __init__(self, delayInMs):
        self.delayInMs = delayInMs

    def send_data(self, device_id: str, sensor_id: str, sensor_property_name: str, data_timestamp: datetime, sensor_data):
        time.sleep(self.delayInMs/1000)
        DelayedTelemetryService.messagesProcessed += 1