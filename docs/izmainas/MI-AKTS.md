# MI-AKTS · MI riska klasifikācijas pasākumu realizācija

Avots: `docs/MI-RISKA-KLASIFIKACIJA.md`. Pilna tabula «pasākums → kods → pārbaude» ir tā 7. sadaļā.

**Kas mainīts**
- `schema.sql` + `app.py` `MIGRACIJAS`: jauna tabula `mi_zurnals` (ieteikums / izmantots / apstiprinats, avots, ieteiktā tēma, vai rediģēts). Esošajam `data.db` tā tiek pievienota automātiski startējot, dati nezūd.
- `app.py`:
  - **obligāta rediģēšana**: MI projektu nevar saglabāt ar neaizpildītām `[vietām]` un bez apliecinājuma rūtiņas;
  - strukturēts žurnāls katrai MI darbībai;
  - `MI_IZSLEGTS` slēdzis;
  - pārskatā MI uzraudzības dati.
- `ai.py`:
  - `ieslegts()`;
  - `anonimizet()` aizstāj e-pastu, tālruni un personas kodu, pirms teksts tiek sūtīts uz API.
- `templates/detalas.html`:
  - apliecinājuma rūtiņa;
  - norāde par `[vietām]`;
  - `data-mi-generets` (mašīnlasāms marķējums, 50. p. 2. d.);
  - izslēgtais stāvoklis;
  - forma ar `novalidate`.
- `templates/palidzigs.html`: `data-mi-generets` katrai MI atbildei, izslēgtais stāvoklis.
- `templates/parskats.html`: sadaļa «MI ieteikumu uzraudzība (pēdējās 30 dienas)» — kvalitātes izlases pārbaude reizi mēnesī.
- `templates/mans_iesniegums.html`: `novalidate`. Atrasts testējot: pārlūks rādīja angļu burbuli mūsu kļūdas vietā.
- `tests/mi_check.py`: jauns tests ar 28 pārbaudēm un 6. sadaļas 5 grūtajiem gadījumiem.
- `docs/MI-RISKA-KLASIFIKACIJA.md`: 7. sadaļa «Realizācija un pārbaude».

**Rezultāts**
- `python tests/mi_check.py`: 0 neizpildītas prasības.
- axe: visās lomās 0 pārkāpumu, arī kļūdu stāvoklī un ar `MI_IZSLEGTS=1`.

**Kā pārbaudīt pārlūkā**
1. Lomā «Darbinieks» atveriet iesniegumu → «Saņemt MI ieteikumu» → «Izmantot projektu» → «Saglabāt atbildi». Redzamas divas kļūdas: «neaizpildītas vietas [termiņš] …» un «Apliecinājiet…».
2. Aizstājiet `[…]`, atzīmējiet rūtiņu un saglabājiet.
3. Lomā «Vadītājs» atveriet «Pārskats». Sadaļā «MI ieteikumu uzraudzība» redzama šī atbilde ar «Darbinieks rediģēja: Jā».
4. Izslēgšana: apturiet serveri un palaidiet `MI_IZSLEGTS=1 python app.py`. MI bloks un MI palīgs rāda «izslēgts».
