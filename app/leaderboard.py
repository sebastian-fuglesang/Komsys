from appJar import gui
from gameDBService import db

def leaderboard():
    app = gui()

    def button_close():
        app.stop()

    #fetch from db
    data = db.readFromDatabase()
<<<<<<< HEAD
=======

    #app setup
>>>>>>> 3190263a643dd9e7b03911a931756c79fec2cb9e
    app.setTitle('Leaderboard')
    app.addLabel('leader', 'The leader is: ' + data[0][0])
    app.addTable('table', [['Name', 'Wins']])
    
    #adds rows in table
    app.addTableRows('table', data)

    app.addButton('leave', button_close)
    
    app.go()
<<<<<<< HEAD
        
leaderboard()
=======


leaderboard()
>>>>>>> 3190263a643dd9e7b03911a931756c79fec2cb9e
