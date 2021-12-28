import sqlite3

conn = sqlite3.connect('example.db')

cur = conn.cursor()

sql_file = open('schema.sql')

sql = sql_file.read()

cur.executescript(sql)

conn.commit()

conn.close()