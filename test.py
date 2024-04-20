import requests

url = "https://api.opensubtitles.com/api/v1/download"

payload = { 
    "file_id": 6744514 
    }

headers = {
    "User-Agent": "Movix",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI0SXd6bFNSVWx6aDVIbk1jdTBSU1BXYmxOTE43U2NGVCIsImV4cCI6MTcwMDM5ODA3N30.bbT4c1MB4k8TjjFff_PnRhzKVzoTjBv4mL9nK46B9M8"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())



#token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI0SXd6bFNSVWx6aDVIbk1jdTBSU1BXYmxOTE43U2NGVCIsImV4cCI6MTcwMDM5ODA3N30.bbT4c1MB4k8TjjFff_PnRhzKVzoTjBv4mL9nK46B9M8