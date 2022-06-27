CREATE EXTENSION pgcrypto;

-- Users

INSERT INTO users VALUES ('edo', 'edo@mail.com', crypt('passedo', gen_salt('bf', 8)), 'Edoardo', 'Cecchinato', 'M', 'Italy', '2000-06-17', 'listener');
INSERT INTO users VALUES ('tia', 'tia@mail.com', crypt('passtia', gen_salt('bf', 8)), 'Mattia', 'Dei Rossi', 'M', 'Italy', '2000-04-04', 'listener');
INSERT INTO users VALUES ('leo', 'leo@mail.com', crypt('passleo', gen_salt('bf', 8)), 'Leonardo', 'Sartori', 'M', 'Italy', '2000-02-20', 'artist');
INSERT INTO users VALUES ('gem', 'gem@mail.com', crypt('passgem', gen_salt('bf', 8)), 'Davide', 'De Luca', 'M', 'Italy', '1994-05-02', 'artist');
INSERT INTO users VALUES ('ed', 'ed@mail.com', crypt('passed', gen_salt('bf', 8)), 'Edward', 'Sheeran', 'M', 'England', '1991-02-17', 'artist');
INSERT INTO users VALUES ('eminem', 'eminem@mail.com', crypt('passeminem', gen_salt('bf', 8)), 'Marshall', 'Mathers', 'M', 'USA', '1972-10-17', 'artist');
INSERT INTO users VALUES ('ade', 'ade@mail.com', crypt('passade', gen_salt('bf', 8)), 'Adele', 'Adkins', 'F', 'England', '1988-05-05', 'artist');
INSERT INTO users (username, email, hashed_password, country, role) VALUES ('bb', 'bb@mail.com', crypt('passbb', gen_salt('bf', 8)), 'USA', 'artist');
INSERT INTO users VALUES ('tay', 'tay@mail.com', crypt('passtay', gen_salt('bf', 8)), 'Taylor', 'Swift', 'F', 'USA', '1988-12-13', 'artist');
INSERT INTO users (username, email, hashed_password, country, role) VALUES ('lp', 'lp@mail.com', crypt('passlp', gen_salt('bf', 8)), 'USA', 'artist');
INSERT INTO users VALUES ('mark', 'mark@mail.com', crypt('passmark', gen_salt('bf', 8)), 'Mark', 'Brown', 'M', 'USA', '2000-08-03', 'listener');
INSERT INTO users VALUES ('sofi', 'sofi@mail.com', crypt('passsofi', gen_salt('bf', 8)), 'Sofia', 'Garcia', 'F', 'Spain', '2001-09-12', 'listener');
INSERT INTO users VALUES ('moni', 'moni@mail.com', crypt('passmoni', gen_salt('bf', 8)), 'Monika', 'Fisher', 'F', 'Germany', '1098-02-21', 'listener');
INSERT INTO users VALUES ('luka', 'luka@mail.com', crypt('passluka', gen_salt('bf', 8)), 'Luka', 'Schneider', 'M', 'Germany', '1097-06-01', 'listener');

-- Listeners

INSERT INTO listeners VALUES ('edo', '2022-06-05');
INSERT INTO listeners VALUES ('tia', '2022-06-05');
INSERT INTO listeners VALUES ('mark', '2022-06-07');
INSERT INTO listeners VALUES ('sofi', '2022-06-07');
INSERT INTO listeners VALUES ('moni', '2022-06-08');
INSERT INTO listeners VALUES ('luka', '2022-06-09');

-- Artists

INSERT INTO artists VALUES ('leo', 'Leonardo Sartori', true, 'bio leo');
INSERT INTO artists VALUES ('gem', 'Gemitaiz', true, 'bio gem');
INSERT INTO artists VALUES ('ed', 'Ed Sheeran', true, 'bio ed');
INSERT INTO artists VALUES ('eminem', 'Eminem', true, 'bio eminem');
INSERT INTO artists VALUES ('ade', 'Adele', true, 'bio ade');
INSERT INTO artists VALUES ('bb', 'Backstreet Boys', false, 'bio bb');
INSERT INTO artists VALUES ('tay', 'Taylor Swift', true, 'bio tay');
INSERT INTO artists VALUES ('lp', 'Linking Park', false, 'bio lp');

-- Elements

