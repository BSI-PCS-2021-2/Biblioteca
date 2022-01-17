import sqlite3

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

        if obra is None:
            return None

        sql = "SELECT * FROM emprestimo WHERE cliente_id = {} AND obra_id = {} AND devolvido = FALSE".format(cliente_id, obra.obra_id)
        
        results = cursor.execute(sql).fetchall()
        if results is None:
            sql = """
                INSERT INTO emprestimo (cliente_id, obra_id) VALUES {}, {}
            """.format(cliente_id, obra.obra_id)

            cursor.execute(sql)
            conn.commit()
            

            sql = "SELECT * FROM emprestimo WHERE cliente_id = {} AND obra_id = {} AND devolvido = FALSE".format(cliente_id, obra.obra_id)

            results = cursor.execute(sql).fetchone()

            return obra.titulo, 

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

def get_emprestimo(client_id):
    conn, cursor = connect_db()

    sql = """
        SELECT titulo, DATE(data_emprestimo), DATE(data_devolucao), emprestimo.id
        FROM emprestimo INNER JOIN obra ON obra_id = obra.id 
         WHERE cliente_id = {} ORDER BY data_emprestimo ASC LIMIT 1
    """.format(client_id)

    results = cursor.execute(sql).fetchone()

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
    
    
create_db()
print(get_emprestimo(1))
#o = Obra(titulo="Teste 1", autor="Nery Pedro", assunto="Terror", data_publicacao="2019-02-01", posicao="A2")
#o.insert_into_db()
#print(o.get())
    