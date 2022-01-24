from flask import Flask, redirect, url_for, render_template, request, flash, session
import sqlite3
from hashlib import md5
import json
import os
from dotenv import load_dotenv

# Import das classes criadas para o projeto
from cliente import Cliente
from funcionario import Funcionario
from obra import *
from reclamacao import *

from oauthlib.oauth2 import WebApplicationClient
import requests

session_cliente = False

session_funcionario = False

from db import *

load_dotenv()

# Nao é a melhor maneira de tratar secret keys
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("home.html")

@app.route("/form_cliente")
def form_cliente():
    return render_template("form_cliente.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    conn, cursor = connect_db()
    global session_cliente

    if request.method == 'GET':
        return "Login via login form"

    if request.method == 'POST':
        
        password = md5(request.form["userPassword"].encode())
        password = password.hexdigest()
        cliente = Cliente(login=request.form["userLogin"], password=password)
        results = cliente.get()
        if not results:
            
            conn.close()
            return render_template('login_insucesso.html')

        else:
            
            if cliente.authenticate():
                
                session_cliente = True
                session["cliente_id"] = results[0]
                session["user_login"] = request.form["userLogin"]
                #cliente.session_on()
                conn.close()
                return render_template('cliente_dashboard.html', login=request.form["userLogin"])    

            else:
                
                conn.close()
                return render_template('login_insucesso.html')

@app.route("/cliente/dashboard")
def cliente_dashboard():
    global session_cliente
    if session_cliente:
        return render_template('cliente_dashboard.html', login=session["user_login"])
    return redirect( url_for("index") )

@app.route("/login-google")
def login_google():
    code = request.args.get("code")
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/login-g",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login-g")
def login_g():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
     # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    return render_template('login_sucesso.html')

@app.route("/cadastro")
def cadastro_cliente():
    global session_cliente
    print(session_cliente)
    if session_cliente:
        return redirect(url_for('index'))
    return render_template("cadastro_cliente.html")

@app.route("/form_cadastro_cliente", methods=["GET", "POST"])
def form_cadastro():
    conn, cursor = connect_db()

    if request.method == "GET":
        return "Cadastro necessário"

    if request.method == "POST":
        sql = """
            SELECT * FROM cliente WHERE email = '{}' OR login = '{}'
        """.format(request.form["userEmail"], request.form["userLogin"])
        cursor.execute(sql)
        cliente = cursor.fetchone()
        l = [request.form["userName"], request.form["userEmail"], request.form["userLogin"], request.form["userPassword"]]
        if cliente is not None or '' in l:
            conn.close()
            return render_template("cadastro_cliente_insucesso.html")
        
        else:

            password = md5(request.form["userPassword"].encode())
            password = password.hexdigest()

            cliente = Cliente(name=request.form["userName"], email=request.form["userEmail"], login=request.form["userLogin"], password=password)
            cliente.insert_into_db()
            print(cliente.get())
            
            return render_template("cadastro_cliente_sucesso.html")


@app.route("/reclamacao")
def reclamacao():
    global session_cliente 
    print(session_cliente)
    if session_cliente:
        return render_template("reclamacao.html")
    else:
        return redirect( url_for('index') )

@app.route("/reclamacao_form", methods=["GET", "POST"])
def form_reclamacao():
    conn, cur = connect_db()
    cliente = Cliente(login=request.form["userLogin"])
    print('test')
    if request.method == "POST":
        if len(request.form["reclamacaoText"]) == 0 or cliente.get() is None:
            print('test2')
            print(request.form["userLogin"], request.form["userEmail"], request.form["reclamacaoText"])
            return render_template("reclamacao_insucesso.html")
        else:
            #email, login, _ = cliente.get_data()
            print('test3')
            reclamacao = Reclamacao(
                login=request.form["userLogin"], recl=request.form["reclamacaoText"],
                email=request.form["userEmail"]
                )
            reclamacao.insert_into_db()
            return render_template("obrigado.html")

