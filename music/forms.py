from flask_wtf import FlaskForm
from music.models import User, Artist, Listener
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import Length, Email, DataRequired, EqualTo, ValidationError


class SignUpForm(FlaskForm):
    username = StringField(label='Username:', validators=[Length(min=3, max = 30), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    name = StringField(label='Name:', validators=[Length(min=2, max=30), DataRequired()])
    surname = StringField(label='Surname:', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])
    password_check = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    nation = StringField(label='Nation:', validators=[Length(min=2, max=30), DataRequired()])
    birthdate = DateField(label='Username:', validators=[DataRequired()]) # vedi DateField
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
