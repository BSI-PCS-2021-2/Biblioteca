import sqlite3

#from flask_login import UserMixin 

from hashlib import md5

from db import *

class Funcionario():
    def __init__(self, name=None, email=None, matricula=None, password=None):
        #self.id = id_
        self.name = name
        self.email = email
        self.matricula = matricula
        self.password = password

    def get(self, matricula=None, email=None):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()

        sql = "SELECT * FROM funcionario WHERE email = '{}' OR matricula = '{}';".format(self.email, self.matricula)

        funcionario = cursor.execute(sql).fetchone()
        if not funcionario:
            return None

        funcionario = Funcionario(
            name=funcionario[1], email=funcionario[2], matricula=funcionario[3], password=funcionario[4]
        )
        return funcionario

    def insert_into_db(self):
        conn, cursor = connect_db()

        sql = "SELECT * FROM funcionario WHERE email = '{}' OR matricula = '{}';".format(self.email, self.matricula)

        funcionario = cursor.execute(sql).fetchone()
        
        if not funcionario:

            sql = """
                INSERT INTO funcionario (name, email, matricula, senha) VALUES ('{}', '{}', '{}', '{}')
            """.format(self.name, self.email, self.matricula, self.password)

            cursor.execute(sql)
            conn.commit()
            conn.close()

    def create(self):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()

        sql = """
            INSERT INTO funcionario (email, matricula, senha) VALUES ('{}', '{}', '{}')
        """.format(self.email, self.matricula, self.password)

        cursor.execute(sql)
        conn.commit()
        conn.close()

    def authenticate(self):
        conn, cursor = connect_db()

        sql = "SELECT * FROM funcionario WHERE matricula = '{}';".format(self.matricula)

        funcionario = cursor.execute(sql).fetchone()
        if not funcionario:
            return False

        else:
            if funcionario[4] == self.password:
                #self.session = True
                return True

        return False

#create_db()
#password = md5("12345".encode())
#password = password.hexdigest()
#f = Funcionario()
#print(f.get(email='funcionario@biblioteca.com'))

#Cliente.create(email="pp@ddsds.com", login="ppn", password=password)
