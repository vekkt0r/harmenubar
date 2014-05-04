import rumps

@rumps.clicked('About')
def about(sender):
    rumps.alert('Testing')

@rumps.timer(4)
def tick(sender):
    app.menu.add(rumps.MenuItem('ANother thing'))
    app.menu['Current Activity: '].title = 'abcd'
    del app.menu['Preferences']

if __name__ == '__main__':
    app = rumps.App('Harmenubar', title='H')
    app.menu = [
        rumps.MenuItem('About'),
        None,
        'Preferences'
    ]
    app.run()