from music.models import *
from sqlalchemy import func

# TODO controllare tutto il testo con lowercase

def commit():
    session.commit()


def rollback():
    session.rollback()


def search_func(select, text):
    text = text.lower()
    if select != 'artists':
        res = session.query(Element).join(select).where(func.lower(Element.title) == text).all()
    else:
        res = session.query(Artist).filter(func.lower(Artist.stage_name) == text).all()
    # TODO trovare titoli simili
    return res


def find_saved_elements(listener):
    elems = {'albums': [], 'tracks': [], 'artists': [], 'playlists': []}

    for elem in elems.keys():
        if elem != 'artists':
            res = session.query(Element.title).join(elem).join(saved_elements).join(Listener)\
                .where(Listener.id == listener).all()
        else:
            res = session.query(Artist.stage_name).join(Follower).join(Listener).where(Listener.id == listener).all()
        for i in res:
            elems[elem].append(i)

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


def get_user(code):
    return session.query(User).filter(User.username == code).first()


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


def get_title(code):
    return session.query(Element.title).filter_by(id=code).first()


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
