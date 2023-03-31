import urllib.request
import os

class FileManagement():
    def get_m3u_file(url, provider) -> str:
        # Check if the URL is a local file path or a remote URL
        print("Downloading m3u playlist...")

        path = f'.local\\{provider}\\'

        playlistSavePath = f'{path}playlist.m3u'

        if not os.path.exists(path):
            os.mkdir(path)

        if url.startswith('http') or url.startswith('https'):
            urllib.request.urlretrieve(url, playlistSavePath)
            return playlistSavePath
        else:
            return url