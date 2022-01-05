import sqlite3
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
        INSERT INTO cliente (email, login, senha) VALUES ('ppnery95@gmail.com', 'ppnery', '{}');
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
        INSERT INTO obra (titulo, nome_autor, assunto, data_publicacao, posicao) 
        VALUES ('Obra de Teste', 'Valeska Popozuda', 'História', '2020-01-01', 'A1')
    """.format(password)

    cur.execute(sql)

    sql = """
        INSERT INTO reclamacao (cliente_email, cliente_login, reclamacao) 
        VALUES ('ppnery95@gmail.com', 'ppnery', 'Recomendo a compra do livro "X"')
    """.format(password)

    cur.execute(sql)

    conn.commit()
    cur.close()

def connect_db():
    conn = sqlite3.connect('biblioteca.db')
    cur = conn.cursor()
    return conn, cur

#create_db()