INSERT INTO elements VALUES (1001, 'Notturno'); INSERT INTO elements VALUES (1002, 'Notturno');
INSERT INTO elements VALUES (1003, 'Falling Snow');
INSERT INTO elements VALUES (1004, 'Falling Snow');
INSERT INTO elements VALUES (1005, 'edo_playlist');
INSERT INTO elements VALUES (1006, 'tia_playlist');
INSERT INTO elements VALUES (1007, 'Kepler');
INSERT INTO elements VALUES (1008, 'traccia1-kepler');
INSERT INTO elements VALUES (1009, 'traccia2-kepler');
INSERT INTO elements VALUES (1010, '21');
INSERT INTO elements VALUES (1011, 'Rolling in the Deep');
INSERT INTO elements VALUES (1012, 'Rumour has it');
INSERT INTO elements VALUES (1013, 'Turning tables');
INSERT INTO elements VALUES (1014, 'Take it all');
INSERT INTO elements VALUES (1015, 'Someone like you');
INSERT INTO elements VALUES (1016, 'Best of Adele');
INSERT INTO elements VALUES (1017, 'Easy on me');
INSERT INTO elements VALUES (1018, 'Easy on me');
INSERT INTO elements VALUES (1019, 'When we were young');
INSERT INTO elements VALUES (1020, 'When we were young');
INSERT INTO elements VALUES (1021, 'Shape of you');
INSERT INTO elements VALUES (1022, 'Shape of you');
INSERT INTO elements VALUES (1023, 'Bad habits');
INSERT INTO elements VALUES (1024, 'Bad habits');
INSERT INTO elements VALUES (1025, 'Lose yourself');
INSERT INTO elements VALUES (1026, 'Lose yourself');
INSERT INTO elements VALUES (1027, 'The Eminem Show');
INSERT INTO elements VALUES (1028, 'Soldier');
INSERT INTO elements VALUES (1029, 'Without me');
INSERT INTO elements VALUES (1030, 'Superman');
INSERT INTO elements VALUES (1031, 'The Marshal Mathers LP');
INSERT INTO elements VALUES (1032, 'Stan');
INSERT INTO elements VALUES (1033, 'The way I am');
INSERT INTO elements VALUES (1034, 'Marshal Mathers');
INSERT INTO elements VALUES (1035, 'I want it that way');
INSERT INTO elements VALUES (1036, 'I want it that way');
INSERT INTO elements VALUES (1037, 'Evermore');
INSERT INTO elements VALUES (1038, 'Happiness');
INSERT INTO elements VALUES (1039, 'Ivy');
INSERT INTO elements VALUES (1040, 'Closure');
INSERT INTO elements VALUES (1041, 'Reputation');
INSERT INTO elements VALUES (1042, 'End game');
INSERT INTO elements VALUES (1043, 'Delicate');
INSERT INTO elements VALUES (1044, 'Dress');
INSERT INTO elements VALUES (1045, 'Lover');
INSERT INTO elements VALUES (1046, 'Lover');
INSERT INTO elements VALUES (1047, 'Bad blood');
INSERT INTO elements VALUES (1048, 'Bad blood');
INSERT INTO elements VALUES (1049, 'Taylor Swift Compilation');
INSERT INTO elements VALUES (1050, 'Hybrid Theory');
INSERT INTO elements VALUES (1051, 'One step closer');
INSERT INTO elements VALUES (1052, 'Runaway');
INSERT INTO elements VALUES (1053, 'In the end');
INSERT INTO elements VALUES (1054, 'Numb');
INSERT INTO elements VALUES (1055, 'Numb');

-- Albums

INSERT INTO albums VALUES (1001, '2021-04-26', 'leo');
INSERT INTO albums VALUES (1003, '2021-12-24', 'leo');
INSERT INTO albums VALUES (1007, '2017-12-24', 'gem');
INSERT INTO albums VALUES (1010, '2011-12-24', 'ade');
INSERT INTO albums VALUES (1017, '2021-11-19', 'ade');
INSERT INTO albums VALUES (1019, '2015-11-19', 'ade');
INSERT INTO albums VALUES (1021, '2017-03-03', 'ed');
INSERT INTO albums VALUES (1023, '2021-10-29', 'ed');
INSERT INTO albums VALUES (1025, '2005-12-06', 'eminem');
INSERT INTO albums VALUES (1027, '2002-05-26', 'eminem');
INSERT INTO albums VALUES (1031, '2000-05-23', 'eminem');
INSERT INTO albums VALUES (1035, '1099-05-18', 'bb');
INSERT INTO albums VALUES (1037, '2020-12-11', 'tay');
INSERT INTO albums VALUES (1041, '2017-11-10', 'tay');
INSERT INTO albums VALUES (1045, '2019-08-23', 'tay');
INSERT INTO albums VALUES (1047, '2015-05-17', 'tay');
INSERT INTO albums VALUES (1050, '2000-10-24', 'lp');
INSERT INTO albums VALUES (1054, '2003-03-24', 'lp');

-- Tracks

