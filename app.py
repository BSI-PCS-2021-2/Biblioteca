from flask import Flask, redirect, url_for, render_template, request, flash


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
    
    #print(request.form.get("userLogin"))
    #print(email, password)
    if request.method == 'GET':
        return "Login via login form"

    if request.method == 'POST':
        file = open("cadastro_clientes.txt", 'r')
    
        if request.form["userLogin"] == cliente["login"] and str(request.form["userPassword"]) == cliente["password"]:
            print(request.form["userLogin"])
            flash('Você está logado!')
            session_cliente["on"] = True
            #session_cliente["user_email"] = login_email
            session_cliente["user_login"] = request.form["userLogin"]
            return render_template('login_sucesso.html')
        else:
            #return redirect(url_for('form_cliente'))
            return render_template('login_insucesso.html')
    #return render_template("login.html")

@app.route("/cadastro")
def cadastro_cliente():
    
    return render_template("cadastro_cliente.html")

@app.route("/form_cadastro_cliente", methods=["GET", "POST"])
def form_cadastro():
    if request.method == "GET":
        return "Cadastro necessário"

    if request.method == "POST":
        file = open("cadastro_clientes.txt", "r")
        if request.form["userEmail"] in file.read() or request.form["userLogin"] in file.read() or "@" not in request.form["userEmail"]:
            return render_template("cadastro_cliente_insucesso.html")
        
        else:
            cliente["login"] = request.form["userLogin"]
            cliente["password"] = request.form["userPassword"]
            cliente["email"] = request.form["userEmail"]
            
            #file = open("cadastro_clientes.txt", "w")
            #file.write(request.form["userLogin"] + " ")
            #file.write(request.form["userPassword"] + " ")
            #file.write(request.form["userEmail"] + " ")
            #file.close()
            return render_template("cadastro_cliente_sucesso.html")


@app.route("/reclamacao")
def reclamacao():
    return render_template("reclamacao.html")

@app.route("/reclamacao_form", methods=["GET", "POST"])
def form_reclamacao():
    if request.method == "POST":
        print(request.form["userLogin"], request.form["userEmail"], request.form["reclamacaoText"])
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
            if str(request.form["userLogin"]) == funcionario_login and request.form["userPassword"] == login_password:
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
    app.run()