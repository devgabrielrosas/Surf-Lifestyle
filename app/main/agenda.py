# app/main/agenda.py
import os, requests
from datetime import date, datetime
from flask import render_template, request, redirect, url_for, flash, current_app

# usa o blueprint que o pacote já fornece (definido em app/main/__init__.py)
from . import main

# horários permitidos (radios do template)
HORARIOS_PERMITIDOS = {"07:00", "08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"}


@main.route("/agenda", methods=["GET", "POST"], strict_slashes=False)
def agenda():
    """
    Rota que exibe o formulário (GET) e processa agendamento (POST).
    Usa 'storage' do pacote app para salvar/ler CSV (import tardio para evitar circular imports).
    """
    # import tardio do storage para evitar circular import no bootstrap do app
    from app import storage

    # garante arquivo/pasta
    try:
        storage.garantir_csv_existe(current_app.root_path)
    except Exception:
        current_app.logger.exception("Falha ao garantir arquivo CSV")
        flash("Erro interno ao preparar armazenamento. Tente novamente mais tarde.", "error")
        return redirect(url_for("main.agenda"))

    # ---- POST: processa envio do formulário ----
    if request.method == "POST":
        nome = (request.form.get("nome") or "").strip()
        telefone = (request.form.get("telefone") or "").strip()
        data_str = (request.form.get("data") or "").strip()                # formato YYYY-MM-DD
        opcao_horario = (request.form.get("horario") or "").strip()       # ex: "07:00"
        horario_personalizado = (request.form.get("horario_personalizado") or "").strip()

        # valida campos obrigatórios
        if not nome:
            flash("Informe seu nome.", "error")
            return redirect(url_for("main.agenda"))
        if not telefone:
            flash("Informe seu telefone.", "error")
            return redirect(url_for("main.agenda"))
        if not data_str:
            flash("Informe a data do agendamento.", "error")
            return redirect(url_for("main.agenda"))

        # valida data ISO e não anterior a hoje
        try:
            data_obj = date.fromisoformat(data_str)
        except Exception:
            flash("Formato de data inválido. Use YYYY-MM-DD.", "error")
            return redirect(url_for("main.agenda"))

        if data_obj < date.today():
            flash("A data não pode ser anterior a hoje.", "error")
            return redirect(url_for("main.agenda"))

        # valida horário
        if not opcao_horario:
            flash("Selecione um horário.", "error")
            return redirect(url_for("main.agenda"))

        if opcao_horario == "outro":
            if not horario_personalizado:
                flash("Você escolheu 'Outro horário'. Informe o horário (HH:MM).", "error")
                return redirect(url_for("main.agenda"))
            try:
                hora_obj = datetime.strptime(horario_personalizado, "%H:%M").time()
            except Exception:
                flash("Horário personalizado inválido (use HH:MM).", "error")
                return redirect(url_for("main.agenda"))
        else:
            if opcao_horario not in HORARIOS_PERMITIDOS:
                flash("Horário selecionado inválido.", "error")
                return redirect(url_for("main.agenda"))
            try:
                hora_obj = datetime.strptime(opcao_horario, "%H:%M").time()
            except Exception:
                flash("Horário inválido.", "error")
                return redirect(url_for("main.agenda"))

        hora_str = hora_obj.strftime("%H:%M")

        # verifica conflito: data + hora
        try:
            agendamentos = storage.ler_agendamentos(current_app.root_path)
        except Exception:
            current_app.logger.exception("Falha ao ler agendamentos")
            flash("Erro interno ao verificar agendamentos. Tente novamente.", "error")
            return redirect(url_for("main.agenda"))

        for a in agendamentos:
            if a.get("data") == data_str and a.get("hora") == hora_str:
                flash(f"Já existe agendamento em {data_str} às {hora_str}. Por favor escolha outro horário.", "error")
                return redirect(url_for("main.agenda"))

        # monta e salva registro
        registro = {
            "nome": nome,
            "telefone": telefone,
            "data": data_str,
            "hora": hora_str,
            "criado_em": datetime.utcnow().isoformat()
        }

        try:
            caminho_salvo = storage.salvar_agendamento(registro, current_app.root_path)
            current_app.logger.info("Registro salvo em %s", caminho_salvo)
        except Exception:
            current_app.logger.exception("Erro ao salvar agendamento")
            flash("Erro interno ao salvar. Tente novamente.", "error")
            return redirect(url_for("main.agenda"))

        flash(f"Agendamento confirmado para {data_obj.strftime('%d/%m/%Y')} às {hora_str}. Obrigado, {nome}!", "success")
        return redirect(url_for("main.agenda"))

    # ---- GET: busca previsão e renderiza o form ----
    previsao = {}
    try:
        lat, lng = -7.0596, -34.8372  # Intermares
        api_key = os.getenv("STORMGLASS_API_KEY")
        if api_key:
            url = f"https://api.stormglass.io/v2/weather/point?lat={lat}&lng={lng}&params=waveHeight,waterTemperature,windSpeed,windDirection"
            headers = {"Authorization": api_key}
            resp = requests.get(url, headers=headers, timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                horas = data.get("hours", [])
                previsao = horas[0] if horas else {}
            else:
                current_app.logger.warning("Stormglass retornou %s", resp.status_code)
    except Exception:
        current_app.logger.exception("Erro ao buscar previsão (Stormglass)")

    data_minima = date.today().isoformat()
    horarios = sorted(HORARIOS_PERMITIDOS)
    return render_template("agenda.html", previsao=previsao, min_date=data_minima, horarios=horarios)
