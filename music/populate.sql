CREATE EXTENSION pgcrypto;

INSERT INTO users VALUES ('edo', 'edo@mail.com', crypt('passedo', gen_salt('bf', 8)), 'Edoardo', 'Cecchinato', 'M', 'Italy', '2000-06-17', 'listener');
INSERT INTO users VALUES ('tia', 'tia@mail.com', crypt('passtia', gen_salt('bf', 8)), 'Mattia', 'Dei Rossi', 'M', 'Italy', '2000-04-04', 'listener');
INSERT INTO users VALUES ('leo', 'leo@mail.com', crypt('passleo', gen_salt('bf', 8)), 'Leonardo', 'Sartori', 'M', 'Italy', '2000-02-20', 'artist');


INSERT INTO listeners VALUES ('edo', '2022-06-05');
INSERT INTO listeners VALUES ('tia', '2022-06-05');


INSERT INTO artists VALUES ('leo', 'Leonardo Sartori', true, 'bio');


INSERT INTO elements VALUES (1, 'Notturno');
INSERT INTO elements VALUES (2, 'Notturno');
INSERT INTO elements VALUES (3, 'Falling Snow');
INSERT INTO elements VALUES (4, 'Falling Snow');
INSERT INTO elements VALUES (5, 'edo_playlist');
INSERT INTO elements VALUES (6, 'tia_playlist');


INSERT INTO albums VALUES (1, '2021-04-26', 'leo');
INSERT INTO albums VALUES (3, '2021-12-24', 'leo');


INSERT INTO tracks VALUES (2, 274, 'copyright', 'neoclassical', 1);
INSERT INTO tracks VALUES (4, 172, 'copyright', 'neoclassical', 3);


INSERT INTO playlists VALUES (5, true, 'edo');
INSERT INTO playlists VALUES (6, false, 'tia');


INSERT INTO payment_cards VALUES (200, '1234 5678 9012 3456', crypt('123', gen_salt('bf', 8)), '2024-07-05', 'tia', 'debit card');


INSERT INTO premiums VALUES ('tia', '2022-06-12', 200);


INSERT INTO followers VALUES ('leo', 'edo', '2022-06-06');
INSERT INTO followers VALUES ('leo', 'tia', '2022-06-06');


INSERT INTO saved_elements VALUES (1, 'edo');
INSERT INTO saved_elements VALUES (4, 'tia');


INSERT INTO playlist_tracks VALUES (2, 5);
INSERT INTO playlist_tracks VALUES (4, 5);
INSERT INTO playlist_tracks VALUES (4, 6);
