CREATE OR REPLACE FUNCTION check_saved_elements() RETURNS trigger AS $$
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
    RAISE EXCEPTION 'Il numero massimo di elementi che un utente premium può salvare è 5!';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS check_saved_elements ON saved_elements;
CREATE TRIGGER check_saved_elements
BEFORE INSERT OR UPDATE
ON saved_elements
FOR EACH ROW
EXECUTE FUNCTION check_saved_elements();

CREATE OR REPLACE FUNCTION delete_premium_elements() RETURNS trigger AS $$
BEGIN
    DELETE FROM saved_elements
    WHERE id_listener = OLD.id;
    DELETE FROM playlists
    WHERE creator = OLD.id AND NOT is_private;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS delete_premium_elements ON premiums;
CREATE TRIGGER delete_premium_elements
AFTER DELETE
ON premiums
FOR EACH ROW
EXECUTE FUNCTION delete_premium_elements();

-- TODO at_least_one_track

CREATE OR REPLACE FUNCTION at_least_one_track() RETURNS trigger AS $$
BEGIN
    IF ( NOT EXISTS( SELECT *
                 FROM tracks
                 WHERE album_id = NEW.id ) ) THEN
        DELETE FROM albums
        WHERE id = NEW.id;
        RAISE EXCEPTION 'Album non caricato correttamente';
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS at_least_one_track ON albums;
CREATE TRIGGER at_least_one_track
AFTER INSERT OR UPDATE
ON albums
FOR EACH ROW
EXECUTE FUNCTION at_least_one_track();



CREATE OR REPLACE FUNCTION not_last_track() RETURNS trigger AS $$
BEGIN
    IF ( NOT EXISTS( SELECT *
                 FROM tracks
                 WHERE album_id = OLD.album_id ) ) THEN
        DELETE FROM albums
        WHERE id = OLD.album_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS not_last_track ON tracks;
CREATE TRIGGER not_last_track
AFTER DELETE OR UPDATE ON tracks
FOR EACH ROW
EXECUTE FUNCTION not_last_track();



CREATE OR REPLACE FUNCTION not_creator_equals_guest() RETURNS trigger AS $$
BEGIN
    IF ( EXISTS( SELECT *
                 FROM events
                 WHERE id = NEW.id_event AND creator = NEW.id_artist ) ) THEN
        RAISE EXCEPTION 'Il creatore di un evento non può essere anche un ospite!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS not_creator_equals_guest ON guests;
CREATE TRIGGER not_creator_equals_guest
BEFORE INSERT OR UPDATE
ON guests
FOR EACH ROW
EXECUTE FUNCTION not_creator_equals_guest();

CREATE OR REPLACE FUNCTION not_creator_equals_feat() RETURNS trigger AS $$
BEGIN
    IF ( EXISTS( SELECT *
                 FROM tracks t JOIN albums a on t.album_id = a.id
                 WHERE t.id = NEW.id_track AND a.artist_id = NEW.id_artist ) ) THEN
        RAISE EXCEPTION 'Chi pubblica la traccia non può essere anche un featuring!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS not_creator_equals_feat ON featuring;
CREATE TRIGGER not_creator_equals_feat
BEFORE INSERT OR UPDATE
ON featuring
FOR EACH ROW
EXECUTE FUNCTION not_creator_equals_feat();



CREATE OR REPLACE FUNCTION check_public_playlist() RETURNS trigger AS $$
BEGIN
    IF ( EXISTS( SELECT *
                 FROM premiums
                 WHERE id = NEW.creator) ) THEN
        RETURN NEW;
    END IF;
    RAISE EXCEPTION 'Solo gli utenti premium possono creare playlist pubbliche!';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS check_public_playlist ON playlists;
CREATE TRIGGER check_public_playlist
BEFORE INSERT OR UPDATE
ON playlists
FOR EACH ROW
WHEN ( NOT NEW.is_private )
EXECUTE FUNCTION check_public_playlist();


-- TODO vedere se anche update

CREATE OR REPLACE FUNCTION delete_elements() RETURNS trigger AS $$
BEGIN
    DELETE FROM elements
    WHERE id = OLD.id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS delete_tracks ON tracks;
CREATE TRIGGER delete_tracks
AFTER DELETE
ON tracks
FOR EACH ROW
EXECUTE FUNCTION delete_elements();

DROP TRIGGER IF EXISTS delete_albums ON albums;
CREATE TRIGGER delete_albums
AFTER DELETE
ON albums
FOR EACH ROW
EXECUTE FUNCTION delete_elements();

DROP TRIGGER IF EXISTS delete_playlists ON playlists;
CREATE TRIGGER delete_playlists
AFTER DELETE
ON playlists
FOR EACH ROW
EXECUTE FUNCTION delete_elements();
