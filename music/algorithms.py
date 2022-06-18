from music.utils import *
from sqlalchemy.sql import text
from random import shuffle

# TODO controllare tutto il testo con lowercase


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


# TRACKS
# consiglia le tracce più ascoltate dagli altri utenti dello stesso genere preferito del mio utente
def advice_func_tracks(username):
    genre = get_favorite_genre(username)
    listener = get_listener(username)
    res = dict()
    tracks = session.query(Track).filter_by(genre=genre).all()
    for track in tracks:
        if get_element(track.id) not in listener.elements:
            res[track] = session.query(saved_elements).filter_by(id_element=track.id).count()
    return [k for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)]


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
                all_albums.append(album)
    shuffle(all_albums)
    return all_albums


# PLAYLISTS
# consiglia playlist contenenti tracce presenti nelle playlist già salvate
def advice_func_playlists(username):
    listener = get_listener(username)
    tracks_in = set()
    res = list()
    for elem in listener.elements:
        if elem is Playlist:
            tracks_in.union(set(elem.tracks_id))
    for playlist in get_all(Playlist):
        if get_element(playlist.id) not in listener.elements:
            for track in playlist.tracks_id:
                if track in tracks_in:
                    res.append(playlist)
                    break
    shuffle(res)
    return res


# ARTISTS
# consiglia gli artisti che compaiono nei featuring delle tracce salvate
def advice_func_artists(username):
    listener = get_listener(username)
    res = set()
    for elem in listener.elements:
        if elem is Track:
            res.union(set(get_track(elem.id).artists_feat))
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


# STATISTICS
'''
    follower
    elementi salvati nelle playlist
    sesso ascoltatori (può essere null)
    nazionalità
    età (può essere null)
    numero tracce salvate
    tracce più salvate
    album più seguito
'''


def stats():
    pass
