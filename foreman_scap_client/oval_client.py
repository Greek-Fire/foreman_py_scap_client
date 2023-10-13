import subprocess
import json
from base_client import BaseClient

class OvalClient(BaseClient):

    def __init__(self, config):
        super().__init__(config)
        self.policy_namespace = "oval"

    def ensure_scan_files(self):
        self.ensure_file("content_path", "download_path", "OVAL content")

    def upload_uri(self):
        return f"{self.foreman_proxy_uri}/compliance/oval_reports/{self.policy_id}"

    def scan_command(self):
        return f"oscap oval eval --results {self.results_path} {self.policy_from_config['content_path']}"

    def print_upload_result(self, response_content):
        parsed = json.loads(response_content)
        if 'reported_at' in parsed:
            print(f"Report successfully uploaded at {parsed['reported_at']}")
        else:
            print(f"Report not uploaded, cause: {parsed['result']}")

