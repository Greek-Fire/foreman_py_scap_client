import subprocess
import os
from packaging import version
from base_client import BaseClient

class Client(BaseClient):
    def __init__(self, config):
        super().__init__(config)
        self.tailored = False

    def policy_namespace(self):
        return 'ds'

    def policy_from_config(self):
        super_policy = super().policy_from_config()
        return super_policy or self.config.get(self.policy_id)

    def ensure_policy_exists(self):
        super().ensure_policy_exists()
        policy_config = self.policy_from_config()
        self.tailored = bool(policy_config.get('tailoring_path'))

    def ensure_scan_files(self):
        self.ensure_scan_file()
        if self.tailored:
            self.ensure_tailoring_file()

    def scan_command(self):
        profile = ''
        policy_config = self.config.get(self.policy_id)
        if policy_config and policy_config.get('profile'):
            profile = f"--profile {policy_config['profile']}"

        fetch_remote_resources = '--fetch-remote-resources' if self.config.get('fetch_remote_resources') else ''

        return (f"oscap xccdf eval {fetch_remote_resources} {self.local_files_subcommand()} "
                f"{profile} {self.tailoring_subcommand()} --results-arf {self.results_path} "
                f"{policy_config['content_path']}")

    def local_files_subcommand(self):
        if self.supports_local_file_option() and not self.config.get('fetch_remote_resources'):
            return '--local-files /root'
        return ''


    def supports_local_file_option(self):
        try:
            # Capture the version string from rpm query
            completed_process = subprocess.run(['rpm', '-q', '--qf', '%{version}', 'openscap'], capture_output=True, text=True, check=True)
            version_output = completed_process.stdout.strip()

            # Here we are assuming the version is in the format X.Y.Z
            # Extracting the major, minor, and patch numbers from the version string
            major, minor, patch = [int(part) for part in version_output.split('.')]

            # Check if the version is greater than or equal to 1.3.6
            if (major, minor, patch) >= (1, 3, 6):
                return True
            else:
                return False

        except subprocess.CalledProcessError:
            # Handle the scenario where the command execution fails, version parsing fails, or the 'openscap' package is not found.
            return False
        except ValueError:
            # Handle the scenario where version string splitting or integer conversion fails.
            return False

    def tailoring_subcommand(self):
        if self.tailored:
            return f"--tailoring-file {self.config[self.policy_id]['tailoring_path']}"
        return ''

    def upload_uri(self):
        return f"{self.foreman_proxy_uri()}/compliance/arf/{self.policy_id}"

    def ensure_scan_file(self):
        self.ensure_file('content_path', 'download_path', 'SCAP content')

    def ensure_tailoring_file(self):
        self.ensure_file('tailoring_path', 'tailoring_download_path', 'Tailoring file')

