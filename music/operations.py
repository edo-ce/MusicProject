from music.models import *

tables = (User, Listener, Artist, Element, Album, Track, Playlist, Event, PaymentCard, Premium, Follower)


def convert_table(table):
    if isinstance(table, str):
        for t in tables:
            if table == t.__tablename__:
                table = t
                break
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
    except Exception as e:
        rollback()
        raise e


def add_no_commit(table, **kwargs):
    try:
        table = convert_table(table)
        elem = table(**kwargs)
        session.add(elem)
        flush()
        return elem
    except Exception as e:
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
    except Exception as e:
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
    except Exception as e:
        rollback()
        raise e
