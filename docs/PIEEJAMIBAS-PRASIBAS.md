# Pieejamība (piekļūstamība) praksē: prasības → izstrāde → testēšana → paziņojums

Attiecas uz uzdevumu «Iesniegumi». Mērķis: pēc 1,5 h izstrādes **pierādīt** atbilstību, ne tikai apgalvot.

## 1. Kas mums ir saistošs

| Līmenis | Akts | Kam | Ko prasa | Kas uzrauga |
|---------|------|-----|----------|-------------|
| ES | Direktīva (ES) 2016/2102 — publiskā sektora tīmekļvietnes un mobilās lietotnes | Iestādēm | Atbilstība EN 301 549; piekļūstamības paziņojums; atgriezeniskās saites mehānisms | Dalībvalstu uzraudzība |
| LV | MK noteikumi Nr. 445 (14.07.2020) «Kārtība, kādā iestādes ievieto informāciju internetā» | Iestāžu tīmekļvietnēm un lietotnēm | EN 301 549 (WCAG 2.1 AA), piekļūstamības paziņojums, izvērtējums pēc VARAM vadlīnijām | VARAM |
| ES | Direktīva (ES) 2019/882 — Eiropas Piekļūstamības akts (EAA), piemēro no 28.06.2025 | Uzņēmumiem: e-komercija, bankas un finanšu pakalpojumi, e-grāmatas, elektroniskie sakari, pasažieru transporta tīmekļvietnes/lietotnes/biļetes, pašapkalpošanās termināļi, datori, viedtālruņi, e-lasītāji | Produkti un pakalpojumi piekļūstami; informācija par piekļūstamību; dokumentācija | Dalībvalstu tirgus uzraudzība |
| LV | Preču un pakalpojumu piekļūstamības likums + MK noteikumi Nr. 128 (27.02.2024), spēkā no 28.06.2025 | Tas pats | Tas pats; izņēmumi: mikrouzņēmumi (pakalpojumiem), nesamērīgs slogs, būtiskas izmaiņas | PTAC |
| Standarts | **EN 301 549** V3.2.1 (2021) → WCAG 2.1 AA; **V4.1.1 (publicēts 02.09.2026)** → WCAG 2.2 AA; V4 citēšana ES Oficiālajā Vēstnesī vēl gaidāma | Tehniskā prasību bāze visiem augstāk minētajiem | 9. nod. tīmeklis, 10. dokumenti, 11. programmatūra, 12. dokumentācija un atbalsts | — |

**Mūsu uzdevumā:** «Iesniegumi» ir iestādes tīmekļvietne → MK 445 + EN 301 549. Mērķējam uz **WCAG 2.2 AA**
(ietver visu 2.1 AA; sešas jaunas AA prasības — zemāk), lai esam gatavi V4.1.1.

Ja tā pati sistēma būtu, piemēram, pašvaldības e-pakalpojums ar maksājumu — papildus EAA / Preču un
pakalpojumu piekļūstamības likums.

## 2. Četri WCAG principi (POUR) — kā tie izskatās mūsu ekrānos

| Princips | Nozīmē | Piemērs uzdevumā |
|----------|--------|------------------|
| **Uztverams** (Perceivable) | Informācija sasniedz lietotāju vismaz vienā maņā | Diagramma pārskatā + tā pati tabula; statuss tekstā, ne tikai krāsa; kontrasts ≥ 4,5:1 |
| **Darbināms** (Operable) | Visu var izdarīt ar tastatūru, bez laika spiediena, bez «lamatām» | Forma aizpildāma ar Tab/Enter; redzams fokuss; skip-link; pogas ≥ 24 px |
| **Saprotams** (Understandable) | Valoda, kļūdas un navigācija ir prognozējamas | `lang="lv"`; kļūda «Ievadiet e-pastu formā vards@domens.lv», ne «Nederīgs»; izvēlne vienāda visās lapās |
| **Robusts** (Robust) | Darbojas ar palīgtehnoloģijām | Semantisks HTML (`<button>`, `<label>`, `<th scope>`); `role="status"` paziņojumiem |

