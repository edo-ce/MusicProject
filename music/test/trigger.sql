/* 2) */
CREATE TRIGGER check_saved_album
BEFORE INSERT OR UPDATE
ON saved_elements
FOR EACH STATEMENT
EXECUTE FUNCTION check_saved_album();

CREATE FUNCTION check_saved_album() RETURNS trigger AS $$
BEGIN
    IF (5 < (   SELECT COUNT(*)
                FROM Listener JOIN saved_album
                WHERE NEW.id_listener = Listener.id ) THEN
        RETURN NEW;

    END IF;
    RETURN NULL;

END;
$$ LANGUAGE plpgsql;