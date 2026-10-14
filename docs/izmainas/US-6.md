# US-6 · Piekļūstamības paziņojums (skelets)

**Kas mainīts**
- `templates/pieklustamiba.html` pārstrukturēts precīzi pēc veidnes `docs/PIEEJAMIBAS-PRASIBAS.md` 5. sadaļā (MK noteikumi Nr. 445, ES paraugs 2018/1523). Zināmais ir aizpildīts: iestāde, vietne, sūdzību ceļš uz Tiesībsargu.
- Lauki, kas atkarīgi no testēšanas, paliek iekavās `[ ]`, un lapa ir marķēta kā «Melnraksts».
- Saite «Piekļūstamības paziņojums» ir kājenē katrā lapā (`base.html`, 3.2.3).

**Papildināts pēc testēšanas (14.10.2026)**
- Kājenē kontakti visās lapās (`KONTAKTI` `app.py`, `<address>` `base.html`, 3.2.6). Kontakti ir izdomāti.
- Paziņojums aizpildīts:
  - atbilstība «daļēji atbilst», jo ekrānlasītāja tests nav veikts;
  - nepiekļūstamais saturs no atradumu reģistra;
  - alternatīvas, saziņa, sūdzības (VARAM → Tiesībsargs);
  - datums un metode.
- Atstāts cilvēkam: «Apstiprināja: [vārds, amats]» un ekrānlasītāja pārbaudes datums.

**Kā pārbaudīt pārlūkā**
- Jebkurā lapā kājenē uzklikšķiniet uz «Piekļūstamības paziņojums».
