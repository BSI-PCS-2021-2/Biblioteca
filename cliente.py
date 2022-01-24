import sqlite3

#from flask_login import UserMixin 

from hashlib import md5

from db import *

class Cliente():
    def __init__(self, name=None, email=None, login=None, password=None):
        #self.id = id_
        self.name = name
        self.email = email
        self.login = login
        self.password = password
        self.session = False

    def get(self, login=None, email=None, password=None):
        conn, cursor = connect_db()

        sql = "SELECT * FROM cliente WHERE email = '{}' OR login = '{}';".format(self.email, self.login)

        cliente = cursor.execute(sql).fetchone()
        if not cliente:
            return None

        #cliente = Cliente(
        #    email=cliente[1], login=cliente[2], password=cliente[3]
        #)
        #self.session = True
        return cliente

    def get_id(self):
        conn, cursor = connect_db()

        sql = "SELECT id FROM cliente WHERE login = '{}'".format(self.login)

        _id = cursor.execute(sql).fetchone()

        return _id[0]

    def get_data(self):
        conn, cursor = connect_db()

        sql = "SELECT * FROM cliente WHERE email = '{}' OR login = '{}';".format(self.email, self.login)

        cliente = cursor.execute(sql).fetchone()
        if not cliente:
            return None

        #cliente = Cliente(
        #    email=cliente[1], login=cliente[2], password=cliente[3]
        #)
        #self.session = True

        email, login, password = cliente[1], cliente[2], cliente[3]

        return email, login, password

    def insert_into_db(self):
        conn, cursor = connect_db()

        sql = "SELECT * FROM cliente WHERE email = '{}' OR login = '{}';".format(self.email, self.login)

        cliente = cursor.execute(sql).fetchone()
        
        if not cliente:

            sql = """
                INSERT INTO cliente (name, email, login, senha) VALUES ('{}', '{}', '{}', '{}')
            """.format(self.name, self.email, self.login, self.password)

            cursor.execute(sql)
            conn.commit()
            conn.close()

    def authenticate(self):
        conn, cursor = connect_db()

        sql = "SELECT * FROM cliente WHERE email = '{}' OR login = '{}';".format(self.email, self.login)

        cliente = cursor.execute(sql).fetchone()
        if not cliente:
            return False

        else:
            if cliente[3] == self.password:
                #self.session = True
                return True

        return False



#create_db()
#password = md5("12345".encode())
#password = password.hexdigest()
#c = Cliente(email='ppnery95@gmail.com', login='ppnery', password=password)
#print(c)

#Cliente.create(email="pp@ddsds.com", login="ppn", password=password)
