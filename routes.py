from flask import render_template, redirect, request, url_for
from extensions import db
from main import app
from models import Transacao, User
from users import verificador_user
from flask import flash, session

#rotas

@app.route("/")
def homepage():
    return redirect("/tela_login")

@app.route("/cadastrar", methods=['POST', "GET"])
def cadastrar():
    if "user_id" not in session:
        flash("Você precisa estar logado para cadastrar uma transação.")
        return redirect("/tela_login")

    if request.method == "POST":
        descricao = request.form["descricao"]
        valor = float(request.form["valor"])
        tipo = request.form["tipo"]
        categoria = request.form['categoria']
        user_id = session["user_id"]

        nova_transacao = Transacao(descricao=descricao, valor=valor,categoria=categoria, tipo=tipo, user_id=user_id)
        db.session.add(nova_transacao)
        db.session.commit()

        return redirect("/cadastrar")
    
    return render_template("homepage.html")

@app.route("/transacoes")
def listar_transacoes():
    if "user_id" not in session:
        flash("Faça login para acessar suas transações.")
        return redirect("/tela_login")

    user_id = session["user_id"]
    transacoes = Transacao.query.filter_by(user_id=user_id).all()
    variavel_teste = 1

    nomes_gastos = [t.descricao for t in transacoes if t.tipo == "gasto"]
    valores_gastos = [t.valor for t in transacoes if t.tipo == "gasto"]

    nomes_entradas = [t.descricao for t in transacoes if t.tipo == "entrada"]
    valores_entradas = [t.valor for t in transacoes if t.tipo == "entrada"]

    return render_template("lista_transacoes.html", transacoes=transacoes, nomes_gastos=nomes_gastos,
                           valores_gastos=valores_gastos,
                           nomes_entradas=nomes_entradas,
                           valores_entradas=valores_entradas,
                           variavel_teste=variavel_teste)


#@app.route("/grafico")
#def grafico():
    if "user_id" not in session:
        flash("Faça login para acessar.")
        return redirect("/tela_login")

    user_id = session["user_id"]
    transacoes = Transacao.query.filter_by(user_id=user_id).all()

    nomes_gastos = [t.descricao for t in transacoes if t.tipo == "gasto"]
    valores_gastos = [t.valor for t in transacoes if t.tipo == "gasto"]

    nomes_entradas = [t.descricao for t in transacoes if t.tipo == "entrada"]
    valores_entradas = [t.valor for t in transacoes if t.tipo == "entrada"]

    return render_template("lista_transacoes.html",
                           nomes_gastos=nomes_gastos,
                           valores_gastos=valores_gastos,
                           nomes_entradas=nomes_entradas,
                           valores_entradas=valores_entradas)

@app.route("/deletar/<int:id>")
def deletar(id):
    if "user_id" not in session:
        flash("Você precisa estar logado para deletar uma transação.")
        return redirect("/tela_login")
    
    transacao = Transacao.query.get_or_404(id)

    db.session.delete(transacao)
    db.session.commit()
    return redirect(url_for('listar_transacoes'))

@app.route("/editar_transacao/<int:id>", methods=['GET'])
def editar_transacao(id):
    if "user_id" not in session:
        flash("Você precisa estar logado para editar uma transação.")
        return redirect("/tela_login")
    
    transacao = Transacao.query.get_or_404(id)

    if transacao.user_id != session["user_id"]:
        flash("Essa transação não é sua.")
        return redirect("/transacoes")
    
    return render_template("editar_transacao.html", transacao=transacao)

@app.route('/atualizar_transacao/<int:id>', methods=['POST'])
def atualizar_transacao(id):
    if "user_id" not in session:
        flash("Você precisa estar logado para atualizar uma transação.")
        return redirect("/tela_login")
    
    transacao = Transacao.query.get_or_404(id)

    # Atualiza os dados
    transacao.valor = request.form['valor']
    transacao.tipo = request.form['tipo']
    transacao.categoria = request.form['categoria']
    transacao.descricao = request.form['descricao']

    db.session.commit()

    return redirect("/transacoes")

@app.route("/tela_login", methods=["POST", "GET"])
def tela_login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Usuário não encontrado!")
            return redirect("/tela_login")
    
        elif user.senha != senha:
            flash("Senha incorreta!")
            return redirect("/tela_login")
    
        else:
            session["user_id"] = user.id
            flash("Login realizado com sucesso!")
            return redirect("/cadastrar")

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

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Você saiu da sua conta.")
    return redirect("/tela_login")
