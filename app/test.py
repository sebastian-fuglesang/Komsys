import mysql.connector
mydb = mysql.connector.connect(host="gameresultdb.mysql.database.azure.com", user ="komsysAdmin", passwd="qwerty123!",  port=3306, database="gameresult")

tableList = []

mycursor = mydb.cursor()

mycursor.execute("DROP TABLE results")

def readFromDatabase():
        mycursor.execute("SELECT * FROM results ORDER BY points DESC")
        data = mycursor.fetchall()
        print(data)

def createTable():
        mycursor.execute("CREATE TABLE results(username VARCHAR(255) PRIMARY KEY, points INT)")

createTable()
readFromDatabase()