# DIZAINS · Vizuālais dizains pēc arhitektūras vizualizācijas

**Ideja**: dizains atkārto arhitektūras shēmas vizuālo valodu.
- Katrai lomai ir sava krāsa: Iedzīvotājs zaļš, Darbinieks zils, Vadītājs oranžs, MI violets, «Visi» pelēks.
- Kartītēm ir krāsaina galvenes josla un tonēts fons, kā shēmas kolonnām.
- Lomām ir burtu apļi I / D / V.

Lapas tēmu nosaka `{% block tema %}` (`body.tema-iedz|darb|vad|mi|visi`), kartītes krāsu — `.k-*` klase.

**Uzstādītās bibliotēkas** (lokāli `static/`, bez ārējiem pieprasījumiem pārlūkā, bez JS un bez būvēšanas soļa):
- **Inter** variable fonts (latin + latin-ext — latviešu burti), `@fontsource-variable/inter@5.1.0`, SIL OFL licence → `static/fonts/`.
- **Lucide** ikonas, `lucide-static@0.460.0`, 32 ikonas apvienotas SVG spraitā `static/ikonas.svg`, ISC licence → `static/LICENSE-lucide.txt`.
  - Ikonas ievieto makro `ikona()` no `templates/_makro.html`.
  - Tās vienmēr ir `aria-hidden="true"`, un nozīmi nes blakus esošais teksts.

CSS ietvarus (Bootstrap, Tailwind) apzināti neizmanto. CLAUDE.md liedz JS ietvarus un būvēšanas soli, un ietvaru noklusētie stili konfliktē ar projekta pieejamības prasībām.

**Kas mainīts**
- `templates/base.html`:
  - augšā četru lomu krāsu josla;
  - zīmols «Novada pašvaldība · **Iesniegumi**» (iestādes nosaukums tagad ir *pirms* «Iesniegumi»);
  - izvēlne kā «pill» pogas ar ikonām, aktīvā lapa iekrāsota;
  - lomas čips ar burtu apli;
  - tumša kājene ar kontaktiem.
- `templates/index.html`:
  - ievaddaļa ar darbību pogām un procesa vizualizāciju «Iesniedzat → Jauns → Apstrādē → Atbildēts/Noraidīts»;
  - lomu kartītes (I/D/V) ar katras lomas ekrāniem;
  - tēmas kā čipi ar ikonām.
- Pārējās lapas:
  - sadaļas kā krāsainas kartītes;
  - detaļu lapā divas kolonnas (darbības | vēsture kā laika līnija ar krāsainiem punktiem pēc notikuma veida);
  - pārskatā KPI kartītes ar ikonām un divas kolonnas;
  - MI palīgā sarunas burbuļi;
  - statusi kā «pill» ar punktu un tekstu.
- `templates/_makro.html`: `ikona()` un `statuss()`.
- `static/style.css`: pārrakstīts.

**Pieejamība pēc pārveides**
- Visas krāsas pārbaudītas:
  - tumšs teksts uz lomu joslām ≥ 7,4:1;
  - balts uz MI joslas 6,8:1;
  - teksti uz toņiem ≥ 5,7:1;
  - statusu pill ≥ 5,7:1;
  - kājenes saites 9,9:1.
- Labots dizaina laikā: teksta laukiem ar kļūdu nebija sarkanā rāmja (selektora specifiskums), tagad ir `:is(input, select, textarea)[aria-invalid="true"]`.
- axe: 0 pārkāpumu visās lomās un 7 papildu stāvokļos.
- Tastatūra: fokuss redzams visur, lamatu nav, mērķi ≥ 24 px.
- 320 px un 200 %: OK.

**Kā pārbaudīt pārlūkā**
1. Pārlādējiet ar Ctrl+Shift+R (jauns CSS un fonts).
2. Sākumlapā izvēlieties lomu kartīti. Augšā redzams «Novada pašvaldība · Iesniegumi».
3. Apskatiet katru lomu: iedzīvotāja lapas ir zaļas, darbinieka zilas, vadītāja oranžas, MI palīgs violets.
