from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def init_app(app):
    db_uri = 'sqlite:///database.db'
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    db.init_app(app)
