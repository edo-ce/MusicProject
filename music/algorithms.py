from music.utils import *
from random import shuffle


def search_func(search_result):
    res = {'albums': [], 'tracks': [], 'playlists': [], 'artists': []}
    elems = listener_session.query(Element).filter(func.lower(Element.title) == search_result).all()
    for key in res.keys():
        if key == 'artists':
            artists = listener_session.query(Artist).filter(func.lower(Artist.stage_name) == search_result).all()
            res['artists'] = artists
        else:
            for elem in elems:
                query = listener_session.query(Element).join(key).where(Element.id == elem.id and Element.id == key+'.id')\
                    .first()
                if query and (key != 'playlists'
                              or not listener_session.query(Playlist.is_private).filter_by(id=query.id).first()[0]):
                    res[key].append(query)
    return res


def find_saved_elements(listener):
    elems = {'albums': [], 'tracks': [], 'artists': [], 'playlists': []}

    for elem in elems.keys():
        if elem != 'artists':
            table_elems = get_element_table(elem)
            listener_elems = get_listener(listener).elements
            for e in listener_elems:
                val = listener_session.query(table_elems).filter_by(id=e.id).first()
                if val is not None and (table_elems != Playlist or val.creator != listener):
                    elems[elem].append(val)
        else:
            res = listener_session.query(Artist).join(Follower).join(Listener).where(Listener.id == listener).all()
            elems[elem] = res

    elems['own playlists'] = get_playlists_by_creator(listener)

    return elems


def display_artist_contents(artist):
    elems = {'albums': [], 'singles': [], 'playlists': [], 'events': []}

    albums = artist_session.query(Album).filter_by(artist_id=artist).all()
    for a in albums:
        if a.number_of_tracks() > 1:
            elems['albums'].append(a)
        else:
            elems['singles'].append(a)
    elems['playlists'] = get_playlists_by_creator(artist)
    elems['events'] = get_artists_events(artist)

    return elems


def is_saved(id_listener, id_save):
    if type(id_save) == str:
        return admin_session.query(Follower).filter(Follower.id_artist == id_save)\
                   .filter(Follower.id_listener == id_listener).first() is not None
    else:
        return get_element(id_save) in get_listener(id_listener).elements


def save_something(id_listener, id_save):
    if type(id_save) == str:
        add_and_commit(Follower, id_artist=id_save, id_listener=id_listener, following_date=date.today())
    else:
        listener = get_listener(id_listener)
        elem = get_element(id_save)
        listener.elements.append(elem)
        commit()


def delete_from_saved(id_listener, id_saved):
    try:
        if type(id_saved) == str:
            listener_session.query(Follower).filter(Follower.id_artist == id_saved)\
                .filter(Follower.id_listener == id_listener).delete()
        else:
            listener_session.query(saved_elements).filter(saved_elements.c.id_listener == id_listener).\
                filter(saved_elements.c.id_element == id_saved).delete()
        listener_session.commit()
    except Exception as e:
        listener_session.rollback()
        raise e


# TRACKS
# consiglia le tracce più ascoltate dagli altri utenti dello stesso genere preferito del mio utente
def advice_func_tracks(username):
    genre = get_favorite_genre(username)
    listener = get_listener(username)
    res = dict()
    tracks = listener_session.query(Track).filter_by(genre=genre).all()
    for track in tracks:
        if get_element(track.id) not in listener.elements:
            res[track] = admin_session.query(saved_elements).filter_by(id_element=track.id).count()
    return [get_element(k.id) for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)]


# ALBUMS
# consiglia album che non ho già salvato degli artisti del mio utente
def advice_func_albums(username):
    listener = get_listener(username)
    artists = get_listener_artists(username)
    all_albums = list()
    for artist in artists:
        albums = get_artist_albums(artist.id)
        for album in albums:
            if get_element(album.id) not in listener.elements:
                all_albums.append(get_element(album.id))
    shuffle(all_albums)
    return all_albums


# PLAYLISTS
# consiglia playlist contenenti tracce presenti nelle playlist già salvate
def advice_func_playlists(username):
    listener = get_listener(username)
    tracks_in = set()
    res = list()
    listener_playlists = [playlist for playlist in get_all(Playlist) if playlist.creator == username]
    for elem in listener_playlists:
        tracks_in = tracks_in.union(set(elem.tracks_id))
    for elem in listener.elements:
        if get_playlist(elem.id):
            tracks_in = tracks_in.union(set(get_playlist(elem.id).tracks_id))
    for playlist in get_all(Playlist):
        if not playlist.is_private and get_element(playlist.id) not in listener.elements \
                and playlist not in listener_playlists:
            for track in playlist.tracks_id:
                if track in tracks_in:
                    res.append(get_element(playlist.id))
                    break
    shuffle(res)
    return res


# ARTISTS
# consiglia gli artisti che compaiono nei featuring delle tracce salvate
def advice_func_artists(username):
    listener = get_listener(username)
    res = set()
    for elem in listener.elements:
        if get_track(elem.id):
            res = res.union(set(artist for artist in get_track(elem.id).artists_feat if not is_saved(username, artist.id)))
    res = list(res)
    shuffle(res)
    return res


def advice_func(username):
    return {
        'tracks': advice_func_tracks(username)[:5],
        'albums': advice_func_albums(username)[:5],
        'playlists': advice_func_playlists(username)[:5],
        'artists': advice_func_artists(username)[:5]
    }


def top_int_the_app(country):
    return {
        'Top artists': top_three_artists(),
        f'Top artists in {country}': top_three_artists(country),
        'Top tracks': top_three_elements(Track),
        f'Top tracks in {country}': top_three_elements(Track, country),
        'Top albums': top_three_elements(Album),
        f'Top albums in {country}': top_three_elements(Album, country),
    }
