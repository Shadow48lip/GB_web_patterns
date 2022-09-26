import sqlite3
import os

path = os.path.join('..', 'db.sqlite')

con = sqlite3.connect(path)
cur = con.cursor()
with open('create_db.sql', 'r') as f:
    text = f.read()
cur.executescript(text)
cur.close()
con.close()
