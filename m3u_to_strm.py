# -*- coding: utf-8 -*-

import os
import sys
import urllib.request
import re
import argparse
import json
from tqdm import tqdm
from m3u.groups import groups

m3uGroups = '';

def parse_m3u(output_path, m3u_data):
    lines = iter(m3u_data.splitlines())
    num_lines = m3u_data.count('\n')
    with tqdm(desc="Parsing m3u file", total=num_lines) as pbar:
        for line in lines:
            if line.startswith('#EXTINF'):
                grouptitleMatch = re.search('group-title="([^"]+)"', line)

                if grouptitleMatch is None:
                    continue

                if not m3uGroups.Include(grouptitleMatch.group(1)):
                    continue

                name = re.search('tvg-name="([^"]+)"', line)
                if name and 'tvg-name' in name.group(0):
                    filename = name.group(1)
                    filename = re.sub(r'[<>:"/\\|?*\x00-\x1f.]', '', filename)

                    groupTitle = re.sub(r'[<>:"/\\|?*\x00-\x1f.]', '', grouptitleMatch.group(1))

                    if '[Series]' in line or 'Series:' in line:
                        titleType = 'Series'
                    elif '[VOD]' in line or 'VOD:' in line:
                        titleType = 'Movies'
                    else:
                        continue

                    outline = filename + ';' + f'{titleType}\{groupTitle}\;' + next(lines)
                    
                    year = get_Title_Year(filename)
                    # title = get_Cleaned_Title(filename)

                    if int(year) > 2010:
                        create_strm_nfo(outline, output_path)

            pbar.update(2)
            pbar.refresh()
            pbar.miniters = 1

def get_Title_Year(title):

    year_pattern = r"\[(\d{4})\]"  # matches a four-digit year

    # find the year in the modified string
    year_match = re.search(year_pattern, title)

    if year_match:
        year = year_match.group(1)
    else:
        year = 0
        
    return(year)

def get_Cleaned_Title(title):

    pattern = r"\[[^\]]*\]"  # matches any square brackets and the characters inside them
    year_pattern = r"\b\d{4}\b"  # matches a four-digit year

    # find all matches of the pattern in the string and replace them with an empty string
    string_without_brackets = re.sub(pattern, "", title)

    return string_without_brackets

def get_m3u_VOD_groups(m3uData):
    # Extract the stream URLs from the m3u data
    streamGroups = []

    lines = iter(m3uData.splitlines())
    num_lines = m3uData.count('\n')
    with tqdm(desc="Building m3u group list", total=num_lines) as pbar:
        for line in lines:
            if line.startswith('#EXTINF'):
                regExResult = re.search('group-title="([^"]+)"', line)

                if '[Series]' in line:
                    include = True
                if 'Series:' in line:
                    include = True
                elif '[VOD]' in line:
                    include = True
                elif 'VOD:' in line:
                    include = True
                else:
                    include = False

                if regExResult and include:
                  groupname = regExResult.group(1)

                  streamGroups.append(groupname)

            pbar.update(2)
            pbar.refresh()
            pbar.miniters = 1
        
        uniqueStreamGroups = set(streamGroups)
        streamGroups = list(uniqueStreamGroups)

    return streamGroups

def load_m3u_file(url):
    # Check if the URL is a local file path or a remote URL
    print("Loading m3u playlist...")

    if url.startswith('http') or url.startswith('https'):
        response = urllib.request.urlopen(url)
        m3uData = response.read().decode()
    else:
        with open(url, 'r', encoding="utf8") as f:
            m3uData = f.read()

    return m3uData

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

        with open(output_strm, 'w', encoding='utf-8') as f:
            f.write(line[2])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts an m3u file to STRM files for Kodi.')
    parser.add_argument('--m3u_file', type=str, help='Input m3u file (either a URL or a local path)')
    parser.add_argument('--output_dir', type=str, help='Output directory for STRM files')
    parser.add_argument('--generate_groups', action='store_true', help='Generate groups for VOD entries')
    args = parser.parse_args()

    m3u_url = args.m3u_file
    output_path = args.output_dir

    if not output_path.endswith("\\"):
        output_path += "\\"

    generate_groups = args.generate_groups

    if not m3u_url or not output_path:
        parser.print_help()
        sys.exit(1)

    m3uData = load_m3u_file(m3u_url)

    if generate_groups:
        groupData = get_m3u_VOD_groups(m3uData)
        m3uGroups = groups(groupData)
        m3uGroups.Save()
    else:
        m3uGroups = groups();

    parse_m3u(output_path, m3uData)
