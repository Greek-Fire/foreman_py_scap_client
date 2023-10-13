class YamlParser:
    def __init__(self, content):
        self.content = content
        self.parsed_data = {}
        self.parse()

    def parse(self):
        lines = [line for line in self.content.split('\n') if line and not line.strip().startswith("#")]
        current_key = None
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line.startswith(":"):
                current_key = stripped_line
                self.parsed_data[current_key] = {}
            else:
                key, value = self.extract_key_value(stripped_line)
                if current_key is None:
                    self.parsed_data[key] = value
                else:
                    self.parsed_data[current_key][key] = value

    def extract_key_value(self, line):
        if ": " in line:
            key, value = line.split(": ", 1)
            return key.strip(), self.convert_value(value.strip())
        else:
            return line.strip(), None

    def convert_value(self, value):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.isdigit():
            return int(value)
        else:
            return value

    def get_data(self):
        return self.parsed_data
