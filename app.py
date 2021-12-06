from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

#login = Login_Manager()

login_email = 'ppnery@edu.unirio.br'
login_password = 'pedronery'

@app.route("/", methods=['GET', 'POST'])
def index():
    #data = request.form['userLogin']
    #print(data)
    #print(url_for(index))
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    print(request.form.get("userLogin"))
    print(url_for('index'))
    if request.form.get("userLogin") == login_email and request.form.get("userPassword") == login_password:
        redirect(url_for('index'))
    return render_template("login.html")

@app.route("/cadastro")
def cadastro_cliente():
    return render_template("cadastro_cliente.html")
'''

@app.route("/admin")
def admin():
    return redirect(url_for("index"))
'''

if __name__ == "__main__":
    app.run()