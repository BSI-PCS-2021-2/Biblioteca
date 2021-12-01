from flask import Flask, redirect #, url_for, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "hello world!"

@app.route("/dashboard")
def dashboard():
    return "pagina do dashboard"

'''
@app.route("/admin")
def admin():
    return redirect(url_for("home"))
'''

if __name__ == "__main__":
    app.run()