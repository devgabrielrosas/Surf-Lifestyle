from flask import Blueprint, request, redirect, url_for, render_template, current_app # type: ignore
import requests # type: ignore
from app import storage
from . import main

@main.route("/prancha", methods=["GET", "POST"])
def surf_form():
    if request.method == "POST":
        nivel = request.form.get("nivel")
        peso = request.form.get("peso")
        altura = request.form.get("altura")
        ondas = request.form.get("ondas")
        objetivo = request.form.get("objetivo")

        # sistema de pontuação
        pontuacao = {
            "longboard": 0,
            "funboard": 0,
            "shortboard": 0,
            "fish": 0
        }

        # --- NÍVEL ---
        if nivel == "iniciante":
            pontuacao["longboard"] += 3
            pontuacao["funboard"] += 2
        elif nivel == "intermediario":
            pontuacao["funboard"] += 2
            pontuacao["fish"] += 2
            pontuacao["shortboard"] += 1
        elif nivel == "avancado":
            pontuacao["shortboard"] += 3
            pontuacao["fish"] += 2

        # --- PESO ---
        if peso == "baixo":
            pontuacao["shortboard"] += 2
            pontuacao["fish"] += 1
        elif peso == "medio":
            pontuacao["funboard"] += 2
        elif peso == "alto":
            pontuacao["longboard"] += 2
            pontuacao["funboard"] += 1

        # --- ALTURA ---
        if altura == "baixo":
            pontuacao["shortboard"] += 1
            pontuacao["fish"] += 2
        elif altura == "medio":
            pontuacao["funboard"] += 1
        elif altura == "alto":
            pontuacao["longboard"] += 2
            pontuacao["funboard"] += 1

        # --- ONDAS ---
        if ondas == "pequenas":
            pontuacao["longboard"] += 2
            pontuacao["fish"] += 2
        elif ondas == "medias":
            pontuacao["funboard"] += 2
            pontuacao["shortboard"] += 2
        elif ondas == "grandes":
            pontuacao["shortboard"] += 3

        # --- OBJETIVO ---
        if objetivo == "aprendizado":
            pontuacao["longboard"] += 3
            pontuacao["funboard"] += 2
        elif objetivo == "manobras":
            pontuacao["shortboard"] += 3
            pontuacao["fish"] += 2
        elif objetivo == "velocidade":
            pontuacao["fish"] += 2
            pontuacao["shortboard"] += 2
        elif objetivo == "tubo":
            pontuacao["shortboard"] += 3

        # Resultado final
        prancha_recomendada = max(pontuacao, key=pontuacao.get)

        return render_template("resultado.html", prancha=prancha_recomendada, pontos=pontuacao)

    return render_template("prancha.html")