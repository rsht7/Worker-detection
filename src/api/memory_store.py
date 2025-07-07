from threading import Lock
from typing import Dict
import queue


class MemoryStore:
    def __init__(self):
        self.zone_data_store: Dict[str, dict] = {}
        self.alert_streams: Dict[str, queue.Queue] = {}
        self.lock = Lock()

    def set_zone_data(self, camera_id: str, zone_data: dict):
        with self.lock:
            self.zone_data_store[camera_id] = zone_data

    def get_zone_data(self, camera_id: str) -> dict | None:
        with self.lock:
            return self.zone_data_store.get(camera_id)

    def push_alert(self, camera_id: str, alert: dict):
        if camera_id not in self.alert_streams:
            self.alert_streams[camera_id] = queue.Queue()
        self.alert_streams[camera_id].put(alert)

    def get_alert_stream(self, camera_id: str):
        if camera_id not in self.alert_streams:
            self.alert_streams[camera_id] = queue.Queue()
        return self.alert_streams[camera_id]
