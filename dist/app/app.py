from datetime import datetime
import secrets
from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import webbrowser


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

##########----------CREATE DB----------##########


class cadoperadores(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    key_login = db.Column(db.String(200))
    data_cadastro = db.Column(db.String(200))
    situacao = db.Column(db.String(10))

    def __init__(self, username, email, password, key_login, data_cadastro, situacao):
        self.username = username
        self.email = email
        self.password = password
        self.key_login = key_login
        self.data_cadastro = data_cadastro
        self.situacao = situacao


class cadclientes(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(200))
    email = db.Column(db.String(200))
    tel_cel = db.Column(db.String(200))
    data_cadastro = db.Column(db.String(200))

    def __init__(self, nome_cliente, email, tel_cel, data_cadastro):
        self.nome_cliente = nome_cliente
        self.email = email
        self.tel_cel = tel_cel
        self.data_cadastro = data_cadastro


class cadprodutos(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50))
    quantidade = db.Column(db.Integer)
    valor = db.Column(db.REAL)
    situacao = db.Column(db.String(50))
    data_cadastro = db.Column(db.String(200))

    def __init__(self, descricao, quantidade, valor, situacao, data_cadastro):
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor = valor
        self.situacao = situacao
        self.data_cadastro = data_cadastro


class cadempresa(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_empresa = db.Column(db.String(50))
    cnpj_cpf = db.Column(db.String(50))
    endereco = db.Column(db.String(50))
    data_cadastro = db.Column(db.String(50))

    def __init__(self, nome_empresa, cnpj_cpf, endereco, data_cadastro):
        self.nome_empresa = nome_empresa
        self.cnpj_cpf = cnpj_cpf
        self.endereco = endereco
        self.data_cadastro = data_cadastro


class produtos_vendidos(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50))
    data_ref = db.Column(db.String(50))
    nome_cliente = db.Column(db.String(50))
    tipo_pagto = db.Column(db.String(50))
    valor_un = db.Column(db.Integer)
    quantidade = db.Column(db.Integer)
    situacao = db.Column(db.String(50))
    valor_total = db.Column(db.REAL)
    desconto = db.Column(db.Integer)
    data_venda = db.Column(db.String(50))

    def __init__(self, descricao, data_ref, nome_cliente, tipo_pagto, valor_un, quantidade, situacao, valor_total, desconto, data_venda):
        self.descricao = descricao
        self.data_ref = data_ref
        self.nome_cliente = nome_cliente
        self.tipo_pagto = tipo_pagto
        self.valor_un = valor_un
        self.quantidade = quantidade
        self.situacao = situacao
        self.valor_total = valor_total
        self.desconto = desconto
        self.data_venda = data_venda


class produtos_comprados(UserMixin, db.Model):
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


