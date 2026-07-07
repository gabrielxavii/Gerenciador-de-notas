from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/leitura")
def leitura():
    return render_template("leitura.html")

@app.route("/roteiros")
def roteiros():
    return render_template("roteiros.html")

@app.route("/transportadoras")
def transportadoras():
    return render_template("transportadora.html")

if __name__ == "__main__":
    app.run(debug=True)