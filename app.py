from flask import Flask, redirect, url_for, render_template, request, flash


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

user_login = 'ppnery'
login_password = 'pedronery'

funcionario_login = 'ppnery@biblioteca.com'

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
    return render_template("form_cliente.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    #print(request.form.get("userLogin"))
    #print(email, password)
    if request.method == 'GET':
        return "Login via login form"

    if request.method == 'POST':
        if request.form["userLogin"] == user_login and request.form["userPassword"] == login_password:
            print(request.form["userLogin"])
            flash('Você está logado!')
            session_cliente["on"] = True
            #session_cliente["user_email"] = login_email
            session_cliente["user_login"] = user_login
            return render_template('login_sucesso.html')
        else:
            redirect(url_for('form_cliente'))
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
        if request.form["userEmail"] in file.read() or request.form["userLogin"]:
            return render_template("cadastro_cliente_insucesso.html")
        
        else:
            file = open("cadastro_clientes.txt", "w")
            file.write(request.form["userLogin"] + "\n")
            file.write(request.form["userPassword"] + "\n")
            file.write(request.form["userEmail"] + "\n")
            file.close()
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
        if "@biblioteca.com" in request.form["userLogin"]:
            if request.form["userLogin"] == funcionario_login and request.form["userPassword"] == login_password:
                print(request.form["userLogin"])
                flash('Você está logado!')
                session_funcionario["on"] = True
                #session["user_email"] = login_email
                session_funcionario["user_login"] = user_login
                return render_template('login_sucesso.html')

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