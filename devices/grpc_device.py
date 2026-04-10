import grpc
from base_device import BaseDevice
from utils.monitor_meta import ApiMonitorMeta

class GrpcDevice(BaseDevice, metaclass=ApiMonitorMeta):
    def __init__(self, target: str, stub_class, **kwargs):
        super().__init__(device_type="gRPC_Service", manufacturer="Generic", model="gRPC_Node")
        self.target = target
        self.stub_class = stub_class
        self.channel = None
        self.stub = None

    def connect(self):
        self.channel = grpc.insecure_channel(self.target)
        self.stub = self.stub_class(self.channel)
        self.is_connected = True

    def execute_task(self, task_type: str, content: str, **kwargs) -> str:
        # 假设 task_type 是 RPC 方法名，content 是参数
        method = getattr(self.stub, task_type)
        response = method(kwargs.get("request_obj")) # 根据实际 proto 定义调整
        return str(response)

    def disconnect(self):
        if self.channel: self.channel.close()