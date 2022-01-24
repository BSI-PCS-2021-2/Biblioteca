import sqlite3
from datetime import datetime, timedelta

from db import *

class Obra():
    def __init__(self, titulo=None, autor=None, assunto=None, data_publicacao=None, posicao=None, obra_id=None):
        self.titulo = titulo
        self.autor = autor
        self.assunto = assunto
        self.data_publicacao = data_publicacao
        self.posicao = posicao
        self.obra_id = obra_id

    def get(self):
        conn, cursor = connect_db()

        sql = "SELECT * FROM obra WHERE posicao = '{}';".format(self.posicao)

        obra = cursor.execute(sql).fetchone()
        if not obra:
            return None
        print(obra)
        obra_id = obra[0]
        obra = Obra(
            titulo=obra[1], autor=obra[2], assunto=obra[3], data_publicacao=obra[4],
            posicao=obra[5], obra_id=obra[0]
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

        obra_id, titulo, autor, assunto, data_publicacao, posicao = obra[0], obra[1], obra[2], obra[3], obra[4], obra[5]
        return titulo, autor, assunto, data_publicacao, posicao, obra_id

    def emprestar(self, cliente_id):
        conn, cursor = connect_db()

        obra = self.get_data()
        print(obra)
        if obra is None:
            return None

        sql = "SELECT * FROM emprestimo WHERE obra_id = {} AND devolvido = FALSE".format(obra[5])
        
        results = cursor.execute(sql).fetchall()
        print(results)
        if not results:
            today = datetime.today()
            return_date = timedelta(days=14)
            return_date = today + return_date
            print(today, return_date)
            sql = """
                INSERT INTO emprestimo (cliente_id, obra_id, data_emprestimo, data_devolucao) VALUES ({}, {}, '{}', '{}')
            """.format(cliente_id, obra[5], today, return_date)

            cursor.execute(sql)

            sql = "UPDATE obra SET baixa = False WHERE id = {}".format(obra[5])
    
            cursor.execute(sql)
            conn.commit()
            print(obra[5], today, return_date)
            return obra[5], today, return_date

        return None

    def devolver(self, cliente_id):
        conn, cursor = connect_db()
        
        sql = "UPDATE EMPRESTIMO SET devolvido = True WHERE obra_id = {} AND cliente_id = {} AND devolvido = False".format(self.obra_id, cliente_id)
        cursor.execute(sql)

        sql = "UPDATE obra SET baixa = False WHERE id = {}".format(self.obra_id)
    
        cursor.execute(sql)
        conn.commit()

        sql = "SELECT * FROM emprestimo WHERE devolvido = False"
        print(cursor.execute(sql).fetchall())


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

def get_emprestimo(cliente_id, obra_posicao):
    conn, cursor = connect_db()

    sql = """
        SELECT titulo, DATE(data_emprestimo), DATE(data_devolucao), emprestimo.id
        FROM emprestimo INNER JOIN obra ON obra_id = obra.id 
         WHERE cliente_id = {} AND posicao = '{}' ORDER BY data_emprestimo ASC LIMIT 1
    """.format(cliente_id, obra_posicao)
    #print(sql)
    results = cursor.execute(sql).fetchone()

    return results

def get_emprestimos(cliente_id):
    conn, cursor = connect_db()

    sql = """
    SELECT titulo, DATE(data_emprestimo), DATE(data_devolucao), posicao
    FROM emprestimo INNER JOIN obra ON obra_id = obra.id 
        WHERE cliente_id = {} AND devolvido = False ORDER BY data_emprestimo ASC LIMIT 3
    """.format(cliente_id)
    #print(sql)

    results = cursor.execute(sql).fetchall()

    return results

def avaliar_emprestimo(emprestimo_id, avaliacao):
    conn, cursor = connect_db()

    if avaliacao == 1:
        sql = """
            UPDATE emprestimo SET avaliacao = 1 WHERE id = {}
        """.format(emprestimo_id)

        cursor.execute(sql)
        conn.commit()
        conn.close()
    
    if avaliacao == 2:
        sql = """
            UPDATE emprestimo SET avaliacao = 2 WHERE id = {}
        """.format(emprestimo_id)

        cursor.execute(sql)
        conn.commit()
        conn.close()

def get_autores():
    conn, curr = connect_db()

    sql = "SELECT DISTINCT nome_autor FROM obra"

    nome_autores = curr.execute(sql).fetchall()

    return nome_autores

def get_generos():
    conn, curr = connect_db()

    sql = "SELECT DISTINCT assunto FROM obra"

    generos = curr.execute(sql).fetchall()

    return generos
    
def get_by_ag(nome_autor, genero):
    conn, cur = connect_db()
    
    sql = """SELECT titulo, nome_autor, assunto, posicao, devolvido 
    FROM obra LEFT JOIN emprestimo ON obra.id = obra_id WHERE nome_autor = '{}' AND assunto = '{}'
    """.format(nome_autor, genero)
    #print(sql)
    results = cur.execute(sql).fetchall()

    return results

def get_by_author(nome_autor):
    conn, cur = connect_db()
    
    sql = """SELECT titulo, nome_autor, assunto, posicao, devolvido 
    FROM obra LEFT JOIN emprestimo ON obra.id = obra_id WHERE nome_autor = '{}' AND baixa = 1
    """.format(nome_autor)
    #print(sql)
    results = cur.execute(sql).fetchall()

    return results

def get_by_genero(genero):
    conn, cur = connect_db()
    
    sql = """SELECT titulo, nome_autor, assunto, posicao, devolvido 
    FROM obra LEFT JOIN emprestimo ON obra.id = obra_id WHERE assunto = '{}' AND baixa = 1
    """.format(genero)
    #print(sql)
    results = cur.execute(sql).fetchall()

    return results

def get_obra_sem_baixa():
    conn, cur = connect_db()

    sql = "SELECT titulo, nome_autor, assunto, posicao FROM obra WHERE baixa = 0"
    results = cur.execute(sql).fetchall()

    return results

def dar_baixa_obra(obra_posicao):
    conn, cur = connect_db()

    sql = "UPDATE obra SET baixa = True WHERE posicao = '{}'".format(obra_posicao)
    cur.execute(sql)
    conn.commit()
    sql = "SELECT * FROM obra WHERE posicao = '{}'".format(obra_posicao)
    
    print(cur.execute(sql).fetchone())

#create_db()
#print(get_generos(), get_autores())
#print(get_by_ag(nome_autor="Tiago N", genero="Romance"))
#print(get_by_author(nome_autor="Tiago N"))
#print(get_by_genero(genero="História"))
#print(get_emprestimos(1))
#o = Obra(titulo="Teste 1", autor="Nery Pedro", assunto="Terror", data_publicacao="2019-02-01", posicao="A2")
#o.insert_into_db()
#print(o.get())
    