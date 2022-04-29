from appJar import gui
from gameDBService import db

def leaderboard():
    app = gui()

    def button_close():
        app.stop()

    #fetch from db
    data = db.readFromDatabase()

    #app setup
    app.setTitle('Leaderboard')
    app.addLabel('leader', 'The leader is: ' + data[0][0])
    app.addTable('table', [['Name', 'Wins']])
    
    #adds rows in table
    app.addTableRows('table', data)

    app.addButton('leave', button_close)
    
    app.go()


leaderboard()
