-- Iesniegumi: datu modelis (minimums). Papildiniet, ja vajag.
-- Visi testa dati ir izdomāti (e-pasti @example.lv).

CREATE TABLE temas (
    id        INTEGER PRIMARY KEY,
    nosaukums TEXT NOT NULL UNIQUE,
    apraksts  TEXT
);

CREATE TABLE iesniegumi (
    id            INTEGER PRIMARY KEY,
    numurs        TEXT NOT NULL UNIQUE,          -- piem., 2026-0001
    temas_id      INTEGER NOT NULL REFERENCES temas(id),
    vards         TEXT NOT NULL,
    epasts        TEXT NOT NULL,
    adrese        TEXT,
    apraksts      TEXT NOT NULL,
    statuss       TEXT NOT NULL DEFAULT 'Jauns'  -- Jauns | Apstrādē | Atbildēts | Noraidīts
                  CHECK (statuss IN ('Jauns', 'Apstrādē', 'Atbildēts', 'Noraidīts')),
    atbilde       TEXT,
    izveidots     TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    atjaunots     TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    pabeigts      TEXT                           -- kad statuss kļuva «Atbildēts» vai «Noraidīts» (US-5)
);

CREATE TABLE notikumi (
    id            INTEGER PRIMARY KEY,
    iesnieguma_id INTEGER NOT NULL REFERENCES iesniegumi(id) ON DELETE CASCADE,
    laiks         TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    veids         TEXT NOT NULL,                 -- statuss | komentars | atbilde | mi_ieteikums
    loma          TEXT,                          -- iedzivotajs | darbinieks | vaditajs | sistema
    teksts        TEXT NOT NULL
);

-- MI akts: strukturēts MI lietošanas žurnāls kvalitātes izlases pārbaudei (docs/MI-RISKA-KLASIFIKACIJA.md, US-7).
-- Papildus (ne vietā) ierakstiem notikumi ar veids='mi_ieteikums'. Tas pats SQL ir app.py MIGRACIJAS.
CREATE TABLE IF NOT EXISTS mi_zurnals (
    id            INTEGER PRIMARY KEY,
    iesnieguma_id INTEGER NOT NULL REFERENCES iesniegumi(id) ON DELETE CASCADE,
    laiks         TEXT NOT NULL,
    loma          TEXT,
    darbiba       TEXT NOT NULL CHECK (darbiba IN ('ieteikums', 'izmantots', 'apstiprinats')),
    avots         TEXT,
    ieteikta_tema TEXT,
    redigets      INTEGER                        -- tikai 'apstiprinats': 1, ja darbinieks mainīja MI projektu
);

INSERT INTO temas (nosaukums, apraksts) VALUES
 ('Ielas un ceļi',        'Bedres, ceļa zīmes, ietves'),
 ('Apgaismojums',         'Nedeg vai bojāts ielu apgaismojums'),
 ('Atkritumi un vide',    'Nesavākti atkritumi, piesārņojums'),
 ('Bērnudārza rinda',     'Jautājumi par rindu un vietām'),
 ('Sociālā palīdzība',    'Pabalsti un sociālie pakalpojumi'),
 ('Cits',                 'Viss pārējais');

-- 10 testa iesniegumi 5 tēmās (1, 2, 3, 4, 6)
INSERT INTO iesniegumi (numurs, temas_id, vards, epasts, adrese, apraksts, statuss, atbilde, izveidots, atjaunots, pabeigts) VALUES
 ('2026-0001', 1, 'Anna Bērziņa',     'anna@example.lv',     'Liepu iela 3',      'Liela bedre pretī mājai, bīstami velosipēdistiem.', 'Jauns', NULL, '2026-10-06 09:12', '2026-10-06 09:12', NULL),
 ('2026-0002', 2, 'Jānis Ozols',      'janis@example.lv',    'Skolas iela 12',    'Nedeg trīs laternas pēc kārtas.', 'Apstrādē', NULL, '2026-10-07 14:30', '2026-10-08 10:00', NULL),
 ('2026-0003', 3, 'Līga Kalniņa',     'liga@example.lv',     'Parka iela',        'Pārpildīts konteiners jau nedēļu.', 'Atbildēts', 'Konteiners iztukšots 03.10. Paldies par ziņojumu.', '2026-10-01 08:05', '2026-10-03 10:20', '2026-10-03 10:20'),
 ('2026-0004', 1, 'Pēteris Liepiņš',  'peteris@example.lv',  'Dzirnavu iela 8',   'Ietve pie veikala ir iegrimusi, krājas ūdens.', 'Apstrādē', NULL, '2026-10-02 11:00', '2026-10-05 09:30', NULL),
 ('2026-0005', 4, 'Ilze Krūmiņa',     'ilze@example.lv',     NULL,                'Kurā vietā rindā ir mans bērns un kad varētu saņemt vietu?', 'Atbildēts', 'Jūsu bērns ir rindā 14. vietā. Vietu plānots piedāvāt no 2027. gada janvāra.', '2026-09-28 13:45', '2026-10-02 09:00', '2026-10-02 09:00'),
 ('2026-0006', 2, 'Mārtiņš Kļaviņš',  'martins@example.lv',  'Ezera iela 21',     'Laterna pie gājēju pārejas mirgo un dažreiz nodziest.', 'Jauns', NULL, '2026-10-10 18:20', '2026-10-10 18:20', NULL),
 ('2026-0007', 3, 'Elīna Zariņa',     'elina@example.lv',    'Meža ceļš, pie tilta', 'Mežmalā izmesti būvgruži un riepas.', 'Apstrādē', NULL, '2026-10-08 07:50', '2026-10-09 13:15', NULL),
 ('2026-0008', 6, 'Roberts Siliņš',   'roberts@example.lv',  'Centrālais parks',  'Lūdzu uzstādīt vairāk soliņu parkā pie strūklakas.', 'Noraidīts', 'Šogad parka labiekārtošanas budžets ir izlietots. Priekšlikumu izskatīsim 2027. gada plānā.', '2026-09-30 16:10', '2026-10-05 12:00', '2026-10-05 12:00'),
 ('2026-0009', 4, 'Kristīne Vītola',  'kristine@example.lv', NULL,                'Vai bērnu var pārcelt uz bērnudārzu tuvāk dzīvesvietai?', 'Jauns', NULL, '2026-10-12 10:05', '2026-10-12 10:05', NULL),
 ('2026-0010', 6, 'Andris Upītis',    'andris@example.lv',   'Stacijas iela 1',   'Būvdarbi notiek naktī pēc plkst. 23, ļoti trokšņaini.', 'Atbildēts', 'Būvniekam izteikts brīdinājums; darbi naktī pārtraukti.', '2026-10-04 08:30', '2026-10-09 15:00', '2026-10-09 15:00');

