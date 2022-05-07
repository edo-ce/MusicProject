from music import login_manager, Base, bcrypt, session
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Boolean, Table, CheckConstraint
from sqlalchemy.orm import relationship
# from music.algorithms import is_artist, get_title

@login_manager.user_loader
def load_user(code):
    return session.query(User).filter_by(username=code).first()


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

    artists = relationship('Artist', backref='user')
    listeners = relationship('Listener', backref='user')
    playlists = relationship('Playlist', backref='user')

    def get_id(self):
        return self.username

    @property
    def mypassword(self):
        return self.password

    @mypassword.setter
    def mypassword(self, psw):
        self.password = bcrypt.generate_password_hash(psw).decode('utf-8')

    def password_check(self, psw):
        return bcrypt.check_password_hash(self.password, psw)

    def __repr__(self):
        return f"<User(username={self.username}, password={self.password}, email={self.email})>"


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(ForeignKey(User.username, ondelete='CASCADE'), primary_key=True)
    stage_name = Column(String, nullable=False)
    is_solo = Column(Boolean, nullable=False)
    bio = Column(String, nullable=False)

    albums = relationship('Album', backref='artist')
    followers = relationship('Follower', backref='artists')

    def __repr__(self):
        return f"Stage Name: {self.stage_name}"


class Listener(Base):
    __tablename__ = 'listeners'

    id = Column(ForeignKey(User.username, ondelete='CASCADE'), primary_key=True)
    registration_date = Column(Date, nullable=False)

    followers = relationship('Follower', backref='listeners')
    premiums_id = relationship('Premium', backref='listener_id')


saved_elements = Table('saved_elements', Base.metadata,
                       Column('id_element', ForeignKey('elements.id'), primary_key=True),
                       Column('id_listener', ForeignKey('listeners.id'), primary_key=True))


class Element(Base):
    __tablename__ = 'elements'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    albums = relationship('Album', backref='element')
    tracks = relationship('Track', backref='element')
    playlists = relationship('Playlist', backref='element')

    listeners = relationship("Listener", secondary=saved_elements, backref="elements")


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
    artist_id = Column(ForeignKey(Artist.id, ondelete='CASCADE'), primary_key=True)

    tracks_in = relationship('Track', backref='album_in')

    def number_of_tracks(self):
        return session.query(Album).join(Track).filter_by(id=self.id).count()


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(ForeignKey(Element.id), primary_key=True)
    duration = Column(String, nullable=False)
    copyright = Column(String, nullable=False)
    genre = Column(ForeignKey(Genre.id, ondelete='CASCADE'), nullable=False)
    album_id = Column(ForeignKey(Album.id, ondelete='CASCADE'), nullable=False)

    artists_feat = relationship("Artist", secondary=featuring, backref="tracks_feat")
    playlists_id = relationship("Playlist", secondary=playlist_tracks, backref="tracks_id")

    def get_album(self):
        return session.query(Album).filter_by(id=self.album_id).first()

    # TODO vedere aggiungere genere
    '''
    def __repr__(self):
        album_name = 'Album: single'
        if self.get_album().number_of_tracks() > 1:
            album_name = f'Album: {get_title(self.get_album())}'
        return f"Title: {get_title(self.id)}, {album_name}, Duration: {self.duration}"
    '''


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(ForeignKey(Element.id, ondelete='CASCADE'), primary_key=True)
    is_private = Column(Boolean, nullable=False)
    creator = Column(ForeignKey(User.username, ondelete='CASCADE'), nullable=False)

    '''
    def __repr__(self):
        private = 'Public'
        if self.is_private:
            private = 'Private'
        creator_name = self.creator
        if is_artist(self.creator):
            creator_name = is_artist(self.creator).stage_name
        return f"Title: {get_title(self.id)}, State: {private}, Creator: {creator_name}"
    '''


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

    __table_args__ = (
        CheckConstraint('end_time > start_time'),
    )


class PaymentCard(Base):
    __tablename__ = 'payment_cards'

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    pin = Column(String, nullable=False)
    expiration_date = Column(Date, nullable=False)
    owner = Column(String, nullable=False)
    type = Column(String, nullable=False)

    premiums = relationship('Premium', backref='card')


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
