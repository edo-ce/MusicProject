from music.models import *
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

tables = {'users': User,
          'listeners': Listener,
          'artists': Artist,
          'elements': Element,
          'albums': Album,
          'tracks': Track,
          'playlists': Playlist,
          'events': Event,
          'payment_cards': PaymentCard,
          'premiums': Premium,
          'followers': Follower}


roles = {'ADMIN': 'admin', 'LISTENER': 'listener', 'ARTIST': 'artist'}


def convert_table(table):
    if table in tables.keys():
        table = tables[table]
    return table


def commit():
    session.commit()


def rollback():
    session.rollback()


def flush():
    session.flush()


def add_and_commit(table, **kwargs):
    try:
        table = convert_table(table)
        elem = table(**kwargs)
        session.add(elem)
        commit()
        return elem
    except IntegrityError as e:
        rollback()
        raise e


def add_no_commit(table, **kwargs):
    try:
        table = convert_table(table)
        elem = table(**kwargs)
        session.add(elem)
        flush()
        return elem
    except IntegrityError as e:
        rollback()
        raise e


def delete_tuple(table, code):
    try:
        table = convert_table(table)
        if table == User:
            session.query(table).filter_by(username=code).delete()
        else:
            session.query(table).filter_by(id=code).delete()
        commit()
    except IntegrityError as e:
        rollback()
        raise e


def update_tuple(table, code, **kwargs):
    try:
        table = convert_table(table)
        if table == User:
            row = session.query(table).filter_by(username=code).first()
        else:
            row = session.query(table).filter_by(id=code).first()
        for attribute, value in kwargs.items():
            setattr(row, attribute, value)
        commit()
    except IntegrityError as e:
        rollback()
        raise e


def roles_required(role_required):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.allowed(role_required):
                flash("You don't have permission to access this resource.", "warning")
                return redirect(url_for('private'))
            return func(*args, **kwargs)
        return decorated_function
    return decorator
