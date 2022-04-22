from music import app
from flask import render_template, redirect, url_for
from music.forms import RegisterForm, LoginForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
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

