from music import login_manager, Base
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


class User(Base, UserMixin):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String(8), nullable=False)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    country = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)

    artists = relationship('Artist', back_populates='user')
    listeners = relationship('Listener', back_populates='user')
    playlists = relationship('Playlist', back_populates='user')


class Artist(User):
    __tablename__ = 'artists'

    id = Column(ForeignKey(User.username, ondelete='CASCADE'), primary_key=True)
    stage_name = Column(String, nullable=False)
    is_solo = Column(Boolean, nullable=False)
    bio = Column(String, nullable=False)

    user = relationship('User', back_populates='artists')
    followers = relationship('Follower', back_populates='artists')


class Listener(User):
    __tablename__ = 'listeners'

    id = Column(ForeignKey(User.username, ondelete='CASCADE'), primary_key=True)
    registration_date = Column(Date, nullable=False)

    user = relationship('User', back_populates='listeners')
    premiums = relationship('Premium', back_populates='listener')
    followers = relationship('Follower', back_populates='listeners')


saved_elements = Table('saved_elements', Base.metadata,
                       Column('id_element', ForeignKey('elements.id'), primary_key=True),
                       Column('id_listener', ForeignKey('listeners.id'), primary_key=True))


class Element(Base):
    __tablename__ = 'elements'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    albums = relationship('Album', back_populates='element')
    tracks = relationship('Track', back_populates='element')
    playlists = relationship('Playlist', back_populates='element')

    listeners = relationship("Listener", secondary=saved_elements, backref="elements")


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    tracks = relationship('Track', back_populates='genre_id')


featuring = Table('featuring', Base.metadata,
                  Column('id_artist', ForeignKey('artists.id'), primary_key=True),
                  Column('id_track', ForeignKey('tracks.id'), primary_key=True))


playlist_tracks = Table('playlist_tracks', Base.metadata,
                        Column('id_track', ForeignKey('tracks.id'), primary_key=True),
                        Column('id_playlist', ForeignKey('playlists.id'), primary_key=True),)


class Album(Element):
    __tablename__ = 'albums'

    id = Column(ForeignKey(Element.id, ondelete='CASCADE'), primary_key=True)
    release_date = Column(Date, nullable=False)

    element = relationship('Element', back_populates='albums')
    tracks = relationship('Track', back_populates='album_id')


class Track(Element):
    __tablename__ = 'tracks'

    id = Column(ForeignKey(Element.id), primary_key=True)
    duration = Column(String, nullable=False)
    copyright = Column(String, nullable=False)
    genre = Column(ForeignKey(Genre.id, ondelete='CASCADE'), nullable=False)
    album = Column(ForeignKey(Album.id, ondelete='CASCADE'), nullable=False)

    element = relationship('Element', back_populates='tracks')
    genre_id = relationship('Genre', back_populates='tracks')
    album_id = relationship('Album', back_populates='tracks')

    artists = relationship("Artist", secondary=featuring, backref="tracks")
    playlists = relationship("Playlist", secondary=playlist_tracks, backref="tracks")


class Playlists(Element):
    __tablename__ = 'playlists'

    id = Column(ForeignKey(Element.id, ondelete='CASCADE'), primary_key=True)
    is_private = Column(Boolean, nullable=False)
    creator = Column(ForeignKey(User.username, ondelete='CASCADE'), nullable=False)

    element = relationship('Element', back_populates='playlists')
    user = relationship('User', back_populates='playlists')


event_participation = Table('event_participation', Base.metadata,
                            Column('id_event', ForeignKey('events.id'), primary_key=True),
                            Column('id_artist', ForeignKey('artists.id'), primary_key=True))


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    location = Column(String, nullable=False)
    link = Column(String, nullable=False)

    artists = relationship("Artist", secondary=event_participation, backref="events")


class PaymentCard(Base):
    __tablename__ = 'payment_cards'

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    security_code = Column(String, nullable=False)
    expiration_date = Column(Date, nullable=False)
    owner = Column(String, nullable=False)
    type = Column(String, nullable=False)

    premiums = relationship('Premium', back_populates='card')


class Premium(Listener):
    __tablename__ = 'premiums'

    id = Column(ForeignKey(Listener.id, ondelete='CASCADE'), primary_key=True)
    registration_date = Column(Date, nullable=False)
    payment_card = Column(ForeignKey(PaymentCard.id, ondelete='CASCADE'), nullable=False)

    listener = relationship('Listener', back_populates='premiums')
    card = relationship('PaymentCard', back_populates='premiums')


class Follower(Base):
    __tablename__ = 'followers'

    id_artist = Column(ForeignKey(Artist.id, ondelete='CASCADE'), primary_key=True)
    id_listener = Column(ForeignKey(Listener.id, ondelete='CASCADE'), primary_key=True)
    following_date = Column(Date, nullable=False)

    artists = relationship('Artist', back_populates='followers')
    listeners = relationship('Listener', back_populates='followers')
