from music.config import *
from sqlalchemy import create_engine, text, DDL
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

url_owner = f"postgresql://{owner}:{password_owner}@{db_ip}:{db_port}/{db_name}"

if not database_exists(url_owner):
    create_database(url_owner)

engine_owner = create_engine(url_owner)

Base = declarative_base()


def create_schema():
    engine_owner.execute(DDL("DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA IF NOT EXISTS public"))


def create_trigger():
    engine_owner.execute(text(open("music/trigger.sql").read()))


def create_roles():
    engine_owner.execute(text(open("music/roles.sql").read()))


def populate():
    engine_owner.execute(text(open("music/populate.sql").read()))


def define_admin_session():
    url_admin = f"postgresql://{user_admin}:{password_admin}@{db_ip}:{db_port}/{db_name}"
    engine_admin = create_engine(url_admin)
    return scoped_session(sessionmaker(bind=engine_admin))


def define_listener_session():
    url_listener = f"postgresql://{user_listener}:{password_listener}@{db_ip}:{db_port}/{db_name}"
    engine_listener = create_engine(url_listener)
    return scoped_session(sessionmaker(bind=engine_listener))


def define_artist_session():
    url_artist = f"postgresql://{user_artist}:{password_artist}@{db_ip}:{db_port}/{db_name}"
    engine_artist = create_engine(url_artist)
    return scoped_session(sessionmaker(bind=engine_artist))
