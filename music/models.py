from music import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

# ------------------------------------------------------
class User(db.Model):
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String(8))
    username = db.Column(db.String)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    gender = db.Column(db.String)
    country = db.Column(db.String)
    birth_date = db.Column(db.Date)


class Artist(User):
    stage_name = db.Column(db.String)
    is_solo = db.Column(db.Boolean)
    bio = db.Column(db.String)

class Listener(User):
    entry_date = db.Column(db.Date)

# ------------------------------------------------------
class Elements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

class Album(Elements):
    release_date = db.Column(db.Date)

class Track(Elements):
    duration = db.Column(db.String)
    genre = db.Column(db.String)

class Playlists(Elements):
    is_private = db.Column(db.Boolean)
    maker = db.Column(db.String)

#-----------------------------------------------------
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date)
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    location = db.Column(db.String)
    link = db.Column(db.String)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class PaymentCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String)
    security_code = db.Column(db.String)
    expiration_date = db.Column(db.Date)
    owner = db.Column(db.String)
    type = db.Column(db.String)

#----------------------------------------------------
class Premium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_date = db.Column(db.Date)

class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    following_data = db.Column(db.Date)



