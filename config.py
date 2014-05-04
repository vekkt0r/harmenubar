import json

class HarmonyConfig(object):
    def __init__(self, config):
        self.json = json.loads(config)

    def get_activities(self):
        return self.json['activity']

    def get_devices(self):
        pass