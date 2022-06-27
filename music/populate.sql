CREATE EXTENSION pgcrypto;

INSERT INTO users VALUES ('edo', 'edo@mail.com', crypt('passedo', gen_salt('bf', 8)), 'Edoardo', 'Cecchinato', 'M', 'Italy', '2000-06-17', 'listener');
INSERT INTO users VALUES ('tia', 'tia@mail.com', crypt('passtia', gen_salt('bf', 8)), 'Mattia', 'Dei Rossi', 'M', 'Italy', '2000-04-04', 'listener');
INSERT INTO users VALUES ('leo', 'leo@mail.com', crypt('passleo', gen_salt('bf', 8)), 'Leonardo', 'Sartori', 'M', 'Italy', '2000-02-20', 'artist');
INSERT INTO users VALUES ('gem', 'gem@mail.com', crypt('passgem', gen_salt('bf', 8)), 'Davide', 'De Luca', 'M', 'Italy', '194-05-02', 'artist');

INSERT INTO listeners VALUES ('edo', '2022-06-05');
INSERT INTO listeners VALUES ('tia', '2022-06-05');


INSERT INTO artists VALUES ('leo', 'Leonardo Sartori', true, 'bio leo');
INSERT INTO artists VALUES ('gem', 'Gemitaiz', true, 'bio gem');


INSERT INTO elements VALUES (1001, 'Notturno');
INSERT INTO elements VALUES (1002, 'Notturno');
INSERT INTO elements VALUES (1003, 'Falling Snow');
INSERT INTO elements VALUES (1004, 'Falling Snow');
INSERT INTO elements VALUES (1005, 'edo_playlist');
INSERT INTO elements VALUES (1006, 'tia_playlist');
INSERT INTO elements VALUES (1007, 'Kepler');
INSERT INTO elements VALUES (1008, 'traccia1-kepler');
INSERT INTO elements VALUES (1009, 'traccia2-kepler');


INSERT INTO albums VALUES (1001, '2021-04-26', 'leo');
INSERT INTO albums VALUES (1003, '2021-12-24', 'leo');
INSERT INTO albums VALUES (1007, '2017-12-24', 'gem');


INSERT INTO tracks VALUES (1002, 274, 'copyright', 'neoclassical', 1001);
INSERT INTO tracks VALUES (1004, 172, 'copyright', 'neoclassical', 1003);
INSERT INTO tracks VALUES (1008, 172, 'copyright', 'rap', 1007);
INSERT INTO tracks VALUES (1009, 172, 'copyright', 'rap', 1007);


INSERT INTO featuring VALUES ('leo', 1008);


INSERT INTO playlists VALUES (1005, true, 'edo');
INSERT INTO playlists VALUES (1006, false, 'tia');


INSERT INTO payment_cards VALUES (2000, '1234567890123456', crypt('123', gen_salt('bf', 8)), '2024-07-05', 'tia', 'debit card');


INSERT INTO premiums VALUES ('tia', '2022-06-12', 2000);


INSERT INTO followers VALUES ('leo', 'edo', '2022-06-06');
INSERT INTO followers VALUES ('leo', 'tia', '2022-06-06');
INSERT INTO followers VALUES ('gem', 'edo', '2022-06-06');
INSERT INTO followers VALUES ('gem', 'edo', '2022-06-06');


INSERT INTO saved_elements VALUES (1001, 'edo');
INSERT INTO saved_elements VALUES (1004, 'tia');


INSERT INTO playlist_tracks VALUES (1002, 1005);
INSERT INTO playlist_tracks VALUES (1004, 1005);
INSERT INTO playlist_tracks VALUES (1004, 1006);

INSERT INTO events VALUES (1001, 'Gemitaiz - Arena di Verona', '2022-09-05', '21:00:00', '23:00:00', 'Verona', 'https://www.gemitaiz.com', 'gem');

INSERT INTO guests VALUES ('leo', 1001);
