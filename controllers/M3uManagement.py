import os
import re
from tqdm import tqdm
from models.Groups import Groups
from utils.FileManagement import FileManagement
from models.Logger import Logger

class M3uManagement:

    groups = None
    logger = None
    provider = None
    m3u_Url = None
    m3u_data = None

    num_titles_sikpped = 0
    num_new_series = 0
    num_new_movies = 0
    num_errors = 0

    def __init__(self, in_group_data = None, in_provider = None, in_generate_groups = None, in_m3u_url = None):
        self.provider = in_provider
        self.m3u_Url = in_m3u_url

        playlistPath = FileManagement.get_m3u_file(self.m3u_Url, self.provider)

        self.m3u_data = self.diffs(f'.local\{self.provider}\current_playlist.m3u', playlistPath)

        self.groups = Groups(generate_groups = in_generate_groups, m3u_data=self.m3u_data, inProvider=self.provider)
        self.logger = Logger(provider=self.provider)

    def parse(self, output_path):
        num_lines = len(self.m3u_data.items())
        
        with tqdm(desc="Parsing m3u file", total=num_lines) as pbar:
            for url, line in self.m3u_data.items():
                tvgIdMatch = re.search('tvg-id=""', line)
                
                if not tvgIdMatch:
                    self.num_titles_sikpped += 1
                    continue

                grouptitleMatch = re.search('group-title="([^"]+)"', line)

                if grouptitleMatch is None:
                    self.num_titles_sikpped += 1
                    continue

                if not self.groups.include(grouptitleMatch.group(1)):
                    self.num_titles_sikpped += 1
                    continue

                name = re.search('tvg-name="([^"]+)"', line)
                if name and 'tvg-name' in name.group(0):

                    if '[Series]' in line or 'Series:' in line:
                        titleType = 'Series'
                    elif '[VOD]' in line or 'VOD:' in line or '(VOD)' in line:
                        titleType = 'Movies'
                    else:
                        self.logger.info(f'TitleType: Line {line} was skipped')
                        continue

                    filename = name.group(1)
                    filename = re.sub(r'[<>:"/\\|?*\x00-\x1f.]', '', filename)
                    subfolder_search = re.search('^(.*?) S\d+', filename)
                    sub_folder = ""

                    if titleType == 'Series':
                        groupTitle = re.sub(r'[<>:"/\\|?*\x00-\x1f.]', '', grouptitleMatch.group(1))                                                
                        sub_folder = subfolder_search.group(1)
                    else:
                        groupTitle = grouptitleMatch.group(1)
                        filename = name.group(1)

                    params = {'filename': filename, 'titleType': titleType, 'groupTitle': groupTitle, 'sub_folder': sub_folder, 'url': url}

                    if self.create_strm(params, output_path):
                        if titleType == 'Series':
                            self.num_new_series += 1
                        elif titleType == 'Movies':
                            self.num_new_movies += 1
                    else:
                        self.num_errors += 1


                pbar.update(1)
                pbar.refresh()

    def create_strm(self, params, output_path) -> bool:
        global share_user_name
        global share_password

        titleType = params['titleType']
        titleType = FileManagement.cleanup_filename(titleType)
        org_titleType = params['titleType']

        filename = re.sub(r'[<>:"/\\|?*\x00-\x1f.]', '', params['filename'])
        filename = FileManagement.cleanup_filename(filename)
        org_filename = params['filename']

        groupTitle = params['groupTitle']
        groupTitle = FileManagement.cleanup_filename(groupTitle)
        org_groupTitle = params['groupTitle']

        sub_folder = params['sub_folder']
        sub_folder = FileManagement.cleanup_filename(sub_folder)
        org_sub_folder = params['sub_folder']

        if titleType == 'Series':
            output_path = os.path.join(output_path, f'{titleType}\\{sub_folder}')
            org_output_path = os.path.join(output_path, f'{org_titleType}\\{org_sub_folder}')
        else:
            output_path = os.path.join(output_path, f'{titleType}\\{groupTitle}\\{filename}')
            org_output_path = os.path.join(output_path, f'{org_titleType}\\{org_groupTitle}\\{org_filename}')

        output_strm = os.path.join(output_path, filename + '.strm')

        if not os.path.exists(output_strm):
            if not os.path.exists(output_path):
                os.makedirs(output_path, exist_ok=True)

            try:
                with open(output_strm, 'w', encoding='utf-8') as f:
                    f.write(params['url'])
                    return True
            except Exception as e:
                self.logger.error(e)
                pass
        else:
            self.logger.info(f'File {output_strm} ({org_output_path}) already exists')

        return False
    
    def get_urls(self, fileName):
        if not os.path.exists(fileName):
            return {}

        url_extinf_pattern = re.compile(r'#EXTINF:-1\s+(.*?)\n(http[s]?://\S+)')

        with open(fileName, 'r', encoding="utf-8") as f:
            contents = f.read()
            matches = url_extinf_pattern.findall(contents)
            url_dict = {}

            for match in matches:
                extinf = match[0]
                url = match[1]
                url_dict[url] = extinf

        return(url_dict)

    def diffs(self, currentFile, newFile):
        currentM3uDict = self.get_urls(currentFile)
        newM3uDict = self.get_urls(newFile)

        keys1 = set(currentM3uDict.keys())
        keys2 = set(newM3uDict.keys())
        diff_keys1 = keys1 - keys2
        diff_keys2 = keys2 - keys1

        diff_items1 = {k: currentM3uDict[k] for k in diff_keys1}
        diff_items2 = {k: newM3uDict[k] for k in diff_keys2}

        result = {**diff_items1, **diff_items2}

        return(result)