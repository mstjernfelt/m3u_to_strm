import requests
import json
import time

url = "http://localhost:8080/jsonrpc" # Replace with your Kodi IP address and port number
headers = {"Content-Type": "application/json"}

# First, we need to enable the event listener
data = {
    "jsonrpc": "2.0",
    "method": "JSONRPC.Subscribe",
    "params": {
        "event": "VideoLibrary.OnScanFinished"
    },
    "id": "1"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("Subscribed to VideoLibrary.OnScanFinished events")
else:
    print("Error: ", response.status_code)

# Now we wait for the event to be triggered
while True:
    data = {
        "jsonrpc": "2.0",
        "method": "JSONRPC.Ping",
        "id": "1"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()["result"]

        if "VideoLibrary.OnScanFinished" in result:
            print("Video library scan finished")
            break

    time.sleep(1)
