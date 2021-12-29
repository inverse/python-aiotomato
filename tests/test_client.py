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
    def test_get_dev_list(self):
        payload = load_fixture("DEVLIST.txt")
        responses.add(responses.POST, "http://example.com:80/update.cgi", body=payload)

        client = ClientTest._get_client()
        result = client.get_dev_list()
        self.assertEqual(2, len(result))

    @staticmethod
    def _get_client() -> Client:
        return Client("example.com", "user", "pass", "http_id")
