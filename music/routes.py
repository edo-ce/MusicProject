from music import app
from flask import render_template, redirect, url_for
from music.forms import SignUpForm, LoginForm


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
    return render_template('login.html')


@app.route('/logout')
def logout():
    return redirect(url_for('home'))


@app.route('/private')
def private():
    return render_template('private_artist.html')


@app.route('/search')
def search():
    return render_template('search.html')

