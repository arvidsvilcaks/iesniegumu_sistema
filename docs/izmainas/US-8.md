# US-8 · Mans iesniegums

**Kas mainīts**
- `app.py`: `GET /mans-iesniegums?numurs=…`, pieejams bez lomas. Pārbauda numura formātu `GGGG-NNNN`.
- `templates/mans_iesniegums.html`: rāda statusu, tēmu, iesniegšanas laiku, pēdējo statusa notikumu un atbildi (tikai tad, ja statuss ir «Atbildēts» vai «Noraidīts»).
- `templates/iesniegts.html`: saite «pārbaudīt iesnieguma … statusu» ar jau ievadītu numuru (3.3.7).
- Izvēlnē ir «Mans iesniegums».

**Datu aizsardzība**: netiek rādīts vārds, e-pasts, adrese, iekšējie komentāri un MI žurnāls.

**Pieejamība**
- Nav CAPTCHA (3.3.8).
- Kļūdas «Ierakstiet iesnieguma numuru», «…formā GGGG-NNNN…» un «Iesniegums ar numuru … nav atrasts» ir tekstā (3.3.1). Ir arī kopsavilkums `role="alert"`, `aria-describedby` un `aria-invalid`.

**Kā pārbaudīt pārlūkā**
1. Atveriet «Mans iesniegums» un ierakstiet `2026-0003`: statuss «Atbildēts» un atbilde.
2. Ierakstiet `2026-0004`: «Apstrādē», bet iekšējais komentārs nav redzams.
3. Ierakstiet `2099-0001`: redzama kļūda «nav atrasts».
