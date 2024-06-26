import requests
import re

class WorldEditor:
    def __init__(self, file_path=None, text=None):
        self.file_path = file_path
        self.text = text
    
    def convert(self, file_type):
        if not self.file_path:
            raise ValueError("File path must be provided for conversion.")
        
        url = f"https://projectlumina.xyz/worldeditor/{file_type}"
        
        with open(self.file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files)
            return response.text
    
    def modify(self, key, new_value):
        if not self.file_path and not self.text:
            raise ValueError("Either file path or text content must be provided.")

        if self.file_path:
            with open(self.file_path, 'r') as file:
                content = file.read()
        elif self.text:
            content = self.text
        
        pattern = rf'{key}: (.*?),'
        replacement = f'{key}: {new_value},'
        modified_content = re.sub(pattern, replacement, content)

        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(modified_content)
        elif self.text:
            self.text = modified_content
            return self.text