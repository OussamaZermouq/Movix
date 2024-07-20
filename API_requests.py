import requests
import json
import wget
import urllib.parse


def fetch_data(name:str):
    response = requests.get(f"https://yts.mx/api/v2/list_movies.json?query_term={urllib.parse.quote(name)}")
    if response.ok:
        data = response.json()
        if 'movies' in data['data'] and data['data']['movies']:
            if 'torrents' in data['data']['movies'][0] and data['data']['movies'][0]['torrents']:
                return data
            else:
                print("No torrents available for the movie.")
                return -1
        else:
            print("No movies found in the response.")
            return -1
    else:
        print(f"Error: {response.status_code}")
        return -1


def get_cover(name:str):
    data = fetch_data(name)
    covers=[]
    for i in range(0,len(data['data']['movies'])):
        covers.append(data['data']['movies'][i]['medium_cover_image'])
    return covers


def get_download_link(name:str):
    
    data = fetch_data(name)
    if data ==-1:
        print('An error has occured.')
        
    else:
        releases = []
        links = {}

        for j in range(0, len(data['data']['movies'])):
            movie_title = data['data']['movies'][j]['title']
            torrents = data['data']['movies'][j]['torrents']

            for i in range(0, len(torrents)):

                torrent_url = torrents[i]['url']
                quality = torrents[i]['quality']
                release_type = torrents[i]['type']
                codec = torrents[i]['video_codec']
                
                links = {'title': movie_title + " " +  quality  + " " +  release_type + " " +  codec, 
                             'url': torrent_url}
                releases.append(links)
            
        return releases



def download_file(url:str, format:str, filename:str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        content = response.read()
    with open(f"./files/{filename}.{format}", "wb") as f:
        f.write(content)
    print(f"Download complete from {url}")


def fetch_stream_link_movie(movie_code:str):
    url = f'https://vidsrc.to/embed/movie/{movie_code}'
    print(url)
    req = requests.get(url)
    if req.status_code == 200:
        return url
    else:
        return 404




