from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/leitura")
def leitura():
    return "<h1>Leitura</h1>"

@app.route("/roteiros")
def roteiros():
    return "<h1>Roteiros</h1>"

@app.route("/transportadoras")
def transportadoras():
    return "<h1>Transportadoras</h1>"

if __name__ == "__main__":
    app.run(debug=True)