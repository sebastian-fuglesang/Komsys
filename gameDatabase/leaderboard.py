from appJar import gui
from writeToDatabase import db

def leaderboard():
    app = gui()

    def button_close():
        app.stop()

    #fetch from db
    data = db.readFromDatabase()
    print(data)

    #testdata for now
    #testdata = [['Nils', 2], ['Olav', 3], ['Tuv', 0]]
    #testdata = sorted(testdata, key = lambda x: x[1], reverse=True)

    #app setup
    app.setTitle('Leaderboard')
    app.addLabel('leader', 'The leader is: ' + data[0][0])
    app.addTable('table', [['Name', 'Wins']])
    
    #adds rows in table
    for user in data:
        app.addTableRow('table', user)

    app.addButton('leave', button_close)
    
    app.go()



leaderboard()