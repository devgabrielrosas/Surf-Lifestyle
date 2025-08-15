from flask import Blueprint, request, redirect, url_for, render_template, current_app # type: ignore
import requests # type: ignore
from . import main

@main.route('/')
def index():
    return render_template('index.html')

