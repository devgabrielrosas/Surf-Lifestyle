from app import create_app
from flask import render_template
from dotenv import load_dotenv
import os

app = create_app()

load_dotenv()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)