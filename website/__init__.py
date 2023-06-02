from flask import Flask
from flask_cors import CORS


def create_app(debug=False):
   
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    CORS(app)
    from .words import words
    app.register_blueprint(words, url_prefix = '/')
    return app