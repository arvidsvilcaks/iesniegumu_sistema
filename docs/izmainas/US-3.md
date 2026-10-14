# US-3 · Iesniegumu saraksts

**Kas mainīts**
- `app.py`: maršruts `/saraksts`, pieejams tikai lomai «Darbinieks» (dekorators `vajadziga_loma`; citām lomām lapa «Nav piekļuves», statuss 403).
- Filtri statuss un tēma, kā arī meklēšana tekstā (numurs, iesniedzējs, adrese, apraksts). Meklēšana neņem vērā burtu lielumu, arī ar garumzīmēm (`lv_lower`).
- `templates/saraksts.html`: GET filtru forma un tabula.
- `templates/nav_piekluves.html`: lapa «Nav piekļuves».
- Pēc lomas izvēles sākumlapā lietotājs nonāk savas lomas sākuma lapā.

**Pieejamība**
- Tabulā ir `<caption>` ar atrasto skaitu, `<th scope="col">` un `<th scope="row">` (1.3.1).
- Statuss ir tekstā («Apstrādē»), krāsa ir tikai papildus (1.4.1).
- Filtri ir `<fieldset><legend>`.
- Saites teksts ir «Iesniegums 2026-0001», ne «Skatīt» (2.4.4).
- Šaurā ekrānā ritinās tikai tabula, nevis visa lapa (1.4.10). Ritināmais apgabals sasniedzams ar tastatūru.

**Kā pārbaudīt pārlūkā**
1. Sākumlapā izvēlieties lomu «Darbinieks» un nospiediet «Turpināt».
2. Izvēlieties statusu «Jauns» un nospiediet «Rādīt iesniegumus»: virsrakstā «atrasti 3».
3. Meklējiet «LATERN»: atrod abus apgaismojuma iesniegumus.
4. Lomā «Iedzīvotājs» atveriet `/saraksts`: redzama lapa «Nav piekļuves».
