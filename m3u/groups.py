import json
import os

class groups:
    groupData = {'groups': []}

    def __init__(self, groupData):
        self.Set(groupData)

    def Load(self):
        if os.path.exists('groups.json'):
            with open('groups.json', 'r') as f:
                self.groupData = json.load(f)
        else:
            self.groupData = {'groups': ['include']} # change to a dictionary with a list value
            open('groups.json', 'w')

        return {'groups': self.groupData}

    def Set(self, streamGroups):
        # Load existing JSON data from file
        self.Load()
        existing_groups = self.groupData

        # Convert JSON data to Python list of groups
        existing_groups = self.groupData['groups']

        # Remove any groups that are no longer in the new list
        existing_groups = [g for g in existing_groups if g in streamGroups]

        # Add any new groups to the list
        for g in streamGroups:
            if g not in existing_groups:
                existing_groups.append(g)

        # Convert Python data structure back to JSON format
        self.groupData = {'groups': existing_groups}
   
    def Save(self):
        json_data = json.dumps(self.groupData, indent=4)

        # Save updated JSON data to file
        with open('groups.json', 'w') as f:
            f.write(json_data)
