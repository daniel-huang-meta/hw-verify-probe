import subprocess
import os
import logging
from devices.base_device import BaseDevice
from utils.monitor_meta import ApiMonitorMeta

logger = logging.getLogger(__name__)

class AdbDevice(BaseDevice, metaclass=ApiMonitorMeta):
    """
    Independent ADB device implementation handling both USB and TCP-based ADB connections.
    """
    def __init__(self, serial: str = None, **kwargs):
        # Initialize BaseDevice metadata
        super().__init__(
            device_type="HMD", 
            manufacturer="Meta",
            model="EVT1"
        )
        self.serial = serial
        self._prefix = f"adb -s {serial}" if serial else "adb"

        # Validate device existence immediately
        if not self._is_device_available():
            error_msg = f"ADB Connection Error: Device '{serial or 'default'}' not found. Please check USB/Network connection."
            logger.error(error_msg)
            raise ConnectionError(error_msg)

    def _is_device_available(self) -> bool:
        """Checks if the device is listed in 'adb devices'."""
        try:
            res = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
            if self.serial:
                return self.serial in res.stdout
            # If no serial, check if any device is in 'device' state
            lines = [line for line in res.stdout.strip().split('\n')[1:] if 'device' in line]
            return len(lines) > 0
        except FileNotFoundError:
            raise RuntimeError("ADB executable not found. Please install ADB and add it to PATH.")

    def connect(self):
        """Finalize state and cache the hardware SN."""
        self.sn = self.shell("getprop ro.serialno")
        self.is_connected = True
        logger.info(f"ADB Device {self.sn} initialized.")

    def disconnect(self):
        self.is_connected = False

    def shell(self, command: str) -> str:
        """Execute adb shell command."""
        res = subprocess.run(f"{self._prefix} shell {command}", shell=True, capture_output=True, text=True)
        return res.stdout.strip()

    def pull(self, remote: str, local: str) -> str:
        """Transfer file from device to local machine."""
        res = subprocess.run(f"{self._prefix} pull {remote} {local}", shell=True, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"ADB Pull failed: {res.stderr}")
        return f"File pulled to {local}"

    def screenshot(self, local_path: str) -> str:
        """Capture screen and save to local path."""
        remote_tmp = "/data/local/tmp/temp_screenshot.png"
        self.shell(f"screencap -p {remote_tmp}")
        return self.pull(remote_tmp, local_path)

    def execute_task(self, task_type: str, content: str, **kwargs) -> str:
        """Polymorphic entry point for the Validation Engine."""
        task_type = task_type.lower()
        if task_type == "shell":
            return self.shell(content)
        elif task_type == "pull":
            return self.pull(content, kwargs.get('Local_Path', './output.file'))
        elif task_type == "screenshot":
            return self.screenshot(content)
        elif task_type == "push":
            remote = kwargs.get('Remote_Path', '/data/local/tmp/')
            subprocess.run(f"{self._prefix} push {content} {remote}", shell=True, check=True)
            return "Push Success"
        raise NotImplementedError(f"AdbDevice logic for {task_type} is not defined.")