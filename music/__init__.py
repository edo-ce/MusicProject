import sys
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# first = sys.argv[1]
# second = sys.argv[2]
first = 'postgres'
second = 'musicsql'

url = f"postgresql://postgres:{first}@localhost/{second}"
if not database_exists(url):
    create_database(url)
engine = create_engine(url, echo=False)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from music import models

Base.metadata.create_all(engine)

from music import routes
