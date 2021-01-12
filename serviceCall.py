import requests
import json

url = 'http://localhost:5555/'
postRequest = requests.post(url + 'calculate_zonal_stats')
print(postRequest.json())