## 3. Kontrolsaraksts «Iesniegumi» (prasība → kritērijs → kā pārbauda → kur)

| # | Prasība | WCAG | Kā pārbauda | Ekrāns | Rezultāts «Iesniegumi» (14.10.2026) |
|---|---------|------|-------------|--------|-----------|
| 1 | Attēliem un diagrammām ir teksta alternatīva | 1.1.1 | axe `image-alt`; vai tabula dublē diagrammu | 6 | ✅ Pārskatā diagramma + tabula ar tiem pašiem datiem; attēlu vietnē nav; axe 0 |
| 2 | Virsrakstu hierarhija, tabulu galvenes, formu lauku saistība | 1.3.1 | axe `heading-order`, `th-has-data-cells`, `label`; ekrānlasītājs: H / T taustiņi | visi | ✅ axe 0 visās lapās; h1 → h2 → h3; `<th scope>`; katram laukam `<label for>` |
| 3 | Krāsa nav vienīgais informācijas nesējs | 1.4.1 | Pelēktoņu filtrs (DevTools › Rendering › Emulate vision deficiencies) | 4, 5 | ✅ Statuss un kļūdas vienmēr tekstā («Apstrādē», «Kļūda: …»). 🟡 Pelēktoņu filtrs ar rokām — jāveic |
| 4 | Teksta kontrasts ≥ 4,5:1, UI elementu un fokusa ≥ 3:1 | 1.4.3, 1.4.11 | axe `color-contrast`; DevTools krāsu pipete | visi | ✅ axe `color-contrast` 0; aprēķināts: teksts ≥ 6,1:1, josla 7,8:1, fokuss (dzeltens + melns) 10,5:1 |
| 5 | 200 % mērogs un 320 px platums bez zuduma un horizontālās ritjoslas | 1.4.4, 1.4.10 | Ctrl + «+» līdz 200 %; DevTools ierīču režīms 320 px | visi | ✅ 320 px un 640 px (= 200 % no 1280 px) visās 8 lapās bez horizontālās ritjoslas. Labots: detaļu `<dl>` bija 340 px |
| 6 | Viss darbināms ar tastatūru; nav fokusa lamatu | 2.1.1, 2.1.2 | Tab cauri visam ceļam «iesniegt iesniegumu» | 2, 5 | ✅ Ceļš «iesniegt» līdz statusam ar tastatūru; Tab cikls katrā lapā atgriežas sākumā (nav lamatu) |
| 7 | Skip-link uz saturu; lapas nosaukums; fokusa secība; saišu teksts | 2.4.1, 2.4.2, 2.4.3, 2.4.4 | Pirmais Tab = «Pāriet uz saturu»; `<title>` unikāls; saite «Iesniegums 2026-0001», ne «Skatīt» | visi | ✅ Pirmais Tab = «Pāriet uz saturu»; `<title>` unikāls (ar «Kļūda:», ja ir kļūdas); saites «Iesniegums 2026-0001» |
| 8 | Fokuss redzams un nav aizsegts | 2.4.7, **2.4.11** (jauns 2.2) | Tab: kontūra redzama; fiksēta galvene neaizsedz fokusēto elementu | visi | ✅ Kontūra ≥ 2 px pārbaudīta katram Tab solim visās lapās; galvene nav fiksēta; pēc darbībām fokuss uz paziņojumu |
| 9 | Mērķa izmērs ≥ 24×24 px | **2.5.8** (jauns 2.2) | DevTools: pogu/saišu izmērs; atstarpes rindās | 4 | ✅ Visi atsevišķie mērķi ≥ 24 px. Labots: saites bija 20 px augstas |
| 10 | Lapas valoda | 3.1.1 | `<html lang="lv">`; axe `html-has-lang` | visi | ✅ `<html lang="lv">` visās lapās |
| 11 | Navigācija un elementi konsekventi; palīdzība vienā vietā | 3.2.3, 3.2.4, **3.2.6** (jauns 2.2) | Izvēlne un kājene vienādas; kontakti vienā vietā | visi | ✅ Izvēlne un kājene no `base.html`; kontakti kājenē vienā vietā visās lapās |
| 12 | Kļūdas identificētas, lauki marķēti, ieteikts labojums | 3.3.1, 3.3.2, 3.3.3 | Iesniedz tukšu formu: kopsavilkums + ziņa pie lauka + fokuss uz kopsavilkumu | 2, 8 | ✅ Kopsavilkums `role="alert"` + ziņa pie lauka + fokuss: iesniegt, mans iesniegums, MI palīgs, detaļas |
| 13 | Nav atkārtotas ievades; nav kognitīvu testu autentifikācijai | **3.3.7**, **3.3.8** (jauni 2.2) | Numurs no apstiprinājuma nav jāpārraksta no galvas; nav CAPTCHA | 3, 8 | ✅ Apstiprinājumā saite uz statusu ar numuru (nav jāpārraksta); nav CAPTCHA |
| 14 | Statusa ziņas nolasa ekrānlasītājs bez fokusa maiņas | 4.1.3 | `role="status"` pēc statusa maiņas; NVDA nolasa | 5 | 🟡 `role="status"` ieviests un axe 0; NVDA nolasīšana vēl nav pārbaudīta |
| 15 | Vilkšanai ir alternatīva (ja ir) | **2.5.7** (jauns 2.2) | Nav drag-and-drop bez pogas alternatīvas | — | ✅ Vilkšanas nav |

