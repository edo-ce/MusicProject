from music.models import *


def commit():
    session.commit()


def rollback():
    session.rollback()


def flush():
    session.flush()


def add_and_commit(table, **kwargs):
    try:
        elem = table(**kwargs)
        session.add(elem)
        commit()
        return elem
    except Exception as e:
        rollback()
        raise e


def add_no_commit(table, **kwargs):
    elem = table(**kwargs)
    session.add(elem)
    flush()
    return elem


def delete_tuple(table, code):
    try:
        # vedere con user
        if table == User or table == 'users':
            session.query(table).filter_by(username=code).delete()
        else:
            session.query(table).filter_by(id=code).delete()
        commit()
    except Exception as e:
        rollback()
        raise e


def update_tuple(table, code, **kwargs):
    if table == User or table == 'users':
        row = session.query(table).filter_by(username=code).first()
    else:
        row = session.query(table).filter_by(id=code).first()
    for attribute, value in kwargs.items():
        setattr(row, attribute, value)
    commit()
