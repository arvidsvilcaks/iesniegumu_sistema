# US-7 · MI ieteikums darbiniekam

**Kas mainīts**
- `ai.py`: `ieteikums(apraksts) -> {tema, atbildes_projekts, avots}`.
  - Noklusēti tiek izmantota atslēgvārdu imitācija bez tīkla.
  - Ja ir `ANTHROPIC_API_KEY`, tiek izmantots Claude API (modelis no `AI_MODEL`, noklusēti `claude-opus-5-5`). Izvade tiek ierobežota ar JSON shēmu, tēma var būt tikai viena no 6.
  - Jebkuras kļūdas, atteikuma vai nepabeigtas atbildes gadījumā atgriežas imitācija.
- `app.py`:
  - `POST /iesniegumi/<numurs>/mi` iegūst ieteikumu un ieraksta žurnālā `notikumi`, `veids='mi_ieteikums'`, ar lomu un laiku;
  - `POST /iesniegumi/<numurs>/mi/izmantot` ievieto projektu atbildes laukā (sesijā) un ieraksta žurnālā. **DB atbilde netiek mainīta**, kamēr darbinieks pats nenospiež «Saglabāt atbildi».
- `templates/detalas.html`: bloks `<section aria-labelledby="mi-virsraksts">` ar marķējumu «Ģenerēts ar MI – pārbaudiet pirms lietošanas», avotu, ieteikto tēmu un projektu. Pie atbildes lauka ir marķējums, ja laukā ir MI teksts.

**MI akts / VDAR**
- Cilvēks apstiprina: nekas netiek saglabāts vai nosūtīts automātiski.
- Uz API tiek sūtīts tikai apraksts (bez vārda un e-pasta).
- Klasifikācija: minimāls vai ierobežots risks (`docs/MI-RISKA-KLASIFIKACIJA.md`, 4. sadaļa).

**Pieejamība**
- Pēc darbības fokuss pāriet uz bloka virsrakstu vai paziņojumu `role="status"`.
- Nav mirgojoša ielādes indikatora (2.3.1): lapa vienkārši ielādējas.
- axe: 0 pārkāpumu.

**Kā pārbaudīt pārlūkā**
1. Lomā «Darbinieks» atveriet «Iesniegums 2026-0001» un nospiediet «Saņemt MI ieteikumu». Jāparādās tēmai «Ielas un ceļi» un projektam ar marķējumu.
2. Nospiediet «Izmantot projektu». Teksts parādās laukā «Atbildes teksts» ar norādi, ka tas vēl nav saglabāts. Vēsturē ir divi «MI ieteikums» ieraksti.
3. Rediģējiet tekstu un nospiediet «Saglabāt atbildi».
