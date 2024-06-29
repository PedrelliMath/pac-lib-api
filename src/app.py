from flask import Flask
from flask_cors import CORS
from src.extensions.database import database
from src.blueprints import blueprints

def create_app():
    app = Flask(__name__)
    CORS(app)
    blueprints.init_app(app)
    database.init_app(app)      
    return app
    