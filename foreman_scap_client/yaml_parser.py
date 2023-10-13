class YamlParser:
    def __init__(self, content):
        self.content = content
        self.parsed_data = {}
        self.current_indentation = 0
        self.context_stack = [self.parsed_data]
        self.parse()

    def parse(self):
        lines = [line for line in self.content.split('\n') if line.strip() and not line.strip().startswith("#")]
        
        for line in lines:
            stripped_line = line.lstrip()
            indentation = len(line) - len(stripped_line)  # Count leading spaces

            if indentation > self.current_indentation:
                self.context_stack.append(self.context_stack[-1][self.current_key])
                self.current_indentation = indentation
            elif indentation < self.current_indentation and len(self.context_stack) > 1:
                while indentation < self.current_indentation and len(self.context_stack) > 1:
                    self.context_stack.pop()
                    self.current_indentation -= 2  # Assuming 2 spaces per indentation level

            if ": " in stripped_line:
                key, value = self.extract_key_value(stripped_line)
                self.context_stack[-1][key] = self.convert_value(value)
                self.current_key = key
            elif stripped_line.endswith(":"):
                key = stripped_line[:-1].strip()  # Remove trailing colon
                self.context_stack[-1][key] = {}
                self.current_key = key

    def extract_key_value(self, line):
        key, value = line.split(": ", 1)
        return key.strip(), value.strip()

    def convert_value(self, value):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.isdigit():
            return int(value)
        elif value.startswith("'") and value.endswith("'"):  # Remove quotes from strings
            return value[1:-1]
        elif value.startswith("[") and value.endswith("]"):  # Convert lists
            # Strip quotes from list elements
            return [elem.strip(' "').strip(' "') for elem in value[1:-1].split(":")]
        else:
            return value

    def get_data(self):
        return self.parsed_data

