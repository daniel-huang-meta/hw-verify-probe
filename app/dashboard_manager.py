import json
from datetime import datetime

class TestDataSchema:
    """定义 Dashboard 接收的数据标准"""
    def __init__(self, device):
        self.meta = device.get_device_metadata()
        self.start_time = datetime.now().isoformat()
        self.steps = []

    def add_step(self, name, status, output, extra=None):
        self.steps.append({
            "step": name,
            "status": status,
            "data": output,
            "extra": extra
        })

    def to_json(self):
        return json.dumps({
            "fixture_id": "COEX_BOX_01",
            "device_info": self.meta,
            "test_time": self.start_time,
            "results": self.steps
        })