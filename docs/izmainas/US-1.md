# US-1 · Iesnieguma iesniegšana

**Kas mainīts**
- `app.py`: maršruts `/iesniegt` (GET/POST), servera puses validācija `validet_iesniegumu()`, numura ģenerēšana `jauns_numurs()` (formāts `GGGG-NNNN`), notikums «Iesniegums reģistrēts» tabulā `notikumi`.
- `templates/iesniegt.html`: lauki vārds, e-pasts, tēma (no DB), adrese/vieta, apraksts, piekrišana datu apstrādei.
- `templates/base.html`: izvēlnē saite «Iesniegt iesniegumu».

**Pieejamība**
- Katram laukam ir `<label for>`. Obligātie lauki apzīmēti ar tekstu «(obligāts)» (1.3.1, 3.3.2, 1.4.1).
- Kļūdas gadījumā:
  - lapas sākumā ir kopsavilkums `<div role="alert">` ar saitēm uz laukiem, un fokuss pāriet uz to (`autofocus`);
  - pie lauka ir teksts «Kļūda: …», saistīts caur `aria-describedby`, un laukam ir `aria-invalid="true"` (3.3.1, 3.3.3);
  - `<title>` sākas ar «Kļūda:».
- Ievadītais pēc kļūdas saglabājas, laika limita nav (2.2.1). Ir `autocomplete` vārdam, e-pastam un adresei (1.3.5).

**Kā pārbaudīt pārlūkā**
1. Atveriet «Iesniegt iesniegumu» un nospiediet «Iesniegt iesniegumu» ar tukšu formu: augšā parādās kļūdu saraksts ar fokusu, pie katra lauka sarkans teksts «Kļūda: …».
2. Aizpildiet daļu laukus un iesniedziet vēlreiz: ievadītais nepazūd.
3. Uzklikšķiniet uz saites kļūdu sarakstā: fokuss pāriet uz attiecīgo lauku.
