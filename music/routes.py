from music import app
from flask import render_template, request
from music.forms import SignUpForm, LoginForm, SignUpFormArtist, PaymentForm, AlbumForm, TrackForm, \
    PlaylistForm, EventForm, PlaylistTrackForm, UserSettingsForm, ArtistSettingsForm
from flask_login import login_user, logout_user, login_required
from music.algorithms import *
from datetime import date

'''
@app.errorhandler(Exception)
def handle_error(e):
    rollback()
    return str(e)
'''


@app.context_processor
def utility_processor():
    return dict(is_premium=is_premium, is_artist=is_artist, is_saved=is_saved, delete_from_saved=delete_from_saved,
                save_something=save_something, advice_func=advice_func, get_title=get_title,
                get_element_creator=get_element_creator)


@app.route('/')
@app.route('/home')
def home():
    top = top_int_the_app(current_user.country) if current_user.is_authenticated else None
    return render_template('home.html', top=top)


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
    return render_template('forms/signup_artist.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = add_no_commit(User, username=form.username.data, email=form.email.data, password=form.password.data,
                    name=form.name.data, lastname=form.lastname.data, country=form.country.data,
                    gender=form.gender.data, birth_date=form.birth_date.data)
        if form.user_type.data == 'Artist':
            user.role = roles['ARTIST']
            return redirect(url_for('signup_artist', username=form.username.data))
        user.role = roles['LISTENER']
        add_and_commit(Listener, id=form.username.data, registration_date=date.today())
        login_user(get_user(form.username.data))
        flash(f"Listener account created successfully! You are logged in {form.username.data}", category="success")
        return redirect(url_for('private'))
    if form.errors != {}:
        for field, message in form.errors.items():
            flash(f"Error: {field} {message}", category="danger")
    return render_template('forms/signup.html', form=form)


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
    return render_template('forms/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out! See you soon', category='info')
    return redirect(url_for('home'))


@app.route('/premium-upgrade', methods=['GET', 'POST'])
@login_required
@roles_required(roles['LISTENER'])
def premium():
    form = PaymentForm()
    if form.validate_on_submit():
        card = get_payment_card_by_number_and_pin(form.number.data, form.pin.data)
        if card is None:
            card = add_no_commit(PaymentCard, number=form.number.data, pin=form.pin.data,
                               expiration_date=form.expiration_date.data,
                               owner=form.holder.data, type=form.type.data)
        add_and_commit(Premium, id=current_user.username, registration_date=date.today(), payment_card=card.id)
        flash('Account Premium create successfully', category='success')
        return redirect(url_for('private'))
    return render_template('forms/premium.html', form=form)


@app.route('/premium-delete')
@login_required
@roles_required(roles['LISTENER'])
def delete_premium():
    if is_premium(current_user.username):
        payment_card = get_payment_card(current_user.username)
        if session.query(PaymentCard).join(Premium).where(
                PaymentCard.id == payment_card.id and PaymentCard.id == Premium.payment_card).count() > 1:
            delete_tuple(Premium, current_user.username)
        else:
            delete_tuple(PaymentCard, payment_card.id)
    return redirect(url_for('private'))


@app.route('/upload-track-<number>', methods=['GET', 'POST'])
@login_required
@roles_required(roles['ARTIST'])
def upload_track(number):
    number = int(number)
    album = request.args.get('album')
    form = TrackForm()
    if form.validate_on_submit():
        # TODO vedere più pezzi con lo stesso titolo

        feats = list()
        if form.featuring.data != '':
            feats = [is_artist(x.strip()) for x in form.featuring.data.split(',')]
            for artist in feats:
                if artist is None:
                    flash(f'Artist {artist} does not exist!', category='danger')
                    return redirect(url_for('upload_track', number=number, album=album))
                elif artist.id == current_user.username:
                    flash(f'Artist {artist.id} is the current user!', category='danger')
                    return redirect(url_for('upload_track', number=number, album=album))

        code = add_no_commit(Element, title=form.title.data).id

        add_no_commit(Track, id=code, duration=form.duration.data, copyright=form.copyright.data,
                      genre=form.genre.data, album_id=int(album), artists_feat=feats)

        if number != 1:
            return redirect(url_for('upload_track', number=number-1, album=album))
        else:
            commit()
            flash('Album uploaded successfully!', category='success')
            return redirect(url_for('private'))
    return render_template('forms/upload_track.html', form=form)


@app.route('/upload-album', methods=['GET', 'POST'])
@login_required
@roles_required(roles['ARTIST'])
def upload_album():
    form = AlbumForm()
    if form.validate_on_submit():
        code = add_no_commit(Element, title=form.title.data).id
        add_no_commit(Album, id=code, release_date=date.today(), artist_id=current_user.username)
        return redirect(url_for('upload_track', number=form.num_tracks.data, album=code))
    return render_template('forms/upload_album.html', form=form)


@app.route('/upload-event', methods=['GET', 'POST'])
@login_required
@roles_required(roles['ARTIST'])
def upload_event():
    form = EventForm()
    if form.validate_on_submit():
        guests = list()
        if form.guests.data != '':
            guests = [is_artist(x.strip()) for x in form.guests.data.split(',')]
            for artist in guests:
                if artist is None:
                    flash(f'Artist does not exist!', category='danger')
                    return redirect(url_for('upload_event'))
                elif artist.id == current_user.username:
                    flash(f'Artist {artist.id} is the current user!', category='danger')
                    return redirect(url_for('upload_event'))

        add_and_commit(Event, name=form.name.data, date=form.date.data, start_time=form.start_time.data,
                      end_time=form.end_time.data, location=form.location.data, link=form.link.data,
                      creator=current_user.username, artists_guests=guests)

        flash('Event uploaded successfully!', category='success')
        return redirect(url_for('private'))
    return render_template('forms/upload_event.html', form=form)


