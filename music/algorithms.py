from music.models import *
from sqlalchemy import func
from sqlalchemy.sql import text

# TODO controllare tutto il testo con lowercase


def commit():
    session.commit()


def rollback():
    session.rollback()


def search_func(text):
    res = {}
    elems = session.query(Element).filter_by(title=text).all()
    for elem in elems:
        e = elem.find_type()
        if res.get(e.__tablename__):
            res[e.__tablename__].append(e)
        else:
            res[e.__tablename__] = e
    res['artists'] = session.query(Artist).filter_by(stage_name=text).all()
    return res


def find_saved_elements(listener):
    elems = {'albums': [], 'tracks': [], 'artists': [], 'playlists': []}

    for elem in elems.keys():
        if elem != 'artists':
            table_elems = get_element_table(elem)
            listener_elems = get_listener(listener).elements
            for e in listener_elems:
                if session.query(table_elems).filter_by(id=e.id).first():
                    elems[elem].append(session.query(table_elems).filter_by(id=e.id).first())
        else:
            res = session.query(Artist).join(Follower).join(Listener).where(Listener.id == listener).all()
            elems[elem] = res

    return elems


def display_artist_contents(artist):
    elems = {'albums': [], 'playlists': [], 'events': []}

    res = session.query(Element.title).join(Album).where(Album.artist_id == artist).all()
    for i in res:
        elems['albums'].append(i)
    res = session.query(Element.title).join(Playlist).where(Playlist.creator == artist).all()
    for i in res:
        elems['playlists'].append(i)
    res = session.query(Event.name, Event.date).join(event_participation).join(Artist).where(Artist.id == artist)\
        .order_by(Event.date).all()
    for i in res:
        elems['events'].append(i[0] + ' ' + i[1])

    return elems


# GET

def get_element_table(name):
    if Album.__tablename__ == name:
        return Album
    elif Track.__tablename__ == name:
        return Track
    else:
        return Playlist


def get_user(code):
    return session.query(User).filter(User.username == code).first()


def get_listener(code):
    return session.query(Listener).filter_by(id=code).first()


def get_artists_events(code):
    return session.query(Event).join(event_participation).join(Artist).where(Artist.id == code).all()


def get_artist_albums(code):
    return session.query(Album).filter(Album.artist_id == code).all()


def get_playlists_by_creator(code):
    return session.query(Playlist).filter(Playlist.creator == code).all()


def get_album_tracks(code):
    return session.query(Track).join(Album).where(Album.id == code).all()


def is_artist(username):
    return session.query(Artist).filter_by(id=username).first()


# FIND


def find_creator_artist(code):
    pass


def find_playlist(code):
    return session.query(Element).join(Playlist).where(Playlist.id == code).first()


def find_album(code):
    return session.query(Element).join(Album).where(Album.id == code).first()


def find_track(code):
    return session.query(Element).join(Track).where(Track.id == code).first()


# OPERATIONS


def update_user_info():
    pass


def update_artist_info():
    pass


def delete_premium_account():
    pass


def get_table(table):
    return session.query(table).all()


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
    return elem


def delete_tuple(table, id):
    try:
        # vedere con user
        session.query(table).filter_by(id=id).delete()
        commit()
    except Exception as e:
        rollback()
        raise e


def advice_func():
    pass


# TO CHANGE

def get_genre_id(name):
    return session.query(Genre.id).filter(Genre.name == name).first()
