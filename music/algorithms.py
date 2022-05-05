from music import Base, engine, session
from music.models import Element, Track, Album, Playlist, Artist, User
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
