import os
import csv
from datetime import date, datetime
import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'troque-essa-chave-local')

# Caminho do CSV (raiz do projeto)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'inscricoes.csv')

# horários oficiais permitidos (coincidem com os radios do template)
ALLOWED_SLOTS = {"07:00", "08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"}

# Helper: ler CSV (retorna lista de dicts)
def read_appointments():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Helper: anexar linha, cria cabeçalho se necessário
def append_appointment(row):
    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['name', 'phone', 'date', 'time', 'created_at'])
        writer.writerow([row['name'], row['phone'], row['date'], row['time'], row['created_at']])

# rota raiz -> redireciona para /agenda
@app.route('/')
def home():
    return redirect(url_for('agenda'))

# rota para exibir o form
@app.route('/agenda', methods=['GET'])
def agenda():
    min_date = date.today().isoformat()
    return render_template('agenda.html', min_date=min_date)

# rota que processa o form
@app.route('/agendar', methods=['POST'])
def agendar():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    date_str = request.form.get('date', '').strip()
    time_slot = request.form.get('time_slot', '').strip()
    time_custom = request.form.get('time_custom', '').strip()

    # validações
    if not name:
        flash('Informe seu nome.', 'error')
        return redirect(url_for('agenda'))

    if not phone:
        flash('Informe seu telefone.', 'error')
        return redirect(url_for('agenda'))

    # valida data
    try:
        date_obj = date.fromisoformat(date_str)
    except Exception:
        flash('Data inválida.', 'error')
        return redirect(url_for('agenda'))

    if date_obj < date.today():
        flash('A data não pode ser anterior a hoje.', 'error')
        return redirect(url_for('agenda'))

    # valida horário
    if not time_slot:
        flash('Selecione um horário.', 'error')
        return redirect(url_for('agenda'))

    if time_slot == 'other':
        if not time_custom:
            flash("Você escolheu 'Outro horário'. Informe o horário.", 'error')
            return redirect(url_for('agenda'))
        try:
            parsed_time = datetime.strptime(time_custom, "%H:%M").time()
        except Exception:
            flash('Horário personalizado inválido (use HH:MM).', 'error')
            return redirect(url_for('agenda'))
    else:
        if time_slot not in ALLOWED_SLOTS:
            flash('Horário selecionado inválido.', 'error')
            return redirect(url_for('agenda'))
        parsed_time = datetime.strptime(time_slot, "%H:%M").time()

    time_str = parsed_time.strftime('%H:%M')

    # verifica conflito no CSV
    existing = read_appointments()
    for appt in existing:
        if appt.get('date') == date_str and appt.get('time') == time_str:
            flash(f'Horário ocupado em {date_str} às {time_str}. Escolha outro horário.', 'error')
            return redirect(url_for('agenda'))

    # chamar webhook do Make (se definido)
    webhook = os.environ.get('MAKE_WEBHOOK_URL')
    payload = {'name': name, 'phone': phone, 'date': date_str, 'time': time_str}

    if webhook:
        try:
            resp = requests.post(webhook, json=payload, timeout=10)
            if not (200 <= resp.status_code < 300):
                app.logger.error('Webhook retornou %s: %s', resp.status_code, resp.text)
                flash('Erro ao notificar automação (Make). Tente novamente mais tarde.', 'error')
                return redirect(url_for('agenda'))
        except Exception:
            app.logger.exception('Erro ao chamar webhook')
            flash('Erro ao notificar automação (Make). Tente novamente mais tarde.', 'error')
            return redirect(url_for('agenda'))
    else:
        # Se o webhook não estiver configurado, salvamos mesmo assim (avisa o usuário)
        flash('Atenção: MAKE_WEBHOOK_URL não configurado. Agendamento será salvo localmente sem notificação externa.', 'error')

    # salvar no CSV
    row = {
        'name': name,
        'phone': phone,
        'date': date_str,
        'time': time_str,
        'created_at': datetime.utcnow().isoformat()
    }
    try:
        append_appointment(row)
    except Exception:
        app.logger.exception('Erro ao salvar CSV')
        flash('Erro interno ao salvar agendamento. Tente novamente.', 'error')
        return redirect(url_for('agenda'))

    flash(f'Agendamento confirmado para {date_obj.strftime("%d/%m/%Y")} às {time_str}. Obrigado, {name}!', 'success')
    return redirect(url_for('agenda'))


if __name__ == '__main__':
    app.run(debug=True)