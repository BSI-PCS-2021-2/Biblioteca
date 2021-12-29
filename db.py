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
    cur.close()

create_db()