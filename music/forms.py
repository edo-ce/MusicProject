from flask_wtf import FlaskForm
from music.models import session, User, Artist, Listener
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, TextAreaField, BooleanField, \
    IntegerField, FieldList, SearchField
from wtforms.validators import Length, Email, DataRequired, EqualTo, ValidationError, InputRequired
from wtforms.widgets import TextArea


class SignUpForm(FlaskForm):
    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    name = StringField(label='Name:', validators=[Length(min=2, max=30)])
    lastname = StringField(label='Lastname:', validators=[Length(min=2, max=30)])
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password_check = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    country = StringField(label='Country:', validators=[Length(min=2, max=30), DataRequired()])
    birth_date = DateField(label='Birth Date:')
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


class PaymentForm(FlaskForm):
    type = StringField(label='Card Type:', validators=[DataRequired()])
    number = StringField(label='Card Number:', validators=[Length(min=13, max=19), DataRequired()])
    holder = StringField(label='Holder:', validators=[Length(min=2, max=60), DataRequired()])
    expiration_date = DateField(label='Expiration Date:', validators=[DataRequired()])
    pin = StringField(label='Pin:', validators=[Length(min=3, max=4), DataRequired()])
    submit = SubmitField(label='Upgrade to Premium')


class SearchForm(FlaskForm):
    search = SearchField('Search:', validators=[DataRequired()])
    submit = SubmitField(label='Search')


class TrackForm(FlaskForm):
    title = StringField(label='Track Title:', validators=[DataRequired()])
    copyright = StringField(label='Copyright:', validators=[DataRequired()])
    duration = IntegerField(label='Duration:', validators=[DataRequired()])
    genre = StringField(label='Genre:', validators=[DataRequired()])
    featuring = FieldList(StringField(label='Feat:', validators=[DataRequired()]))
    submit = SubmitField(label='Upload')


class AlbumForm(FlaskForm):
    title = StringField(label='Album Title:', validators=[DataRequired()])
    num_tracks = IntegerField(label='Number of tracks:', validators=[DataRequired()])
    submit = SubmitField(label='Upload')


class PlaylistForm(FlaskForm):
    title = StringField(label='Album Title:', validators=[DataRequired()])
    private = BooleanField(label='Is Private:', validators=[DataRequired()])
    submit = SubmitField(label='Upload')
