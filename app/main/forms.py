from flask import Blueprint, request, redirect, url_for, render_template, current_app, flash # type: ignore
import requests # type: ignore
from app import storage
from . import main

MAKE_WEBHOOK_URL = "https://hook.us2.make.com/xfk1lnl2kie69u8taswfccd6176k11rx"


@main.route("/", methods=["GET", "POST"])
def enviar():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip().lower()

        if not nome or not email:
            flash("Preencha todos os campos.", "error")
            return redirect(url_for("main.enviar"))

        caminho = storage.csv_path  # caminho do CSV

        # --- abre arquivo em modo 'a+' (cria se não existir) e lê conteúdo ---
        f = open(caminho, "a+", encoding="utf-8")
        f.seek(0)  # reposiciona no início para ler tudo
        linhas = f.read().splitlines()

        # --- garante cabeçalho ---
        if len(linhas) == 0 or linhas[0].strip() != "nome,email":
            # reescreve cabeçalho e mantém linhas seguintes (se houver)
            f.seek(0)
            f.truncate()
            f.write("nome,email\n")
            if len(linhas) > 0:
                for linha in linhas[1:]:
                    f.write(linha + "\n")
            linhas = ["nome,email"] + linhas[1:]

        # --- verifica se o email já existe ---
        for linha in linhas[1:]:
            partes = linha.strip().split(",")
            if len(partes) >= 2 and partes[1].lower() == email:
                f.close()
                flash("Email já cadastrado.", "error")
                return redirect(url_for("main.enviar"))

        # --- envia para webhook ---
        requests.post(MAKE_WEBHOOK_URL, json={'nome': nome, 'email': email})

        # --- adiciona localmente e salva no CSV ---
        current_app.posts.append({'nome': nome, 'email': email})
        f.write(f"{nome},{email}\n")
        f.close()

        flash("Cadastro concluído com sucesso!", "success")
        return redirect(url_for("main.enviar"))

    return render_template("index.html")

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