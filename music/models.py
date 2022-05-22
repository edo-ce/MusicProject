from music import login_manager, Base, bcrypt, session
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Boolean, Table, CheckConstraint
from sqlalchemy.orm import relationship
import json
from datetime import date

@login_manager.user_loader
def load_user(code):
    return session.query(User).filter_by(username=code).first()


def get_title(code):
    return session.query(Element.title).filter_by(id=code).first()[0]


class User(Base, UserMixin):
    __tablename__ = 'users'

    username = Column(String(length=30), primary_key=True)
    email = Column(String(length=30), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String)
    lastname = Column(String)
    gender = Column(String)
    country = Column(String, nullable=False)
    birth_date = Column(Date)

    artists = relationship('Artist', backref='user')
    listeners = relationship('Listener', backref='user')
    playlists = relationship('Playlist', backref='user')

    def get_id(self):
        return self.username

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, psw):
        self.hashed_password = bcrypt.generate_password_hash(psw).decode('utf-8')

    def password_check(self, psw):
        return bcrypt.check_password_hash(self.hashed_password, psw)

    def __repr__(self):
        ret = {
            'username' : self.username,
            'password' : self.hashed_password,
            'email' : self.email
        }
        return json.dumps(ret, indent=4)


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(ForeignKey(User.username, ondelete='CASCADE'), primary_key=True)
    stage_name = Column(String, nullable=False)
    is_solo = Column(Boolean, nullable=False)
    bio = Column(String, nullable=False)

    albums = relationship('Album', backref='artist')
    followers = relationship('Follower', backref='artists')

    def get_stage_name(self):
        return self.stage_name

    def __repr__(self):
        ret = {
           'Stage Name': self.stage_name,
            'Type': "Solo" if self.is_solo else "group",
            'Bio': self.bio[0:30] + '...' if len(self.bio) > 30 else self.bio[0:30]
        }
        return json.dumps(ret, indent=4)


saved_elements = Table('saved_elements', Base.metadata,
                       Column('id_element', ForeignKey('elements.id'), primary_key=True),
                       Column('id_listener', ForeignKey('listeners.id'), primary_key=True))


class Listener(Base):
    __tablename__ = 'listeners'

    id = Column(ForeignKey(User.username, ondelete='CASCADE'), primary_key=True)
    registration_date = Column(Date, nullable=False)

    followers = relationship('Follower', backref='listeners')
    premiums_id = relationship('Premium', backref='listener_id')

    elements = relationship("Element", secondary=saved_elements, backref="listeners")


class Element(Base):
    __tablename__ = 'elements'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    albums = relationship('Album', backref='element')
    tracks = relationship('Track', backref='element')
    playlists = relationship('Playlist', backref='element')

    def find_type(self):
        return session.query(Track).filter_by(id=self.id).first() or session.query(Album).filter_by(id=self.id)\
            .first() or session.query(Playlist).filter_by(id=self.id).first()


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    tracks = relationship('Track', backref='genre_id')


featuring = Table('featuring', Base.metadata,
                  Column('id_artist', ForeignKey('artists.id'), primary_key=True),
                  Column('id_track', ForeignKey('tracks.id'), primary_key=True))


playlist_tracks = Table('playlist_tracks', Base.metadata,
                        Column('id_track', ForeignKey('tracks.id'), primary_key=True),
                        Column('id_playlist', ForeignKey('playlists.id'), primary_key=True),)


