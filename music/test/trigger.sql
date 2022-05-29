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