from flask_wtf import FlaskForm
from music.models import User, Artist, Listener
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, TextAreaField, BooleanField, \
    IntegerField, FieldList
from wtforms.validators import Length, Email, DataRequired, EqualTo, ValidationError
from wtforms.widgets import TextArea


class SignUpForm(FlaskForm):
    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    name = StringField(label='Name:', validators=[Length(min=2, max=30), DataRequired()])
    surname = StringField(label='Surname:', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])
    password_check = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    nation = StringField(label='Nation:', validators=[Length(min=2, max=30), DataRequired()])
    birthdate = DateField(label='Username:', format='%d/%m/%Y', validators=[DataRequired()])
    gender = SelectField(label='Gender', choices=['M', 'F'])
    submit = SubmitField(label='Create Account')

    def username_check(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists!')

    def email_check(self, email):
        email_res = User.query.filter_by(email=email.data).first()
        if email_res:
            raise ValidationError('Email already exists!')


class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class PaymentForm(FlaskForm):
    type = StringField(label='Card Type:', validators=[DataRequired()])
    number = StringField(label='Card Number:', validators=[Length(min=13, max=19), DataRequired()])
    holder = StringField(label='Holder:', validators=[Length(min=2, max=60), DataRequired()])
    expiration_date = DateField(label='Expiration Date:', format='%d/%m/%Y', validators=[DataRequired()])
    pin = StringField(label='Pin:', validators=[Length(min=3, max=4), DataRequired()])
    submit = SubmitField(label='Login')


class SearchForm(FlaskForm):
    text = StringField(label='Search:', validators=[DataRequired()])
    submit = SubmitField(label='Search')


class TrackForm(FlaskForm):
    title = StringField(label='Track Title:', validators=[DataRequired()])
    copyright = StringField(label='Copyright:', validators=[DataRequired()])
    genre = StringField(label='Copyright:', validators=[DataRequired()])
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