class Album(Base):
    __tablename__ = 'albums'

    id = Column(ForeignKey(Element.id, ondelete='CASCADE'), primary_key=True)
    release_date = Column(Date, nullable=False)
    artist_id = Column(ForeignKey(Artist.id, ondelete='CASCADE'))

    tracks_in = relationship('Track', backref='album_in')

    def number_of_tracks(self):
        return session.query(Album).join(Track).where(Track.album_id == self.id).count()

    def get_artist(self):
        return session.query(Artist).filter_by(id=self.artist_id).first()

    def __repr__(self):
        a = {'Title': get_title(self.id),
              'Release Date': str(self.release_date),
              'Artist': self.get_artist().stage_name
              }
        return json.dumps(a, indent=4)


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(ForeignKey(Element.id), primary_key=True)
    duration = Column(Integer, nullable=False)
    copyright = Column(String, nullable=False)
    genre = Column(ForeignKey(Genre.id, ondelete='CASCADE'), nullable=False)
    album_id = Column(ForeignKey(Album.id, ondelete='CASCADE'), nullable=False)

    artists_feat = relationship("Artist", secondary=featuring, backref="tracks_feat")
    playlists_id = relationship("Playlist", secondary=playlist_tracks, backref="tracks_id")

    def get_album(self):
        return session.query(Album).filter_by(id=self.album_id).first()

    def get_genre(self):
        return session.query(Genre).filter_by(id=self.genre).first()

    # TODO vedere aggiungere genere
    # TODO sistemare la durata

    def __repr__(self):

        ret = {
            'Title': get_title(self.id),
            'Artist': self.get_album().get_artist().stage_name,
            'Featuring': ", ".join(f.stage_name for f in self.artists_feat),
            'Duration': self.duration,
            'Genre': self.get_genre().name,
            'Copyright': self.copyright,
            'Album': 'single' if self.get_album().number_of_tracks() > 1 else 'Single'
        }

        return json.dumps(ret, indent=4)


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(ForeignKey(Element.id, ondelete='CASCADE'), primary_key=True)
    is_private = Column(Boolean, nullable=False)
    creator = Column(ForeignKey(User.username, ondelete='CASCADE'), nullable=False)

    def get_creator_name(self):
        artist = session.query(Artist).filter_by(id=self.creator).first()
        listener = session.query(Listener).filter_by(id=self.creator).first()
        return artist.stage_name if artist else listener.id

    def __repr__(self):
        ret = {
            'Title': get_title(self.id),
            'Playlist Type': 'Private' if self.is_private else 'Public',
            'Creator': self.get_creator_name()
        }
        return json.dumps(ret, indent=4)


guests = Table('guests', Base.metadata,
                  Column('id_artist', ForeignKey('artists.id'), primary_key=True),
                  Column('id_event', ForeignKey('events.id'), primary_key=True))


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    location = Column(String, nullable=False)
    link = Column(String, nullable=False)
    creator = Column(ForeignKey(Artist.id, ondelete='CASCADE'), nullable=False)

    # TODO change schema
    artists_guests = relationship("Artist", secondary=guests, backref="events_guests")

    __table_args__ = (
        CheckConstraint('end_time > start_time'),
    )

    def __repr__(self):
        ret = {
            'Name': f'{self.name} - {session.query(Artist.stage_name).filter_by(id=self.creator).first()[0]}',
            'Date': str(self.date),
            'Time': f'{self.start_time} - {self.end_time}',
            'Location': self.location,
            'Link': self.link
        }
        return json.dumps(ret, indent=4)


class PaymentCard(Base):
    __tablename__ = 'payment_cards'

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    security_pin = Column(String, nullable=False)
    # TODO check expiration_date > date.today()
    expiration_date = Column(Date, nullable=False)
    owner = Column(String, nullable=False)
    type = Column(String, nullable=False)

    premiums = relationship('Premium', backref='card')

    @property
    def pin(self):
        return self.pin

    @pin.setter
    def pin(self, p):
        self.security_pin = bcrypt.generate_password_hash(p).decode('utf-8')


class Premium(Base):
    __tablename__ = 'premiums'

    id = Column(ForeignKey(Listener.id, ondelete='CASCADE'), primary_key=True)
    registration_date = Column(Date, nullable=False)
    payment_card = Column(ForeignKey(PaymentCard.id, ondelete='CASCADE'), nullable=False)


class Follower(Base):
    __tablename__ = 'followers'

    id_artist = Column(ForeignKey(Artist.id, ondelete='CASCADE'), primary_key=True)
    id_listener = Column(ForeignKey(Listener.id, ondelete='CASCADE'), primary_key=True)
    following_date = Column(Date, nullable=False)
