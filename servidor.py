from flask import Flask, render_template, request, flash, redirect, url_for, session, Request
#import funcoes as fun
import mysql.connector
import datetime

from utils import Cliente,dic_coluna_valor_db
import json
#Função para realizar conexão com banco de dados
def conexao():
    global con
    con = mysql.connector.connect(
    host="localhost", 
    user="root", 
    #password="projeto123",
    password="1234",   
    db="catalogoonline")

app = Flask(__name__)

cliente_cadastro={}

@app.route("/") # raiz - página inicial # 100% ok
@app.route("/index") # 100% ok
def index():
    
    imagens_dos_produtos = [
    {
        'nome': "Sushi",
        'img' : "/img/Sushi.png"
    },
    {
        'nome': "Feijoada",
        'img' : "/img/Feijoada.png"
    },
    {
        'nome': "Pizza",
        'img' : "/img/Pizza.png"
    },
    {
        'nome': "Manutenção de Computadores",
        'img' : "/img/Manutencao.png"
    },
    {
        'nome': "Montagem de Móveis",
        'img' : "/img/Montagem.png"
    },
    {
        'nome': "Limpeza de Piscina",
        'img': "/img/Limpeza.png"
    },
]

    cor = "FCC404"
    tipos_de_servicos = [
        {
            'nome': "Moveis",
            'img':f"https://img.icons8.com/ios/50/{cor}/furniture.png",
            'alt': 'furniture'
        },
        {
            'nome': "Limpeza",
            'img':f"https://img.icons8.com/wired/64/{cor}/housekeeping.png",
            'alt': 'housekeeping'
        },
        {
            'nome': "Alimentos",
            'img':f"https://img.icons8.com/ios/50/{cor}/omlette.png",
            'alt': 'omlette'
        },
        {
            'nome': "Roupas",
            'img':f"https://img.icons8.com/carbon-copy/100/{cor}/clothes.png",
            'alt': 'clothes'
        },
        {
            'nome': "Tecnologia",
            'img':f"https://img.icons8.com/dotty/80/{cor}/workstation.png",
            'alt': 'workstation'
        },
        {
            'nome': "Construção Civil",
            'img':f"https://img.icons8.com/dotty/80/{cor}/engineer.png",
            'alt': 'engineer'
        },
    ]
    
    return render_template("index.html", imagens = imagens_dos_produtos, servicos = tipos_de_servicos) # chama o html da página inicial
    
@app.route('/home') #Rota para pagina restrita ao usuário logado
def home():
    if not session:
        return render_template('login.html')
    
    else:
        print("sessao",session)
        id_cliente = session['Id Cliente']
        conexao()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM plano WHERE id_cliente = %s", (session['Id Cliente'], ) )
        dados = cursor.fetchall()
        dataAtual = datetime.datetime.today().date()
        print("dados: ",dados)
        for i in range(0, len(dados)):        
        
            if dataAtual == dados[i][3]:
                msg = "OPS! Inicia Hoje a Vigência do Plano"
                return render_template('home.html', nome=session['email'], msg=msg)
            elif dataAtual == dados[i][4]:
                msg = "Atenção! Finaliza Hoje a Vigência do Plano"
                return render_template('home.html', nome=session['email'], msg=msg)
        #else:
        return render_template('home.html', nome=session['email'])
        #aqui
                 
        #realizar login, renderiza o formulário para inserção dos dados
    
@app.route("/login")
def inicio():
    if 'Logged in' in session:
        return redirect('home')
    else:
        return render_template('login.html')

