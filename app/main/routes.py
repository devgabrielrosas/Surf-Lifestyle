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