@app.route("/cliente/check-consulta")
def tela_consulta():
    global session_cliente
    if session_cliente:
        autores = get_autores()
        generos = get_generos()
        return render_template("consulta_emprestimo.html", autores=autores, generos=generos)
    else:
        return redirect( url_for("index") )

@app.route("/cliente/consulta", methods=["GET", "POST"])
def consulta_emprestimo():
    conn, cursor = connect_db()

    if request.method == "GET":
        return "Cadastro necessário"

    if request.method == "POST":
        # consultar se livro não foi emprestado

        if request.form["authorName"] == '' and request.form["assunto"] == '':
            return render_template("emprestimo_consulta_insucesso.html")
        
        else:
            if request.form["assunto"] != '' and request.form["authorName"] != '':
                print("t1")
                results = get_by_ag(nome_autor=request.form["authorName"], genero=request.form["assunto"])
                print(results)
                return render_template("consulta_sucesso.html", results=results)
            
            if request.form["assunto"] != '':
                print("t2")
                results = get_by_genero(genero=request.form["assunto"])
                print(results)
                return render_template("consulta_sucesso.html", results=results)

            if request.form["authorName"] != '':
                print("t3")
                results = get_by_author(nome_autor=request.form["authorName"])
                print(results)
                return render_template("consulta_sucesso.html", results=results)

            #if request.form["posicao"]: 
            #    obra = Obra(posicao=request.form["posicao"])
            #    obra = obra.get()
            #    print(obra.titulo)
            #    titulo, data_emprestimo, data_devolucao = obra.emprestar(cliente_id=session["cliente_id"])
            #    return render_template("emprestimo_sucesso.html", obra=obra, data_emprestimo=data_emprestimo, data_devolucao=data_devolucao)

            return render_template("emprestimo_consulta_insucesso.html")

@app.route("/cliente/emprestimo", methods=["GET", "POST"])
def emprestimo():
    conn, curr = connect_db()

    if request.method == "POST":
        # consultar se livro não foi emprestado
        if request.form["posicao"] != '': 
            obra = Obra(posicao=request.form["posicao"])
            
            obra = obra.get()
            print(obra.titulo)
            titulo, data_emprestimo, data_devolucao = obra.emprestar(cliente_id=session["cliente_id"])
            return render_template("emprestimo_sucesso.html", obra=obra, data_emprestimo=data_emprestimo, data_devolucao=data_devolucao)

@app.route("/cliente/check-obras-emprestadas")
def tela_emprestimos():
    if session_cliente:
        
        emprestimos = get_emprestimos(session["cliente_id"])
        print(emprestimos)
        return render_template("obras_emprestadas.html", emprestimos=emprestimos)
    return render_template( url_for("index") )


@app.route("/cliente/devolver-obra", methods=["GET", "POST"])
def devolver_obra():
    conn, curr = connect_db()

    if request.method == "POST":
        # consultar se livro não foi emprestado
        if request.form["posicao"]: 
            session["obra_posicao"] = request.form["posicao"]
            obra = Obra(posicao=request.form["posicao"])
            obra = obra.get()
            print(obra.titulo)
            obra.devolver(cliente_id=session["cliente_id"])
            return render_template("devolucao_sucesso.html", obra=obra)

@app.route("/cliente/check-avaliar")
def tela_avaliacao():
    global session_cliente
    if session_cliente:
        session["emprestimo"] = get_emprestimo(session["cliente_id"], session["obra_posicao"]) 
        #emprestimo = get_emprestimo(session["cliente_id"])
        print(session["emprestimo"])
        return render_template("avaliar_obra.html", emprestimo=session["emprestimo"])
    else:
        return redirect( url_for("index") )

@app.route("/cliente/avaliar-positivo")
def avaliar_positivo():
    conn, cursor = connect_db()
    session["emprestimo"] = get_emprestimo(session["cliente_id"], session["obra_posicao"])
    avaliar_emprestimo(emprestimo_id=session["emprestimo"][3], avaliacao=2)

    return render_template("avaliacao_positiva.html")

