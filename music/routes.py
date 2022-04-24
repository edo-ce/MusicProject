from music import app, db, bcrypt
from flask import render_template, redirect, url_for, flash
from music.models import User
from music.forms import SignUpForm, LoginForm
from flask_login import login_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    flash(f'Hi! You are logged in', category='success')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Hi {user.username}! You are logged in', category='success')
            return render_template('private_listener.html')
        else:
            flash('Username and password are not correct!', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out! See you soon', category='info')
    return redirect(url_for('home'))


@app.route('/private')
def private():
    return render_template('private_artist.html')


@app.route('/search')
def search():
    return render_template('search.html')

