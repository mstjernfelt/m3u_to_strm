import os
import sys
import urllib.request
import re
from tqdm import tqdm

def parse_m3u(url, output_path):
    # Check if the URL is a local file path or a remote URL
    if url.startswith('http') or url.startswith('https'):
        response = urllib.request.urlopen(url)
        m3u_data = response.read().decode()
    else:
        with open(url, 'r') as f:
            m3u_data = f.read()

    # Extract the stream URLs from the M3U data
    stream_urls = []
    lines = iter(m3u_data.splitlines())
    num_lines = m3u_data.count('\n')
    with tqdm(desc="Parsing M3U file", total=num_lines) as pbar:
        for line in lines:
            if line.startswith('#EXTINF'):
                name = re.search('tvg-name="([^"]+)"', line)
                if name and 'tvg-name' in name.group(0):
                    filename = name.group(1)
                    filename = re.sub(r'[<>:"/\\|?*\x00-\x1f.]', '', filename)

                if '[Series]' in line:
                    outline = filename + ';' + 'Series;' + next(lines)
                elif '[VOD]' in line:
                    outline = filename + ';' + 'Movies;' + next(lines)
                else:
                    continue

                create_strm_nfo(outline, output_path)

            pbar.update(2)
            pbar.refresh()
            pbar.miniters = 1
    return stream_urls

def create_strm_nfo(stream_url, output_path):
    line = stream_url.split(';')
    filename = line[0]
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1f.]', '', filename)
    show_name = re.sub(r'S\d+E\d+', '', filename).strip()
    folderName = line[1]
    output_path = os.path.join(output_path, folderName)
    folder_path = os.path.join(output_path, show_name)

    output_strm = os.path.join(folder_path, filename[0:30] + '.strm')
    if not os.path.exists(output_strm):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(output_strm, 'w') as f:
            f.write(line[2])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python m3u_to_strm.py <input m3u file url or local path> <output directory>')
        sys.exit(1)

    m3u_url = sys.argv[1]
    output_path = sys.argv[2]

    parse_m3u(m3u_url, output_path)