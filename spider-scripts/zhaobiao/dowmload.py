import requests

def download(url):
    """
    Downloads a file from the given URL and saves it to the current directory.

    Args:
        url (str): The URL of the file to download.

    Returns:
        str: The path of the downloaded file.
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the filename from the URL
        return response.content