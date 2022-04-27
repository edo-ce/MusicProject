from music import login_manager, Base
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Boolean
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


class Artist(User):
    __tablename__ = 'artists'

    id = Column(ForeignKey(User.username, ondelete='CASCADE'), primary_key=True)
    stage_name = Column(String, nullable=False)
    is_solo = Column(Boolean, nullable=False)
    bio = Column(String, nullable=False)

    user = relationship('User', back_populates='artists')


class Listener(User):
    __tablename__ = 'listeners'

    id = Column(ForeignKey(User.username, ondelete='CASCADE'), primary_key=True)
    registration_date = Column(Date, nullable=False)

    user = relationship('User', back_populates='listeners')
    premiums = relationship('Premium', back_populates='listener')


class Element(Base):
    __tablename__ = 'elements'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    albums = relationship('Album', back_populates='element')
    tracks = relationship('Track', back_populates='element')
    playlists = relationship('Playlist', back_populates='element')


class Album(Element):
    __tablename__ = 'albums'

    id = Column(ForeignKey(Element.id), primary_key=True)
    release_date = Column(Date, nullable=False)

    element = relationship('Element', back_populates='albums')


class Track(Element):
    __tablename__ = 'tracks'

    id = Column(ForeignKey(Element.id), primary_key=True)
    duration = Column(String, nullable=False)
    genre = Column(String, nullable=False)

    element = relationship('Element', back_populates='tracks')


class Playlists(Element):
    __tablename__ = 'playlists'

    id = Column(ForeignKey(Element.id), primary_key=True)
    is_private = Column(Boolean, nullable=False)
    maker = Column(String, nullable=False)

    element = relationship('Element', back_populates='playlists')


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    location = Column(String, nullable=False)
    link = Column(String, nullable=False)


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


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
    # basta eliminare la carta per eliminare l'account premium
    payment_card = Column(ForeignKey(PaymentCard.id, ondelete='CASCADE'), nullable=False)

    listener = relationship('Listener', back_populates='premiums')
    card = relationship('PaymentCard', back_populates='premiums')


class Follower(Base):
    __tablename__ = 'followers'

    id = Column(Integer, primary_key=True)
    following_date = Column(Date, nullable=False)
