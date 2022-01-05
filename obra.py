import sqlite3

from db import *

class Obra():
    def __init__(self, titulo=None, autor=None, assunto=None, data_publicacao=None, posicao=None):
        self.titulo = titulo
        self.autor = autor
        self.assunto = assunto
        self.data_publicacao = data_publicacao
        self.posicao = posicao

    def get(self):
        conn, cursor = connect_db()

        sql = "SELECT * FROM obra WHERE posicao = '{}';".format(self.posicao)

        obra = cursor.execute(sql).fetchone()
        if not obra:
            return None
        print(obra)
        obra = Obra(
            titulo=obra[1], autor=obra[2], assunto=obra[3], data_publicacao=obra[4],
            posicao=obra[1]
        )
        return obra

    def insert_into_db(self):
        conn, cursor = connect_db()

        sql = "SELECT * FROM obra WHERE posicao = '{}';".format(self.posicao)

        obra = cursor.execute(sql).fetchone()
        
        if not obra:

            sql = """
                INSERT INTO obra (titulo, nome_autor, assunto, data_publicacao, posicao) 
                VALUES ('{}', '{}', '{}', '{}', '{}')
            """.format(self.titulo, self.autor, self.assunto, self.data_publicacao, self.posicao)

            cursor.execute(sql)
            conn.commit()
            conn.close()

    def get_data(self):
        conn, cursor = connect_db()

        sql = "SELECT * FROM obra WHERE posicao = '{}';".format(self.posicao)

        obra = cursor.execute(sql).fetchone()
        if not obra:
            return None

        titulo, autor, assunto, data_publicacao, posicao = obra[1], obra[2], obra[3], obra[4], obra[5]
        return titulo, autor, assunto, data_publicacao, posicao

    def delete(self):
        conn, cursor = connect_db()

        sql = "SELECT * FROM obra WHERE posicao = '{}';".format(self.posicao)

        obra = cursor.execute(sql).fetchone()
        if not obra:
            return
        
        sql = "DELETE FROM obra WHERE posicao = '{}';".format(self.posicao)

        cursor.execute(sql)
        conn.commit()
        conn.close()
    
#create_db()
#o = Obra(titulo="Teste 1", autor="Nery Pedro", assunto="Terror", data_publicacao="2019-02-01", posicao="A2")
#o.insert_into_db()
#print(o.get())
    