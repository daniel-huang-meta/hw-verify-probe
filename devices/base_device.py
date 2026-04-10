from abc import ABC, abstractmethod
from datetime import datetime

class BaseDevice(ABC):
    """Root abstraction for all hardware devices."""
    def __init__(self, device_type: str, manufacturer: str, model: str):
        self.device_type = device_type
        self.manufacturer = manufacturer
        self.model = model
        self.version = "1.0.0"
        self.sn = "unknown"
        self.is_connected = False

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def execute_task(self, task_type: str, content: str, **kwargs) -> str:
        """Polymorphic interface to handle different command types."""
        pass

    def get_device_metadata(self) -> dict:
        """Standardized metadata for reporting."""
        return {
            "type": self.device_type,
            "vendor": self.manufacturer,
            "sn": self.sn,
            "status": "Online" if self.is_connected else "Offline",
            "timestamp": datetime.now().isoformat()
        }