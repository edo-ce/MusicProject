from music import app
from flask import render_template, redirect, url_for, flash, request
from music.forms import SignUpForm, LoginForm, SearchForm, SignUpFormArtist, PaymentForm, AlbumForm, TrackForm, \
    PlaylistForm
from flask_login import login_user, logout_user, login_required, current_user
from music.algorithms import *
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
        add_and_commit(Artist, id=username, stage_name=form.stage_name.data, is_solo=(form.solo_group.data == 'Solo'),
                        bio=form.bio.data)
        login_user(get_user(username))
        flash(f"Artist account created successfully! You are logged in {username}", category="success")
        return redirect(url_for('private'))
    return render_template('signup_artist.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        add_no_commit(User, username=form.username.data, email=form.email.data, password=form.password.data,
                    name=form.name.data, lastname=form.lastname.data, country=form.country.data,
                    gender=form.gender.data, birth_date=form.birth_date.data)
        if form.user_type.data == 'Artist':
            return redirect(url_for('signup_artist', username=form.username.data))
        add_and_commit(Listener, id=form.username.data, registration_date=date.today())
        login_user(get_user(form.username.data))
        flash(f"Listener account created successfully! You are logged in {form.username.data}", category="success")
        return redirect(url_for('private'))
    if form.errors != {}:
        for field, message in form.errors.items():
            flash(f"Error: {field} {message}", category="danger")
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.username.data)
        if user and user.password_check(psw=form.password.data):
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
        card = add_no_commit(PaymentCard, number=form.number.data, pin=form.pin.data,
                           expiration_date=form.expiration_date.data,
                           owner=form.holder.data, type=form.type.data)
        add_and_commit(Premium, id=current_user.username, registration_date=date.today(), payment_card=card.id)
        flash('Account Premium create successfully', category='success')
        return redirect(url_for('private'))
    return render_template('premium.html', form=form)


@app.route('/upload-track', methods=['GET', 'POST'])
@login_required
def upload_track():
    form = TrackForm()
    if form.validate_on_submit():
        code = add_no_commit(Element, title=form.title.data)
        add_no_commit(Track, id=code, duration=form.duration.data, genre=get_genre_id(form.genre.data),
                      copywright=form.copyright.data)
        # TODO featuring
    return render_template('upload_track.html')


@app.route('/upload-album', methods=['GET', 'POST'])
@login_required
def upload_album():
    form = AlbumForm()
    if form.validate_on_submit():
        code = add_no_commit(Element, title=form.title.data)
        add_no_commit(Album, id=code, release_date=date.today(), artist_id=current_user.username)
        for i in range(form.num_tracks.data):
            upload_track()
        commit()
    return render_template('upload_album.html', form=form)


@app.route('/create-playlist', methods=['GET', 'POST'])
@login_required
def create_playlist():
    form = PlaylistForm()
    return render_template('create_playlist.html')


@app.route('/private')
@login_required
def private():
    def title(code):
        return get_title(code)
    if is_artist(current_user.username):
        elems = display_artist_contents(current_user.username)
        return render_template('private_artist.html', elems=elems, get_title=title)
    else:
        elems = find_saved_elements(current_user.username)
        return render_template('private_listener.html', elems=elems, get_title=title)


@app.route('/view/<username>')
@login_required
def view(username):
    if not username_exists(username):
        return redirect(url_for('home'))
    artist = is_artist(username) is not None
    if artist:
        elems = find_saved_elements(username)
    else:
        elems = get_playlists_by_creator(username)
    return render_template('view.html', elems=elems, artist=artist)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        res = search_func(form.search.data.lower())
        return redirect(url_for('search_results', elems=res))
    return render_template('base.html', form=form)


@app.route('/search-results')
@login_required
def search_results():
    res = request.args.get('res')
    return render_template('search.html', res=res)