## 4. Testēšanas protokols (aizpilda komanda)

> Aizpildīts 14.10.2026. Daļas A–C izpildītas automatizēti ar Playwright (Chromium). Daļa D (ekrānlasītājs) **vēl nav veikta** —
> to nevar aizstāt ar automātisku rīku, tā jāveic komandai.

**A. Automātiski** — `python tests/a11y_check.py` (axe-core, visas lapas). Pārbaudiet arī formu ar kļūdām:
iesniedziet tukšu formu un palaidiet testu uz to pašu URL ar rezultātu.
Papildus: Chrome DevTools › Lighthouse › Accessibility; WAVE paplašinājums.
Automātiskie rīki atrod tikai **daļu** problēmu (tipiski 30–50 %). Pārējais — ar rokām.

| Palaišana | Lapas | critical / serious / moderate / minor |
|-----------|-------|----------------------------------------|
| `python tests/a11y_check.py` (bez lomas) | 5 | 0 / 0 / 0 / 0 |
| `LOMA=darbinieks python tests/a11y_check.py` | 16 (iesk. 10 detaļu lapas) | 0 / 0 / 0 / 0 |
| `LOMA=vaditajs python tests/a11y_check.py` | 6 | 0 / 0 / 0 / 0 |
| Stāvokļi, ko rāpulis neaizsniedz: tukša forma, «nav atrasts», čats ar sarunu un ar kļūdu, MI ieteikums, MI projekts laukā, «Nav piekļuves», 404 | 9 | 0 / 0 / 0 / 0 |

**B. Tastatūra** (10 min, ceļš: sākums → loma → iesniegt → apstiprinājums → mans iesniegums)

