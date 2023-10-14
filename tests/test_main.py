# tests/test_main.py

import unittest
from unittest.mock import patch
import sys
import json
from pathlib import Path

from foreman_scap_client.yaml_parser import YamlParser



class TestMain(unittest.TestCase):

    def test_expected_keys(self):
        config_path = Path(__file__).parent.parent / 'config' / 'config.yaml.example'
        with config_path.open() as f:
            content = f.read()

        parser = YamlParser(content)
        data = parser.get_data()

        expected_keys = [
            ':server',
            ':port',
            ':timeout',
            ':fetch_remote_resources',
            ':http_proxy_server',
            ':http_proxy_port',
            ':ca_file',
            ':host_certificate',
            ':host_private_key',
            ':ciphers'
        ]

        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, data)

    def test_expected_dicts(self):
        config_path = Path(__file__).parent.parent / 'config' / 'config.yaml.example'
        with config_path.open() as f:
            content = f.read()


        expected_dicts_keys = ['1', '2',':oval']

        parser = YamlParser(content)
        data = parser.get_data()

        for key in expected_dicts_keys:
            with self.subTest(key=key):
                self.assertIn(key, data)
                self.assertIsInstance(data[key], dict)