INSERT INTO notikumi (iesnieguma_id, laiks, veids, loma, teksts) VALUES
 (1,  '2026-10-06 09:12', 'statuss',   'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (2,  '2026-10-07 14:30', 'statuss',   'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (2,  '2026-10-08 10:00', 'statuss',   'darbinieks', 'Statuss mainīts no «Jauns» uz «Apstrādē».'),
 (3,  '2026-10-01 08:05', 'statuss',   'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (3,  '2026-10-02 09:00', 'statuss',   'darbinieks', 'Statuss mainīts no «Jauns» uz «Apstrādē».'),
 (3,  '2026-10-03 10:15', 'atbilde',   'darbinieks', 'Konteiners iztukšots 03.10. Paldies par ziņojumu.'),
 (3,  '2026-10-03 10:20', 'statuss',   'darbinieks', 'Statuss mainīts no «Apstrādē» uz «Atbildēts».'),
 (4,  '2026-10-02 11:00', 'statuss',   'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (4,  '2026-10-05 09:30', 'statuss',   'darbinieks', 'Statuss mainīts no «Jauns» uz «Apstrādē».'),
 (4,  '2026-10-05 09:35', 'komentars', 'darbinieks', 'Nodots Komunālajam dienestam apsekošanai.'),
 (5,  '2026-09-28 13:45', 'statuss',   'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (5,  '2026-09-29 10:00', 'statuss',   'darbinieks', 'Statuss mainīts no «Jauns» uz «Apstrādē».'),
 (5,  '2026-10-02 08:55', 'atbilde',   'darbinieks', 'Jūsu bērns ir rindā 14. vietā. Vietu plānots piedāvāt no 2027. gada janvāra.'),
 (5,  '2026-10-02 09:00', 'statuss',   'darbinieks', 'Statuss mainīts no «Apstrādē» uz «Atbildēts».'),
 (6,  '2026-10-10 18:20', 'statuss',   'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (7,  '2026-10-08 07:50', 'statuss',   'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (7,  '2026-10-09 13:15', 'statuss',   'darbinieks', 'Statuss mainīts no «Jauns» uz «Apstrādē».'),
 (8,  '2026-09-30 16:10', 'statuss',   'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (8,  '2026-10-01 11:00', 'statuss',   'darbinieks', 'Statuss mainīts no «Jauns» uz «Apstrādē».'),
 (8,  '2026-10-05 11:55', 'atbilde',   'darbinieks', 'Šogad parka labiekārtošanas budžets ir izlietots. Priekšlikumu izskatīsim 2027. gada plānā.'),
 (8,  '2026-10-05 12:00', 'statuss',   'darbinieks', 'Statuss mainīts no «Apstrādē» uz «Noraidīts».'),
 (9,  '2026-10-12 10:05', 'statuss',   'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (10, '2026-10-04 08:30', 'statuss',   'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (10, '2026-10-06 09:00', 'statuss',   'darbinieks', 'Statuss mainīts no «Jauns» uz «Apstrādē».'),
 (10, '2026-10-09 14:50', 'atbilde',   'darbinieks', 'Būvniekam izteikts brīdinājums; darbi naktī pārtraukti.'),
 (10, '2026-10-09 15:00', 'statuss',   'darbinieks', 'Statuss mainīts no «Apstrādē» uz «Atbildēts».');
