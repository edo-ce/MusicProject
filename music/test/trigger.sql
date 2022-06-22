/* 2) */
CREATE TRIGGER check_saved_elements
BEFORE INSERT OR UPDATE
ON saved_elements
FOR EACH ROW
EXECUTE FUNCTION check_saved_elements();

CREATE FUNCTION check_saved_elements() RETURNS trigger AS $$
BEGIN
    IF ( EXISTS( SELECT *
                 FROM Premiums
                 WHERE NEW.id_listener = Premiums.id ) ) THEN
        RETURN NEW;
    END IF;
    IF (5 > (   SELECT COUNT(*)
                FROM saved_elements
                WHERE NEW.id_listener = saved_elements.id_listener ) ) THEN
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_premium_elements
AFTER DELETE /* TODO UPDATE? */
ON premiums
FOR EACH ROW
EXECUTE FUNCTION delete_premium_elements();

CREATE FUNCTION delete_premium_elements() RETURNS trigger AS $$
BEGIN
    DELETE FROM saved_elements
    WHERE id_listener = OLD.id;
    DELETE FROM playlists
    WHERE creator = OLD.id AND NOT is_private;
    RETURN;
END;
$$ LANGUAGE plpgsql;

/* 1) Un'artista non può avere più di un album (o traccia?) con lo stesso nome */
CREATE TRIGGER only_one_name
BEFORE INSERT OR UPDATE
ON elements
FOR EACH ROW
WHEN elements.album == New.album
EXECUTE FUNCTION only_one_name();

CREATE FUNCTION only_one_name() RETURNS trigger AS $$
BEGIN
    IF ( EXISTS( SELECT *
                 FROM Artist
                 WHERE id = New.id ) ) THEN
        RETURN NULL;
    END IF;
    RETURN NEW;

END;
$$ LANGUAGE plpgsql;

/* 4) album deve contenere almeno una traccia (coinvolge + tabelle)*/
CREATE TRIGGER at_least_one_track
BEFORE INSERT OR UPDATE
ON albums
FOR EACH ROW
EXECUTE FUNCTION at_least_one_track();

CREATE FUNCTION at_least_one_track() RETURNS trigger AS $$
BEGIN
    IF ( EXISTS( SELECT *
                 FROM tracks
                 WHERE album_id == NEW.id ) ) THEN
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

/* se viene eliminata l'ultima traccia elimino l'album */
CREATE TRIGGER not_last_track
AFTER DELETE OR UPDATE ON tracks
FOR EACH ROW /* TODO TABLE? */
EXECUTE FUNCTION not_last_track();

CREATE FUNCTION not_last_track() RETURNS trigger AS $$
BEGIN
    IF ( NOT EXISTS( SELECT *
                 FROM tracks
                 WHERE album_id == OLD.id_album ) ) THEN
        DELETE FROM albums
        WHERE id = OLD.id_album;
    END IF;
    RETURN;
END;
$$ LANGUAGE plpgsql;

/*5) Un artista deve pubblicare almeno un album nella piattaforma per essere considerato tale (scadenza)*/
CREATE TRIGGER deadline_artist
BEFORE INSERT OR UPDATE
ON Artist
FOR EACH ROW
EXECUTE FUNCTION deadline_artist();

CREATE FUNCTION deadline_artist() RETURNS trigger AS $$
BEGIN
    IF ( EXISTS( SELECT tracks_in
                 FROM Album
                 WHERE Artist.id = artist) ) THEN
        RETURN NEW;
    END IF;

    IF( time_now > deadline)
        rimuovi album vuoto
        rimuovi artista


END;
$$ LANGUAGE plpgsql;

/* 6) Un artista non può essere ospite al suo stesso evento o un feat nella sua stessa traccia */
CREATE TRIGGER not_creator_equals_guest
BEFORE INSERT OR UPDATE
ON guests
FOR EACH ROW
EXECUTE FUNCTION not_creator_equals_guest();

CREATE FUNCTION not_creator_equals_guest() RETURNS trigger AS $$
BEGIN
    IF ( EXISTS( SELECT *
                 FROM events
                 WHERE id = NEW.id_event AND creator = NEW.id_artist ) ) THEN
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER not_creator_equals_feat
BEFORE INSERT OR UPDATE
ON featuring
FOR EACH ROW
EXECUTE FUNCTION not_creator_equals_feat();

CREATE FUNCTION not_creator_equals_feat() RETURNS trigger AS $$
BEGIN
    IF ( EXISTS( SELECT *
                 FROM tracks t JOIN albums a on t.album_id = a.id
                 WHERE t.id = NEW.id_track AND a.artist_id = NEW.id_artist ) ) THEN
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

/* 7) Un utente può creare una playlist pubblica solo se è un utente premium */
/* Il caso in cui un utente non sia più premium viene gestito in delete_premium_elements */
CREATE TRIGGER check_public_playlist
BEFORE INSERT OR UPDATE
ON playlists
FOR EACH ROW
WHEN ( NOT NEW.is_private )
EXECUTE FUNCTION check_public_playlist();

CREATE FUNCTION check_public_playlist() RETURNS trigger AS $$
BEGIN
    IF ( EXISTS( SELECT *
                 FROM premiums
                 WHERE id = NEW.creator) ) THEN
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

/* TODO controllare se possibile fare con sqlalchemy */
CREATE TRIGGER delete_tracks
AFTER DELETE
ON tracks
FOR EACH ROW
EXECUTE FUNCTION delete_elements();

CREATE TRIGGER delete_albums
AFTER DELETE
ON albums
FOR EACH ROW
EXECUTE FUNCTION delete_elements();

CREATE TRIGGER delete_playlists
AFTER DELETE
ON playlists
FOR EACH ROW
EXECUTE FUNCTION delete_elements();

CREATE FUNCTION delete_elements() RETURNS trigger AS $$
BEGIN
    DELETE FROM elements
    WHERE id = OLD.id;
END;
$$ LANGUAGE plpgsql;
