from app import create_app
from flask import render_template
from dotenv import load_dotenv
from jinja2 import TemplateNotFound
import os

app = create_app()

load_dotenv()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def erro_interno(e):
    return render_template("500.html"), 500

@app.errorhandler(TemplateNotFound)
def template_nao_encontrado(e):
    return render_template("404.html", mensagem="Template não encontrado!"), 500

if __name__ == '__main__':
    app.run(debug=True)