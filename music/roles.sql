DROP USER IF EXISTS admin;
DROP USER IF EXISTS listener;
DROP USER IF EXISTS artist;

CREATE USER admin WITH PASSWORD 'admin';
CREATE USER listener WITH PASSWORD 'listener';
CREATE USER artist WITH PASSWORD 'artist';

GRANT USAGE ON SCHEMA public TO admin;
GRANT USAGE ON SCHEMA public TO listener;
GRANT USAGE ON SCHEMA public TO artist;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;

-- admin fa session di inserimento di users, listeners e artists

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE playlists, premiums, payment_cards TO listener;
GRANT SELECT, INSERT ON TABLE saved_elements, followers TO listener;
GRANT SELECT, UPDATE, DELETE ON TABLE users, listeners TO listener;
GRANT SELECT ON TABLE albums, tracks, artists TO listener;

-- decidere se è possibile modificare un evento

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE playlists, events, guests TO artist;
GRANT SELECT, INSERT, DELETE ON TABLE elements, albums, tracks, featuring TO artist;
GRANT SELECT, UPDATE, DELETE ON TABLE users, artists TO artist;
GRANT SELECT ON TABLE listeners, tracks, artists TO artist;
