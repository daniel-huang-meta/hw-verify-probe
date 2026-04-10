import logging
from devices.base_device import BaseDevice

logger = logging.getLogger(__name__)

class DeviceOperator:
    """
    Core controller responsible for executing a single task on a device and validating the output.
    """
    def __init__(self, device: BaseDevice):
        self.device = device

    def execute_and_verify(self, task_type: str, content: str, expect: str = None, **kwargs) -> dict:
        """
        Executes a specific task and returns a standardized result dictionary.
        """
        try:
            # Polymorphic execution via the device's execute_task
            actual_res = self.device.execute_task(task_type, content, **kwargs)

            # Validation logic
            status = "PASS"
            if expect and str(expect).lower() != 'nan':
                if str(expect) not in str(actual_res):
                    status = "FAIL"

            return {
                "status": status,
                "actual": actual_res,
                "error": None
            }
        except Exception as e:
            logger.error(f"Operation failed on {self.device.model}: {e}")
            return {
                "status": "ERROR",
                "actual": None,
                "error": str(e)
            }