@app.route('/add-<playlist>-track-<number>', methods=['GET', 'POST'])
@login_required
def add_playlist_track(playlist, number):
    number = int(number)
    playlist = int(playlist)
    form = PlaylistTrackForm()
    if form.validate_on_submit():
        track = get_playlist_track(form.title.data.lower(), form.album.data.lower(), form.artist.data.lower())
        if track is None:
            flash(f'Track {form.title.data} does not exist!', category='danger')
            return redirect(url_for('add_playlist_track', number=number, playlist=playlist))
        p = get_playlist(playlist)
        already = False
        for e in p.tracks_id:
            if e.id == track.id:
                already = True
                break
        if already:
            flash(f'Track is already in the playlist', category='danger')
            return redirect(url_for('add_playlist_track', number=number, playlist=playlist))
        p.tracks_id.append(track)
        flush()
        if number != 1:
            return redirect(url_for('add_playlist_track', number=number-1, playlist=playlist))
        else:
            commit()
            flash('Playlist uploaded successfully!', category='success')
            return redirect(url_for('private'))
    return render_template('forms/add_playlist_track.html', form=form)


@app.route('/create-playlist', methods=['GET', 'POST'])
@login_required
def create_playlist():
    form = PlaylistForm()
    if form.validate_on_submit():
        code = add_no_commit(Element, title=form.title.data).id
        if is_artist(current_user.username):
            is_private = False
        elif not is_premium(current_user.username):
            is_private = True
        else:
            is_private = form.private.data
        add_no_commit(Playlist, id=code, is_private=is_private, creator=current_user.username)
        return redirect(url_for('add_playlist_track', number=form.number_tracks.data, playlist=code))
    return render_template('forms/create_playlist.html', form=form)


@app.route('/delete-<table>-<code>')
@login_required
def delete_elements(table, code):
    deletable_tables = ('albums', 'tracks', 'playlists')
    if table in deletable_tables and get_element_creator(table, code) == current_user.username:
        delete_tuple(Element, code)
    elif table == 'events' and get_event(code).creator == current_user.username:
        delete_tuple(Event, code)
    return redirect(url_for('private'))


@app.route('/private')
@login_required
def private():
    if is_artist(current_user.username):
        elems = display_artist_contents(current_user.username)
    else:
        elems = find_saved_elements(current_user.username)
    return render_template('personal_page.html', elems=elems, username=current_user.username)


# per visualizzare la pagina di un'artista (album, playlist, eventi)
# per visualizzare la pagina di un utente (playlist)
@app.route('/view-<username>')
@login_required
@roles_required(roles['LISTENER'])
def view(username):
    if not username_exists(username):
        flash('The user does not exists!', 'warning')
        return redirect(url_for('home'))
    if username == current_user.username:
        return redirect(url_for('private'))
    artist = is_artist(username) is not None
    if artist:
        elems = display_artist_contents(username)
    else:
        elems = dict()
        elems['playlists'] = get_playlists_by_creator(username)
    return render_template('personal_page.html', elems=elems, artist=artist, username=username)


@app.route('/search-results', methods=['GET', 'POST'])
@login_required
@roles_required(roles['LISTENER'])
def search_results():
    # TODO advice non funziona con artist
    advice = advice_func(current_user.username)
    res = search_func(request.form['search_text'].lower())
    return render_template('search.html', advice=advice, dict=res)


@app.route('/delete-<id_elem>', methods=['GET', 'POST'])
@login_required
@roles_required(roles['LISTENER'])
def delete_route(id_elem):
    try:
        id_elem = int(id_elem)
    except ValueError:
        pass
    delete_from_saved(current_user.username, id_elem)
    return redirect(url_for('private'))


@app.route('/save-<id_elem>', methods=['GET', 'POST'])
@login_required
@roles_required(roles['LISTENER'])
def save_route(id_elem):
    try:
        id_elem = int(id_elem)
    except ValueError:
        pass
    save_something(current_user.username, id_elem)
    return redirect(url_for('private'))


@app.route('/delete-user')
@login_required
def delete_user():
    code = current_user.username
    logout_user()
    delete_tuple(User, code)
    return redirect(url_for('home'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    fields = 'email name lastname country'
    form = None
    if is_artist(current_user.username):
        form = ArtistSettingsForm()
        fields = fields + ' stage_name solo_group bio'
    else:
        form = UserSettingsForm()

    user_changes = dict()
    artist_changes = dict()

    if form.validate_on_submit():
        for key, value in form.data.items():
            if value != '':
                if key != 'stage_name' and key != 'solo_group' and key != 'bio':
                    user_changes[key] = value
                else:
                    artist_changes[key] = value

        update_tuple(User, current_user.username, **user_changes)
        update_tuple(Artist, current_user.username, **artist_changes)

        flash('Changes uploaded successfully!', category='success')
        return redirect(url_for('private'))
    return render_template('forms/settings.html', form=form, fields=fields)


@app.route('/stats', methods=['GET', 'POST'])
@login_required
@roles_required(roles['ARTIST'])
def stats():
    # get_country_listener(current_user.username) --> 'Italy,0.6,Germany,0.3,England,0.1'
    return render_template('statistics.html', get_gender_listener=get_gender_listener,
                           get_followers_count=get_followers_count, get_country_listener=get_country_listener)
