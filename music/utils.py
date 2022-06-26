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


def get_event(code):
    return session.query(Event).filter_by(id=code).first()


def get_element_creator(table, code):
    if table == 'albums':
        return get_album(code).artist_id
    if table == 'tracks':
        return get_track(code).get_album().artist_id
    if table == 'playlists':
        return get_playlist(code).creator
    return None


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


def get_payment_card_by_number_and_pin(number, pin):
    card = session.query(PaymentCard).filter_by(number=number).first()
    if card and card.pin_check(pin):
        return card
    return None


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


# STATISTICS


def get_followers_count(code):
    return session.query(Follower).filter_by(id_artist=code).count()


def get_gender_listener(code):
    number_users = session.query(User).outerjoin(Follower, User.username == Follower.id_listener)\
        .filter(Follower.id_artist == code).count()
    number_male = session.query(User).outerjoin(Follower, User.username == Follower.id_listener)\
        .filter(Follower.id_artist == code).filter(User.gender == 'M').count()
    number_female = session.query(User).outerjoin(Follower, User.username == Follower.id_listener)\
        .filter(Follower.id_artist == code).filter(User.gender == 'F').count()

    if(number_users == 0):
        return f"{0},{0},{0}"

    return f"{number_male/number_users},{number_female/number_users},{(number_users-number_male-number_female)/number_users}"


def get_saved_element(creator):
    return session.query(Playlist).filter_by(creator=creator).count()


def get_genre_listener(album):
    # selezione il conteggio dei generi dai users (listeners) joinnati con l'album in questione
    session.query(Album, Listener).select_from(User.gender).join(Listener, User).where(id=album)
