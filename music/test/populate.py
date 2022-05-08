#!/usr/bin/env python
"""A simple script that searches for a release in the MusicBrainz.
 $ ./populate.py Gemitaiz Kepler
"""
"""
import musicbrainzngs
import sys
import json
from music.models import *
from datetime import *



# online db
musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)

if __name__ == '__main__':
    # cath artist and album from cmdline
    args=sys.argv[1:]
    if len(args) !=2:
        sys.exit("usage: {} ARTIST ALBUM".format(sys.argv[0]))
    artist, album=args

    #query result
    tracks = musicbrainzngs.search_recordings(artist=artist, release=album, limit=10)

    #print(json.dumps(tracks.get('recording-list')[0].get('title'), indent=4, sort_keys=True))

    # Genere
    genre = Genre(name="Rap")
    # Users
    user_obj = User(username="tt0", name="Davide", lastname="De Luca", gender="M", country="Italy", birth_date=str(datetime.now()), email="gemi@gemi.com", password="password" )
    # Artist
    artist_obj = Artist(id=user_obj.username, stage_name="Gemitaiz", is_solo=True, bio="gemi Bio")
    # Album
    album_element = Element(title=album)
    album_obj = Album(release_date=date.today(), artist_id=artist_obj.id, id=album_element.id, )

    #containers
    element_vect = []
    track_vect = []

    #add tracks
    for id, track in enumerate (tracks.get('recording-list')):

        print(id, '{}'.format( track ) )
        element_vect.append( Element( title= track['title'] ) )
        track_vect.append( Track( id=element_vect[-1].id, duration= track['length'], copyright="example",genre=genre,album_id=album_obj.id))


    #session.query(Element).delete()


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
        print ("rollback")

    session.commit()
"""
