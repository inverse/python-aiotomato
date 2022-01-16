# AIOTomato

![CI](https://github.com/inverse/python-aiotomato/workflows/CI/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple and limited wrapper for Tomato based router firmwares such as [FreshTomato][0].

It's limited to only WIFI enabled devices due to what the API provides.

## Usage

Below is an example of how it can be used to print out a list of devices and get their online status.

```python
import os

from aiotomato.client import Client

client = Client(
    os.getenv("ROUTER_HOST", ""),
    os.getenv("ROUTER_USER", ""),
    os.getenv("ROUTER_PASS", ""),
    os.getenv("ROUTER_HTTP_ID", ""),
)

print(client.fetch_devices())
```

Where the HTTP ID can be obtained by inspecting the source code when logged into the admin inteface of the router searching for `http_id`.

## Licence

MIT

[0]: https://freshtomato.org/
