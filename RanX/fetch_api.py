import requests
from requests_cache import CachedSession
import time



def fetch_user(username:str, tag:str):
    url = f'https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}?force=false'
    headers = {
        "Accept": "application/json"
    }
    urls_expire_after = {
        url: -1,    
    }
    session = CachedSession('session', urls_expire_after=urls_expire_after, cache_control='no-cache')
    response = session.get(url, headers=headers)
    if response.json()['status']==200:
        return response.json()
    elif response.json()['status'] == 429:
        print('Rate limit exceeded, sleeping for 60 seconds')
        return -2
    else:
        print(response.json()['status'])
        return -1

def get_puuid(username:str, tag:str):
    data = fetch_user(username=username, tag=tag)
    if data is None:
        return None
    elif data == -1:
        return -1
    elif data == -2:
        return -2
    elif data['status'] == 200:
        puuid = data['data']['puuid']
        return puuid

def fetch_rank(puuid:str, episode = 'e8a1'):
    url = f'https://api.henrikdev.xyz/valorant/v2/by-puuid/mmr/eu/{puuid}?season={episode}'
    headers = {
        "Accept": "application/json"
    }
    urls_expire_after = {
        url: -1,
    }
    session = CachedSession('session_ranks', urls_expire_after=urls_expire_after, cache_control='no-cache')
    response = session.get(url, headers=headers)
    if response.json()['status'] == 200:
        return response.json()['data']['final_rank_patched']
    elif response.json()['status'] == 429:
        return -2
    else:
        return -1

def get_rr(puuid:str):
    url = f"https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/eu/{puuid}"
    headers = {
        "Accept": "application/json"
    }
    urls_expire_after = {
        url: -1,
    }
    session = CachedSession('session_rr', urls_expire_after=urls_expire_after, cache_control='no-cache')

    response = session.get(url, headers=headers)
    if response.json()['status'] == 200:
        return response.json()['data']['ranking_in_tier']
    elif response.json()['status'] == 429:
        return -2


def get_level(username:str,tag:str):
    return fetch_user(username,tag)['data']['account_level']