#
# Todos:
# - Keychain integration
# - load stored json file at startup, fetch from server if missing
# - build menu from json
#
import rumps
import control

class Harmenubar(rumps.App):
    def __init__(self):
        super(Harmenubar,self).__init__('Harmenubar',icon='resources/icon.png')
        print 'Logging in to Logitech'
        self.session_token = control.login_to_logitech('adreg@megalan.org', 'ankeborg', '192.168.0.158')
        print 'Connecting client'
        client = control.get_client('192.168.0.158', self.session_token)
        print 'Getting current activity'
        self.activity = client.get_current_activity() # 5337127
        client.disconnect(send_close=True)
        self.activity_names = {5337127: 'Listen to Music',
                               5337061: 'Play a Game',
                               5337082: 'Watch a Movie',
                               5337244: 'Plex',
                               -1: 'Off'}
        activity_menu = []
        for k,v in self.activity_names.iteritems():
            activity_menu.append(rumps.MenuItem(v, callback=lambda m,i=k: self.set_activity(m,i)))

        self.menu = [
            rumps.MenuItem('Current Activity:'),
            None,
            rumps.MenuItem('Power Off', callback=lambda m: self.set_activity(m,-1)),
            {'Activity': activity_menu},
            {'Device': ['Samsung', 'Cambridge', 'Wifa', 'Xbox360']},
        ]
        self.update_current_activity(self.activity)

    def set_activity(self, menu,id_):
        print 'Setting activity:', menu,id_
        client = control.get_client('192.168.0.158', self.session_token)
        print 'call start_activity'
        client.start_activity(id_)
        client.disconnect(send_close=True)
        self.update_current_activity(id_)

    def update_current_activity(self, activity):
        self.menu['Current Activity:'].title = 'Current Activity: ' + self.activity_names[activity]
        self.activity = activity

if __name__ == '__main__':
    Harmenubar().run()
