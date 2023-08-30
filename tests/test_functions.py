import unittest
from data.functions import get_plug_status, enable_plug, disable_plug
from pprint import pprint


class TestFunctions(unittest.TestCase):
    def test_plug_status(self):
        keys = ["power", "Ws", "relay", "temperature"]
        status = get_plug_status("10.0.0.35")
        for key in keys:
            self.assertIn(key, status)
    def test_plug_enable(self):
        response = enable_plug("10.0.0.35")
        assert(response, 200)
    def test_enable_plug(self):
        response = enable_plug("10.0.0.35")
        assert(response, True)
    def test_disable_plug(self):
        response = disable_plug("10.0.0.35")
        assert(response, True)
