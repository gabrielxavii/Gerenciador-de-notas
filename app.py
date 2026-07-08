from flask import Flask, render_template, redirect, request
from database import(
    criar_banco,
    cadastrar_transportadora,
    listar_transportadoras,
    atualizar_transportadora,
    buscar_transportadora
)

app = Flask(__name__)

criar_banco()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/leitura")
def leitura():
    return render_template("leitura.html")

@app.route("/roteiros")
def roteiros():
    return render_template("roteiros.html")

@app.route("/transportadoras", methods=["GET", "POST"])
def transportadoras():

    if request.method == "POST":

        nome = request.form["nome"]

        cadastrar_transportadora(nome)

        return redirect("/transportadoras")
    
    transportadoras = listar_transportadoras()

    return render_template(
        "transportadoras.html",
        transportadoras=transportadoras
    )

@app.route("/transportadoras/<int:id>/editar", methods=["GET", "POST"])
def editar_transportadoras(id):

    if request.method == "POST":

        nome = request.form["nome"]

        atualizar_transportadora(id, nome)

        return redirect("/transportadoras")
    
    transportadora = buscar_transportadora(id)

    return render_template(
            "editar_transportadora.html",
            transportadora=transportadora
        )

if __name__ == "__main__":
    app.run(debug=True)