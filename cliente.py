import sqlite3

from flask_login import UserMixin 

from hashlib import md5

from db import create_db

class Cliente():
    def __init__(self, email, login, password):
        #self.id = id_
        #self.name = name
        self.email = email
        self.login = login
        self.password = password

    def get(email):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()

        sql = "SELECT * FROM cliente WHERE email = '{}'".format(email)

        cliente = cursor.execute(sql).fetchone()
        if not cliente:
            return None

        cliente = Cliente(
            email=cliente[1], login=cliente[2], password=cliente[3]
        )
        return cliente

    def create(self):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()

        sql = """
            INSERT INTO cliente (email, login, senha) VALUES ('{}', '{}', '{}')
        """.format(self.email, self.login, self.password)

        cursor.execute(sql)
        conn.commit()
        conn.close()

create_db()
password = md5("12345".encode())
password = password.hexdigest()
c = Cliente(email="pp@ddsds.com", login="ppn", password=password)
print(c.email)
c.create()
print(c.get("pp@ddsds.com"))
#Cliente.create(email="pp@ddsds.com", login="ppn", password=password)
