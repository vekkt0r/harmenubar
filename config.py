import json

class HarmonyConfig(object):
    def __init__(self, config_file):
        with open(config_file) as f:
            self.json = json.loads(f.read())

    def get_activities(self):
        activities = {}
        for a in self.json['activity']:
            activities.update({int(a['id']): a['label']})
        return activities

    def get_devices(self):
        pass