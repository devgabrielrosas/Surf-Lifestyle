from flask import Blueprint, request, redirect, url_for, render_template, current_app # type: ignore
import requests # type: ignore
from . import main

@main.route('/')
def index():
    posts = current_app.posts
    return render_template('index.html')

@main.route('/nosso_blog')
def pagina_historia():
    return render_template('nosso_blog.html')

@main.route('/politica_privacidade')
def politica_privacidade():
    return render_template('politica_privacidade.html')