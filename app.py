from flask import Flask, render_template, url_for, request, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import json
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'chavesecreta' 

logado = False

@app.route('/cadastrarViagem')
def cadastrarViagem():
    if logado == False:
        return redirect('/')
    return render_template('cadastrarViagem.html')

@app.route('/home')
def home():
    if logado == False:
        return redirect('/') 
    with open('viagens.json') as viagemTemp:
        viagens = json.load(viagemTemp)

    return render_template('home.html', viagens=viagens, id=session.get('id'))

        
@app.route('/', methods=["GET"])    
def index():
    return render_template('./index.html') 

@app.route('/register') 
def register():
    return render_template('./register.html') 

@app.route('/login', methods=["POST"])
def login():
    global logado

    email = request.form.get('email') 
    senha = request.form.get('senha') 

    with open('users.json') as users: 
        usuarios = json.load(users) 
        for usuario in usuarios:    
            if usuario['email'] == email and check_password_hash(usuario['senha'], senha): 
                session['id'] = usuario['id']
                logado = True
                return redirect('/home')
        else: 
            flash('Erro no Login!')
            return redirect('/') 


@app.route('/cadastrar', methods=["POST"]) 
def cadastrar():
    user = []       
    nome = request.form.get('nome') 
    email = request.form.get('email') 
    senha = request.form.get('senha') 
    verificarSenha = request.form.get('VerificarSenha') 
    id = random.randint(1, 99999999999)

    with open('users.json') as users: 
        usuarios = json.load(users)
        for usuario in usuarios:
            if usuario['id'] == id:
                id = random.randint(1, 99999999999)

    if senha != verificarSenha: 
        flash('As senhas digitadas são diferentes!')
        return redirect('/register') 

    hashedPassword = generate_password_hash(senha)

    user = [            
        {
        "nome": nome,
        "email": email,
        "senha": hashedPassword,
        "id": id
        }
    ]

    with open('users.json') as userTemp:  
        usuarios = json.load(userTemp)  
    
    new_user = user + usuarios     
    with open('users.json', 'w') as temp:   
        json.dump(new_user, temp, indent=5) 


    return redirect('/') 

@app.route('/registrarViagem', methods=["POST"])
def registrarViagem():
    viagem = []
    start = request.form.get('start')
    end = request.form.get('end')
    dataInicial = request.form.get('dataInicial')
    dataFinal = request.form.get('dataFinal')
    roteiro = request.form.get('roteiro')
    eid = random.randint(1, 999999999999999)


    if dataInicial > dataFinal:
        flash('A data inicial não pode ser maior que a data final!')
        return redirect('/cadastrarViagem')

    viagem = [
        {
        "id": session['id'],
        "start": start,
        "end": end,
        "dataInicial": dataInicial,
        "dataFinal": dataFinal,
        "roteiro": roteiro,
        "eid": eid
        }
    ]

    with open('viagens.json') as viagemTemp:  
        viagens = json.load(viagemTemp)  
    
    new_viagem = viagem + viagens 
    with open('viagens.json', 'w') as temp:   
        json.dump(new_viagem, temp, indent=8) 

    return redirect('/home')

@app.route('/excluirViagem', methods=["POST"])
def excluirViagem():
    viagem_id = int(request.form['eid'])

    with open('viagens.json', 'r') as file:  
        viagens = json.load(file)

    viagens = [viagem for viagem in viagens if viagem['eid'] != viagem_id]

    with open('viagens.json', 'w') as viagemTemp:  
        viagens = json.dump(viagens, viagemTemp, indent=8)
    
    return redirect('/home')

@app.route('/logout', methods=["POST"])
def logout():
    global logado
    logado = False
    return redirect('/')

@app.route('/filtrarViagem', methods=["POST"])
def filtrarViagem():
    dataFiltrada = request.form.get('dataFiltrada')

    with open('viagens.json') as viagemTemp:
        viagens = json.load(viagemTemp)
    
    viagemFiltrada = []

    for viagem in viagens:
        if viagem['dataFinal'] == dataFiltrada or viagem['dataInicial'] == dataFiltrada:
            viagemFiltrada.append(viagem)
    
    return render_template('home.html', viagens=viagemFiltrada, id=session.get('id'))

if __name__ == '__main__': 
    app.run(debug=True)