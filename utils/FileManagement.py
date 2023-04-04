import urllib.request
import os
import re

class FileManagement():
    def get_m3u_file(url, provider) -> str:
        # Check if the URL is a local file path or a remote URL
        print("Downloading m3u playlist...")

        path = f'.local/{provider}/'

        playlistSavePath = f'{path}playlist.m3u'

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        if url.startswith('http') or url.startswith('https'):
            urllib.request.urlretrieve(url, playlistSavePath)
            return playlistSavePath
        else:
            return url
        
    def cleanup_filename(filename) -> str:
        pattern = r"[@$%&\\/:\*\?\"'<>\|~`#\^\+=\{\}\[\];!]"

        new_string = re.sub(pattern, "", filename)

        return(new_string)