| Pārbaude | Rezultāts | Piezīme |
|----------|-----------|---------|
| Pirmais Tab atver «Pāriet uz saturu» | ☑ OK ☐ Nē | Visās lapās (skip-link pirmais `base.html`) |
| Fokuss redzams uz katra elementa | ☑ OK ☐ Nē | Katram Tab solim 8 lapās: kontūra ≥ 2 px (3 px dzeltena + melna ēna) |
| Secība loģiska (pa lapu no augšas uz leju) | ☑ OK ☐ Nē | Sākumlapā: skip-link → logo → izvēlne → loma → forma → kājenes kontakti → paziņojums; nav `tabindex > 0` |
| Formu var iesniegt ar Enter; radio ar bultiņām | ☑ OK ☐ Nē | Enter iesniedz lomas un iesnieguma formu; bultiņa ↓ pārslēdz lomu |
| Pēc kļūdas fokuss nonāk uz kļūdu kopsavilkumu | ☑ OK ☐ Nē | `#kludas`; saite kopsavilkumā fokusē lauku |
| Nav vietas, kur fokuss «iestrēgst» | ☑ OK ☐ Nē | Tab cikls katrā lapā atgriežas sākumā |

**C. Mērogs un reflow** — 200 % (Ctrl +) un 320 px (DevTools): teksts nepārklājas, nav horizontālās ritjoslas, tabulas lasāmas.

Rezultāts: 320 px un 640 px (= 1280 px logs pie 200 %) — visas 8 lapas bez horizontālās ritjoslas. Atrasts un labots: detaļu
lapas datu saraksts 320 px platumā bija 340 px (atradums Nr. 1). Ieteicams vēl apskatīt ar aci īstā pārlūkā ar Ctrl +.

**D. Ekrānlasītājs** (10 min; NVDA + Firefox/Chrome uz Windows, VoiceOver uz Mac, Narrator kā rezerve)

**Nav veikts** — jāveic komandai. Sagatavotais, ko pārbaudīt:

| Pārbaude | Rezultāts |
|----------|-----------|
| Lapas nosaukums tiek nolasīts, atverot lapu | ☐ (`<title>` unikāls — pārbaudīts) |
| H taustiņš staigā pa virsrakstiem loģiskā secībā | ☐ (hierarhija pārbaudīta HTML) |
| D taustiņš — orientieri: banner, navigation, main, contentinfo | ☐ (`header`, `nav`, `main`, `footer` ir) |
| Formas laukiem nolasa nosaukumu, obligātumu, kļūdu | ☐ (`label`, `required`, `aria-describedby`, `aria-invalid`) |
| Tabulā nolasa kolonnu galvenes, pārvietojoties pa šūnām | ☐ (`th scope`) |
| Pēc statusa maiņas paziņojums nolasīts | ☐ (`role="status"`, fokuss uz `#pazinojums`) |
| MI bloks tiek nosaukts kā «Ģenerēts ar MI …» | ☐ (teksts «Ģenerēts ar MI – pārbaudiet pirms lietošanas» blokā un pie lauka) |

**E. Saturs** — vienkārša valoda, saišu teksts, kļūdu ziņojumi saka, *kā* labot.

Kļūdu ziņojumi saka, kā labot, piemēram, «Ierakstiet e-pasta adresi pareizā formātā, piemēram, vards@example.lv.»,
«Ierakstiet numuru formā GGGG-NNNN, piemēram, 2026-0001.». Saites saprotamas ārpus konteksta. Valodas vienkāršība — jāvērtē cilvēkam.

**Atradumu reģistrs**

