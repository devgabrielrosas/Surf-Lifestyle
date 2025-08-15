from flask import Blueprint, request, redirect, url_for, render_template, current_app # type: ignore
import requests # type: ignore
from . import main

MAKE_WEBOHOOK_URL = "https://hook.us2.make.com/xfk1lnl2kie69u8taswfccd6176k11rx"

@main.route("/", methods=["GET", "POST"])
def enviar():
    if request.method == 'POST':
        nome = request.form.get("nome")
        email = request.form.get("email")
        data = {'email': email, 'nome': nome}
        r = requests.post(MAKE_WEBOHOOK_URL, json=data)
        mensagem = 'Cadastro concluído!'
        return render_template('index.html', mensagem=mensagem)