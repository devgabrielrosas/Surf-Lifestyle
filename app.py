from flask import Flask, render_template, request # type: ignore
import requests # type: ignore
app = Flask(__name__)

MAKE_WEBOHOOK_URL = "https://hook.us2.make.com/xfk1lnl2kie69u8taswfccd6176k11rx"

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/", methods=["GET", "POST"])
def enviar():
    if request.method == 'POST':
        nome = request.form.get("nome")
        email = request.form.get("email")
        data = {'email': email, 'nome': nome}
        r = requests.post(MAKE_WEBOHOOK_URL, json=data)
        mensagem = 'Cadastro concluído!'
        return render_template('index.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)