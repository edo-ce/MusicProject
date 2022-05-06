from music import app, session
from flask import render_template, redirect, url_for, flash, request
from music.models import User, Artist, Listener, Premium, PaymentCard
from music.forms import SignUpForm, LoginForm, PaymentForm, SearchForm, SignUpFormArtist
from flask_login import login_user, logout_user, login_required, current_user
from music.algorithms import search_func, find_creator_artist, find_saved_elements, is_artist
from datetime import date


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/signup-artist', methods=['GET', 'POST'])
def signup_artist():
    form = SignUpFormArtist()
    username = request.args['username']
    if form.validate_on_submit():
        artist = Artist(id=username, stage_name=form.stage_name.data, is_solo=(form.solo_group.data == 'Solo'),
                        bio=form.bio.data)
        session.add(artist)
        session.commit()
        login_user(session.query(User).filter_by(username=username).first())
        flash(f"Artist account created successfully! You are logged in {artist.id}", category="success")
        return redirect(url_for('private_artist'))
    return render_template('signup_artist.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data,
                    name=form.name.data, lastname=form.lastname.data, country=form.country.data,
                    gender=form.gender.data, birth_date=form.birth_date.data)
        session.add(user)
        if form.user_type.data == 'Artist':
            return redirect(url_for('signup_artist', username=user.username))
        listener = Listener(id=form.username.data, registration_date=date.today())
        session.add(listener)
        session.commit()
        login_user(user)
        flash(f"Listener account created successfully! You are logged in {user.username}", category="success")
        return redirect(url_for('private_listener'))
    if form.errors != {}:
        for field, message in form.errors.items():
            flash(f"Error: {field} {message}", category="danger")
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(username=form.username.data).first()
        if user and user.check_password(psw=form.password.data):
            login_user(user)
            flash(f'Hi {user.username}! You are logged in', category='success')
            return redirect(url_for('private'))
        else:
            flash('Username and password are not correct!', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out! See you soon', category='info')
    return redirect(url_for('home'))


@app.route('/premium-upgrade', methods=['GET', 'POST'])
@login_required
def premium():
    form = PaymentForm()
    if form.validate_on_submit():
        card = PaymentCard(number=form.number.data, pin=form.pin.data,
                           expiration_date=form.expiration_date.data,
                           owner=form.holder.data, type=form.type.data)
        premium_listener = Premium(id=current_user.username, registration_date=date.today(), payment_card=card.id)
        session.add(card)
        session.add(premium_listener)
        session.commit()
        flash('Account Premium create successfully', category='success')
        return redirect(url_for('private_listener'))
    return render_template('premium.html', form=form)


@app.route('/private')
@login_required
def private():
    if is_artist(current_user.username):
        return redirect(url_for('private_artist'))
    else:
        return redirect(url_for('private_listener'))


@app.route('/private-listener')
@login_required
def private_listener():
    saved_elements = find_saved_elements(current_user.username)
    return render_template('private_listener.html', elems=saved_elements)


@app.route('/private-artist')
@login_required
def private_artist():
    return render_template('private_artist.html')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        res = search_func(form.select.data, form.search.data)
        return redirect(url_for('search_results', res=res))
    return render_template('search.html', form=form)


@app.route('/search-results')
@login_required
def search_results():
    res = request.args.get('res')
    return render_template('search.html', res=res)
