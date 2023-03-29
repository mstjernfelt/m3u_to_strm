import json
import os

class groups:
    groupData = ''

    def __init__(self, inGroupData = None):
        if inGroupData is not None:
            self.Set(inGroupData)
        else:
            self.Load()

    def Load(self):
        if os.path.exists('groups.json'):
            with open('groups.json', 'r') as f:
                self.groupData = json.load(f)
        else:
            self.groupData = {'groups': []}
            open('groups.json', 'w')

        # Set "include" subvalue to True for new groups
        existing_groups = self.groupData['groups']
        existing_names = [g['name'] for g in existing_groups]

        for g in existing_names:
            if g not in [group['name'] for group in self.groupData['groups']]:
                self.groupData['groups'].append({'name': g, 'include': False})

        return {'groups': self.groupData}

    def Include(self, groupTitle) -> bool:
        for group in self.groupData["groups"]:
            if groupTitle in group.values():
                return(group['include'])

    def Set(self, streamGroups):
        # Load existing JSON data from file
        self.Load()
        existing_groups = self.groupData['groups']

        # Remove any groups that are no longer in the new list
        existing_names = [g['name'] for g in existing_groups]
        existing_groups = [g for g in existing_groups if g['name'] in streamGroups]

        # Add any new groups to the list
        for g in streamGroups:
            if g not in existing_names:
                existing_groups.append({'name': g, 'include': True})

        # Remove any groups that are not in the new list
        new_names = [g['name'] for g in existing_groups]
        for g in existing_groups:
            if g['name'] not in new_names:
                existing_groups.remove(g)

        # Convert Python data structure back to JSON format
        self.groupData = {'groups': existing_groups}

        # Save updated JSON data to file
        self.Save()

    def Save(self):
        json_data = json.dumps(self.groupData, indent=4)

        # Save updated JSON data to file
        with open('groups.json', 'w') as f:
            f.write(json_data)
