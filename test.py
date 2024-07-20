import requests

url = "https://api.themoviedb.org/3/movie/872585/recommendations?language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NTc4N2M2NTNiYWIzM2Y1OGVhYjlhNzc0NmZmNTU0MiIsIm5iZiI6MTcxOTM1ODMxNC41NzY2OTUsInN1YiI6IjY1MzNkM2IwNDJkODM3MDBlYWM1ODNkMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.GpBsoWQ2EpjA_zKpeVvexVJ3G9xv64c97xZrpQCNJdw"
}

response = requests.get(url, headers=headers)

print(response.text)