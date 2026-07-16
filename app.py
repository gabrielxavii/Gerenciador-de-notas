from flask import Flask, render_template, redirect, request, url_for
from database import(
    criar_banco,
    cadastrar_transportadora,
    listar_transportadoras,
    atualizar_transportadora,
    buscar_transportadora,
    excluir_transportadora,
    criar_roteiro,
    listar_roteiros,
    buscar_roteiro,
    fechar_roteiro
)

app = Flask(__name__)

criar_banco()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/leitura")
def leitura():
    return render_template("leitura.html")

@app.route("/roteiros", methods=["GET", "POST"])
def roteiros():

    if request.method == "POST":

        criado = criar_roteiro()

        return redirect("/roteiros")
    
    roteiros = listar_roteiros()
    
    return render_template(
        "roteiros.html",
        roteiros=roteiros
        )

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

@app.route("/transportadora/<int:id>/excluir", methods= ["POST"])
def excluir_transportadora_rota(id):
    excluir_transportadora(id)
    return redirect(url_for("transportadoras"))

@app.route("/roteiros/<int:id>")
def vizualizar_roteiro(id):

    roteiro = buscar_roteiro(id)

    return render_template(
        "vizualizar_roteiro.html",
        roteiro=roteiro
    )

@app.route("/roteiros/<int:id>/fechar", methods=["POST"])
def fechar_roteiro_rota(id):

    fechar_roteiro(id)

    return redirect("/roteiros")

if __name__ == "__main__":
    app.run(debug=True)