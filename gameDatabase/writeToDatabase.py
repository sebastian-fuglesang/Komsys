import mysql.connector
import re
mydb = mysql.connector.connect(host="gameresultdb.mysql.database.azure.com", user ="komsysAdmin", passwd="qwerty123!",  port=3306, database="gameresult")

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
    mycursor.execute("SELECT * FROM results ORDER BY points DESC")

    for x in mycursor:
        print(x)


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

#print(defineUsername("Jacob Fredheim"))
#main()
#writeToDatabase("nils")
#checkUsername("nils")
#readFromDatabase()
