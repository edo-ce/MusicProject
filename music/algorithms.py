from music import session
from music.models import Element, Track, Album, Playlist, Artist, Listener, User, saved_elements, Follower
from sqlalchemy import func

# TODO controllare tutto il testo con lowercase


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


def is_artist(username):
    return session.query(Artist).filter_by(id=username).first()


def get_title(code):
    return session.query(Element.title).filter_by(id=code).first()


def find_creator_artist(code):
    pass


def find_playlist(code):
    return session.query(Element).join(Playlist).where(Playlist.id == code).first()


def find_album(code):
    return session.query(Element).join(Album).where(Album.id == code).first()


def find_track(code):
    return session.query(Element).join(Track).where(Track.id == code).first()


def advice_func():
    pass
