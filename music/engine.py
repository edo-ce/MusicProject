from music.config.config import config_diz as cf
from sqlalchemy import create_engine, text, DDL
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

url = f"postgresql://{cf['username']}:{cf['password']}@{cf['address']}/{cf['database']}"
if not database_exists(url):
    create_database(url)
engine = create_engine(url, echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


def create_schema():
    engine.execute(DDL("DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA IF NOT EXISTS public"))


def create_trigger():
    engine.execute(text(open("music/trigger.sql").read()))


def create_roles():
    engine.execute(text(open("music/roles.sql").read()))


def populate():
    engine.execute(text(open("music/populate.sql").read()))
