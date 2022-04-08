import mysql.connector
mydb = mysql.connector.connect(host="localhost", user ="root", passwd="komsysTeam07")

mycursor = mydb.cursor()

def main():
    mycursor.execute("CREATE DATABASE gameResults")

#Denne databasen er kun på localhost, holder det?