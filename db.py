import sqlite3
from datetime import datetime, timedelta
from hashlib import md5

def create_db():
    conn = sqlite3.connect('biblioteca.db')
    cur = conn.cursor()
    sql_file = open('schema.sql')
    sql = sql_file.read()
    cur.executescript(sql)
    #conn.commit()
    

    password = md5(b'12345')
    password = password.hexdigest()
    sql = """ 
        INSERT INTO cliente (name, email, login, senha) VALUES ('Pedro Nery', 'ppnery95@gmail.com', 'ppnery', '{}');
    """.format(password)

    cur.execute(sql)

    conn.commit()
    
    email = 'ppnery@edu.unirio.br'
    sql = """ 
        SELECT * FROM cliente WHERE email = '{}';
    """.format(email)

    cur.execute(sql)

    sql = """
        INSERT INTO funcionario (name, email, matricula, senha) VALUES ('Sr Funcionario', 'funcionario@biblioteca.com', '000001', '{}')
    """.format(password)

    cur.execute(sql)

    sql = """
        INSERT INTO obra (titulo, nome_autor, assunto, data_publicacao, posicao, baixa) 
        VALUES ('Obra de Teste', 'Tiago Nunes', 'História', '2020-01-01', 'A1', False)
    """

    cur.execute(sql)

    sql = """
        INSERT INTO obra (titulo, nome_autor, assunto, data_publicacao, posicao) 
        VALUES ('Obra de Teste 2', 'Tiago N', 'Romance', '2020-01-01', 'C1')
    """

    cur.execute(sql)

    sql = """
        INSERT INTO reclamacao (cliente_email, cliente_login, reclamacao) 
        VALUES ('ppnery95@gmail.com', 'ppnery', 'Recomendo a compra do livro "X"')
    """

    cur.execute(sql)

    sql = """
        INSERT INTO emprestimo (cliente_id, obra_id, data_emprestimo, data_devolucao) 
        VALUES (1, 1, '{}', '{}')
    """.format(datetime.now() + timedelta(days=-15), datetime.now() + timedelta(days=-1))

    cur.execute(sql)

    conn.commit()
    cur.close()

def connect_db():
    conn = sqlite3.connect('biblioteca.db')
    cur = conn.cursor()
    return conn, cur

#create_db()