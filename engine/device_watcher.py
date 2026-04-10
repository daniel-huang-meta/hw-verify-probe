import time
import threading
import subprocess
import serial.tools.list_ports

class DeviceWatcher:
    def __init__(self, interval=2):
        self.interval = interval
        self.callbacks = []
        self._last_adb = set()
        self._last_serial = set()
        self._running = False

    def on_change(self, callback):
        """注册回调函数: callback(event_type, device_list)"""
        self.callbacks.append(callback)

    def _check(self):
        while self._running:
            # Check ADB
            current_adb = set(subprocess.check_output("adb devices").decode().splitlines()[1:])
            if current_adb != self._last_adb:
                self._notify("ADB_CHANGE", current_adb)
                self._last_adb = current_adb

            # Check Serial
            current_serial = set([p.device for p in serial.tools.list_ports.comports()])
            if current_serial != self._last_serial:
                self._notify("SERIAL_CHANGE", current_serial)
                self._last_serial = current_serial
            
            time.sleep(self.interval)

    def _notify(self, event_type, data):
        for cb in self.callbacks: cb(event_type, data)

    def start(self):
        self._running = True
        threading.Thread(target=self._check, daemon=True).start()