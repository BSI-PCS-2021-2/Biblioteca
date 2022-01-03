import sqlite3

from flask_login import UserMixin 

from hashlib import md5

from db import *

class Funcionario(UserMixin):
    def __init__(self, name=None, email=None, matricula=None, password=None):
        #self.id = id_
        #self.name = name
        self.email = email
        self.matricula = matricula
        self.password = password

    def get(self, matricula=None, email=None):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()

        sql = "SELECT * FROM funcionario WHERE email = '{}' OR matricula = '{}';".format(email, matricula)

        funcionario = cursor.execute(sql).fetchone()
        if not funcionario:
            return None

        funcionario = Funcionario(
            email=funcionario[1], matricula=funcionario[2], password=funcionario[3]
        )
        return funcionario

    def create(self):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()

        sql = """
            INSERT INTO funcionario (email, matricula, senha) VALUES ('{}', '{}', '{}')
        """.format(self.email, self.matricula, self.password)

        cursor.execute(sql)
        conn.commit()
        conn.close()

#create_db()
#password = md5("12345".encode())
#password = password.hexdigest()
#f = Funcionario()
#print(f.get(email='funcionario@biblioteca.com'))

#Cliente.create(email="pp@ddsds.com", login="ppn", password=password)
