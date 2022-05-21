CREATE TRIGGER check_saved_album
BEFORE INSERT OR UPDATE
ON saved_elements
FOR EACH ROW
EXECUTE FUNCTION check_saved_album();

CREATE FUNCTION check_saved_album() RETURNS trigger AS $$
BEGIN
    IF NEW.idElemento = (SELECT idElemento
                         FROM
                         WHERE



END;
$$ LANGUAGE plpgsql;