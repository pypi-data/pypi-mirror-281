import requests

BASE_URL = 'https://urchin-app-2-6chag.ondigitalocean.app'

def get_data(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.text  # Use response.text for string responses

def shorten_url(url):
    endpoint = f"shorten_url/{url}"
    return get_data(endpoint)
