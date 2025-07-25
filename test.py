import requests

headers = {
    "Authorization": "fsq3eyCr2Y5W4KxYIl62Np7FG4KTNVDURyyF+cpdm23zKGA=",
    "accept": "application/json"
}

url = "https://api.foursquare.com/v3/places/search?ll=41.7151,44.8271&limit=3"
response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print("Data:", response.text)