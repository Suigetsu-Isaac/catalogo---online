
from flask import Request

def Cliente(cliente:dict ,type: str,url:Request,part=1):
    
    print('chegou na função')
    print(f"paramentros dic{cliente}, type {type}, request {url}, parte {part}")

    if(part == 1):
        print('parte 1')
        cliente['nome'] = url.form['nome']
        cliente['telefone']=url.form['telefone']
        cliente['email']=url.form['email']
        cliente['senha']=url.form['senha']
        
        cliente['cpf']=url.form['cpf']
        
        try:
             
            cliente['data_nascimento']= url.form['data_nascimento']
        except:
            pass
        
    elif (part == 2):
        print('parte 2')
        cliente['endereco']=url.form['endereco']
        cliente['complemento']=url.form['complemento']
        cliente['cidade']=url.form['cidade']
        cliente['estado']=url.form['estado']
        cliente['cep']=url.form['cep']
    
    
    
    return cliente


def dic_coluna_valor_db(colunas,dados, dados_id=0):
    
    
    c = [e[0].replace("_"," ") for e in colunas]
    
    print("\n\n Debugando os dados do db ",dados)
    
    d = dados[dados_id]
    res = { c[i].upper() : d[i] for i in range(len(d)) }
    
    res.pop("ID CLIENTE")
    return res
    
