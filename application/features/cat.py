import requests


def get_cat_image():
    api_url = "https://api.thecatapi.com/v1/images/search"  # The API endpoint
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        if data:  # Ensure the response is not empty
            return data[0]["url"]  # Extract image URL
    return None

