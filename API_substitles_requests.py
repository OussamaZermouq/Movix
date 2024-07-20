import requests
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()
token_bearer = os.getenv('OPENSUB_BEARER')
api_token = os.getenv('OPEN_API_TOKEN')

token = token_bearer

def fetch_subtitle(imdb_id: str, language: str):

    url = "https://api.opensubtitles.com/api/v1/subtitles"

    querystring = {
        "imdb_id": f"{urllib.parse.quote(imdb_id)}",
        "languages": f"{language}"
    }

    headers = {
        "Api-Key": f"{api_token}",
        "User-Agent": "Movix v1.0.0"
    }

    try:
        response = requests.get(url=url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")

subs = fetch_subtitle('tt15398776','en')['data']
for sub in subs:
    print(sub['id'])