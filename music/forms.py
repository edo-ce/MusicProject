from flask_wtf import FlaskForm
from music.models import session, User, Artist, Listener
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, TextAreaField, BooleanField, \
    IntegerField, FieldList, SearchField, TimeField, URLField, FormField
from wtforms.validators import Length, Email, DataRequired, EqualTo, ValidationError, InputRequired, NumberRange, URL, \
    Optional


# TODO add constraints


class SignUpForm(FlaskForm):
    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    name = StringField(label='Name:', validators=[Optional(), Length(min=2, max=30)])
    lastname = StringField(label='Lastname:', validators=[Optional(), Length(min=2, max=30)])
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password_check = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    country = StringField(label='Country:', validators=[Length(min=2, max=30), DataRequired()])
    birth_date = DateField(label='Birth Date:', validators=[Optional()])
    gender = SelectField(label='Gender', choices=['M', 'F'])
    user_type = SelectField(label='User Type:', choices=['Listener', 'Artist'], validators=[DataRequired()])
    submit = SubmitField(label='Create Account')

    def username_check(self, username):
        user = session.query(User).filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists!')

    def email_check(self, email):
        email_res = session.query(User).filter_by(email=email.data).first()
        if email_res:
            raise ValidationError('Email already exists!')


class SignUpFormArtist(FlaskForm):
    stage_name = StringField(label='Stage Name:', validators=[Length(min=2, max=30), DataRequired()])
    solo_group = SelectField(label='Solo/Group:', choices=['Solo', 'Group'], validators=[DataRequired()])
    bio = TextAreaField(label='Bio:', validators=[InputRequired()])
    submit = SubmitField(label='Create Artist Account')


class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class UserSettingsForm(FlaskForm):
    email = StringField(label='Email:', validators=[Optional(), Email()])
    name = StringField(label='Name:', validators=[Optional(), Length(min=2, max=30)])
    lastname = StringField(label='Lastname:', validators=[Optional(), Length(min=2, max=30)])
    country = StringField(label='Country:', validators=[Optional(), Length(min=2, max=30)])
    submit = SubmitField(label='Upload changes')

    def email_check(self, email):
        email_res = session.query(User).filter_by(email=email.data).first()
        if email_res:
            raise ValidationError('Email already exists!')


class ArtistSettingsForm(UserSettingsForm):
    stage_name = StringField(label='Stage Name:', validators=[Optional(), Length(min=2, max=30)])
    solo_group = SelectField(label='Solo/Group:', validators=[Optional()], choices=['Solo', 'Group'])
    bio = TextAreaField(label='Bio:')


class PaymentForm(FlaskForm):
    type = StringField(label='Card Type:', validators=[DataRequired()])
    number = StringField(label='Card Number:', validators=[Length(min=13, max=19), DataRequired()])
    holder = StringField(label='Holder:', validators=[Length(min=2, max=60), DataRequired()])
    expiration_date = DateField(label='Expiration Date:', validators=[DataRequired()])
    pin = StringField(label='Pin:', validators=[Length(min=3, max=4), DataRequired()])
    submit = SubmitField(label='Upgrade to Premium')


class TrackForm(FlaskForm):
    title = StringField(label='Track Title:', validators=[DataRequired()])
    copyright = StringField(label='Copyright:', validators=[DataRequired()])
    duration = IntegerField(label='Duration (seconds):', validators=[DataRequired(), NumberRange(min=0)])
    genre = StringField(label='Genre:', validators=[DataRequired()])
    featuring = StringField(label='Featuring', validators=[Optional()])
    submit = SubmitField(label='Upload Track')


class AlbumForm(FlaskForm):
    title = StringField(label='Album Title:', validators=[DataRequired()])
    num_tracks = IntegerField(label='Number of tracks:', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField(label='Upload Album')


class PlaylistTrackForm(FlaskForm):
    title = StringField(label='Track Title:', validators=[DataRequired()])
    album = StringField(label='Album Title:', validators=[DataRequired()])
    artist = StringField(label='Artist Title:', validators=[DataRequired()])
    submit = SubmitField(label='Add Track')


class PlaylistForm(FlaskForm):
    title = StringField(label='Playlist Title:', validators=[DataRequired()])
    private = BooleanField(label='Is Private:', default=True, false_values=('False', 'false', ''))
    number_tracks = IntegerField(label='Number of tracks:', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField(label='Upload Playlist')


class EventForm(FlaskForm):
    name = StringField(label='Event Name:', validators=[DataRequired()])
    date = DateField(label='Birth Date:', validators=[DataRequired()])
    start_time = TimeField(label='Start Time:', validators=[DataRequired()])
    end_time = TimeField(label='End Time:', validators=[DataRequired()])
    location = StringField(label='Location:', validators=[DataRequired()])
    link = URLField(label='Link:', validators=[URL(), DataRequired()])
    guests = StringField(label='Guests username:', validators=[Optional()])
    submit = SubmitField(label='Upload')
