from flask import Flask, redirect, url_for, render_template, request, flash
import pandas as pd
import sqlite3
from hashlib import md5
from db import create_db

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

user_login = 'ppnery'
login_password = 'pedronery'

funcionario_login = '000001'

cliente = {}

session_cliente = {
    'on':False
}
session_funcionario = {
    'on':False
}

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("home.html")

@app.route("/form_cliente")
def form_cliente():
    print(cliente)
    return render_template("form_cliente.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    client_db = pd.read_csv("client_db.csv", sep=";")
    #print(request.form.get("userLogin"))
    #print(email, password)
    if request.method == 'GET':
        return "Login via login form"

    if request.method == 'POST':
        #file = open("cadastro_clientes.txt", 'r')
        cliente = client_db.loc[client_db["login"] == request.form["userLogin"]]
        if len(cliente) == 1:
            if request.form["userLogin"] == cliente["login"].item() and str(request.form["userPassword"]) == str(cliente["senha"].item()):
                print(request.form["userLogin"])
                flash('Você está logado!')
                session_cliente["on"] = True
                #session_cliente["user_email"] = login_email
                session_cliente["user_login"] = request.form["userLogin"]
                return render_template('login_sucesso.html')
            else:
                #return redirect(url_for('form_cliente'))
                return render_template('login_insucesso.html')
        else:
            return render_template('login_insucesso.html')
        #return render_template("login.html")

@app.route("/cadastro")
def cadastro_cliente():
    
    return render_template("cadastro_cliente.html")

@app.route("/form_cadastro_cliente", methods=["GET", "POST"])
def form_cadastro():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()


    client_db = pd.read_csv("client_db.csv", sep=";")
    if request.method == "GET":
        return "Cadastro necessário"

    if request.method == "POST":
        #file = open("cadastro_clientes.txt", "r")
        sql = """
            SELECT * FROM user WHERE email = {} OR login = {}
        """.format(request.form["userEmail"], request.form["userLogin"])
        cursor.execute(sql)
        if len(cursor.fetchall()) != 0:
            return render_template("cadastro_cliente_insucesso.html")
        #if request.form["userEmail"] in client_db["email"].tolist() or request.form["userLogin"] in client_db["login"].tolist() or "@" not in request.form["userEmail"] or len(request.form["userPassword"]) < 5:
        #    return render_template("cadastro_cliente_insucesso.html")
        
        else:

            password = md5(request.form["userPassword"].encode())
            sql = """
                INSERT INTO user (email, login, senha) VALUES ({email}, {login}, {senha})
            """.format(email=request.form["userEmail"], login=request.form["userLogin"], senha=password.hexdigest())
            cursor.execute(sql)
            conn.commit()
        #else:
        #    cliente = pd.DataFrame(columns=['login', 'email', 'senha'], data=[[ request.form["userLogin"], request.form["userEmail"], request.form["userPassword"]]])
        #    client_db = client_db.append(cliente)
        #    client_db.to_csv("client_db.csv", sep=";")
        #    return render_template("cadastro_cliente_sucesso.html")


@app.route("/reclamacao")
def reclamacao():
    return render_template("reclamacao.html")

@app.route("/reclamacao_form", methods=["GET", "POST"])
def form_reclamacao():
    client_db = pd.read_csv("client_db.csv", sep=";")
    if request.method == "POST":
        if len(request.form["reclamacaoText"]) == 0 or request.form["userLogin"] not in client_db["login"].tolist():
            print(request.form["userLogin"], request.form["userEmail"], request.form["reclamacaoText"])
            return render_template("reclamacao_insucesso.html")
        else:
            return render_template("obrigado.html")

@app.route("/form_funcionario")
def form_funcionario():
    return render_template("form_funcionario.html")

@app.route("/login_funcionario", methods=["GET", "POST"])
def login_funcionario():
    #print(request.form.get("userLogin"))
    #print(email, password)
    if request.method == 'GET':
        return "Login via login form"

    if request.method == 'POST':
        if len(str(request.form["userLogin"])) == 6:
            if str(request.form["userLogin"]) == funcionario_login and str(request.form["userPassword"]) == str(login_password):
                print(request.form["userLogin"])
                flash('Você está logado!')
                session_funcionario["on"] = True
                #session["user_email"] = login_email
                session_funcionario["user_login"] = user_login
                return render_template('login_sucesso.html')

            else:
                return render_template("login_insucesso.html")
        else:
            return render_template("login_insucesso.html")
       
    #return render_template("login.html")

'''

@app.route("/admin")
def admin():
    return redirect(url_for("index"))
'''

if __name__ == "__main__":
    create_db()
    app.run()