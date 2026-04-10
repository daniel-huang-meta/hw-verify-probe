import serial
import logging
from devices.base_device import BaseDevice
from utils.monitor_meta import ApiMonitorMeta

logger = logging.getLogger(__name__)

class SerialDevice(BaseDevice, metaclass=ApiMonitorMeta):
    """
    Standard Serial protocol implementation for ATP Platform.
    Supports USB-to-Serial and native COM ports.
    """
    def __init__(self, port: str, baudrate: int = 115200, timeout: int = 2, **kwargs):
        super().__init__(
            device_type="Serial_Instrument", 
            manufacturer="Generic", 
            model="UART_Device"
        )
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._serial = None

        # Immediate validation: check if the port is available
        if not self._check_port_exists():
            raise ConnectionError(f"Serial Error: Port '{port}' is not available or occupied.")

    def _check_port_exists(self) -> bool:
        """Check if the specified COM port exists on the system."""
        import serial.tools.list_ports
        ports = [p.device for p in serial.tools.list_ports.comports()]
        return self.port in ports

    def connect(self):
        """Open the serial port with specified parameters."""
        self._serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout
        )
        self.is_connected = True
        logger.info(f"Serial port {self.port} connected at {self.baudrate}bps.")

    def disconnect(self):
        if self._serial and self._serial.is_open:
            self._serial.close()
        self.is_connected = False

    def write(self, data: str):
        """Send raw string to serial port."""
        self._serial.write(f"{data}\n".encode('utf-8'))
        self._serial.flush()

    def read(self) -> str:
        """Read one line from serial port."""
        return self._serial.readline().decode('utf-8').strip()

    def execute_task(self, task_type: str, content: str, **kwargs) -> str:
        """
        Polymorphic interface for Serial tasks.
        Maps Excel 'Type' to Serial operations.
        """
        task_type = task_type.lower()
        if task_type == "write":
            self.write(content)
            return "Write Success"
        elif task_type == "read":
            return self.read()
        elif task_type == "query":
            # Send command and wait for response
            self.write(content)
            return self.read()

        raise NotImplementedError(f"SerialDevice does not support task: {task_type}")