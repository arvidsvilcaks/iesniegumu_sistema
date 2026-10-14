# US-4 · Iesnieguma detaļas un apstrāde

**Kas mainīts**
- `app.py`: `/iesniegumi/<numurs>` (tikai darbiniekam) un trīs POST darbības: `/statuss`, `/komentars`, `/atbilde`.
- Atļautās statusa pārejas: Jauns → Apstrādē → Atbildēts / Noraidīts. Statusu «Atbildēts» var iestatīt tikai pēc tam, kad atbilde saglabāta.
- Katra darbība pierakstās `notikumi` ar laiku un lomu un atjauno `atjaunots`. Slēdzot iesniegumu, aizpildās `pabeigts`.
- `templates/detalas.html`: dati (e-pasts redzams tikai darbiniekam), statusa maiņa, atbilde, iekšējais komentārs, hronoloģiska vēsture.
- `templates/404.html`: lapa «Lapa nav atrasta» nezināmam numuram.

**Pieejamība**
- Virsraksti h1 «Iesniegums …» → h2 sadaļas (1.3.1, 2.4.6).
- Pēc darbības parādās paziņojums `<p role="status">` (4.1.3). Pāradresācija uz `#pazinojums`, tāpēc fokuss nonāk pie paziņojuma un nepazūd (2.4.11; galvene nav fiksēta).
- Pogām ir skaidrs teksts: «Mainīt statusu», «Saglabāt atbildi», «Pievienot komentāru» (4.1.2).
- Kļūdām tāds pats kopsavilkums un `aria-describedby` / `aria-invalid` kā US-1.

**Kā pārbaudīt pārlūkā**
1. Lomā «Darbinieks» atveriet «Iesniegums 2026-0001».
2. Nomainiet statusu uz «Apstrādē»: augšā parādās zaļš paziņojums, vēsturē jauns ieraksts.
3. Mēģiniet iestatīt «Atbildēts» bez atbildes: redzams kļūdas paziņojums.
4. Saglabājiet atbildi, tad iestatiet «Atbildēts»: statusa forma pazūd ar tekstu «Iesniegums ir slēgts».
