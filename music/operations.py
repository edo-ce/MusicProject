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
    admin_session.commit()


def rollback():
    admin_session.rollback()


def flush():
    admin_session.flush()


def add_and_commit(table, **kwargs):
    try:
        table = convert_table(table)
        elem = table(**kwargs)
        admin_session.add(elem)
        commit()
        return elem
    except IntegrityError as e:
        raise e


def add_no_commit(table, **kwargs):
    try:
        table = convert_table(table)
        elem = table(**kwargs)
        admin_session.add(elem)
        flush()
        return elem
    except IntegrityError as e:
        raise e


def delete_tuple(table, code):
    try:
        table = convert_table(table)
        if table == User:
            admin_session.query(table).filter_by(username=code).delete()
        else:
            admin_session.query(table).filter_by(id=code).delete()
        commit()
    except IntegrityError as e:
        raise e


def update_tuple(table, code, **kwargs):
    try:
        table = convert_table(table)
        if table == User:
            row = admin_session.query(table).filter_by(username=code).first()
        else:
            row = admin_session.query(table).filter_by(id=code).first()
        for attribute, value in kwargs.items():
            setattr(row, attribute, value)
        commit()
    except IntegrityError as e:
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
