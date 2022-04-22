from appJar import gui
#from writeToDatabase import db

def winner(player):
    app = gui()

    def get_input():
        print(app.getEntry('winner'))
        name = app.getEntry('winner')
        
        app.stop()

    #fetch from db
    #data = db.readFromDatabase()
    #print(data)

    #testdata for now
    #testdata = [['Nils', 2], ['Olav', 3], ['Tuv', 0]]
    #testdata = sorted(testdata, key = lambda x: x[1], reverse=True)
    #app setup
    app.addTitle("Congratulations!")
    if player == 1:
        app.setLable('Winner is 1 (O)')
    app.setLable('Winner is 2 (X)')
    
    app.addEntry('winner')
    #adds rows in table
    #for user in data:
    #    app.addTableRow('table', user)

    app.addButton('Submit', get_input)
    
    app.go()

