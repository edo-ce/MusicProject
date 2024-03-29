from music.operations import *
from sqlalchemy import func


def username_exists(code):
    return admin_session.query(User).filter_by(username=code).first()


def is_premium(code):
    return admin_session.query(Premium).filter_by(id=code).first() is not None


def print_error_msg(e):
    index1 = str(e).find(' ') + 1
    index2 = str(e).find('!') + 1
    error_msg = str(e)[index1:index2]
    flash(error_msg, 'danger')


# GET


def get_all(table):
    return admin_session.query(table).all()


def get_element_table(name):
    if Album.__tablename__ == name:
        return Album
    elif Track.__tablename__ == name:
        return Track
    else:
        return Playlist


def get_user(code):
    return admin_session.query(User).filter_by(username=code).first()


def get_listener(code):
    return admin_session.query(Listener).filter_by(id=code).first()


def get_element(code):
    return admin_session.query(Element).filter_by(id=code).first()


def get_playlist(code):
    return admin_session.query(Playlist).filter_by(id=code).first()


def get_track(code):
    return admin_session.query(Track).filter_by(id=code).first()


def get_album(code):
    return admin_session.query(Album).filter_by(id=code).first()


def get_event(code):
    return admin_session.query(Event).filter_by(id=code).first()


def get_element_creator(table, code):
    if table == 'albums' and get_album(code):
        return get_album(code).artist_id
    if table == 'tracks' and get_track(code):
        return get_track(code).get_album().artist_id
    if table == 'playlists' and get_playlist(code):
        return get_playlist(code).creator
    return None


def get_listener_artists(code):
    artists_id = admin_session.query(Follower.id_artist).filter_by(id_listener=code).all()
    if len(artists_id) > 0:
        artists_id = [x[0] for x in artists_id]
    return [is_artist(x) for x in artists_id]


def get_artists_events(code):
    return admin_session.query(Event).filter_by(creator=code).all()


def get_artist_albums(code):
    return admin_session.query(Album).filter_by(artist_id=code).all()


def get_artist_tracks(code):
    return admin_session.query(Track).join(Album, Album.id == Track.album_id).filter(Album.artist_id == code).all()


def get_playlists_by_creator(code):
    return admin_session.query(Playlist).filter_by(creator=code).all()


def get_payment_card(code):
    return admin_session.query(PaymentCard).join(Premium).where(
        Premium.id == code and PaymentCard.id == Premium.payment_card).first()


def get_payment_card_by_number_and_pin(number, pin):
    card = admin_session.query(PaymentCard).filter_by(number=number).first()
    if card and card.pin_check(pin):
        return card
    return None


def get_playlist_track(title, album, artist):
    album_id = admin_session.query(Album.id).join(Element, Element.id == Album.id)\
        .join(Artist, Artist.id == Album.artist_id).filter(func.lower(Artist.stage_name) == artist)\
        .filter(func.lower(Element.title) == album).first()
    if album_id is None:
        return None
    else:
        return admin_session.query(Track).join(Element, Element.id == Track.id)\
            .filter(func.lower(Element.title) == title).filter(Track.album_id == album_id[0]).first()


def is_artist(username):
    return admin_session.query(Artist).filter_by(id=username).first()


def get_table(table):
    return admin_session.query(table).all()


def get_favorite_genre(code):
    res = admin_session.query(Track.genre).join(saved_elements, saved_elements.c.id_element == Track.id)\
        .filter(saved_elements.c.id_listener == code).group_by(Track.genre).order_by(func.count().desc()).first()
    return res[0] if res else None


# TOP LIST


def top_three_artists(country=None):
    if country is None:
        res = listener_session.query(Artist)\
            .join(Follower, Artist.id == Follower.id_artist).group_by(Artist.id).order_by(func.count(Follower.id_listener).desc())
    else:
        res = listener_session.query(Artist) \
            .join(Follower, Artist.id == Follower.id_artist).join(User, Artist.id == User.username)\
            .filter(User.country == country).group_by(Artist.id).order_by(func.count(Follower.id_listener).desc())
    return res[:3]


def top_three_elements(table, country=None):
    if country is None:
        res = listener_session.query(table)\
            .join(Element, Element.id == table.id).join(saved_elements, table.id == saved_elements.c.id_element)\
            .group_by(table.id).order_by(func.count(saved_elements.c.id_listener).desc())
    else:
        res = listener_session.query(table) \
            .join(Element, Element.id == table.id).join(saved_elements, table.id == saved_elements.c.id_element)\
            .join(User, saved_elements.c.id_listener == User.username).filter(User.country == country)\
            .group_by(table.id).order_by(func.count(saved_elements.c.id_listener).desc())
    return res[:3]


# STATISTICS

# Artist
def get_followers_count(code):
    return artist_session.query(Follower).filter_by(id_artist=code).count()


def get_gender_listener(code):
    number_users = artist_session.query(Follower).filter_by(id_artist=code).count()
    if number_users == 0:
        return f"{0},{0},{0}"
    number_male = artist_session.query(User).outerjoin(Follower, User.username == Follower.id_listener)\
        .filter(Follower.id_artist == code).filter(User.gender == 'M').count()
    number_female = artist_session.query(User).outerjoin(Follower, User.username == Follower.id_listener)\
        .filter(Follower.id_artist == code).filter(User.gender == 'F').count()
    return f"{format(number_male/number_users, '.2f')},{format(number_female/number_users, '.2f')}," \
           f"{format((number_users-number_male-number_female)/number_users, '.2f')}"


def get_country_listener(code):
    res = dict()
    number_users = artist_session.query(Follower).filter_by(id_artist=code).count()
    if number_users == 0:
        return res
    countries = artist_session.query(User.country, func.count()).join(Follower, Follower.id_listener == User.username)\
        .filter(Follower.id_artist == code).group_by(User.country)
    for country in countries:
        res[country[0]] = country[1]/number_users
    return res


def artist_best_elems(code, table):
    if table == Track:
        res = get_artist_tracks(code)
    else:
        res = get_artist_albums(code)
    res.sort(key=lambda x: number_save(x.id), reverse=True)
    return res[:3]
