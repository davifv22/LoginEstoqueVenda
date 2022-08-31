from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import webbrowser
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "random string"

login_manager = LoginManager()
db = SQLAlchemy(app)


class operadores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    situacao = db.Column(db.String(1))
    data_cadastro = db.Column(db.String(50))

    def __init__(self, nome, username, password, situacao, data_cadastro):
        self.nome = nome
        self.username = username
        self.password = password
        self.situacao = situacao
        self.data_cadastro = data_cadastro


class produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50))
    quantidade = db.Column(db.Integer)
    valor = db.Column(db.REAL)

    def __init__(self, descricao, quantidade, valor):
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor = valor


class produtos_vendidos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50))
    quantidade = db.Column(db.Integer)
    valor = db.Column(db.REAL)
    data_venda = db.Column(db.String(50))

    def __init__(self, descricao, quantidade, valor, data_venda):
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor = valor
        self.data_venda = data_venda


class produtos_comprados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50))
    quantidade = db.Column(db.Integer)
    valor = db.Column(db.REAL)
    data_compra = db.Column(db.String(50))

    def __init__(self, descricao, quantidade, valor, data_compra):
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor = valor
        self.data_compra = data_compra


@app.route('/login', methods=["GET", "POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None:
        redirect(url_for('login'))
    login_query = operadores.query.filter_by(username=username).first()
    user_query = login_query
    if user_query is None:
        redirect(url_for('login'))
    else:
        return redirect(url_for('index.html'))
    return render_template("login.html")


@app.route('/', methods=["GET", "POST"])
def dashboard():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    todos_produtos = produtos.query.paginate(page, per_page)

    vrDebito_query = 5000.0
    vrDebito = f'R${vrDebito_query:.2f}'
    vrDebito = vrDebito = f'R$ {vrDebito_query:.2f}'.replace('.', ',')

    vrVendaMensal_query = db.session.query(
        db.func.sum(produtos_vendidos.valor)).scalar()
    vrVendaMensal = f'R${vrVendaMensal_query:.2f}'
    vrVendaMensal = vrVendaMensal = f'R$ {vrVendaMensal_query:.2f}'.replace(
        '.', ',')

    vrCompraMensal_query = db.session.query(
        db.func.sum(produtos_comprados.valor)).scalar()
    vrCompraMensal = f'R${vrCompraMensal_query:.2f}'
    vrCompraMensal = vrCompraMensal = f'R$ {vrCompraMensal_query:.2f}'.replace(
        '.', ',')

    vrTotal_query = vrDebito_query + vrVendaMensal_query - vrCompraMensal_query
    vrTotal = f'R${vrTotal_query:.2f}'
    vrTotal = vrTotal = f'R$ {vrTotal_query:.2f}'.replace('.', ',')

    return render_template("index.html", produtos=todos_produtos, vrDebito=vrDebito, valorVendaMensal=vrVendaMensal, vrCompraMensal=vrCompraMensal, vrTotal=vrTotal)


@app.route('/estoque')
def estoque():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    todos_produtos = produtos.query.paginate(page, per_page)
    return render_template("estoque.html", produtos=todos_produtos)


@app.route('/cria_estoque', methods=["GET", "POST"])
def cria_estoque():
    descricao = request.form.get('descricao')
    quantidade = request.form.get('quantidade')
    valor = request.form.get('valor')

    if request.method == 'POST':
        if not descricao or not quantidade or not valor:
            flash("Preencha todos os campos do formulário", "error")
        else:
            produto = produtos(str(descricao), quantidade, valor)
            db.session.add(produto)
            db.session.commit()
            return redirect(url_for('estoque'))
    return render_template("cria_estoque.html")


@app.route('/<int:id>/atualiza_estoque', methods=['GET', 'POST'])
def atualiza_estoque(id):
    produto = produtos.query.filter_by(id=id).first()
    if request.method == 'POST':
        descricao = request.form["descricao"]
        quantidade = request.form["quantidade"]
        valor = request.form["valor"]

        produtos.query.filter_by(id=id).update(
            {"descricao": descricao, "quantidade": quantidade, "valor": valor})
        db.session.commit()
        return redirect(url_for('estoque'))
    return render_template("atualiza_estoque.html", produto=produto)


@app.route('/<int:id>/remove_estoque')
def remove_estoque(id):
    produto = produtos.query.filter_by(id=id).first()
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('estoque'))


if __name__ == "__main__":
    db.create_all()
    # webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
