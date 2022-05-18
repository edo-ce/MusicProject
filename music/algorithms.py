from music.models import *
from sqlalchemy import func
from sqlalchemy.sql import text

# TODO controllare tutto il testo con lowercase


def commit():
    session.commit()


def rollback():
    session.rollback()


def flush():
    session.flush()


def username_exists(code):
    return session.query(User).filter_by(username=code).first()


def is_premium(code):
    return session.query(Premium).filter_by(id=code).first() is not None


def search_func(search_result):
    res = {'albums': [], 'tracks': [], 'playlists': [], 'artists': []}
    elems = session.query(Element).filter(func.lower(Element.title) == search_result).all()
    for key in res.keys():
        if key == 'artists':
            artists = session.query(Artist.stage_name).filter(func.lower(Artist.stage_name) == search_result).all()
            for stage_name in artists:
                res['artists'].append(stage_name[0])
        else:
            for elem in elems:
                query = session.query(Element.title).join(key).where(Element.id == elem.id and Element.id == key+'id').first()
                if query:
                    res[key].append(query[0])
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
    elems = {'albums': [], 'singles': [], 'playlists': [], 'events': []}

    albums = session.query(Album).filter_by(artist_id=artist).all()
    for a in albums:
        if a.number_of_tracks() > 1:
            elems['albums'].append(a)
        else:
            elems['singles'].append(a)
    elems['playlists'] = get_playlists_by_creator(artist)
    elems['events'] = get_artists_events(artist)

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


def get_playlist(code):
    return session.query(Playlist).filter_by(id=code).first()


def get_artists_events(code):
    # TODO
    pass


def get_artist_albums(code):
    return session.query(Album).filter(Album.artist_id == code).all()


def get_playlists_by_creator(code):
    return session.query(Playlist).filter(Playlist.creator == code).all()


def get_payment_card(code):
    return session.query(PaymentCard).join(Premium).where(
        Premium.id == code and PaymentCard.id == Premium.payment_card).first()


def get_playlist_track(title, album, artist):
    # TODO gestire il caso in cui c'è un artista con il nome uguale e anche il nome di un album uguale
    album_id = session.query(Album.id).join(Element).join(Artist).where(Element.id == Album.id and
                                                                        Album.artist_id == Artist.id and
                                                                        Artist.stage_name == artist and
                                                                        Element.title == album).first()
    return session.query(Track).join(Element).where(Element.id == Track.id and Element.title == title and
                                                    Track.album_id == album_id).first()


def get_album_tracks(code):
    return session.query(Track).join(Album).where(Album.id == code).all()


def get_playlist_tracks(code):
    return session.query(Track).join(Playlist).where(Playlist.id == code).all()


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
    flush()
    return elem


def delete_tuple(table, id):
    try:
        # vedere con user
        if table == User or table == 'users':
            session.query(table).filter_by(username=id).delete()
        else:
            session.query(table).filter_by(id=id).delete()
        commit()
    except Exception as e:
        rollback()
        raise e


def update_tuple(table, code, **kwargs):
    row = session.query(table).filter_by(id=code).first()
    for attribute, value in kwargs.items():
        setattr(row, attribute, value)
    commit()


def advice_func():
    pass


# TO CHANGE

def get_genre_id(name):
    return session.query(Genre.id).filter(Genre.name == name).first()
