import mysql.connector
mydb = mysql.connector.connect(host="localhost", user ="root", passwd="komsysTeam07", database="gameResults")

tableList = []

mycursor = mydb.cursor()



def createTable():
    mycursor.execute("CREATE TABLE results(username VARCHAR(255) PRIMARY KEY, points INT)")



def writeToDatabase(username):
    if(checkExistingUser(username)):
        mycursor.execute("UPDATE results SET points = points +1 WHERE username = %s", ([username]))
        mydb.commit()
    else:
        mycursor.execute("INSERT INTO results (username, points) VALUES (%s, 1)",([username]))
        mydb.commit()

def readFromDatabase():
    #Litt avhengig av hva slags format Nils ønsker på output. 
    print("l")

def checkWinner(player1, player2, result):
    #   writeToDatabase(winner)
    #  Spørs om vi skal ta med resultat for begge spillere, eller kun notere den som vinner. 
    #  Hvis vi skal ha med vinner og taper må database strukturen endres og poengsystemet endres.
    print("k")


def checkExistingUser(username):
    mycursor.execute("SELECT username FROM results WHERE username = %s", ([username]))

    if(mycursor.fetchone() == ((username,))):
        return True
    else:
        return False

def main():
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        tableList.append(x)
    

    if("('results',)" not in str(tableList)):
        createTable()

#main()
writeToDatabase("nils")