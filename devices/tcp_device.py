import socket
from devices.base_device import BaseDevice

class TcpDevice(BaseDevice):
    """Base class for TCP communication."""
    def __init__(self, host: str, port: int, **kwargs):
        super().__init__(**kwargs)
        self.host = host
        self.port = port
        self._sock = None

    def connect(self):
        self._sock = socket.create_connection((self.host, self.port), timeout=10)
        self.is_connected = True

    def disconnect(self):
        if self._sock: self._sock.close()
        self.is_connected = False

    def transport(self, data: str) -> str:
        self._sock.sendall(data.encode())
        return self._sock.recv(4096).decode()