class cadfornecedores(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_fornecedor = db.Column(db.String(50))
    email = db.Column(db.String(50))
    tel_cel = db.Column(db.Integer)
    situacao = db.Column(db.String(50))
    data_cadastro = db.Column(db.String(50))

    def __init__(self, nome_fornecedor, email, tel_cel, situacao, data_cadastro):
        self.nome_fornecedor = nome_fornecedor
        self.email = email
        self.tel_cel = tel_cel
        self.situacao = situacao
        self.data_cadastro = data_cadastro


class controle(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    debito_atual = db.Column(db.String(50))

    def __init__(self, debito_atual):
        self.debito_atual = debito_atual


class caixa(UserMixin, db.Model):
    data_caixa = db.Column(db.String(50), primary_key=True)
    data_fechamento = db.Column(db.String(50))
    data_ref = db.Column(db.String(50))
    valor_caixa = db.Column(db.String(50))
    qtde_vendidos = db.Column(db.Integer)
    situacao = db.Column(db.String(50))

    def __init__(self, data_caixa, data_fechamento, data_ref, valor_caixa, qtde_vendidos, situacao):
        self.data_caixa = data_caixa
        self.data_fechamento = data_fechamento
        self.data_ref = data_ref
        self.valor_caixa = valor_caixa
        self.qtde_vendidos = qtde_vendidos
        self.situacao = situacao


class vendas_agrupadas(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(50))
    data_ref = db.Column(db.String(50))
    tipo_pagto = db.Column(db.String(50))
    id_itens = db.Column(db.Integer)
    qntde_itens = db.Column(db.Integer)
    valor_venda = db.Column(db.String(50))
    desconto = db.Column(db.Integer)
    data_baixa = db.Column(db.String(50))

    def __init__(self, nome_cliente, data_ref, tipo_pagto, id_itens, qntde_itens, valor_venda, desconto, data_baixa):
        self.nome_cliente = nome_cliente
        self.data_ref = data_ref
        self.tipo_pagto = tipo_pagto
        self.id_itens = id_itens
        self.qntde_itens = qntde_itens
        self.valor_venda = valor_venda
        self.desconto = desconto
        self.data_baixa = data_baixa


##########----------FUNÇÕES DASHBOARD----------##########


@login_manager.user_loader
def get(key_login):
    return cadoperadores.query.get(key_login)


@app.route('/', methods=['GET'])
@login_required
def get_home():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    return render_template('home.html', nome=nome_empresa, user=user)


@app.route('/dashboard', methods=["GET"])
@login_required
def get_dashboard():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    month = datetime.now().strftime('%m-%Y')
    date_query = caixa.query.filter_by(data_caixa=date).first()
    if date_query is None:
        data_fechamento = ''
        situacao = 'ABERTO'
        dados = caixa(date, data_fechamento, month, 0, 0, situacao)
        db.session.add(dados)
        db.session.commit()
    date = datetime.now().strftime('%d-%m-%Y')
    page = request.args.get('page', 1, type=int)
    per_page = 5
    todos_produtos = cadprodutos.query.filter_by().paginate(page, per_page)
    vrDebito_query = db.session.query(
        db.func.sum(controle.debito_atual)).scalar()
    if vrDebito_query is None:
        vrDebito_query = 0.00
    vrDebito = f'R$ {vrDebito_query:.2f}'.replace('.', ',')
    vrVendaMensal_query = db.session.query(db.func.sum(
        produtos_vendidos.valor_total)).filter_by(data_ref=month, situacao='BAIXADO').scalar()
    if vrVendaMensal_query is None:
        vrVendaMensal_query = 0.00
    vrVendaMensal = f'R$ {vrVendaMensal_query:.2f}'.replace('.', ',')
    vrCompraMensal_query = db.session.query(
        db.func.sum(produtos_comprados.valor)).scalar()
    if vrCompraMensal_query is None:
        vrCompraMensal_query = 0.00
    vrCompraMensal = f'R$ {vrCompraMensal_query:.2f}'.replace('.', ',')
    vrTotal_query = vrDebito_query + vrVendaMensal_query - vrCompraMensal_query
    vrTotal = f'R$ {vrTotal_query:.2f}'.replace('.', ',')
    return render_template("dashboard.html", month=month, date=date, user=user, nome=nome_empresa, produtos=todos_produtos, vrDebito=vrDebito, valorVendaMensal=vrVendaMensal, vrCompraMensal=vrCompraMensal, vrTotal=vrTotal)

##########----------MENU DE VENDAS----------##########


@app.route('/vendas/<data_caixa>', methods=["GET"])
@login_required
def get_vendas_caixa(data_caixa):
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    month = datetime.now().strftime('%m-%Y')
    caixa_query = caixa.query.filter_by(data_caixa=data_caixa).first()
    qtde_vendidos = db.session.query(db.func.sum(
        caixa.qtde_vendidos)).filter_by(data_caixa=data_caixa).scalar()
    vrCaixa_query = db.session.query(db.func.sum(
        caixa.valor_caixa)).filter_by(data_caixa=data_caixa).scalar()
    if vrCaixa_query is None:
        vrCaixa_query = 0.00
        if qtde_vendidos is None:
            qtde_vendidos = 0
    vrCaixa = f'R$ {vrCaixa_query:.2f}'.replace('.', ',')
    dtCaixa_query = db.session.query(
        caixa.data_caixa).filter_by(data_ref=month).all()
    dtCaixa = dtCaixa_query
    produtos = cadprodutos.query.filter_by(situacao='ATIVO').all()
    clientes = db.session.query(cadclientes.nome_cliente).all()
    page = request.args.get('page', 1, type=int)
    per_page = 100
    produtos_lancados = produtos_vendidos.query.filter_by(
        situacao='LANCADO', data_venda=data_caixa).paginate(page=page, per_page=per_page)
    for produto in produtos_lancados.items:
        produto.valor_total = f'{int(produto.valor_total):.2f}'.replace(
            '.', '.')
        produto.valor_total = float(produto.valor_total)
    for qntde in produtos_lancados.items:
        qntde.valor_un = f'{int(qntde.valor_un):.2f}'.replace('.', '.')
        qntde.valor_un = float(qntde.valor_un)
    total_lancados = db.session.query(db.func.sum(produtos_vendidos.valor_total)).filter_by(
        data_venda=data_caixa, situacao='LANCADO').scalar()
    qtde_lancados = db.session.query(db.func.sum(produtos_vendidos.quantidade)).filter_by(
        data_venda=data_caixa, situacao='LANCADO').scalar()
    if total_lancados is None:
        total_lancados = 0.00
        if qtde_lancados is None:
            qtde_lancados = 0
    total_lancados = f'R$ {total_lancados:.2f}'.replace('.', ',')
    return render_template("vendas.html", qtde_lancados=qtde_lancados, total_lancados=total_lancados, produtos_lancados=produtos_lancados, caixa_query=caixa_query, clientes=clientes, produtos=produtos, date=date, qtde_vendidos=qtde_vendidos, dtCaixa=dtCaixa, vrCaixa=vrCaixa, user=user, nome=nome_empresa)


@app.route('/vendas/<data_caixa>', methods=["POST"])
@login_required
def post_vendas_caixa(data_caixa):
    dt_caixa = request.form["data_caixa"]
    return redirect(f'/vendas/{dt_caixa}')


@app.route('/vendas/<data_caixa>/lanc', methods=["POST"])
@login_required
def post_vendas_lancar(data_caixa):
    dt_caixa = data_caixa
    nome_produto = request.form["descricao"]
    nome_cliente = request.form["nome_cliente"]
    tipo_pagto = request.form["tipo_pagto"]
    valor_un_query = cadprodutos.query.filter_by(
        descricao=nome_produto).first()
    valor_un = valor_un_query.valor
    quantidade = request.form["quantidade"]
    situacao = 'LANCADO'
    valor_total = valor_un * int(quantidade)
    desconto = 0
    data_venda = datetime.now().strftime('%d-%m-%Y')
    month = datetime.now().strftime('%m-%Y')
    dados_produto = produtos_vendidos(nome_produto, month, nome_cliente, tipo_pagto,
                                      valor_un, quantidade, situacao, valor_total, desconto, data_venda)
    db.session.add(dados_produto)
    db.session.commit()
    return redirect(f'/vendas/{dt_caixa}')


@app.route('/vendas/<data_caixa>/fechar')
@login_required
def post_fechar_caixa(data_caixa):
    dt_caixa = data_caixa
    data_fechamento = datetime.now().strftime('%d-%m-%Y')
    situacao = 'FECHADO'
    caixa.query.filter_by(data_caixa=dt_caixa).update(
        {"situacao": situacao, "data_fechamento": data_fechamento})
    db.session.commit()
    return redirect(f'/vendas/{dt_caixa}')


@app.route('/vendas/<data_caixa>/abrir')
@login_required
def post_abrir_caixa(data_caixa):
    dt_caixa = data_caixa
    data_fechamento = ''
    situacao = 'ABERTO'
    caixa.query.filter_by(data_caixa=dt_caixa).update(
        {"situacao": situacao, "data_fechamento": data_fechamento})
    db.session.commit()
    return redirect(f'/vendas/{dt_caixa}')


@app.route('/vendas/<data_caixa>/limpar')
@login_required
def post_limpar_caixa(data_caixa):
    dt_caixa = data_caixa
    produtos_query = produtos_vendidos.query.filter_by(
        situacao='LANCADO', data_venda=dt_caixa).all()
    for produto in produtos_query:
        db.session.delete(produto)
        db.session.commit()
    return redirect(f'/vendas/{dt_caixa}')


@app.route('/vendas/<data_caixa>/baixar')
@login_required
def post_baixar_caixa(data_caixa):
    dt_caixa = data_caixa
    produtos_query = produtos_vendidos.query.filter_by(
        situacao='LANCADO', data_venda=dt_caixa).all()
    for produto in produtos_query:
        caixa_query = caixa.query.filter_by(data_caixa=dt_caixa).first()
        valor_produto = produto.valor_total
        quantidade = produto.quantidade
        valor_caixa = caixa_query.valor_caixa + valor_produto
        quantidade = caixa_query.qtde_vendidos + quantidade
        caixa.query.filter_by(data_caixa=dt_caixa).update(
            {"valor_caixa": valor_caixa, "qtde_vendidos": quantidade})
        db.session.commit()
    venda_query = produtos_vendidos.query.filter_by(situacao='LANCADO', data_venda=dt_caixa).all()
    id_itens = []
    qntde_itens = 0
    valor_venda = 0
    for venda in venda_query:
        id_itens.append(venda.id)
        qntde_itens = qntde_itens + venda.quantidade
        valor_venda = valor_venda + venda.valor_total
    id_itens = f'{id_itens}'
    nome_cliente = venda.nome_cliente
    data_ref = venda.data_ref
    tipo_pagto = venda.tipo_pagto
    desconto = venda.desconto
    data_baixa = datetime.now().strftime('%d-%m-%Y')
    dados_venda = vendas_agrupadas(nome_cliente, data_ref, tipo_pagto, id_itens, qntde_itens, valor_venda, desconto, data_baixa)
    db.session.add(dados_venda)
    db.session.commit()
    situacao = 'BAIXADO'
    produtos_vendidos.query.filter_by(situacao='LANCADO', data_venda=dt_caixa).update({"situacao": situacao})
    db.session.commit()
    return redirect(f'/vendas/{dt_caixa}')


@app.route('/vendas/<data_caixa>/adddesconto', methods=['POST'])
@login_required
def post_desconto_caixa(data_caixa):
    dt_caixa = data_caixa
    produtos_query = produtos_vendidos.query.filter_by(
        situacao='LANCADO', data_venda=dt_caixa).all()
    desconto = request.form.get("desconto")
    for produto in produtos_query:
        id_produto = produto.id
        valor_produto = produto.valor_total
        valor_produto = valor_produto - (valor_produto * int(desconto) / 100)
        produtos_vendidos.query.filter_by(data_venda=dt_caixa, id=id_produto).update(
            {"valor_total": valor_produto, "desconto": desconto})
        db.session.commit()
    return redirect(f'/vendas/{dt_caixa}')

##########----------MENU DE COMPRAS----------##########


@app.route('/compras', methods=["GET"])
@login_required
def get_compras():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    return render_template("compras.html", date=date, user=user, nome=nome_empresa)


@app.route('/compras', methods=["POST"])
@login_required
def post_compras():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    return render_template("compras.html", user=user, nome=nome_empresa)


##########----------MENU DE PARAMETRIZAÇÃO----------##########

@app.route('/parametrizacao', methods=["GET"])
@login_required
def get_parametrizacao():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    vrDebito_query = db.session.query(
        db.func.sum(controle.debito_atual)).scalar()
    if vrDebito_query is None:
        vrDebito_query = 0.00
    vrDebito = f'R${vrDebito_query:.2f}'
    vrDebito = f'R$ {vrDebito_query:.2f}'.replace('.', ',')
    return render_template("parametrizacao.html", date=date, vrDebito=vrDebito, user=user, nome=nome_empresa)


@app.route('/parametrizacao', methods=["POST"])
@login_required
def post_parametrizacao():
    debito_atual = request.form.get('debito_atual')
    controle.query.filter_by(id=1).update({"debito_atual": debito_atual})
    db.session.commit()
    return redirect('/parametrizacao')

##########----------MENU DE EMPRESA----------##########


@app.route('/empresa', methods=["GET"])
@login_required
def get_empresa():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    page = request.args.get('page', 1, type=int)
    per_page = 1
    todos_dados = cadempresa.query.paginate(page, per_page)
    return render_template("empresa.html", date=date, dados=todos_dados, user=user, nome=nome_empresa)


@app.route('/cria_empresa', methods=["GET"])
@login_required
def get_cria_empresa():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    page = request.args.get('page', 1, type=int)
    per_page = 1
    todos_dados = cadempresa.query.paginate(page, per_page)
    return render_template("cria_empresa.html", date=date, dados=todos_dados, user=user, nome=nome_empresa)


@app.route('/cria_empresa', methods=["POST"])
@login_required
def post_cria_empresa():
    nome_empresa = request.form.get('nome_empresa')
    cnpj_cpf = request.form.get('cnpj_cpf')
    endereco = request.form.get('endereco')
    if not nome_empresa:
        flash("Preencha todos os campos do formulário", "error")
    else:
        var = cadempresa.query.filter_by(id=1).first()
        if var is None:
            dados = cadempresa(nome_empresa, cnpj_cpf, endereco,
                               datetime.now().strftime('%d-%m-%Y'))
            db.session.add(dados)
            db.session.commit()
        else:
            cadempresa.query.filter_by(id=1).update(
                {"nome_empresa": nome_empresa, "cnpj_cpf": cnpj_cpf, "endereco": endereco})
            db.session.commit()
        return redirect('empresa')


##########----------MENU DE OPERADORES----------##########

@app.route('/operadores', methods=["GET"])
@login_required
def get_operadores():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    todos_dados = cadoperadores.query.paginate(page, per_page)
    return render_template("operadores.html", date=date, dados=todos_dados, user=user, nome=nome_empresa)


@app.route('/cria_operador', methods=["GET"])
@login_required
def get_cria_operador():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    todos_dados = cadoperadores.query.paginate(page, per_page)
    return render_template("cria_operador.html", date=date, dados=todos_dados, user=user, nome=nome_empresa)


@app.route('/cria_operador', methods=["POST"])
@login_required
def post_cria_operador():
    username = request.form.get('username')
    email = request.form.get('email')
    senha = request.form.get('senha')
    key_login = f"{datetime.now().strftime('%d%m%Y%H%M%S')}{secrets.token_hex(10)}"
    data_cadastro = datetime.now().strftime('%d-%m-%Y')
    situacao = 'ATIVO'
    dados = cadoperadores(username, email, senha,
                          key_login, data_cadastro, situacao)
    db.session.add(dados)
    db.session.commit()
    return redirect('operadores')


@app.route('/<int:id>/atualiza_operador', methods=["GET"])
@login_required
def get_atualiza_operador(id):
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    operador = cadoperadores.query.filter_by(id=id).first()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    todos_dados = cadoperadores.query.paginate(page, per_page)
    situacao = [{'situacao': 'ATIVO'}, {'situacao': 'CANCELADO'}]
    return render_template("atualiza_operador.html", date=date, operador=operador, dados=todos_dados, user=user, situacao=situacao, nome=nome_empresa)


@app.route('/<int:id>/atualiza_operador', methods=["POST"])
@login_required
def post_atualiza_operador(id):
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    situacao = request.form["situacao"]
    cadoperadores.query.filter_by(id=id).update(
        {"username": username, "email": email, "password": password, "situacao": situacao})
    db.session.commit()
    return redirect('/operadores')


@app.route('/<int:id>/remove_operador')
def remove_operador(id):
    operador = cadoperadores.query.filter_by(id=id).first()
    db.session.delete(operador)
    db.session.commit()
    return redirect('/operadores')

##########----------MENU DE ESTOQUE----------##########


@app.route('/estoque', methods=['GET'])
@login_required
def get_estoque():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    todos_produtos = cadprodutos.query.paginate(page, per_page)
    return render_template("estoque.html", date=date, produtos=todos_produtos, user=user, nome=nome_empresa)


@app.route('/cria_estoque', methods=["GET"])
@login_required
def get_cria_estoque():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    return render_template("cria_estoque.html", date=date, user=user, nome=nome_empresa)


@app.route('/cria_estoque', methods=["POST"])
@login_required
def post_cria_estoque():
    descricao = request.form.get('descricao')
    quantidade = request.form.get('quantidade')
    valor = request.form.get('valor')
    situacao = 'ATIVO'
    data_cadastro = datetime.now().strftime('%d-%m-%Y')
    if not descricao or not quantidade or not valor:
        flash("Preencha todos os campos do formulário", "error")
    else:
        produto = cadprodutos(descricao, quantidade,
                              valor, situacao, data_cadastro)
        db.session.add(produto)
        db.session.commit()
    return redirect('estoque')


@app.route('/<int:id>/atualiza_estoque', methods=['GET'])
def get_atualiza_estoque(id):
    produto = cadprodutos.query.filter_by(id=id).first()
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    return render_template("atualiza_estoque.html", date=date, produto=produto, user=user, nome=nome_empresa)


@app.route('/<int:id>/atualiza_estoque', methods=['POST'])
def post_atualiza_estoque(id):
    descricao = request.form["descricao"]
    quantidade = request.form["quantidade"]
    valor = request.form["valor"]
    situacao = request.form["situacao"]
    cadprodutos.query.filter_by(id=id).update(
        {"descricao": descricao, "quantidade": quantidade, "valor": valor, "situacao": situacao})
    db.session.commit()
    return redirect('/estoque')


@app.route('/<int:id>/remove_estoque')
def remove_estoque(id):
    produto = cadprodutos.query.filter_by(id=id).first()
    db.session.delete(produto)
    db.session.commit()
    return redirect('/estoque')


##########----------MENU DE CLIENTES----------##########


@app.route('/clientes', methods=['GET'])
@login_required
def get_clientes():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    todos_clientes = cadclientes.query.paginate(page, per_page)
    return render_template("clientes.html", date=date, clientes=todos_clientes, user=user, nome=nome_empresa)


@app.route('/cria_cliente', methods=["GET"])
@login_required
def get_cria_cliente():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    return render_template("cria_cliente.html", date=date, user=user, nome=nome_empresa)


@app.route('/cria_cliente', methods=["POST"])
@login_required
def post_cria_cliente():
    nome_cliente = request.form.get('nome_cliente')
    email = request.form.get('email')
    tel_cel = request.form.get('tel_cel')
    if not nome_cliente or not email or not tel_cel:
        flash("Preencha todos os campos do formulário", "error")
    else:
        data_cadastro = datetime.now().strftime('%d-%m-%Y')
        cliente = cadclientes(nome_cliente=nome_cliente, email=email,
                              tel_cel=tel_cel, data_cadastro=data_cadastro)
        db.session.add(cliente)
        db.session.commit()
        return redirect('clientes')


@app.route('/<int:id>/atualiza_cliente', methods=['GET'])
def get_atualiza_cliente(id):
    cliente = cadclientes.query.filter_by(id=id).first()
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    return render_template("atualiza_cliente.html", date=date, cliente=cliente, user=user, nome=nome_empresa)


@app.route('/<int:id>/atualiza_cliente', methods=['POST'])
def post_atualiza_cliente(id):
    nome_cliente = request.form["nome_cliente"]
    email = request.form["email"]
    tel_cel = request.form["tel_cel"]
    cadclientes.query.filter_by(id=id).update(
        {"nome_cliente": nome_cliente, "email": email, "tel_cel": tel_cel})
    db.session.commit()
    return redirect('/clientes')


@app.route('/<int:id>/remove_cliente')
def remove_cliente(id):
    cliente = cadclientes.query.filter_by(id=id).first()
    db.session.delete(cliente)
    db.session.commit()
    return redirect('/clientes')

##########----------MENU DE CLIENTES----------##########


@app.route('/fornecedores', methods=['GET'])
@login_required
def get_fornecedores():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    todos_fornecedores = cadfornecedores.query.paginate(page, per_page)
    return render_template("fornecedores.html", date=date, fornecedores=todos_fornecedores, user=user, nome=nome_empresa)


@app.route('/cria_fornecedor', methods=["GET"])
@login_required
def get_cria_fornecedor():
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    return render_template("cria_fornecedor.html", date=date, user=user, nome=nome_empresa)


@app.route('/cria_fornecedor', methods=["POST"])
@login_required
def post_cria_fornecedor():
    nome_fornecedor = request.form.get('nome_fornecedor')
    email = request.form.get('email')
    tel_cel = request.form.get('tel_cel')
    if not nome_fornecedor or not email or not tel_cel:
        flash("Preencha todos os campos do formulário", "error")
    else:
        data_cadastro = datetime.now().strftime('%d-%m-%Y')
        situacao = 'ATIVO'
        fornecedor = cadfornecedores(nome_fornecedor=nome_fornecedor, email=email,
                                     tel_cel=tel_cel, situacao=situacao, data_cadastro=data_cadastro)
        db.session.add(fornecedor)
        db.session.commit()
        return redirect('fornecedores')


@app.route('/<int:id>/atualiza_fornecedor', methods=['GET'])
def get_atualiza_fornecedor(id):
    fornecedor = cadfornecedores.query.filter_by(id=id).first()
    user = current_user.username
    nome_empresa = cadempresa.query.filter_by(id=1).first()
    date = datetime.now().strftime('%d-%m-%Y')
    situacao = [{'situacao': 'ATIVO'}, {'situacao': 'CANCELADO'}]
    return render_template("atualiza_fornecedor.html", date=date, fornecedor=fornecedor, situacao=situacao, user=user, nome=nome_empresa)


@app.route('/<int:id>/atualiza_fornecedor', methods=['POST'])
def post_atualiza_fornecedor(id):
    nome_fornecedor = request.form["nome_fornecedor"]
    email = request.form["email"]
    tel_cel = request.form["tel_cel"]
    situacao = request.form["situacao"]
    cadfornecedores.query.filter_by(id=id).update(
        {"nome_fornecedor": nome_fornecedor, "email": email, "tel_cel": tel_cel, "situacao": situacao})
    db.session.commit()
    return redirect('/fornecedores')


@app.route('/<int:id>/remove_fornecedor')
def remove_fornecedor(id):
    fornecedor = cadfornecedores.query.filter_by(id=id).first()
    db.session.delete(fornecedor)
    db.session.commit()
    return redirect('/fornecedores')


##########----------FUNÇÕES DE LOGIN----------##########

@app.route('/login', methods=['GET'])
def get_login():
    logout_user()
    return render_template('login.html')


@app.route('/signup', methods=['GET'])
def get_signup():
    return render_template('signup.html')


@app.route('/login', methods=['POST'])
def login_login():
    email = request.form['email']
    password = request.form['password']
    user = cadoperadores.query.filter_by(email=email).first()
    password = cadoperadores.query.filter_by(password=password).first()
    if user is None or password is None:
        return redirect('/login')
    else:
        login_user(user)
    return redirect('/dashboard')


@app.route('/signup', methods=['POST'])
def post_signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    if not username or not email or not password:
        return redirect('/signup')
    else:
        key_login = f"{datetime.now().strftime('%d%m%Y%H%M%S')}{secrets.token_hex(10)}"
        data_cadastro = datetime.now().strftime('%d-%m-%Y')
        situacao = 'ATIVO'
        user = cadoperadores(username=username, email=email, password=password,
                             key_login=key_login, data_cadastro=data_cadastro, situacao=situacao)
        db.session.add(user)
        db.session.commit()
        user = cadoperadores.query.filter_by(key_login=key_login).first()
        login_user(user)
    return redirect('/dashboard')


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')


if __name__ == '__main__':
    db.create_all()
    webbrowser.open_new('http://127.0.0.1:5000/login')
    app.run()
