from appJar import gui
from gameDBService import db

def leaderboard():
    app = gui()

    def button_close():
        app.stop()

    #fetch from db
    data = db.readFromDatabase()
    app.setTitle('Leaderboard')
    app.addLabel('leader', 'The leader is: ' + data[0][0])
    app.addTable('table', [['Name', 'Wins']])
    
    #adds rows in table
    for user in data:
        app.addTableRow('table', user)

    app.addButton('leave', button_close)
    
    app.go()
        
leaderboard()