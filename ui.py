#
# Todos:
# - move out activities to main menu?
import os
import sys
import rumps
import control
import config
import json
import logging

class Harmenubar(rumps.App):
    APP_SETTINGS = 'settings.json'
    REMOTE_CONFIG = 'remote.json'

    def __init__(self):
        self.resource_path = os.environ.get('RESOURCEPATH')
        if self.resource_path is None:
            self.resource_path = 'resources/'

        # Rumps initialization
        super(Harmenubar,self).__init__('Harmenubar',
			icon=self.resource_path + '/icon.png')

        self.log = logging.getLogger('harmenubar')

        self.settings = self.load_config_file(self.APP_SETTINGS)
        if self.settings is None:
            self.settings_popup()

        self.auth()
        self.activity = self.get_current_activity()

        cfg = self.load_config_file(self.REMOTE_CONFIG)
        if cfg is None:
            cfg = self.get_and_store_config()
        else:
            self.log.info('Using cached harmony configuration from disk')

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
            rumps.MenuItem('Refresh config', callback=lambda m: self.get_and_store_config()),
            rumps.MenuItem('Preferences', callback=lambda m: self.settings_popup())
        ]
        self.update_current_activity(self.activity)

    def get_current_activity(self):
        client = self.get_client()
        activity = client.get_current_activity()
        client.disconnect(send_close=True)
        return activity

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
        w = rumps.Window('Change settings in the textbox below', 'Harmenubar settings')
        w.icon = self.resource_path + 'icon.png'
        if self.settings is None:
            w.default_text = json.dumps(settings, indent=4)
        else:
            w.default_text = json.dumps(self.settings, indent=4)
        w.add_button('Cancel')
        r = w.run()
        if r.clicked == 1:
            self.settings = json.loads(r.text)
            self.save_settings()
        else:
            rumps.alert('No settings enterred, quitting')
            sys.exit('')

    def save_settings(self):
        with self.open(self.APP_SETTINGS, 'w') as f:
            f.write(json.dumps(self.settings))

    def auth(self):
        if 'auth_token' in self.settings:
            self.log.info('Re-using session token from config')
            self.session_token = self.settings['auth_token']
        else:
            self.log.info('Logging in to Logitech..')
            self.session_token = control.login_to_logitech(
                self.settings['username'],
                self.settings['password'],
                self.settings['harmony_ip'])
            self.settings['auth_token'] = self.session_token
            self.save_settings()
        self.log.debug('Token: %s', self.session_token)

    def get_client(self):
        c = control.get_client(self.settings['harmony_ip'], self.session_token)
        if c is None:
            self.log.error('Could not get client, trying to get new session token')
            self.settings.pop('auth_token')
            self.auth()
            c = control.get_client(self.settings['harmony_ip'], self.session_token)
        return c

    def get_and_store_config(self):
        client = self.get_client()
        self.log.debug('Getting configuration..')
        cfg = client.get_config()
        client.disconnect(send_close=True)
        with self.open(self.REMOTE_CONFIG,'w') as f:
            f.write(json.dumps(cfg))
        self.log.info('Configuration saved.')
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
            if type(value) == list:
               pass
            elif key != -1:
                menu.append(rumps.MenuItem(value))
        return menu

    def set_activity(self, menu, id_):
        self.log.info('Setting activity: %s, %d', menu, id_)
        client = self.get_client()
        self.log.debug('call start_activity')
        client.start_activity(id_)
        client.disconnect(send_close=True)
        self.update_current_activity(id_)

    def update_current_activity(self, activity):
        self.menu['Current Activity:'].title = 'Current Activity: ' + self.activities[activity]
        self.activity = activity

    @rumps.timer(3600)
    def check_activity(self,sender):
        self.log.debug('Checking activity...')
        current = self.get_current_activity()
        if current != self.activity:
            self.update_current_activity(current)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    Harmenubar().run()
