
if sys.version_info[0] < 3:
    # Python 2
    import httplib
    from urlparse import urlparse
else:
    # Python 3
    import http.client as httplib
    from urllib.parse import urlparse

import sys
import os
import json
import ssl

class ForemanScapWebInterface:
    def __init__(self, config, policy_id, results_bzip_path):
        self.config = config
        self.policy_id = policy_id
        self.results_bzip_path = results_bzip_path

    def http_proxy_uri(self):
        if not self.config.get('http_proxy_server') or not self.config.get('http_proxy_port'):
            return None
        http_proxy_server = self.config['http_proxy_server']
        http_proxy_port = self.config['http_proxy_port']
        return f"http://{http_proxy_server}:{http_proxy_port}"

    def upload_uri(self):
        return f"{self.config['foreman_proxy_uri']}/compliance/arf/{self.policy_id}"

    def upload(self):
        uri = urlparse(self.upload_uri())
        print(f"Uploading results to {uri.geturl()}")

        # Setup SSL Context
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=self.config.get('host_certificate'), keyfile=self.config.get('host_private_key'))
        if self.config.get('ca_file'):
            ssl_context.load_verify_locations(cafile=self.config.get('ca_file'))
        if self.config.get('ciphers'):
            ssl_context.set_ciphers(self.config['ciphers'])

        # Create connection
        connection = http.client.HTTPSConnection(uri.hostname, uri.port, context=ssl_context)
        if self.config.get('timeout'):
            connection.timeout = self.config['timeout']

        # Read and upload file
        try:
            with open(self.results_bzip_path, "rb") as f:
                file_content = f.read()
            
            headers = {
                'Content-Type': 'text/xml',
                'Content-Encoding': 'x-bzip2'
            }
            connection.request("POST", uri.path, body=file_content, headers=headers)

            response = connection.getresponse()
            print(f"Status: {response.status}")
            print(f"Response: {response.read().decode()}")

        except Exception as e:
            print(f"Upload failed: {str(e)}")
            sys.exit(4)

        connection.close()
