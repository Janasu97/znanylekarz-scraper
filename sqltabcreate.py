import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
# Establish MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="testdatabase"
)
cursor = db.cursor()

