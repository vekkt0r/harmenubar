#
# Todos:
# - Keychain integration
# - move out activities to main menu?
#
import rumps
import control
import config
import json

class Harmenubar(rumps.App):
    def __init__(self):
        super(Harmenubar,self).__init__('Harmenubar',icon='resources/icon.png')
        self.activity = 5337127
        self.auth()

        try:
            with self.open('config.json','r') as f:
                cfg = json.loads(f.read())
        except IOError:
            cfg = self.get_and_store_config()

        self.cfg = config.HarmonyConfig(cfg)
        self.activities = self.cfg.get_activities()
        self.devices = self.cfg.get_devices()

        self.menu = [
            rumps.MenuItem('Current Activity:'),
            None,
            rumps.MenuItem('Power Off', callback=lambda m: self.set_activity(m,-1)),
            {'Activity': self.build_activity_menu()},
            {'Device': self.build_device_menu()},
        ]
        self.update_current_activity(self.activity)

    def auth(self):
        print 'Logging in to Logitech..'
        self.session_token = control.login_to_logitech('adreg@megalan.org', 'ankeborg', '192.168.0.158')
        print 'Connecting client..'
        client = control.get_client('192.168.0.158', self.session_token)
        print 'Get current activity..'
        self.activity = client.get_current_activity()
        client.disconnect(send_close=True)

    def get_and_store_config(self):
        client = control.get_client('192.168.0.158', self.session_token)
        print 'Get configuration..'
        cfg = client.get_config()
        client.disconnect(send_close=True)
        with self.open('config.json','w') as f:
            f.write(json.dumps(cfg))
        return cfg

    def build_activity_menu(self):
        menu = []
        for key,value in self.activities.iteritems():
            if key != -1:
                menu.append(rumps.MenuItem(value, 
                                           callback=lambda m,i=key: self.set_activity(m,i)))
        return menu

    def build_device_menu(self):
        menu = []
        for key,value in self.devices.iteritems():
            if key != -1:
                menu.append(rumps.MenuItem(value))
        return menu

    def set_activity(self, menu,id_):
        print 'Setting activity:', menu,id_
        client = control.get_client('192.168.0.158', self.session_token)
        print 'call start_activity'
        client.start_activity(id_)
        client.disconnect(send_close=True)
        self.update_current_activity(id_)

    def update_current_activity(self, activity):
        self.menu['Current Activity:'].title = 'Current Activity: ' + self.activities[activity]
        self.activity = activity

if __name__ == '__main__':
    Harmenubar().run()