@app.route('/login',methods = ["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
                
        conexao()
        cursor = con.cursor()
        query1 = "SELECT * FROM cliente WHERE email = %s AND senha = %s"
        cursor.execute(query1, (email, senha))
        resultado = cursor.fetchone()
        print("resultado: ",resultado)
        print("resultado Login")
        if resultado:
            session['Logged in'] = True
            session['Id Cliente'] =resultado[0]  
            session['email'] = resultado[1]
            return redirect(url_for('home'))
        else:
            msg = "Email/senha Incorretos. Tente Novamente!"
    
    return render_template('login.html', msg=msg)

# Logout
@app.route('/logout')
def logout():
    session.pop('Logged in', None)
    session.pop('Id Cliente', None)
    session.pop('email', None)
    return redirect(url_for('index'))

@app.post('/cadastrar/parte1')
def cadastrar_cliente():
    
    print("Cadastrar Cliente")
    
    global cliente_cadastro
    cliente_cadastro = Cliente(cliente_cadastro, request.form['cpfcnpj'],request,1)
    
    #debugar a respostar em JSON
            
    print(cliente_cadastro)
            
    return render_template('cadastro-Complementar.html')
@app.post('/cadastrar/parte2')
def cadastrar_cliente_complementar():
    print("Cadastrar Cliente complementar")
    global cliente_cadastro   
    cliente_cadastro = Cliente(cliente_cadastro, None,request,2)
    
    print(cliente_cadastro)
    response = app.response_class(
        response=json.dumps(cliente_cadastro),
        status=200,
        mimetype='application/json'
    )
    
    conexao()
    cursor = con.cursor()
        
    table = ''
    values = ''
    for k, v in cliente_cadastro.items():
        
        table+=k+', '
        values+=f"'{v}', "
    
    table = table[0:-2]
    values = values[0:-2]
    
    query = f"insert into cliente({table}) values ({values})"    
    print(query)
    cursor.execute(query)
    con.commit()
    con.close()
    
    flash("Dados cadastrados", "success")
    mensagem = "Cliente Cadastrado com Sucesso"
    return render_template("login.html", msg = mensagem)



@app.post('/cadastrar')    
def cadastro():
    print("Chegou no cadastro")

    
    return render_template('cadastro.html')

#@app.route("/cadastrar", methods=["POST"]) # 100% ok
#def cadastrar():
#    mensagem = "Cadastrar"
#    return render_template("cadastro.html", msg = mensagem)

#cadastrar os clientes, renderiza o formulário para inserção dos dados
#@app.route("/cadastrar-cliente")
#def cadastrar_clientes():
#    return render_template('cadastrar-cliente.html')


#@app.route("/cadastrar-cliente", methods=["POST","GET"]) # 100% ok
#def cadastrar_cliente():
#    if request.method == 'POST':
#        nome = request.form['nome']
#        cpf = request.form['cpf_cnpj']
#        data_nascimento = request.form['data_nascimento']
#        email = request.form['email']
#        senha = request.form['senha']
#        confirmaSenha = request.form['confirmaSenha']
#        telefone = request.form['telefone']
#        endereco = request.form['address']
#        complemento = request.form['address2']
#        cidade = request.form['city']
#        estado = request.form['estado']
#        cep = request.form['cep']
#        if senha != confirmaSenha:
#            error = "As Senhas São Diferentes"
#            return render_template("cadastrar-cliente.html", error=error)
#    conexao()
#    cursor=con.cursor()
#    cursor.execute("insert into cliente(nome, cpf, data_nascimento, email, senha, confirmaSenha, telefone, endereco, complemento, cidade, estado, cep) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nome, cpf, data_nascimento, email, senha, confirmaSenha, telefone, endereco, complemento, cidade, estado, cep))
#    con.commit()
#    con.close()
#    flash("Dados cadastrados", "success")
#    mensagem = "Cliente Cadastrado com Sucesso"
#    return render_template("login.html", msg = mensagem)

#cadastrar os produtos, renderiza o formulário para inserção dos dados
@app.route("/cadastrar-produto")
def cadastrar_produtos():
    if 'loggedin' in session:
        id_cliente = session['Id Cliente']
    conexao()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM plano WHERE id_cliente = %s", (session['Id Cliente'], ) )
    dados = cursor.fetchall()
    dataAtual = datetime.datetime.today().date()

    for i in range(len(dados)): 
        if (dataAtual < dados[i][3]) and (dataAtual < dados[i][4]):
            msg = "OPS! Fora da vigência do Plano"
            return render_template("home.html", msg=msg)
        elif dados[i][6] == dados[i][2]:
            msg = "OPS! Quantidade de anuncios máxima esgotada, para cadastrar novos anuncios, considere outros planos"
            return render_template("home.html", msg=msg)
        else:
            return render_template('cadastrar-produto.html')

@app.route("/cadastrar-produto", methods=["POST","GET"]) # 100% ok
        
def cadastrar_produto():
    if request.method == 'POST':
        titulo = request.form['nome_produto']
        tipo = request.form['tipo']
        descricao = request.form['descricao']
        preco = request.form['preco']
        arquivo = request.form['arquivo']
        if 'loggedin' in session:
            id_cliente = session['Id Cliente']

        conexao() #inserindo o anúncio no banco
        cursor = con.cursor() 
        cursor.execute(
        "insert into produto (titulo, tipo, descricao, preco, arquivo, id_cliente) values (%s,%s,%s,%s, %s, %s)",
        (titulo, tipo, descricao, preco, arquivo, session['Id Cliente']))
        con.commit()
        con.close()
        #-----------------

        conexao() #pegando a quantidade de anúncios cadastrados

        cursor2 = con.cursor()
        cursor2.execute("SELECT * FROM plano WHERE id_cliente = %s", (session['Id Cliente'], ) ) 
        dados = cursor2.fetchall()

        for i in range(len(dados)):
           if dados[i][6] <= dados[i][2]:
                qtd_anuncios = dados[i][6] 

        qtd_anuncios = qtd_anuncios + int(1) 

        con.commit()
        con.close()

        conexao() #incremento a quantidade de anúncios no banco

        cursor3 = con.cursor()
        cursor3.execute(
            "update plano SET qtd_anuncios = '%s' where id_cliente = '%s'"
            % (qtd_anuncios, session ['id_cliente']))
        
        con.commit()
        con.close()
        #-------------------
        flash("Dados cadastrados", "success")
        mensagem = "Produto Cadastrado" + str(qtd_anuncios) #tirar teste
        return render_template("home.html", msg = mensagem)
      

#cadastrar o pagamento, renderiza o formulário para inserção dos dados        
@app.route("/cadastrar-pagamento")
def cadastrar_pagamentos():
    return render_template('cadastrar-pagamento.html')

@app.route("/cadastrar-pagamento", methods=["POST","GET"]) # 100% ok
def cadastrar_pagamento():
    if request.method == 'POST':
        tipo_pagamento = request.form['tipo_pagamento']
        valor = request.form['valor']
        desconto = request.form['desconto']
        data_pagamento = datetime.datetime.today().date() #request.form['data_pagamento']
        parcelas = request.form['parcelas']
        if 'loggedin' in session:
            nome_pagador = session['email']
        conexao()
        cursor = con.cursor()
        cursor.execute(
                                        "insert into pagamento(nome_pagador, tipo_pagamento, valor, desconto, data_pagamento, parcelas) values (%s,%s, %s, %s, %s, %s)",
        (session['email'], tipo_pagamento, valor, desconto, data_pagamento, parcelas))
        con.commit()
        con.close()
        flash("Dados cadastrados", "success")
        mensagem = "Plano Cadastrado Com Sucesso"
        return render_template("home.html", msg = mensagem)


#Exibe as opções de planos
@app.route("/planos")
def planos():
    return render_template('planos.html')

#Cadastro de plano básico
@app.route("/plano-basico", methods=["POST", "GET"])
def plano_basico():
    data_atual = datetime.datetime.today().date()
    data_final = data_atual + datetime.timedelta(days=7)
    preco=float(50)
    anuncios=10
    return render_template('plano-basico.html', dtInicio=data_atual, dtFinal=data_final, preco=preco, anuncios=anuncios)


#Cadastro de plano intermediario
@app.route("/plano-intermediario", methods=["POST", "GET"])
def plano_intermediario():
    data_atual = datetime.datetime.today().date()
    data_final = data_atual + datetime.timedelta(days=29)
    preco=120
    anuncios=30
    return render_template('plano-intermediario.html', dtInicio=data_atual, dtFinal=data_final, preco=preco, anuncios=anuncios)

#Cadastro de plano premium
@app.route("/plano-premium", methods=["POST", "GET"])
def plano_premium():
    data_atual = datetime.datetime.today().date()
    data_final = data_atual + datetime.timedelta(days=179)
    preco=220
    anuncios=50
    return render_template('plano-premium.html', dtInicio=data_atual, dtFinal=data_final, preco=preco, anuncios=anuncios)

#Rota para cadastro dos planos básico, intermediário e premium
@app.route("/plano-fixo", methods=["POST", "GET"]) # 100% ok
def plano_fixo():
    if request.method == 'POST':
        preco =request.form['valor'].replace("R$: ","")
        print("preco ",preco)
        preco = float(preco)
        print("preco ",preco)
        vigencia = request.form['vigencia']#Quantidade de anúncios diários
        dataInicio = request.form['dataInicio']
        dataFim = request.form['dataFim']
        #dataInicio = datetime.datetime.strptime(dataInicio, "%Y-%m-%d") #"%H:%M:%S")
        #dataFim = datetime.datetime.strptime(dataFim, "%Y-%m-%d") #%H:%M:%S")
        #dias=abs((dataFim - dataInicio).days)
        #preco =float( dias* float(vigencia))
        if 'loggedin' in session:
            id_cliente = session['Id Cliente']
        conexao()
        cursor = con.cursor()
        cursor.execute(
                                        "insert into plano(preco, vigencia, data_inicio, data_fim, id_cliente) values (%s,%s,%s,%s,%s)",
                                        (preco, vigencia, dataInicio, dataFim, session['Id Cliente']))
        con.commit()
        con.close()
        flash("Dados cadastrados", "success")
        mensagem = "Plano Cadastrado"
        return render_template("cadastrar-pagamento.html", msg = mensagem, preco=preco)

#cadastrar o plano personalizado, renderiza o formulário para inserção dosdados
@app.route("/plano-personalizado", methods=["POST", "GET"])
def plano_personalizado():
    return render_template('cadastrar-plano.html')

#Realiza o cadastro do plano personalizado
@app.route("/cadastrar-plano", methods=["POST", "GET"]) # 100% ok
def cadastrar_plano():
    if request.method == 'POST':
        #preco = request.form['valor']
        vigencia = request.form['vigencia']#Quantidade de anúncios diários
        dataInicio = request.form['dataInicio']
        dataFim = request.form['dataFim']
        dataInicio = datetime.datetime.strptime(dataInicio, "%Y-%m-%d") #"%H:%M:%S")
        dataFim = datetime.datetime.strptime(dataFim, "%Y-%m-%d") #%H:%M:%S")
        dias=abs((dataFim - dataInicio).days)
        preco =float( dias* float(vigencia))
        if 'loggedin' in session:
            id_cliente = session['Id Cliente']
        conexao()
        cursor = con.cursor()
        cursor.execute(
                                        "insert into plano(preco, vigencia, data_inicio, data_fim, id_cliente) values (%s,%s,%s,%s,%s)",
                                        (preco, vigencia, dataInicio, dataFim, session['Id Cliente']))
        con.commit()
        con.close()
        flash("Dados cadastrados", "success")
        mensagem = "Plano Cadastrado"
        return render_template("cadastrar-pagamento.html", msg = mensagem, preco=preco)
    
                               
#@app.route("/consultar", methods=["POST"]) # 100% ok
#def consultar():
    #mensagem = "Consultar"
    #cliente = fun.listar_tabela("cliente")
    #produto = fun.listar_tabela("produto")
    #pagamento = fun.listar_tabela("pagamento")
    #plano = fun.listar_tabela("plano")
    #return render_template("consulta.html", msg = mensagem, cliente=cliente, produto=produto, pagamento=pagamento, plano=plano)


@app.route("/consultar-cliente", methods=["POST", "GET"]) # 100% ok
def consultar_cliente():
    
    if 'Logged in' in session:
        id_cliente = session['Id Cliente']
        print("id",id_cliente)
    
    else:
        return render_template('login.html')   
    
    conexao()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM cliente WHERE id_cliente = %s", (session['Id Cliente'], ) )
     
    dados = cursor.fetchall()
    
    print("dados do cliente: ",dados)
    cursor.execute("SHOW COLUMNS FROM cliente ")
    colunas = cursor.fetchall()
    res = dic_coluna_valor_db(colunas,dados)
    res.pop('SENHA')
    print(res)    
    mensagem = "DADOS PESSOAIS"
    
    return render_template('home.html', res=res, msg=mensagem, nome=session['email'])

    #cliente = fun.listar_tabela("cliente")
    #return render_template("consulta.html", msg = mensagem, lista=cliente)

############
#Exibir Anúncios por Pesquisa
@app.route("/pesquisar-produto", methods=["POST", "GET"]) # 100% ok
def pesquisar_produto():    
    if request.method=='POST':
        pesquisa = request.form['pesquisa']
#    if 'loggedin' in session:
        #id_cliente = session['Id Cliente']
    conexao()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM produto WHERE titulo = %s", (pesquisa, ) )
     
    dados = cursor.fetchall()
    return render_template('index.html', dados=dados, produto=dados)
################

@app.route("/consultar-produto", methods=["POST", "GET"]) # 100% ok
def consultar_produto():
    mensagem = "Consultar"
    if 'loggedin' in session:
        id_cliente = session['Id Cliente']
    conexao()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM produto WHERE id_cliente = %s", (session['Id Cliente'], ) )
     
    dados = cursor.fetchall()
    
    cursor.execute("SHOW COLUMNS FROM produto ")
    colunas = cursor.fetchall()
    
    lista=[]
    
    
    for e in range(len(dados)):
        
        res = dic_coluna_valor_db(colunas,dados,e)  
        res['IMAGEM'] = res.pop('ARQUIVO')
        res['PRECO'] = f"R$: {format(res['PRECO'],'.2f')}".replace('.',',')
        lista.append(res)
        
    print(lista)
    
    msg='ANÚNCIOS'
    return render_template('home.html', dados=dados, msg=msg , lista=lista, nome=session['email'])

    #produto = fun.listar_tabela("produto")
    #return render_template("consulta.html", msg = mensagem, lista=produto)


@app.route("/consultar-pagamento", methods=["POST","GET"]) # 100% ok
def consultar_pagamento():
    
    if 'loggedin' in session:
        nome_pagador = session['email']
    conexao()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM pagamento WHERE nome_pagador = %s", (session['email'], ) )
     
    dados = cursor.fetchall()
    mensagem = "COMPROVANTE DE PAGAMENTO"
    return render_template('home.html', msg = mensagem ,pagamento=dados, nome=session['email'])

    #pagamento = fun.listar_tabela("pagamento")
    #return render_template("consulta.html", msg = mensagem, lista=pagamento)

@app.route("/consultar-plano", methods=["POST","GET"]) # 100% ok
def consultar_plano():
    
    if 'loggedin' in session:
        id_cliente = session['Id Cliente']
    conexao()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM plano WHERE id_cliente = %s", (session['Id Cliente'], ) )
     
    dados = cursor.fetchall()
    cursor.execute("SHOW COLUMNS FROM plano ")
    colunas = cursor.fetchall()
    try:
        res = dic_coluna_valor_db(colunas,dados)
        res['PRECO'] = f"R$: {format(res['PRECO'],'.2f')}".replace('.',',')
        res['DATA INICIO'] = res['DATA INICIO'].strftime("%d-%m-%Y")
        res['DATA FIM']= res['DATA FIM'].strftime("%d-%m-%Y")
    except: res = {"Que Pena":"Ainda não tem plano"}
    mensagem = "MEUS PLANOS"
    return render_template('home.html', msg = mensagem ,res=res, nome=session['email'])

    #plano = fun.listar_tabela("plano")
    #return render_template("consulta.html", msg = mensagem, lista=plano)


#@app.route("/atualizar", methods=["POST"]) # 100% ok
#def atualizar():
    #mensagem = "Atualizar"
    #return render_template("atualizar.html", msg = mensagem)
@app.route("/atualizar-cliente") # 100% ok
def atualizar_clientes():
    mensagem = "Atualizar"
    return render_template("atualizar-cliente.html", msg = mensagem)

@app.route("/atualizar-cliente", methods=["POST","GET"]) # 100% ok
def atualizar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf_cnpj']
        data_nascimento = request.form['data_nascimento']
        email = request.form['email']
        senha = request.form['senha']
        confirmaSenha = request.form['confirmaSenha']
        telefone = request.form['telefone']
        endereco = request.form['address']
        complemento = request.form['address2']
        cidade = request.form['city']
        estado = request.form['estado']
        cep = request.form['cep']
        if senha != confirmaSenha:
            error = "Senhas Diferentes"
            return render_template('atualizar-cliente.html', error=error)
        if 'loggedin' in session:
            id_cliente = session['Id Cliente']
    conexao()        
    cursor = con.cursor()
    cursor.execute(
    "update cliente SET nome = '%s', cpf = '%s', data_nascimento = '%s', email = '%s', senha = '%s', confirmaSenha = '%s', telefone = '%s', endereco = '%s', complemento = '%s', cidade = '%s', estado = '%s', cep = '%s' where id_cliente = '%s'"
                                        % (nome, cpf, data_nascimento, email, senha, confirmaSenha, telefone, endereco, complemento, cidade, estado, cep, session['Id Cliente']))                                
    con.commit()
    con.close()
    mensagem = "Dados Atualizado"
    return render_template("home.html", msg=mensagem)
                                

@app.route("/atualizar-produto", methods=["POST", "GET"]) # 100% ok
def atualizar_produto():
    if request.method == 'POST':
        idProduto = request.form['idProduto']
        titulo = request.form['nome_produto']
        tipo = request.form['tipo']
        descricao = request.form['descricao']
        preco = request.form['preco']
        arquivo = request.form['arquivo']
        conexao()
    cursor = con.cursor()
    cursor.execute(
                                        "update produto SET titulo = '%s', tipo = '%s', descricao = '%s', preco = '%s', arquivo = '%s' where idProduto = '%s'"
                                        % (titulo, tipo, descricao, preco, arquivo, idProduto))
    con.commit()
    con.close()
    mensagem = "Produto Atualizado"
    return render_template("atualizar.html", msg=mensagem)


@app.route("/atualizar-pagamento", methods=["POST", "GET"]) # 100% ok
def atualizar_pagamento():
    if request.method == 'POST':
        idPagamento = request.form['idPagamento']
        nome_pagador = request.form['nome_pagador']
        tipo_pagamento = request.form['tipo_pagamento']
        valor = request.form['valor']
        desconto = request.form['desconto']
        data_pagamento = date.today() #request.form['dataPagamento']
        parcelas = request.form['parcelas']
        conexao()
    cursor = con.cursor()
    cursor.execute(
        "update pagamento SET nome_pagador = '%s', tipo_pagamento = '%s', valor = '%s', desconto = '%s', data_pagamento = '%s', parcelas = '%s' where idPagamento = '%s' "
        % (nome_pagador, tipo_pagamento, valor, desconto, data_pagamento, parcelas, idPagamento))
    con.commit()
    con.close()
    mensagem = "Pagamento Atualizado"
    return render_template("atualizar.html", msg=mensagem)


@app.route("/atualizar-plano", methods=["POST", "GET"]) # 100% ok
def atualizar_plano():
    if request.method == 'POST':
        idPlano = request.form['idPlano']
        preco = request.form['valorPlano']
        vigencia = request.form['vigencia']
        dataInicio = date.today() #request.form['dataInicio']
        dataFim = date.today() #request.form['dataFim']
        conexao()
    cursor = con.cursor()
    cursor.execute(
                                        "update plano SET preco = '%s', vigencia = '%s', data_inicio = '%s', data_fim = '%s' where id_plano = '%s'"
                                        % (preco, vigencia, dataInicio, dataFim, idPlano))
    con.commit()
    con.close()
    mensagem = "Plano Atualizado"
    return render_template("atualizar.html", msg=mensagem)

                               
@app.route("/remover", methods=["POST"]) # 100% ok
def remover():
    mensagem = "Remover"
    return render_template("remocao.html", msg = mensagem)


@app.route("/remover-cliente", methods=["POST", "GET"])
def remover_cliente():
    #if request.method == 'POST':
        #id_cliente = request.form['id_cliente']
        if 'loggedin' in session:
            id_cliente = session['Id Cliente']
        
            conexao()
            cursor = con.cursor()
            cursor.execute("delete from cliente where id_cliente = '%s'" % id_cliente)
            con.commit()
            con.close()
       
        mensagem = "Cadastro Cancelado com Sucesso"
    #return render_template("remocao.html", msg=mensagem)
        return render_template('login.html', msg=mensagem) 


@app.route("/remover-produto", methods=["POST"])
def remover_produto():
    if request.method == 'POST':
        idProduto = request.form['idProduto']
        conexao()
        cursor = con.cursor()
        cursor.execute("delete from produto where idProduto = '%s'" % idProduto)
        con.commit()
        con.close()
        mensagem = "Produto Removido"
        return render_template("remocao.html", msg = mensagem)


@app.route("/remover-pagamento", methods=["POST"])
def remover_pagamento():
    if request.method == 'POST':
        idPagamento = request.form['idPagamento']
        conexao()
        cursor = con.cursor()
        cursor.execute("delete from pagamento where idPagamento = '%s'" % idPagamento)
        con.commit()
        con.close()
        mensagem = "Pagamento Removido"
        return render_template("remocao.html", msg=mensagem)


@app.route("/remover-plano", methods=["POST"])
def remover_plano():
    if request.method == 'POST':
        idPlano = request.form['idPlano']
        conexao()
        cursor = con.cursor()
        cursor.execute("delete from plano where idPlano = '%s'" % idPlano)
        con.commit()
        con.close()
        mensagem = "Plano Removido"
        return render_template("remocao.html", msg=mensagem)


if __name__ =="__main__":
    app.secret_key = "admin123"
    app.run(debug=True)