INSERT INTO tracks VALUES (1002, 274, 'copyright', 'neoclassical', 1001);
INSERT INTO tracks VALUES (1004, 172, 'copyright', 'neoclassical', 1003);
INSERT INTO tracks VALUES (1008, 172, 'copyright', 'rap', 1007);
INSERT INTO tracks VALUES (1009, 172, 'copyright', 'rap', 1007);
INSERT INTO tracks VALUES (1011, 222, 'copyright', 'pop', 1010);
INSERT INTO tracks VALUES (1012, 222, 'copyright', 'pop', 1010);
INSERT INTO tracks VALUES (1013, 222, 'copyright', 'pop', 1010);
INSERT INTO tracks VALUES (1014, 222, 'copyright', 'pop', 1010);
INSERT INTO tracks VALUES (1015, 222, 'copyright', 'pop', 1010);
INSERT INTO tracks VALUES (1018, 222, 'copyright', 'pop', 1017);
INSERT INTO tracks VALUES (1020, 222, 'copyright', 'pop', 1019);
INSERT INTO tracks VALUES (1022, 222, 'copyright', 'pop', 1021);
INSERT INTO tracks VALUES (1024, 222, 'copyright', 'pop', 1023);
INSERT INTO tracks VALUES (1026, 222, 'copyright', 'rap', 1025);
INSERT INTO tracks VALUES (1028, 222, 'copyright', 'rap', 1027);
INSERT INTO tracks VALUES (1029, 222, 'copyright', 'rap', 1027);
INSERT INTO tracks VALUES (1030, 222, 'copyright', 'rap', 1027);
INSERT INTO tracks VALUES (1032, 222, 'copyright', 'rap', 1031);
INSERT INTO tracks VALUES (1033, 222, 'copyright', 'rap', 1031);
INSERT INTO tracks VALUES (1034, 222, 'copyright', 'rap', 1031);
INSERT INTO tracks VALUES (1036, 222, 'copyright', 'dance-pop', 1035);
INSERT INTO tracks VALUES (1038, 222, 'copyright', 'pop', 1037);
INSERT INTO tracks VALUES (1039, 222, 'copyright', 'pop', 1037);
INSERT INTO tracks VALUES (1040, 222, 'copyright', 'pop', 1037);
INSERT INTO tracks VALUES (1042, 222, 'copyright', 'pop', 1041);
INSERT INTO tracks VALUES (1043, 222, 'copyright', 'pop', 1041);
INSERT INTO tracks VALUES (1044, 222, 'copyright', 'pop', 1041);
INSERT INTO tracks VALUES (1046, 222, 'copyright', 'pop', 1045);
INSERT INTO tracks VALUES (1048, 222, 'copyright', 'pop', 1047);
INSERT INTO tracks VALUES (1051, 222, 'copyright', 'rock', 1050);
INSERT INTO tracks VALUES (1052, 222, 'copyright', 'rock', 1050);
INSERT INTO tracks VALUES (1053, 222, 'copyright', 'rock', 1050);
INSERT INTO tracks VALUES (1055, 222, 'copyright', 'rock', 1054);

-- Featuring

INSERT INTO featuring VALUES ('leo', 1008);
INSERT INTO featuring VALUES ('eminem', 1013);
INSERT INTO featuring VALUES ('tay', 1024);
INSERT INTO featuring VALUES ('ade', 1039);
INSERT INTO featuring VALUES ('bb', 1048);

-- Playlists

INSERT INTO playlists VALUES (1005, true, 'edo');
INSERT INTO playlists VALUES (1006, false, 'tia');
INSERT INTO playlists VALUES (1016, false, 'ade');
INSERT INTO playlists VALUES (1049, false, 'tay');

-- PaymentCards

INSERT INTO payment_cards VALUES (2000, '1234567890123456', crypt('123', gen_salt('bf', 8)), '2024-07-05', 'Mattia Dei Rossi', 'debit card');
INSERT INTO payment_cards VALUES (2001, '1234567890123457', crypt('321', gen_salt('bf', 8)), '2024-08-06', 'Luka Schneider', 'debit card');

-- Premiums

INSERT INTO premiums VALUES ('tia', '2022-06-12', 2000);
INSERT INTO premiums VALUES ('luka', '2022-06-12', 2001);

-- Followers

