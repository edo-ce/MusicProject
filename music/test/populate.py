#!/usr/bin/env python
"""A simple script that searches for a release in the MusicBrainz.
 $ ./populate.py Gemitaiz Kepler
"""
import musicbrainzngs
import sys
import json

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
    tracks = musicbrainzngs.search_recordings(artist=artist, release=album, limit=5)

    #print(json.dumps(tracks.get('recording-list')[0].get('title'), indent=4, sort_keys=True))
    #printing title of tracks
    for id, track in enumerate (tracks.get('recording-list')):
        print(id, '{}'.format( track['title'] ) )


    #from music import base, engine, session
    #from music.models import *
    #Base.metadata.create_all(engine)

    #for id, track in enumerate(tracks.get('recording-list')):
    #    print(track['title'])

