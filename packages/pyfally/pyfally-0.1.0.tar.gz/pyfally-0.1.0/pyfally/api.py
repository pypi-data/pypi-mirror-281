import requests

class FlaskAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url)
        response.raise_for_status()
        return response.text  # Use response.text for string responses

    def post_data(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.text  # Use response.text for string responses

    def shorten_url(self , url):
        return ( self.get_data(f"shorten_url/{url}") )