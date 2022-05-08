#!/usr/bin/env python
"""A simple script that searches for a release in the MusicBrainz.
 $ ./populate.py Gemitaiz Kepler
"""

import musicbrainzngs
from music.models import *
from datetime import date

models_list = [ User, Artist, Listener, Element, Genre, Album, Track, Playlist, Event, PaymentCard, Premium, Follower]


def delete_all_records():
    try:
        for it in models_list:
            session.query(it).delete()
    except Exception as ex:
        print(ex)
        session.rollback()

    session.commit()


# online db
musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)

if __name__ == '__main__':

    artist = "Gemitaiz"
    album = "Kepler"

    #query result
    tracks = musicbrainzngs.search_recordings(artist=artist, release=album, limit=10)
    artist_searched = musicbrainzngs.search_artists(artist=artist)
    print(artist_searched)

    #print(json.dumps(tracks.get('recording-list')[0].get('title'), indent=4, sort_keys=True))

    #delete all rows
    delete_all_records()

    # Genere
    genre = Genre(name="Rap")
    # Users
    user_obj = User(username="tt0", email="gemi@gemi.com", password="password",
                    name="Davide", lastname="De Luca", country="Italy",
                    gender="M", birth_date=date.today())
    # Artist
    artist_obj = Artist(id=user_obj.username, stage_name="Gemitaiz", is_solo=True, bio="gemi Bio")
    # Album
    album_element = Element(title=album)
    album_obj = Album(release_date=date.today(), artist_id=artist_obj.id, id=album_element.id )

    #containers
    element_vect = []
    track_vect = []

    #add tracks
    for id, track in enumerate (tracks.get('recording-list')):

        #print(id, '{}'.format( track ) )
        element_vect.append( Element( title= track['title'] ) )
        track_vect.append( Track( id=element_vect[-1].id, duration= track['length'], copyright="example",genre=genre,album_id=album_obj.id))




    #upload elements
    try:
        session.add(user_obj)
        session.add(artist_obj)
        session.add(album_element)
        session.add(album_obj)
        session.add(genre)

        session.add_all(element_vect)
        session.add_all(track_vect)
    except Exception as ex:
        print(ex)
        session.rollback()

    session.commit()
