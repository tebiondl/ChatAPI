import requests
import json

endpoint = "generate"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
}

data = {"prompt": "Once upon a time"}
json_data = json.dumps(data)

response = requests.post("http://127.0.0.1:5000/" + endpoint, data=json_data, headers=headers)

print(response.json())