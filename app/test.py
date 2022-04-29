import re
import mysql.connector

mydb = mysql.connector.connect(host="gameresultdb.mysql.database.azure.com", user ="komsysAdmin", passwd="qwerty123!",  port=3306, database="gameresult")

tableList = []

mycursor = mydb.cursor()

#mycursor.execute("DROP TABLE results")

def readFromDatabase():
        mycursor.execute("SELECT * FROM results ORDER BY points DESC")
        data = mycursor.fetchall()
        print(data)

def createTable():
        mycursor.execute("DELETE FROM gameresult.results WHERE username='yep' ")

#createTable()
#readFromDatabase()

def prov(name):
    print(re.sub('[^a-zA-Z]+', '', name.replace(" ", "").upper()))

#"prov("jacobv red")
createTable()