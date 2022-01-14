import sqlite3
from datetime import datetime, timezone, date
from db import *

class Reclamacao():
    def __init__(self, _id=None, login=None, recl=None, email=None, date=None):
        self.id = _id
        self.login = login
        self.recl = recl
        self.email = email
        self.date = date

    def insert_into_db(self):
        conn, cursor = connect_db()

        sql = """
            INSERT INTO reclamacao (cliente_email, cliente_login, reclamacao) 
            VALUES ('{}', '{}', '{}')
        """.format(self.email, self.login, self.recl)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def get(self, n=5):
        conn, cursor = connect_db()
        sql = """
            SELECT * FROM reclamacao WHERE cliente_login = '{}'
        """.format(self.login)

        results = cursor.execute(sql).fetchall()
        return results

def get_old_reclamacao():
    conn, cursor = connect_db()
    sql = "SELECT * FROM reclamacao WHERE respondida = 0 ORDER BY data_reclamacao ASC LIMIT 1"
    results = cursor.execute(sql).fetchone()
    return results

def update_reclamacao(_id):
    conn, cursor = connect_db()
    sql = """
        UPDATE reclamacao 
        SET respondida = 1 
        WHERE id = {}
    """.format(_id)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    

#create_db()
#txt = "Não consigo renovar meu pedido"
#login = "ppnery"
#email = "ppnery95@gmail.com"
#data = date.today()

#rec = Reclamacao(login=login, email=email, date=data, recl=txt)
#rec.insert_into_db()
#print(rec.get())