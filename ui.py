#
# Todos:
# - load stored json file at startup, fetch from server if missing
# - build menu from json
# - Keychain integration
#
import rumps
import control
import config

class Harmenubar(rumps.App):
    def __init__(self):
        super(Harmenubar,self).__init__('Harmenubar',icon='resources/icon.png')
        print 'Logging in to Logitech'
#        self.session_token = control.login_to_logitech('adreg@megalan.org', 'ankeborg', '192.168.0.158')
        print 'Connecting client'
#        client = control.get_client('192.168.0.158', self.session_token)
        print 'Getting current activity'
#        self.activity = client.get_current_activity() # 5337127
        self.activity = 5337127
#        client.disconnect(send_close=True)

        self.cfg = config.HarmonyConfig('harmony.json')
        self.activities = self.cfg.get_activities()
        activity_menu = self.build_activity_menu()
        device_menu = self.build_device_menu()

        self.menu = [
            rumps.MenuItem('Current Activity:'),
            None,
            rumps.MenuItem('Power Off', callback=lambda m: self.set_activity(m,-1)),
            {'Activity': activity_menu},
            {'Device': ['Samsung', 'Cambridge', 'Wifa', 'Xbox360']},
        ]
        self.update_current_activity(self.activity)

    def build_activity_menu(self):
        menu = []
        for key,value in self.activities.iteritems():
            if key != -1:
                menu.append(rumps.MenuItem(value, 
                                           callback=lambda m,i=key: self.set_activity(m,i)))
        return menu

    def build_device_menu(self):
        menu = []
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
