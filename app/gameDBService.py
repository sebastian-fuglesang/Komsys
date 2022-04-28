import mysql.connector
mydb = mysql.connector.connect(host="gameresultdb.mysql.database.azure.com", user ="komsysAdmin", passwd="qwerty123!",  port=3306, database="gameresult")

tableList = []

mycursor = mydb.cursor()

class db:
    def createTable():
        mycursor.execute("CREATE TABLE results(username VARCHAR(255) PRIMARY KEY, points INT)")

    def writeToDatabase(username):
        if(db.checkExistingUser(username)):
            mycursor.execute("UPDATE results SET points = points +1 WHERE username = %s", ([username]))
            mydb.commit()
        else:
            mycursor.execute("INSERT INTO results (username, points) VALUES (%s, 1)",([username]))
            mydb.commit()

    def checkUsername(username):
        mycursor.execute("SELECT username FROM results WHERE username = %s", ([username]))

        if(mycursor.fetchone() == ((username,))):
            print("this username is already in use")
        else:
            db.writeToDatabase(username)


    def readFromDatabase():
        mycursor.execute("SELECT * FROM results ORDER BY points DESC")
        data = mycursor.fetchall()
        print(data)
        return data
        #for x in mycursor:
        #    print(x)
        #Litt avhengig av hva slags format Nils ønsker på output.
        # Vil nok ha en finere output her.  


    def checkExistingUser(username):
        mycursor.execute("SELECT username FROM results WHERE username = %s", ([username]))

        if(mycursor.fetchone() == ((username,))):
            return True
        else:
            return False


#main()
#writeToDatabase("nils")
#checkUsername("nils")
test = db()
