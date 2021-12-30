import os
import unittest

import responses

from aiotomato.client import Client


def load_fixture(name: str) -> str:
    fixture_path = os.path.join(os.path.dirname(__file__), f"fixtures/{name}")
    with open(fixture_path) as fp:
        return fp.read()


class ClientTest(unittest.TestCase):
    @responses.activate
    def test_fetch_devices(self):
        payload = load_fixture("DEVLIST.txt")
        responses.add(responses.POST, "http://example.com:80/update.cgi", body=payload)

        client = ClientTest._get_client()
        result = client.fetch_devices()
        self.assertEqual(3, len(result))
        self.assertEqual("", result[0].name)
        self.assertEqual("192.168.1.30", result[0].ip)
        self.assertEqual("00:1E:06:48:AA:AC", result[0].mac)
        self.assertEqual("wifi-device-online", result[1].name)
        self.assertEqual("192.168.1.101", result[1].ip)
        self.assertEqual("00:1E:06:48:AA:AB", result[1].mac)
        self.assertEqual("some-device", result[2].name)
        self.assertEqual("192.168.1.100", result[2].ip)
        self.assertEqual("00:1E:06:48:AA:AA", result[2].mac)

    @staticmethod
    def _get_client() -> Client:
        return Client("example.com", "user", "pass", "http_id")
