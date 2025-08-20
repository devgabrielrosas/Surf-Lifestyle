from flask import Blueprint, request, redirect, url_for, render_template, current_app # type: ignore
import requests # type: ignore
from app import storage
from . import main

MAKE_WEBHOOK_URL = "https://hook.us2.make.com/xfk1lnl2kie69u8taswfccd6176k11rx"


@main.route("/", methods=["GET", "POST"])
def enviar():
    mensagem = None
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        
        data = {'nome': nome, 'email': email}
        requests.post(MAKE_WEBHOOK_URL, json=data)
        
        current_app.posts.append({'nome': nome, 'email': email})
        storage.escrever_csv(nome, email)

        mensagem = 'Cadastro concluído!'
        return redirect(url_for('main.enviar'))
    
    return render_template('index.html', mensagem=mensagem)


@main.route('/enviar_inscritos')
def enviar_inscritos_csv():
    token = request.args.get("token")
    if token != "alan_jairo_rosas_thalyson":
        return "Acesso não autorizado", 403

    inscritos = storage.ler_csv()
    for inscrito in inscritos:
        data = {
            'nome': inscrito['nome'],
            'email': inscrito['email']
        }
        requests.post(..., json=data)
        print(inscrito)
    return "Inscrições enviadas para o Make!"