INSERT INTO followers VALUES ('leo', 'edo', '2022-06-06');
INSERT INTO followers VALUES ('leo', 'tia', '2022-06-06');
INSERT INTO followers VALUES ('gem', 'edo', '2022-06-06');
INSERT INTO followers VALUES ('gem', 'tia', '2022-06-06');
INSERT INTO followers VALUES ('leo', 'mark', '2022-06-06');
INSERT INTO followers VALUES ('eminem', 'mark', '2022-06-06');
INSERT INTO followers VALUES ('ade', 'mark', '2022-06-06');
INSERT INTO followers VALUES ('ade', 'sofi', '2022-06-06');
INSERT INTO followers VALUES ('tay', 'sofi', '2022-06-06');
INSERT INTO followers VALUES ('leo', 'sofi', '2022-06-06');
INSERT INTO followers VALUES ('bb', 'sofi', '2022-06-06');
INSERT INTO followers VALUES ('eminem', 'moni', '2022-06-06');
INSERT INTO followers VALUES ('gem', 'moni', '2022-06-06');
INSERT INTO followers VALUES ('lp', 'moni', '2022-06-06');
INSERT INTO followers VALUES ('ed', 'moni', '2022-06-06');
INSERT INTO followers VALUES ('ade', 'moni', '2022-06-06');
INSERT INTO followers VALUES ('ed', 'luka', '2022-06-06');
INSERT INTO followers VALUES ('tay', 'luka', '2022-06-06');
INSERT INTO followers VALUES ('leo', 'luka', '2022-06-06');

-- Saved Elements         1001 - 1055

INSERT INTO saved_elements VALUES (1001, 'edo');
INSERT INTO saved_elements VALUES (1022, 'edo');
INSERT INTO saved_elements VALUES (1040, 'edo');
INSERT INTO saved_elements VALUES (1031, 'edo');
INSERT INTO saved_elements VALUES (1012, 'edo');
INSERT INTO saved_elements VALUES (1055, 'edo');
INSERT INTO saved_elements VALUES (1004, 'tia');
INSERT INTO saved_elements VALUES (1033, 'tia');
INSERT INTO saved_elements VALUES (1027, 'tia');
INSERT INTO saved_elements VALUES (1044, 'tia');
INSERT INTO saved_elements VALUES (1012, 'tia');
INSERT INTO saved_elements VALUES (1037, 'tia');
INSERT INTO saved_elements VALUES (1019, 'tia');
INSERT INTO saved_elements VALUES (1034, 'mark');
INSERT INTO saved_elements VALUES (1026, 'mark');
INSERT INTO saved_elements VALUES (1049, 'mark');
INSERT INTO saved_elements VALUES (1052, 'mark');
INSERT INTO saved_elements VALUES (1030, 'sofi');
INSERT INTO saved_elements VALUES (1025, 'sofi');
INSERT INTO saved_elements VALUES (1011, 'sofi');
INSERT INTO saved_elements VALUES (1039, 'sofi');
INSERT INTO saved_elements VALUES (1023, 'moni');
INSERT INTO saved_elements VALUES (1041, 'moni');
INSERT INTO saved_elements VALUES (1020, 'moni');
INSERT INTO saved_elements VALUES (1047, 'moni');
INSERT INTO saved_elements VALUES (1006, 'luka');
INSERT INTO saved_elements VALUES (1018, 'luka');
INSERT INTO saved_elements VALUES (1028, 'luka');
INSERT INTO saved_elements VALUES (1035, 'luka');
INSERT INTO saved_elements VALUES (1042, 'luka');
INSERT INTO saved_elements VALUES (1050, 'luka');
INSERT INTO saved_elements VALUES (1036, 'luka');

-- Playlist Tracks

INSERT INTO playlist_tracks VALUES (1002, 1005);
INSERT INTO playlist_tracks VALUES (1004, 1005);
INSERT INTO playlist_tracks VALUES (1004, 1006);
INSERT INTO playlist_tracks VALUES (1011, 1016);
INSERT INTO playlist_tracks VALUES (1012, 1016);
INSERT INTO playlist_tracks VALUES (1015, 1016);
INSERT INTO playlist_tracks VALUES (1048, 1049);
INSERT INTO playlist_tracks VALUES (1039, 1049);
INSERT INTO playlist_tracks VALUES (1043, 1049);

-- Events

INSERT INTO events VALUES (1001, 'Gemitaiz - Arena di Verona', '2022-09-05', '21:00:00', '23:00:00', 'Verona (Italy)', 'https://www.gemitaiz.com', 'gem');
INSERT INTO events VALUES (1002, 'Coachella', '2023-04-14', '21:00:00', '23:00:00', 'Indio (USA)', 'https://www.coachella.com', 'tay');

-- Guests

INSERT INTO guests VALUES ('leo', 1001);
INSERT INTO guests VALUES ('bb', 1002);
INSERT INTO guests VALUES ('lp', 1002);
INSERT INTO guests VALUES ('eminem', 1002);
INSERT INTO guests VALUES ('ed', 1002);
INSERT INTO guests VALUES ('ade', 1002);
