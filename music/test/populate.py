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

    #print(json.dumps(tracks.get('recording-list')[0].get('title'), indent=4, sort_keys=True))

    #delete all rows
    delete_all_records()

    # Genere
    genre = Genre(id=77, name="Rap")
    # Users
    user_obj = User(username="tt0", email="gemi@gemi.com", password="password",
                    name="Davide", lastname="De Luca", country="Italy",
                    gender="M", birth_date=date.today())
    # Artist
    artist_obj = Artist(id=user_obj.username, stage_name="Gemitaiz", is_solo=True, bio="gemi Bio")
    # Album
    album_element = Element(id=98, title=album)
    album_obj = Album(release_date=date.today(), artist_id=artist_obj.id, id=album_element.id)

    #containers
    element_vect = []
    track_vect = []

    #add tracks
    i = 100
    for _ in range(10):
        #print(id, '{}'.format( track ) )
        i = i + 1
        element_vect.append(Element(id=i, title=str(i)))
        track_vect.append(Track(id=element_vect[-1].id, duration=34, copyright="example",genre=genre.id,
                                  album_id=album_obj.id))


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
        session.rollback()
        raise ex

    session.commit()

    u = User(username='edo', email='idjdd@ddkod.com', password='password', country='Italy')
    session.add(u)
    l = Listener(id='edo', registration_date=date.today())
    l.elements.append(session.query(Element).filter_by(id=98).first())
    l.elements.append(session.query(Element).filter_by(id=102).first())


    session.add(l)
    session.commit()
