from appJar import gui

def leaderboard():
    app = gui()

    def button_close():
        app.stop()

    #fetch from db

    #testdata for now
    testdata = [['Nils', 2], ['Olav', 3], ['Tuv', 0]]
    testdata = sorted(testdata, key = lambda x: x[1], reverse=True)

    #app setup
    app.setTitle('Leaderboard')
    app.addLabel('leader', 'The leader is: Nils')
    app.addTable('table', [['Name', 'Wins']])
    
    #adds rows in table
    for user in testdata:
        app.addTableRow('table', user)

    app.addButton('leave', button_close)
    
    
    
    app.go()


leaderboard()