| # | Lapa | Problēma | WCAG | Smagums | Labots (commit) / Paliek paziņojumā |
|---|------|----------|------|---------|------------------------------------|
| 1 | `/iesniegumi/<numurs>` | 320 px platumā horizontālā ritjosla — datu saraksts `<dl>` 340 px | 1.4.10 | serious | Labots `static/style.css` (`.dati` šaurā ekrānā vienā kolonnā); commit vēl nav |
| 2 | vairākas (sākums, saraksts, detaļas) | Atsevišķas saites 20 px augstas («Izvēlēties lomu», «Iesniegums …» tabulā, «Atpakaļ …») | 2.5.8 | minor | Labots `static/style.css` (`a { padding-block }` → 24 px); commit vēl nav |
| 3 | visas | Nav veikta pārbaude ar ekrānlasītāju | 1.3.1, 4.1.2, 4.1.3 | — | Paliek paziņojumā līdz pārbaudei |
| 4 | MI palīgs, detaļas | MI ģenerēta teksta valodas skaidrību nevar pārbaudīt iepriekš | 3.1 (ieteikums) | minor | Paliek paziņojumā; teksts marķēts, atbildi apstiprina cilvēks |
| 5 | `/mans-iesniegums`, detaļas (atbilde ar MI projektu) | Formām trūka `novalidate`: pārlūks rādīja savu (angļu) burbuli, nevis kļūdu kopsavilkumu un ziņu pie lauka | 3.3.1, 3.1.2 | serious | Labots: `novalidate` (servera validācija ar kopsavilkumu); commit vēl nav |

## 5. Piekļūstamības paziņojuma veidne (MK 445; ES paraugs — Īstenošanas lēmums (ES) 2018/1523)

> Aizpildīts paziņojums ar 4. sadaļas atradumiem: lapa `/pieklustamiba` (`templates/pieklustamiba.html`). Jāapstiprina atbildīgajai personai.

```
PIEKĻŪSTAMĪBAS PAZIŅOJUMS
[Iestāde] apņemas nodrošināt tīmekļvietnes [nosaukums, URL] piekļūstamību saskaņā ar
MK 14.07.2020. noteikumiem Nr. 445 «Kārtība, kādā iestādes ievieto informāciju internetā».

Cik piekļūstama ir šī tīmekļvietne?
[Pilnībā atbilst / Daļēji atbilst / Neatbilst] EN 301 549 (WCAG 2.1 AA) prasībām.

Nepiekļūstamais saturs
- [Problēma] — [lapa] — [WCAG kritērijs] — [iemesls: neatbilstība / nesamērīgs slogs / nav prasību tvērumā] — [termiņš].

Piekļūstamības alternatīvas
[Tālrunis, e-pasts, klātiene; kā saņemt to pašu pakalpojumu]

Atsauksmēm un saziņai
[E-pasts, tālrunis; atbildes termiņš]

Sūdzību iesniegšana
Ja atbilde nav saņemta vai neapmierina — [pārraugošā iestāde]; tālāk — Tiesībsargs.

Ziņas par paziņojuma sagatavošanu
Sagatavots [datums]. Metode: [pašnovērtējums pēc VARAM vadlīnijām / automātiskais tests (axe) /
manuālā pārbaude ar tastatūru un ekrānlasītāju]. Apstiprināja: [vārds, amats]. Pārskatīts: [datums].
```

## 6. Prompti Claude Code pieejamībai (kopējiet un pielāgojiet)

- «Pārskati `templates/iesniegt.html` pret WCAG 2.2 AA: label, kļūdu ziņojumi ar aria-describedby, kļūdu kopsavilkums ar role="alert" un fokusu, obligātie lauki tekstā. Saraksti, ko maini un kāpēc, pēc tam labo.»
- «Palaid `python tests/a11y_check.py`, izlasi a11y-report.md un izlabo visus critical un serious atradumus. Pēc labošanas palaid vēlreiz.»
- «Pārbaudi, vai saraksta tabulai ir caption un th scope, un vai statuss ir nodots tekstā, ne tikai ar krāsu.»
- «Pārskata diagrammai pievieno teksta alternatīvu: tā pati informācija tabulā un aria-hidden diagrammai, ja tā ir dekoratīva.»
- «Izveido lapu /pieklustamiba pēc docs/PIEEJAMIBAS-PRASIBAS.md 5. sadaļas veidnes un ieliec tajā šos atradumus: …»

**Ko Claude NEVAR izdarīt jūsu vietā:** pārbaudīt ar tastatūru un ekrānlasītāju, novērtēt, vai kļūdu ziņa ir saprotama cilvēkam, un uzņemties atbildību paziņojumā.
