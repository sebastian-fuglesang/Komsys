from appJar import gui
from gameDBService import db
import re

def winner(player):
    app = gui()
    
    def get_input():
        name = app.getEntry('winner')
        print(name)
        re.sub('[^a-zA-Z]+', '', name.replace(" ", "").upper())
        db.writeToDatabase(name)
        app.stop()

    app.setTitle("Congratulations!")
    if player == 1:
        app.addLabel('winnerlabel', 'Winner is 1 (O)')
    else:
        app.addLabel('winnerlabeltwo', 'Winner is 2 (X)')
    
    app.addEntry('winner')

    app.addButton('Submit', get_input)
    
    app.go()
