import requests

class Api:
    @staticmethod
    def fetch(endpoint):
        url = f"https://projectlumina.xyz/shortcut/{endpoint}"
        response = requests.get(url)

        if response.status_code != 200:
            raise ValueError(f"Failed to fetch {endpoint}: Status code {response.status_code}")
        
        ext = endpoint.split('.')[-1].lower()
        
        if ext == 'json':
            return response.json()
        elif ext == 'txt':
            return response.text
        else:
            return response.content

    @property
    def about(self):
        return self.fetch('about.txt')

    @property
    def connections(self):
        return self.fetch('connections.json')

    @property
    def options(self):
        return self.fetch('options.json')

    @property
    def packs(self):
        return self.fetch('packs.json')

    @property
    def releases(self):
        return self.fetch('releases.json')