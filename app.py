import sqlite3
from flask import Flask, render_template, redirect, request, url_for, flash
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
    fechar_roteiro,
    buscar_roteiro_aberto,
    cadastrar_nota,
    listar_notas,
    listar_notas_roteiro,
    voltar_pendente,
    marcar_pronta,
    pesquisar_notas,
    total_notas,
    total_pendentes,
    total_prontas,
    total_poor_transportadora,
    existe_roteiro_aberto
    
)

app = Flask(__name__)

app.secret_key = "logisticweb"

criar_banco()

# ==========================
# DASHBOARD
# ==========================

@app.route("/")
def dashboard():

    total = total_notas()
    pendentes = total_pendentes()
    prontas = total_prontas()
    totais_transportadoras = total_poor_transportadora()


    if total > 0:
        porcentagem_pendentes = round((pendentes / total) * 100, 1)
        porcentagem_prontas = round((prontas / total) * 100, 1)
    else:
        porcentagem_pendentes = 0
        porcentagem_prontas = 0

    return render_template(
        "dashboard.html",
        total=total,
        pendentes=pendentes,
        prontas=prontas,
        porcentagem_pendentes=porcentagem_pendentes,
        porcentagem_prontas=porcentagem_prontas,
        totais_transportadoras=totais_transportadoras
        )


# ==========================
# NOTAS
# ==========================

@app.route("/leitura", methods=["GET", "POST"])
def leitura():

    if request.method == "POST":

        numero_nf = request.form["numero_nf"]
        transportadora_id = request.form["transportadora_id"]

        if not numero_nf:
            flash("Informe o número da nota fiscal.", "error")
            return redirect("/leitura")

        if not transportadora_id:
            flash("Selecione uma transportadora.", "error")
            return redirect("/leitura")

        try:

            cadastrar_nota(numero_nf, transportadora_id)

            flash("Nota cadastrada com sucesso!!", "success")

        except sqlite3.IntegrityError:

            flash("Essa nota fiscal já está cadastrada", "error")

        return redirect("/leitura")
    
    transportadoras = listar_transportadoras()

    pesquisa = request.args.get("pesquisa","")

    if pesquisa:

        notas = pesquisar_notas(pesquisa)

    else:

        notas = listar_notas()

    return render_template(
    "leitura.html",
    transportadoras=transportadoras,
    notas=notas
    )

@app.route("/notas/<int:id>/pronta", methods=["POST"])
def marcar_pronta_rota(id):

    marcar_pronta(id)

    return redirect(request.referrer)

@app.route("/notas/<int:id>/pendente", methods=["POST"])
def voltar_pendente_rota(id):

    voltar_pendente(id)

    return redirect(request.referrer)

# ==========================
# ROTEIROS
# ==========================

@app.route("/roteiros", methods=["GET", "POST"])
def roteiros():

    if request.method == "POST":

        if existe_roteiro_aberto():
        
                flash(
                    "Já existe um roteiro aberto. Feche o roteiro atual antes de criar outro.",
                    "error"
                )
        
                return redirect("/roteiros")

        criado = criar_roteiro()

        flash(
            "Roteiro aberto com sucesso!",
            "success"
        )

        return redirect("/roteiros")
    
    roteiros = listar_roteiros()
    
    return render_template(
        "roteiros.html",
        roteiros=roteiros
        )

@app.route("/roteiros/<int:id>")
def vizualizar_roteiro(id):

    roteiro = buscar_roteiro(id)

    notas = listar_notas_roteiro(id)

    return render_template(
        "vizualizar_roteiro.html",
        roteiro=roteiro,
        notas=notas
    )

@app.route("/roteiros/<int:id>/fechar", methods=["POST"])
def fechar_roteiro_rota(id):

    fechar_roteiro(id)

    return redirect("/roteiros")

# ==========================
# TRANSPORTADORAS
# ==========================
@app.route("/transportadoras", methods=["GET", "POST"])
def transportadoras():

    if request.method == "POST":

        nome = request.form["nome"].strip()

        if not nome:
            flash("Informe o nome da transportadora.", "error")
            return redirect("/transportadoras")

        try:
            cadastrar_transportadora(nome)

            flash("Transportadora cadastrada com sucesso!", "success")

        except sqlite3.IntegrityError:

            flash("Essa transportadora já está cadastrada.", "error")

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




if __name__ == "__main__":
    app.run(debug=True)