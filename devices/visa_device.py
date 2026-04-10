import pyvisa
from base_device import BaseDevice
from utils.monitor_meta import ApiMonitorMeta

class VisaDevice(BaseDevice, metaclass=ApiMonitorMeta):
    def __init__(self, resource_name: str, **kwargs):
        super().__init__(device_type="Instrument", manufacturer="Generic", model="VISA_Device")
        self.resource_name = resource_name
        self.rm = pyvisa.ResourceManager()
        self.instr = None

    def connect(self):
        self.instr = self.rm.open_resource(self.resource_name)
        self.is_connected = True

    def execute_task(self, task_type: str, content: str, **kwargs) -> str:
        if task_type == "query":
            return self.instr.query(content)
        elif task_type == "write":
            self.instr.write(content)
            return "Write Success"
        raise NotImplementedError(f"VISA doesn't support {task_type}")