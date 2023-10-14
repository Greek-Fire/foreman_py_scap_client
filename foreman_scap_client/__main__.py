# main.py

import argparse
import json
from yaml_parser import YamlParser  # make sure yaml_parser.py is in the same directory


def main():
    parser = argparse.ArgumentParser(description='YAML Parser')
    parser.add_argument('-f', '--file', dest='filepath', required=True, help='Path to the YAML file')

    args = parser.parse_args()
    filepath = args.filepath

    try:
        with open(filepath, 'r') as file:
            content = file.read()
            yaml_parser = YamlParser(content)
            x = yaml_parser.get_data()
            print(json.dumps(x,indent=2))
    except FileNotFoundError:
        print(f"File {filepath} not found.")
    except IOError as e:
        print(f"Error reading file {filepath}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
