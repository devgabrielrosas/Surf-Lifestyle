from flask import Blueprint, request, redirect, url_for, render_template, current_app # type: ignore
import requests, os # type: ignore
from datetime import date, datetime
from . import main

@main.route('/')
def index():
    posts = current_app.posts
    return render_template('index.html')

@main.route('/politica_privacidade')
def politica_privacidade():
    return render_template('politica_privacidade.html')

@main.route('/prancha')
def prancha():
    return render_template('prancha.html')

@main.route('/nosso_blog')
def historia():
    return render_template('nosso_blog.html')

"""
@main.route('/agenda', methods=["GET", "POST"], strict_slashes=False)
def agenda():
    # Coordenadas da praia de Intermares (João Pessoa - PB)
    lat, lng = -7.0596, -34.8372  
    
    # Chave da API (coloque no .env por segurança)
    api_key = os.getenv("STORMGLASS_API_KEY")
    
    # URL da API pedindo altura da onda, temp. da água, vento
    url = f"https://api.stormglass.io/v2/weather/point?lat={lat}&lng={lng}&params=waveHeight,waterTemperature,windSpeed,windDirection"

    # Cabeçalho com a chave
    headers = {"Authorization": api_key}
    
    # Faz o pedido (chamando a API de fato)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # A API devolve dados hora a hora. Pegamos a 1ª hora só como exemplo
        horas = data.get("hours", [])
        previsao = horas[0] if horas else {}
    else:
        previsao = {}

    # Envia os dados para o HTML
    return render_template("agenda.html", previsao=previsao)"""