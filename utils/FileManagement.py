import urllib.request
import shutil
import tempfile
import os
import re

class FileManagement():

    m3u_file_path = ""
    m3u_tempfile_path = ""

    def get_m3u_file(self, url, provider) -> str:
        # Check if the URL is a local file path or a remote URL
        print("Downloading m3u playlist...")

        path = f'.local/{provider}/'

        self.m3u_file_path = f'{path}playlist.m3u'

        if os.path.exists(self.m3u_file_path):
            # create a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                # get the path of the temporary file
                self.m3u_tempfile_path = temp.name

                # use shutil.copy() to copy the contents of the source file to the temporary file
                shutil.copy(self.m3u_file_path, self.m3u_tempfile_path)

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        if url.startswith('http') or url.startswith('https'):
            urllib.request.urlretrieve(url, self.m3u_file_path)
        else:
            self.m3u_file_path = url
        
    def cleanup_filename(filename) -> str:
        pattern = r"[@$%&\\/:\*\?\"'<>\|~`#\^\+=\{\}\[\];!]"

        new_string = re.sub(pattern, "", filename)

        return(new_string)