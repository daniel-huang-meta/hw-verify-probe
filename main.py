import click
import logging
import sys
from pathlib import Path
from app.batch_cmd import BatchCmdRunner
from engine.device_operator import DeviceOperator
from engine.device_watcher import DeviceWatcher
from devices.coex_fixture import CoexFixture
from devices.adb_device import AdbDevice

# 针对 MacOS 的日志美化
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

@click.group()
def cli():
    """Hardware Verify Probe (HVP) - 硬件验证工具 MacOS 版"""
    pass

@cli.command()
@click.option('--file', '-f', type=click.Path(exists=True), required=True, help='指令 Excel/CSV 文件')
@click.option('--dev_type', '-d', type=click.Choice(['fixture', 'adb', 'serial', 'visa']), default='fixture')
@click.option('--host', default='192.168.1.100', help='工装 IP 地址')
def run(file, dev_type, host):
    """批量执行硬件验证指令"""
    click.secho(f"🔎 正在通过 {dev_type} 模式运行探测任务: {file}", fg='blue', bold=True)
    try:
        if dev_type == 'fixture':
            device = CoexFixture(host=host, port=8080)
        else:
            device = AdbDevice() # 内部已含重写后的检测逻辑
            
        device.connect()
        operator = DeviceOperator(device)
        runner = BatchCmdRunner(operator)
        
        click.secho(f"🚀 开始执行: {Path(file).name}", fg='cyan', bold=True)
        runner.run_file(file)
        click.secho("✅ 所有任务执行完毕", fg='green')
        
    except Exception as e:
        click.secho(f"❌ 运行失败: {e}", fg='red', err=True)
    finally:
        if 'device' in locals():
            device.disconnect()

@cli.command()
def watch():
    """监听 MacOS 端口变化 (ADB/USB-Serial)"""
    watcher = DeviceWatcher()
    
    def on_change(dtype, added, removed):
        for item in added:
            click.secho(f"✨ 发现设备: {item} ({dtype})", fg='green')
        for item in removed:
            click.secho(f"🔌 设备断开: {item} ({dtype})", fg='yellow')

    watcher.register_handler(on_change)
    click.echo("👀 正在监听设备状态... (按 Ctrl+C 停止)")
    watcher.start()
    
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("\n停止监听。")

if __name__ == '__main__':
    cli()