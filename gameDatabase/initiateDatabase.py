import mysql.connector
mydb = mysql.connector.connect(host="gameresultdb.mysql.database.azure.com", user ="komsysAdmin", passwd="qwerty123!", port=3306, ssl_disabled=True)

mycursor = mydb.cursor()

def main():
    mycursor.execute("CREATE DATABASE gameResults")

#Denne databasen er kun på localhost, holder det?