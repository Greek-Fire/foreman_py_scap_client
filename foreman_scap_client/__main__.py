# foreman_scap_client/__main__.py
import sys
import argparse
from .client import Client  # Assuming Client is your main class

def main():
    # Create a parser for handling command line arguments
    parser = argparse.ArgumentParser(description='Foreman SCAP client for compliance reporting')
    parser.add_argument('policy_id', type=int, help='The ID of the policy to be used')

    # Add any additional arguments you need here...

    # Parse arguments
    args = parser.parse_args()

    # Create an instance of your client class
    client = Client(policy_id=args.policy_id)

    # Here, you would have methods on your Client to execute whatever action is needed
    # For example, if you have a method in your Client class to start the scan, you'd do:
    client.execute_scan()

if __name__ == '__main__':
    main()

