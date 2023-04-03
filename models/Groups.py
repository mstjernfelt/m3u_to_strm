import json
import os
import re
from tqdm import tqdm

class Groups:
    groupData = ''
    provider = ''

    def __init__(self, m3u_data = None, inProvider = None, generate_groups = None):
        self.provider = inProvider 

        if generate_groups:
            group_data = self.get_groups(m3u_data)
            self.set(group_data)
        else:
            self.load()

    def load(self):
        if os.path.exists(f'.local/{self.provider}/groups.json'):
            try:
                with open(f'.local/{self.provider}/groups.json', 'r') as f:
                    self.groupData = json.load(f)

                    if len(self.groupData) == 0:
                        self.groupData = {'groups': []}
                        return
                    
            except json.decoder.JSONDecodeError as e:
                self.groupData = {'groups': []}  # or any other default value you want to use
                return self.groupData
        else:
            self.groupData = {'groups': []}
            return self.groupData

    def include(self, groupTitle) -> bool:
        for group in self.groupData.values():
            for item in group:
                if item['name'] == groupTitle:
                    return item['include']
        return False

    def set(self, streamGroups):
        # Load existing JSON data from file
        self.load()
        existing_groups = self.groupData['groups']

        # Remove any groups that are no longer in the new list
        existing_names = [g['name'] for g in existing_groups]
        existing_groups = [g for g in existing_groups if g['name'] in streamGroups]

        # Add any new groups to the list
        for g in streamGroups:
            if g not in existing_names:
                existing_groups.append({'name': g, 'include': False})

        # Remove any groups that are not in the new list
        new_names = [g['name'] for g in existing_groups]
        for g in existing_groups:
            if g['name'] not in new_names:
                existing_groups.remove(g)

        # Convert Python data structure back to JSON format
        self.groupData = {'groups': existing_groups}

    def save(self) -> int:
        if os.path.exists(f'.local/{self.provider}/groups.json'):
            try:
                with open(f'.local/{self.provider}/groups.json', 'r') as f:
                    old_data = json.load(f)
            except json.decoder.JSONDecodeError as e:
                old_data = {}
        else:
            old_data = {}

        newGroupData = {}

        # Merge the old data with the new data
        for key, value in self.groupData.items():
            for group in value:
                groupName = group.get('name')
                groups = old_data.get('groups')

        # Update the original dictionary with the new data
        if len(newGroupData) > 0:
            self.groupData = newGroupData

        # Save the updated JSON data to file
        with open(f'.local/{self.provider}/groups.json', 'w') as f:
            json.dump(self.groupData, f, indent=4)

        oldDataCount = len(old_data)
        newDataCount = len(self.groupData['groups'])

        return(newDataCount - oldDataCount)
    
    def get_groups(self, m3uData):
        # Extract the stream URLs from the m3u data
        streamGroups = []

        num_lines = len(m3uData.values())
        with tqdm(desc="Building m3u group list", total=num_lines) as pbar:
            for line in m3uData.values():
                regExResult = re.search('group-title="([^"]+)"', line)

                if regExResult:
                    groupname = regExResult.group(1)

                    streamGroups.append(groupname)

                pbar.update(1)
                pbar.refresh()
                #pbar.miniters = 1
            
            uniqueStreamGroups = set(streamGroups)
            streamGroups = list(uniqueStreamGroups)

        return streamGroups    