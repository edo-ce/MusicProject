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


GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE users, playlists, premiums, payment_cards, saved_elements, followers TO listener;
GRANT SELECT, INSERT, DELETE ON TABLE saved_elements, followers, listeners TO listener;
GRANT SELECT ON TABLE albums, tracks, artists, events TO listener;


GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE users, artists, playlists TO artist;
GRANT SELECT, INSERT, DELETE ON TABLE elements, albums, tracks, featuring, events, guests TO artist;
GRANT SELECT ON TABLE listeners TO artist;
