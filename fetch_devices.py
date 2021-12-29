import os

from aiotomato.client import Client

client = Client(
    os.getenv("ROUTER_HOST", ""),
    os.getenv("ROUTER_USER", ""),
    os.getenv("ROUTER_PASS", ""),
    os.getenv("ROUTER_HTTP_ID", ""),
)

print(client.get_dev_list())
