import sqlite3
from hashlib import md5

def create_db():
    conn = sqlite3.connect('biblioteca.db')
    cur = conn.cursor()
    sql_file = open('schema.sql')
    sql = sql_file.read()
    cur.executescript(sql)

    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())
    #conn.commit()
    

    password = md5(b'12345')
    password = password.hexdigest()
    sql = """ 
        INSERT INTO user (email, login, senha) VALUES ('ppnery95@gmail.com', 'ppnery', '{}');
    """.format(password)

    cur.execute(sql)

    conn.commit()
    print(cur.rowcount)
    email = 'ppnery@edu.unirio.br'
    sql = """ 
        SELECT * FROM user WHERE email = '{}';
    """.format(email)
    print(sql)

    cur.execute(sql)
    print(cur.fetchall())
    print(len(cur.fetchall()) == 0)
    cur.close()

create_db()