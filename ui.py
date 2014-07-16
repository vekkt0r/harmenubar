#
# Todos:
# - Keychain integration
# - move out activities to main menu?
# - cyclic check of current activity
#
import rumps
import control
import config
import json

class Harmenubar(rumps.App):
    APP_SETTINGS = 'settings.json'
    REMOTE_CONFIG = 'remote.json'

    def __init__(self):
        super(Harmenubar,self).__init__('Harmenubar',icon='resources/icon.png')

        self.settings = self.load_config_file(self.APP_SETTINGS)
        if self.settings is None:
            self.settings = self.settings_popup()

        self.auth()

        cfg = self.load_config_file(self.REMOTE_CONFIG)
        if cfg is None:
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
            None,
            rumps.MenuItem('Preferences', callback=lambda m: self.settings_popup())
        ]
        self.update_current_activity(self.activity)

    def load_config_file(self, fname):
        try:
            with self.open(fname,'r') as f:
                return json.loads(f.read())
        except IOError:
            return None

    def settings_popup(self):
        settings = {'username':'',
                    'password':'',
                    'harmony_ip':'',}
        w = rumps.Window('')
        w.title = 'Harmenubar settings'
        if self.settings is None:
            w.default_text = json.dumps(settings, indent=4)
        else:
            w.default_text = json.dumps(self.settings, indent=4)
        w.add_button('Cancel')
        r = w.run()
        if r.clicked == 1:
            self.settings = json.loads(r.text)
            self.save_settings()

    def save_settings(self):
        with self.open(self.APP_SETTINGS, 'w') as f:
            f.write(json.dumps(self.settings))

    def auth(self):
        if 'auth_token' in self.settings:
            print 'Re-using session token from config'
            self.session_token = self.settings['auth_token']
        else:
            print 'Logging in to Logitech..'
            self.session_token = control.login_to_logitech(
                self.settings['username'], 
                self.settings['password'], 
                self.settings['harmony_ip'])
            self.settings['auth_token'] = self.session_token
            self.save_settings()
        print self.session_token
        print 'Connecting client..'
        client = self.get_client()
        print 'Get current activity..'
        self.activity = client.get_current_activity()
        client.disconnect(send_close=True)

    def get_client(self):
        return control.get_client(self.settings['harmony_ip'], self.session_token)

    def get_and_store_config(self):
        client = self.get_client()
        print 'Getting configuration..'
        cfg = client.get_config()
        client.disconnect(send_close=True)
        with self.open(self.REMOTE_CONFIG,'w') as f:
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
        client = self.get_client()
        print 'call start_activity'
        client.start_activity(id_)
        client.disconnect(send_close=True)
        self.update_current_activity(id_)

    def update_current_activity(self, activity):
        self.menu['Current Activity:'].title = 'Current Activity: ' + self.activities[activity]
        self.activity = activity

if __name__ == '__main__':
    Harmenubar().run()
