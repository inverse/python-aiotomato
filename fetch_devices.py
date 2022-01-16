import os

from aiotomato.client import Client

client = Client(
    os.getenv("ROUTER_HOST", ""),
    os.getenv("ROUTER_USER", ""),
    os.getenv("ROUTER_PASS", ""),
    os.getenv("ROUTER_HTTP_ID", ""),
)

for device in client.fetch_devices():
    print(f"name: {device.name}")
    print(f"ip: {device.ip}")
    print(f"mac: {device.mac}")
    print(f"is_online: {device.is_online}")
