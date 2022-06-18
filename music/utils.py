from music.operations import *
from sqlalchemy import func


def username_exists(code):
    return session.query(User).filter_by(username=code).first()


def is_premium(code):
    return session.query(Premium).filter_by(id=code).first() is not None


# GET


def get_all(table):
    return session.query(table).all()


def get_element_table(name):
    if Album.__tablename__ == name:
        return Album
    elif Track.__tablename__ == name:
        return Track
    else:
        return Playlist


def get_user(code):
    return session.query(User).filter_by(username=code).first()


def get_listener(code):
    return session.query(Listener).filter_by(id=code).first()


def get_element(code):
    return session.query(Element).filter_by(id=code).first()


def get_playlist(code):
    return session.query(Playlist).filter_by(id=code).first()


def get_track(code):
    return session.query(Track).filter_by(id=code).first()


def get_album(code):
    return session.query(Album).filter_by(id=code).first()


def get_listener_artists(code):
    artists_id = session.query(Follower.id_artist).filter_by(id_listener=code).all()
    if len(artists_id) > 0:
        artists_id = [x[0] for x in artists_id]
    return [is_artist(x) for x in artists_id]


def get_artists_events(code):
    return session.query(Event).filter_by(creator=code).all()


def get_artist_albums(code):
    return session.query(Album).filter_by(artist_id=code).all()


def get_playlists_by_creator(code):
    return session.query(Playlist).filter_by(creator=code).all()


def get_payment_card(code):
    return session.query(PaymentCard).join(Premium).where(
        Premium.id == code and PaymentCard.id == Premium.payment_card).first()


def get_playlist_track(title, album, artist):
    # TODO gestire il caso in cui c'è un artista con il nome uguale e anche il nome di un album uguale
    album_id = session.query(Album.id).join(Element).join(Artist).filter(func.lower(Artist.stage_name) == artist)\
        .filter(func.lower(Element.title) == album).filter(Element.id == Album.id).filter(Album.artist_id == Artist.id)\
        .first()
    if album_id is None:
        return None
    else:
        return session.query(Track).join(Element).filter(func.lower(Element.title) == title)\
            .filter(Track.album_id == album_id[0]).filter(Element.id == Track.id).first()


def get_album_tracks(code):
    return session.query(Track).join(Album).where(Album.id == code).all()


def get_playlist_tracks(code):
    return session.query(Track).join(Playlist).where(Playlist.id == code).all()


def is_artist(username):
    return session.query(Artist).filter_by(id=username).first()


def get_table(table):
    return session.query(table).all()


def get_favorite_genre(code):
    listener = get_listener(code)
    genres = dict()
    max = 0
    res = None
    for elem in listener.elements:
        track = get_track(elem.id)
        if track:
            if track.genre in genres.keys():
                genres[track.genre] += 1
            else:
                genres[track.genre] = 1
            if genres[track.genre] > max:
                max = genres[track.genre]
                res = track.genre
    return res


# TODO CHANGE get_genre_id get_favorite_genre advice_func_tracks


def get_genre_id(name):
    if session.query(Genre.id).filter(func.lower(Genre.name) == name).first():
        return session.query(Genre.id).filter(func.lower(Genre.name) == name).first()[0]
    else:
        return None


# STATISTICS


def get_followers(artist):
    return session.query(Follower).filter_by(id_artist=artist).count()


def get_saved_element(creator):
    return session.query(Playlist).filter_by(creator=creator).count()


def get_genre_listener(album):
    # selezione il conteggio dei generi dai users (listeners) joinnati con l'album in questione
    session.query(Album, Listener).select_from(User.gender).join(Listener, User).where(id=album)
