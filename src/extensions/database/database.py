import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
load_dotenv()

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def init_app(app):
    #db_user = os.getenv('MYSQL_USER')
    #db_pass = os.getenv('MYSQL_PASSWD')
    #db_host = os.getenv('MYSQL_HOST')
    #db_db = os.getenv('MYSQL_DATABASE')
    #db_uri = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_db}'
    db_uri = 'sqlite:///database.db'
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    #app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
