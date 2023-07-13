
import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
# Establish MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="znanylekarzdb"
)
cursor = db.cursor()
cursor.execute("CREATE TABLE DOCDAT (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")
# cursor.execute("DESCRIBE Person")
# cursor.execute("INSERT INTO Person (name, age) VALUES (%s,%s)", ("Joe", 22)) #Inserting the data record to the Table of datafile
# db.commit() #Without that the data base will not be updated
# cursor.execute("SELECT * FROM Person")
#
# for x in cursor:
#     print(x)

# cursor.execute("CREATE TABLE Test (name varchar(50) NOT NULL, created datetime NOT NULL, gender ENUM('M', 'F', 'O') NOT NULL, id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
# cursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s, %s, %s)", ("Janna", datetime.now(), "F"))
# db.commit()

# cursor.execute("SELECT id, name FROM Test WHERE gender = 'F' ORDER BY id DESC")
# cursor.execute("ALTER TABLE Test ADD COLUMN food VARCHAR(50) NOT NULL")
# cursor.execute("ALTER TABLE Test DROP food")
# cursor.execute("ALTER TABLE Test CHANGE first_name first_name VARCHAR(50)")
# cursor.execute("DESCRIBE Test")

Q1 = "CREATE TABLE Users (id int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), passwd VARCHAR(50))"
Q2 = "CREATE TABLE Scores (userID int PRIMARY KEY , FOREIGN KEY(userID) REFERENCES Users(id), game1 int DEFAULT 0, game2 int DEFAULT 0)"

users = [("tim", "techwithtim"),
         ("joe", "joey123"),
         ("sarah", "sarah1234")]

user_scores = [(20, 100),
               (30, 200),
               (15, 135)]
# cursor.execute(Q1)
# cursor.execute(Q2)
# cursor.execute("SHOW TABLES")



Q3 = "INSERT INTO users (name, passwd) VALUES (%s, %s)"
Q4 = "INSERT INTO scores (userID, game1, game2) VALUES (%s, %s, %s)"

# for x, user in enumerate(users):
#     cursor.execute(Q3, user)
#     last_id = cursor.lastrowid
#     cursor.execute(Q4, (last_id,) + user_scores[x])
#
# db.commit()

cursor.execute("SELECT * FROM Users")

for x in cursor:
    print(x)

