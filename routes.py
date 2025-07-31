from flask import render_template, redirect, request, url_for
from extensions import db
from main import app
from models import Transacao, User
from users import verificador_user
from flask import flash

#rotas

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/cadastrar", methods=['POST'])
def cadastrar():
    descricao = request.form["descricao"]
    valor = float(request.form["valor"])
    tipo = request.form["tipo"]
    categoria = request.form['categoria']
    user_id = 1

    nova_transacao = Transacao(descricao=descricao, valor=valor,categoria=categoria, tipo=tipo, user_id=1) #user id temporario
    db.session.add(nova_transacao)
    db.session.commit()

    return redirect("/")

@app.route("/transacoes")
def listar_transacoes():
    transacoes = Transacao.query.all()
    return render_template("lista_transacoes.html", transacoes=transacoes)

@app.route("/deletar/<int:id>")
def deletar(id):
    transacao = Transacao.query.get_or_404(id)
    db.session.delete(transacao)
    db.session.commit()
    return redirect(url_for('listar_transacoes'))

@app.route("/editar_transacao/<int:id>", methods=['GET'])
def editar_transacao(id):
    transacao = Transacao.query.get_or_404(id)
    return render_template("editar_transacao.html", transacao=transacao)

@app.route('/atualizar_transacao/<int:id>', methods=['POST'])
def atualizar_transacao(id):
    transacao = Transacao.query.get_or_404(id)

    # Atualiza os dados
    transacao.valor = request.form['valor']
    transacao.tipo = request.form['tipo']
    transacao.categoria = request.form['categoria']
    transacao.descricao = request.form['descricao']

    db.session.commit()

    return redirect("/transacoes")

@app.route("/tela_login")
def tela_login():
    return render_template("login.html")

@app.route("/registro", methods=["POST", "GET"])
def registro():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        if verificador_user(email):
            flash("O usuario ja existe!", "erro")

        else:
            novo_user = User(email=email, senha=senha)
            db.session.add(novo_user)
            db.session.commit()
            flash("Cadastro feito com sucesso!", "sucesso")
            return redirect(url_for("tela_login"))

    return render_template("registro.html")
