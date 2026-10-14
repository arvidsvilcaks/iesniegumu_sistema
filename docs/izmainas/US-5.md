# US-5 · Pārskats vadītājam

**Kas mainīts**
- `app.py`: maršruts `/parskats`, pieejams tikai lomai «Vadītājs».
- Lapā ir:
  - kopsavilkums: kopējais skaits, pabeigto skaits, vidējais apstrādes laiks;
  - tabula pa statusiem;
  - tabula pa tēmām ar vidējo apstrādes laiku;
  - CSS joslu diagramma pa tēmām.
- Apstrādes laiks ir no `izveidots` līdz `pabeigts` (statuss «Atbildēts» vai «Noraidīts»).
- `templates/parskats.html`, `static/style.css` (diagrammas stils).

**Pieejamība**
- Diagrammas dati ir arī tabulā, un `figcaption` to norāda (1.1.1). Diagrammā ir arī skaitļi tekstā, tā nav vienīgais informācijas avots.
- Josla `#0b5394` uz balta ir 7,8:1 (≥ 3:1, 1.4.11).
- Tabulās ir `<caption>` un `<th scope>`.

**Kā pārbaudīt pārlūkā**
- Sākumlapā izvēlieties lomu «Vadītājs». Ar testa datiem redzams: 10 iesniegumi, 4 pabeigti, vidējais apstrādes laiks 4,0 dienas.
- Joslu garums atbilst skaitļiem tabulā.