@app.route("/cliente/avaliar-negativo")
def avaliar_negativo():
    conn, cursor = connect_db()
    session["emprestimo"] = get_emprestimo(session["cliente_id"], session["obra_posicao"])
    avaliar_emprestimo(emprestimo_id=session["emprestimo"][3], avaliacao=1)

    return render_template("avaliacao_negativa.html")
        

@app.route("/cadastro_funcionario")
def cadastro_funcionario():
    if session_funcionario:
        return render_template("cadastro_funcionario.html", session_funcionario=session_funcionario)

    else:
        return redirect( url_for("index") )

@app.route("/form_cadastro_funcionario", methods=["GET", "POST"])
def form_cadastro_funcionario():
    conn, cursor = connect_db()

    if request.method == "GET":
        return "Cadastro necessário"

    if request.method == "POST":
        sql = """
            SELECT * FROM funcionario WHERE email = '{}'
        """.format(request.form["userEmail"])
        cursor.execute(sql)
        funcionario = cursor.fetchone()
        l = [request.form["userEmail"], request.form["userMatricula"], request.form["userPassword"]]
        if funcionario is not None or '' in l:
            conn.close()
            return render_template("cadastro_funcionario_insucesso.html")
        
        else:

            password = md5(request.form["userPassword"].encode())
            password = password.hexdigest()

            funcionario = Funcionario(email=request.form["userEmail"], matricula=request.form["userMatricula"], password=password)
            funcionario.insert_into_db()
            print(funcionario.get())
            
            return render_template("cadastro_funcionario_sucesso.html")

@app.route("/form_funcionario")
def form_funcionario():
    return render_template("form_funcionario.html")

@app.route("/login_funcionario", methods=["GET", "POST"])
def login_funcionario():
    conn, cursor = connect_db()
    
    global session_funcionario

    if request.method == 'GET':
        return "Login via login form"

    if request.method == 'POST':
        
        password = md5(request.form["userPassword"].encode())
        password = password.hexdigest()
        funcionario = Funcionario(matricula=request.form["userMatricula"], password=password)
        results = funcionario.get()
        print(results)
        if not results:
            
            conn.close()
            return render_template("login_insucesso.html")

        else:
            if funcionario.authenticate():
                session_funcionario = True
                conn.close()
                return redirect(url_for("func_check_dashboard"))

            else:
                
                conn.close()
                return render_template("login_insucesso.html")
        


@app.route("/funcionario/check-dashboard")
def func_check_dashboard():
    if session_funcionario:
        return render_template("funcionario_dashboard.html")
    else:
        return redirect( url_for("index") )

@app.route("/funcionario/dashboard", methods=["GET", "POST"])
def funcinario_dashboard():
    
    pass

@app.route("/funcionario/obra", methods=["GET", "POST"])
def tela_obras():
    if session_funcionario:
        return render_template("tela_obras.html")
    else:
        return redirect( url_for("index") )

@app.route("/funcionario/obra/check-cadastro", methods=["GET", "POST"])
def tela_cadastro_obra():
    if session_funcionario:
        return render_template("cadastro_obras.html")
    else:
        return redirect( url_for("index") )

@app.route("/funcionario/obra/cadastro", methods=["GET", "POST"])
def cadastrar_obra():
    conn, cursor = connect_db()

    if request.method == "GET":
        return "Cadastro necessário"

    if request.method == "POST":

        obra = Obra(titulo=request.form["obraName"], autor=request.form["authorName"],
                assunto=request.form["assunto"], data_publicacao=request.form["date"],
                posicao=request.form["posicao"])
        l = [request.form["obraName"], request.form["authorName"], request.form["assunto"],
            request.form["date"], request.form["posicao"]]
        print(l)
        if obra.get() or '' in l:
            return render_template("cadastro_obra_insucesso.html", titulo=request.form["obraName"])
        
        else:
            obra.insert_into_db()
            return render_template("cadastro_obra_sucesso.html", titulo=request.form["obraName"])

@app.route("/funcionario/obra/check-consulta")
def tela_consulta_obras():
    if session_funcionario:
        return render_template("consulta_obra.html")
    else:
        return redirect( url_for("index") )

