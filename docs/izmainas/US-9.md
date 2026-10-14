# US-9 · Pieejamības tests zaļš + `docs/PIEEJAMIBAS-PRASIBAS.md` realizācija

**Kas mainīts**
- `docs/PIEEJAMIBAS-PRASIBAS.md`:
  - 3. sadaļa: kontrolsarakstam pievienota kolonna ar rezultātu katram no 15 punktiem;
  - 4. sadaļa: aizpildīts protokols A (axe), B (tastatūra), C (reflow, 200 %) un E (saturs), kā arī atradumu reģistrs;
  - D (ekrānlasītājs) atzīmēts kā **neveikts**.
- Labojumi pēc atradumiem (`static/style.css`):
  1. 1.4.10: detaļu lapas `<dl>` 320 px platumā bija 340 px. Tagad šaurā ekrānā tas ir vienā kolonnā.
  2. 2.5.8: atsevišķas saites bija 20 px augstas. Tagad `a { padding-block: 0.125rem }`, tātad 24 px.
- Kontrolsaraksta 11. punkts (3.2.6): kontakti kājenē visās lapās.

**Rezultāts**
- axe: 0 critical / 0 serious / 0 moderate / 0 minor visās lomās (5 + 16 + 6 lapas), kā arī 9 stāvokļos ar kļūdām un MI saturu.
- Tastatūra: visos 8 ekrānos fokuss redzams, lamatu nav, mērķi ≥ 24 px.
- 320 px un 200 %: OK.

**Kas jāizdara cilvēkam**
- NVDA vai VoiceOver pārbaude (4.D).
- Pelēktoņu filtrs.
- Paziņojuma apstiprināšana.
