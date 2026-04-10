import ast
import logging
from devices.tcp_device import TcpDevice
from utils.monitor_meta import ApiMonitorMeta

logger = logging.getLogger(__name__)

class CoexFixture(TcpDevice, metaclass=ApiMonitorMeta):
    """
    Renamed Fixture class for Coexistence testing.
    Inherits automated retry, CSV logging, and alarm triggers.
    """
    # Methods excluded from auto-retry to prevent recursion or unnecessary overhead
    _EXCLUDE_FROM_MONITOR = ["signal_light_on", "disconnect", "get_device_metadata"]

    def __init__(self, host: str, port: int):
        super().__init__(
            host=host, 
            port=port, 
            device_type="Fixture", 
            manufacturer="CoexTech", 
            model="CoexBox_V2"
        )

    def on_api_final_failure(self, api_name: str, error: Exception):
        """
        Triggered by ApiMonitorMeta after 3 failed attempts.
        Standard safety protocol: turn on the red alert light.
        """
        logger.error(f"CRITICAL FAILURE in {api_name}: {error}. Activating Alarm.")
        try:
            self.signal_light_on("red")
        except Exception as e:
            logger.critical(f"Failed to activate alarm light: {e}")

    def execute_task(self, task_type: str, content: str, **kwargs) -> str:
        """
        Universal entry point for the Validation Engine.
        Maps Excel/CSV 'Type' to internal API methods.
        """
        task_type = task_type.lower()
        if task_type == "api":
            # Uses reflection to call methods like 'init' or 'move_x'
            method = getattr(self, content, None)
            if method:
                return str(method(**kwargs))
            raise AttributeError(f"API '{content}' not found in CoexFixture")
        
        elif task_type == "raw":
            return self.transport(content)
            
        raise NotImplementedError(f"CoexFixture does not support task: {task_type}")

    def execute(self, cmd: str):
        """Internal helper to send commands and validate status."""
        raw_resp = self.transport(cmd)
        resp = ast.literal_eval(raw_resp)
        if not resp[0]:
            raise RuntimeError(f"Fixture reported error: {resp[1]}")
        return resp

    def init(self, **kwargs):
        """Reset all motors to home position."""
        return self.execute("all_motor_home")

    def signal_light_on(self, color: str, **kwargs):
        """Activate signal tower light."""
        return self.execute(f"{color}_light")