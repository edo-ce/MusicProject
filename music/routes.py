from music import app, bcrypt, session
from flask import render_template, redirect, url_for, flash
from music.models import User, Artist, Listener, Premium, PaymentCard
from music.forms import SignUpForm, LoginForm, PaymentForm, SearchForm
from flask_login import login_user, logout_user, login_required
from music.algorithms import search_func


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
    if form.validate_on_submit():
        user = session.query(User).filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Hi {user.username}! You are logged in', category='success')
            artist = session.query(Artist).filter_by(username=user.username).first()
            if artist:
                return render_template('private_artist.html')
            return render_template('private_listener.html')
        else:
            flash('Username and password are not correct!', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out! See you soon', category='info')
    return redirect(url_for('home'))


@app.route('/premium')
@login_required
def premium():
    form = PaymentForm()
    if form.validate_on_submit():
        card = PaymentCard(number=form.number.data, security_code=form.pin.data,
                           expiration_date=form.expiration_date.data,
                           owner=form.holder.data, type=form.type.data)
        session.add(card)
        session.commit()
        flash('Account Premium create successfully', category='success')
        return redirect(url_for('private'))
    return render_template('premium.html', form=form)


@app.route('/private')
@login_required
def private():
    return render_template('private_artist.html')


@app.route('/search')
@login_required
def search():
    form = SearchForm()
    res = search_func(form.text.data)
    return render_template('search.html', res=res)

