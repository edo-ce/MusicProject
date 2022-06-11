/* 2) */
CREATE TRIGGER check_saved_album
BEFORE INSERT OR UPDATE
ON saved_elements
FOR EACH ROW
EXECUTE FUNCTION check_saved_album();

CREATE FUNCTION check_saved_album() RETURNS trigger AS $$
BEGIN
    IF ( EXISTS( SELECT *
                 FROM Premiums
                 WHERE NEW.id_listener = Premiums.id ) ) THEN
        RETURN NEW;
    END IF;
    IF (5 < (   SELECT COUNT(*)
                FROM saved_elements
                WHERE (NEW.id_listener = saved_elements.id_listener ) THEN
        RETURN NEW;

    END IF;
    RETURN NULL;

END;
$$ LANGUAGE plpgsql;

/* 1) Un'artista non può avere più di un album (o traccia?) con lo stesso nome */
CREATE TRIGGER only_one_name
BEFORE INSERT OR UPDATE
ON element
FOR EACH ROW
WHEN element.albums == New.albums
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
CREATE TRIGGER at_least_traks
BEFORE INSERT
ON Album
FOR EACH ROW
EXECUTE FUNCTION at_least_traks();

CREATE FUNCTION at_least_traks() RETURNS trigger AS $$
BEGIN
    IF ( New.tracks_in != emty)
        RETURN NEW;
    END IF;
    rimuovi album vuoto;
    RETURN NULL;

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