@app.route("/funcionario/obra/consulta", methods=["GET", "POST"])
def consulta_obra():
    conn, cursor = connect_db()

    if request.method == "GET":
        return "Cadastro necessário"

    if request.method == "POST":
        
        obra = Obra(posicao=request.form["posicao"])

        if obra.get():
            titulo, autor, assunto, data, posicao, id = obra.get_data()
            return render_template("consulta_obra_sucesso.html", titulo=titulo, autor=autor, assunto=assunto, data=data, posicao=posicao)

        else:
            return render_template("consulta_obra_insucesso.html", posicao=request.form["posicao"])

@app.route("/funcionario/obra/check-baixa")
def tela_baixa_obra():
    if session_funcionario:
        obras = get_obra_sem_baixa()
        print(obras)
        return render_template("baixa_obra.html", obras=obras)
    else:
        return redirect( url_for("index") )

@app.route("/funcionario/obra/check-baixa", methods=["GET", "POST"])
def dar_baixa():
    conn, curr = connect_db()

    if request.method == "POST":
        # consultar se livro não foi emprestado
        if request.form["posicao"] != '': 
            obra = Obra(posicao=request.form["posicao"])
            dar_baixa_obra(request.form["posicao"])
            obra = obra.get()
            #print(obra.titulo)
            #titulo, data_emprestimo, data_devolucao = obra.emprestar(cliente_id=session["cliente_id"])
            return render_template("baixa_sucesso.html", obra=obra)


@app.route("/funcionario/obra/check-remocao")
def tela_remocao_obra():
    if session_funcionario:
        return render_template("remocao_obra.html")
    else:
        return redirect( url_for("index") )

@app.route("/funcionario/obra/remocao", methods=["GET", "POST"])
def remover_obra():
    conn, cursor = connect_db()

    if request.method == "GET":
        return "Cadastro necessário"

    if request.method == "POST":

        obra = Obra(posicao=request.form["posicao"])

        if obra.get():
            titulo, autor, assunto, data, posicao, id = obra.get_data()
            session["titulo_obra"] = titulo
            session["posicao_obra"] = posicao
            return render_template("remocao_obra_sucesso.html", titulo=titulo, autor=autor, assunto=assunto, data=data, posicao=posicao)

        else:
            return render_template("consulta_obra_insucesso.html", posicao=request.form["posicao"])

@app.route("/funcionario/obra/confirmar-remocao", methods=["GET", "POST"])
def confirmar_remocao_obra():
    conn, cursor = connect_db()

    titulo = session.get("titulo_obra")
    posicao = session.get("posicao_obra")
    print(titulo)

    if request.method == "GET":
        return "Cadastro necessário"

    if request.method == "POST":

        obra = Obra(posicao=posicao)

        if obra.get():
            
            titulo = request.form["obraName"]
            obra.delete()
            return render_template("remocao_obra_finalizada.html", titulo=titulo)

        else:
            return render_template("consulta_obra_insucesso.html", posicao=posicao)

@app.route("/funcionario/check-reclamacao")
def tela_reclamacao():
    if session_funcionario:
        reclamacao = get_old_reclamacao()
        print(reclamacao)
        session["reclamacao"] = reclamacao
        return render_template("funcionario_reclamacao.html", reclamacao=reclamacao)
    else:
        return redirect( url_for("index") )

@app.route("/funcionario/reclamacao", methods=["GET", "POST"])
def responder_reclamacao():
    conn, cursor = connect_db()

    if request.method == "GET":
        return "Cadastro necessário"

    if request.method == "POST":
        if request.form["reclamacaoText"] is None:
            return render_template("resposta_erro.html")
        else:
            session["reclamacao"][0]
            update_reclamacao(session["reclamacao"][0])
            return render_template("resposta_acerto.html")

@app.route("/logout")
def logout():
    global session_cliente
    if session_cliente:
        session_cliente = False
        return redirect( url_for("index") )

    global session_funcionario
    if session_funcionario:
        session_funcionario = False
        return redirect( url_for("index") )
    return redirect( url_for("index") )


if __name__ == "__main__":
    create_db()
    app.run()