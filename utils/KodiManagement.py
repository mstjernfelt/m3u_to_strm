import urllib
import urllib.parse
import urllib.request
import json
import requests
import time

class Kodi:

    hostname = ""
    username = ""
    password = ""
    port = 8080
    url = ""
    request = None

    def __init__(self, hostname, username, password, port = 8080) -> None:
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

        self.url = f'http://{hostname}:{port}/jsonrpc'

        # Set up the request headers for authentication
        headers = {
            'Content-Type': 'application/json'
        }

        passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, f"{hostname}:{port}", username, password)

        auth_handler = urllib.request.HTTPBasicAuthHandler(passman)
        auth_handler.add_password(realm=None, uri=self.url, user=username, passwd=password)
        opener = urllib.request.build_opener(auth_handler)
        urllib.request.install_opener(opener)

        # Send the JSON-RPC request to Kodi
        self.request = urllib.request.Request(self.url, headers=headers)

    def UpdateVideoLibrary(self):
        # JSON-RPC method to trigger a media update
        method = 'VideoLibrary.Scan'

        # JSON-RPC parameters
        params = {'directory': ''}

        # JSON-RPC request payload
        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': 1
        }

        # Encode the payload as a byte string
        data = json.dumps(payload).encode('utf-8')

        response = urllib.request.urlopen(self.request, data=data)

        # Check if the response is successful
        if response.status == 200:
            print('Media library update triggered successfully.')
        else:
            print('Failed to trigger media library update.')
    
    def GetOnScanFinished(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "VideoLibrary.OnScanFinished",
            "params": {
                "event": "VideoLibrary.OnScanFinished"
            },
            "id": "1"
        }

        # Encode the payload as a byte string
        data = json.dumps(payload).encode('utf-8')

        # Wait for the media update to finish
        status = 'running'
        while status == 'running':
            response = urllib.request.urlopen(self.request, data=data)

            print(response)

            data = response.read()
            print(data)
            encoding = response.info().get_content_charset('utf-8')
            JSON_object = json.loads(data.decode(encoding))

            if response.status == 200 and 'error' not in JSON_object:
                status = response.json()['result']['status']
                print('Media library update status:', status)
            else:
                print('Failed to get media library update status.')
            time.sleep(1)

        print('Media library update complete.')