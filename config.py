class HarmonyConfig(object):
    def __init__(self, config):
        self.json = config

    def get_activities(self):
        return self._build_kv_menu('activity')

    def get_devices(self):
        return self._build_kv_menu('device')

    def _build_kv_menu(self, key):
        menu = {}
        for d in self.json[key]:
            menu.update({int(d['id']): d['label']})
        return menu