# US-2 · Apstiprinājums

**Kas mainīts**
- `app.py`: pēc veiksmīga POST tiek veikta pāradresācija (`302`) uz `/iesniegts` (POST → redirect → GET). Numurs tiek nodots caur sesiju, nevis URL, tāpēc citi to nevar uzminēt.
- `templates/iesniegts.html`: iesnieguma numurs, tēma, laiks un saraksts «Kas notiks tālāk».

**Pieejamība**
- `<title>` ir «Iesniegums reģistrēts – Iesniegumi» (2.4.2).
- Numurs ir tekstā, ne attēlā (1.1.1).

**Kā pārbaudīt pārlūkā**
1. Iesniedziet derīgu iesniegumu. Atveras lapa «Iesniegums reģistrēts» ar numuru, piemēram, `2026-0011`.
2. Nospiediet F5: lapa vienkārši pārlādējas, un jauns iesniegums netiek izveidots (pārbaudiet sarakstā lomā «Darbinieks»).
