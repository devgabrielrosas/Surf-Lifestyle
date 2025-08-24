from flask import Flask
from .main import main as main_bp
from . import storage

def create_app():
    app = Flask(__name__)

    storage.inicializar_csv()
    
    app.posts = storage.ler_csv()

    app.secret_key = 'projeto-surf'

    app.register_blueprint(main_bp)

    with app.app_context():
        print(app.url_map)
    
    return app