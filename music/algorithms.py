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
            artists = session.query(Artist).filter(func.lower(Artist.stage_name) == search_result).all()
            res['artists'] = artists
        else:
            for elem in elems:
                query = session.query(Element).join(key).where(Element.id == elem.id and Element.id == key+'.id')\
                    .first()
                if query and (key != 'playlists'
                              or not session.query(Playlist.is_private).filter_by(id=query.id).first()[0]):
                    res[key].append(query)
    return res


def find_saved_elements(listener):
    elems = {'albums': [], 'tracks': [], 'artists': [], 'playlists': []}

    for elem in elems.keys():
        if elem != 'artists':
            table_elems = get_element_table(elem)
            listener_elems = get_listener(listener).elements
            for e in listener_elems:
                val = session.query(table_elems).filter_by(id=e.id).first()
                if val is not None and (table_elems != Playlist or val.creator != listener):
                    elems[elem].append(val)
        else:
            res = session.query(Artist).join(Follower).join(Listener).where(Listener.id == listener).all()
            elems[elem] = res

    elems['own playlists'] = get_playlists_by_creator(listener)

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
    return session.query(User).filter_by(username=code).first()


def get_listener(code):
    return session.query(Listener).filter_by(id=code).first()


def get_element(code):
    return session.query(Element).filter_by(id=code).first()


def get_playlist(code):
    return session.query(Playlist).filter_by(id=code).first()


def get_track(code):
    return session.query(Track).filter_by(id=code).first()


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


def is_saved(id_listener, id_save):
    if type(id_save) == str:
        return session.query(Follower).filter(Follower.id_artist == id_save and Follower.id_listener == id_listener)\
                   .first() is not None
    else:
        return get_element(id_save) in get_listener(id_listener).elements


def save_something(id_listener, id_save):
    if type(id_save) == str:
        add_and_commit(Follower, id_artist=id_save, id_listener=id_listener, following_date=date.today())
    else:
        # get_listener(id_listener).elements.append(get_element(id_save))
        listener = get_listener(id_listener)
        elem = get_element(id_save)
        listener.elements.append(elem)
        commit()


def delete_from_saved(id_listener, id_saved):
    try:
        if type(id_saved) == str:
            session.query(Follower).filter(Follower.id_artist == id_saved and Follower.id_listener == id_listener)\
                .delete()
        else:
            get_listener(id_listener).elements = []
        commit()
    except Exception as e:
        rollback()
        raise e


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


def advice_func():
    pass


# TO CHANGE

def get_genre_id(name):
    if session.query(Genre.id).filter(func.lower(Genre.name) == name).first():
        return session.query(Genre.id).filter(func.lower(Genre.name) == name).first()[0]
    else:
        return None


# STATISTICS
def get_followers(artist):
    return session.query(Follower).filter_by(id_artist=artist).count()
