# Required Python standard libraries similar to Ruby's
import os
import sys
import json
import tempfile
import subprocess
import http.client
from urllib.parse import urlparse
import ssl

# Assuming yaml_parser.py is in the same directory
from yaml_parser import YamlParser

class ForemanScapClientBase:
    CONFIG_FILE = '/etc/foreman_scap_client/config.yaml'

    def __init__(self):
        self.policy_id = None
        self.config = None
        self.tmp_dir = None
        self.report = None

    def run(self, policy_id, skip_upload=False):
        self.policy_id = policy_id
        self.load_config()
        self.ensure_scan_files()
        self.run_in_tmpdir(skip_upload)

    def load_config(self):
        try:
            with open(self.CONFIG_FILE, 'r') as stream:
                file_content = stream.read()
                parser = YamlParser(file_content)
                self.config = parser.get_data()
                self.ensure_policy_exists()
        except Exception as e:
            print('Config file could not be loaded')
            print(e)
            sys.exit(1)

    def ensure_policy_exists(self):
        if not self.policy_from_config():
            print(f"Policy id {self.policy_id} not found.")
            sys.exit(1)

    def policy_from_config(self):
        # Navigate through the nested configuration dictionary safely
        return self.config.get(self.policy_namespace(), {}).get(self.policy_id)

    # These methods should be implemented in the derived classes
    def ensure_scan_files(self):
        raise NotImplementedError("The 'ensure_scan_files' method must be implemented in the subclass.")

    def policy_namespace(self):
        raise NotImplementedError("The 'policy_namespace' method must be implemented in the subclass.")

    def upload_uri(self):
        raise NotImplementedError("The 'upload_uri' method must be implemented in the subclass.")

    def scan_command(self):
        raise NotImplementedError("The 'scan_command' method must be implemented in the subclass.")

    def run_in_tmpdir(self, skip_upload):
        if skip_upload:
            self.tmp_dir = tempfile.mkdtemp()
            self.scan()
            self.bzip()
        else:
            with tempfile.TemporaryDirectory() as dir:
                self.tmp_dir = dir
                self.scan()
                self.bzip()
                self.upload()

    def scan(self):
        command = self.scan_command()
        env_vars = self.scan_command_env_vars()
        print(f"DEBUG: running: {command}")
        if env_vars:
            print(f"with ENV vars: {env_vars}")

        # Python's subprocess can be used as an equivalent to Ruby's Open3
        process = subprocess.Popen(command, env=env_vars, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout_str, error_str = process.communicate()
        result = process.returncode
        # Mimicking the specific behavior of the original script with return codes
        if result == 0 or result == 2:
            filtered_errors = '\n'.join(
                [item for item in error_str.decode().split('\n') if item.startswith('WARNING:') or item.startswith('Downloading')]
            )
            print(filtered_errors)
            self.report = self.results_path()
        else:
            print('Scan failed')
            print(stdout_str.decode())
            print(error_str.decode())
            sys.exit(2)

    def scan_command_env_vars(self):
        if self.http_proxy_uri():
            return {
                'HTTP_PROXY': self.http_proxy_uri(),
                'HTTPS_PROXY': self.http_proxy_uri()
            }
        else:
            return {}

    def http_proxy_uri(self):
        if 'http_proxy_server' in self.config and 'http_proxy_port' in self.config:
            http_proxy_server = self.config['http_proxy_server']
            http_proxy_port = self.config['http_proxy_port']
            return f"http://{http_proxy_server}:{http_proxy_port}"
        return None

    def results_path(self):
        return os.path.join(self.tmp_dir, 'results.xml')

    def results_bzip_path(self):
        return f"{self.results_path()}.bz2"

    def bzip_command(self):
        return f"/usr/bin/env bzip2 {self.results_path()}"

    def bzip(self):
        command = self.bzip_command()
        print(f'DEBUG: running: {command}')
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print('bzip failed')
            print(result.stdout.decode())
           

