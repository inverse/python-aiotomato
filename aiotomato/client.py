import json
import logging
import re
from dataclasses import dataclass
from typing import List

import requests
from requests.auth import HTTPBasicAuth

_LOGGER = logging.getLogger(__name__)


class Commands:
    DEVLIST = "devlist"
    NETDEV = "netdev"


@dataclass
class Device:
    name: str
    ip: str
    mac: str
    is_online: bool


class Client:
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        http_id: str,
        port: int = 80,
        use_ssl: bool = False,
        verify_ssl: bool = True,
    ):
        self.host = host
        self.username = username
        self.password = password
        self.http_id = http_id
        self.port = port
        self.use_ssl = use_ssl
        self.verify_ssl = verify_ssl
        self.parse_api_pattern = re.compile(r"(?P<param>\w*) = (?P<value>.*);")

    def fetch_devices(self) -> List[Device]:
        response = self._make_request(Commands.DEVLIST)
        data = {}
        for param, value in self.parse_api_pattern.findall(response):
            data[param] = json.loads(value.replace("'", '"'))

        result = []
        for item in data.get("dhcpd_lease", []):
            matched_online = [
                device for device in data.get("wldev", []) if device[1] == item[2]
            ]
            result.append(Device(item[0], item[1], item[2], len(matched_online) != 0))

        return result

    def _make_request(self, command: str) -> str:
        request = requests.Request(
            "POST",
            f"http{'s' if self.use_ssl else ''}://{self.host}:{self.port}/update.cgi",
            data={"_http_id": self.http_id, "exec": command},
            auth=HTTPBasicAuth(self.username, self.password),
        ).prepare()

        if self.use_ssl:
            response = requests.Session().send(
                request, timeout=3, verify=self.verify_ssl
            )
        else:
            response = requests.Session().send(request, timeout=3)

        response.raise_for_status()

        return response.content.decode("utf-8")
