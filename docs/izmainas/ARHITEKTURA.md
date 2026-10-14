# ARHITEKTURA · Atbilstība konceptuālajai arhitektūrai

Salīdzināts ar shēmu «Konceptuālā arhitektūra: «Iesniegumi»» (14.10.2026).

| Arhitektūras elements | Pirms | Kas izdarīts | Tagad |
|---|---|---|---|
| Lietotāji: iedzīvotājs, darbinieks, vadītājs (loma sesijā) | ✅ | — | ✅ |
| Flask, servera pusē renderēts HTML, viens process, viens repo | ✅ | — | ✅ |
| `base.html`: skip-link, orientieri, fokuss | ✅ | Kājenē pievienoti kontakti | ✅ |
| Iedzīvotājs: Sākums/loma, US-1, US-2 | ✅ | Apstiprinājumā saite uz statusu | ✅ |
| Iedzīvotājs: **US-8 Mans iesniegums** | ❌ | `/mans-iesniegums` — [US-8](US-8.md) | ✅ |
| Darbinieks: US-3 saraksts, US-4 detaļas un statuss | ✅ | — | ✅ |
| Darbinieks: **MI ieteikums detaļās** | ❌ | MI bloks + «Izmantot projektu» — [US-7](US-7.md) | ✅ |
| Vadītājs: US-5 tabula + diagramma | ✅ | — | ✅ |
| Visi: US-6 piekļūstamības paziņojums | 🟡 skelets | Aizpildīts ar testēšanas atradumiem — [US-6](US-6.md) | ✅ (jāapstiprina cilvēkam) |
| Visi: **kājene — kontakti** | ❌ | `KONTAKTI` + `<address>` kājenē visās lapās (3.2.6) — [US-6](US-6.md) | ✅ |
| 8 ekrāni | 7 | + Mans iesniegums; papildus MI palīgs (US-10) | ✅ 8 + MI palīgs |
| Lietojuma loģika: maršruti, validācija, numurs 2026-NNNN, statusu plūsma, filtri, aprēķini, POST → redirect → GET | ✅ | Tas pats princips arī MI un čata darbībām | ✅ |
| Dati: `temas`, `iesniegumi`, `notikumi` (statuss, komentārs, atbilde, mi_ieteikums) | 🟡 `mi_ieteikums` netika izmantots | MI ieteikums un tā izmantošana tiek pierakstīti `notikumi` ar lomu un laiku | ✅ |
| **MI komponents `ai.py`** | ❌ nav faila | `ai.py`: `ieteikums()` un `cata_atbilde()` | ✅ |
| US-7 tēma + atbildes projekts — minimāls risks; darbinieks rediģē, marķēts, žurnāls | ❌ | [US-7](US-7.md) | ✅ |
| US-10 čata palīgs — ierobežots risks; informē, ka tas ir MI (50. p.) | ❌ | `/palidzigs` — [US-10](US-10.md) | ✅ |
| US-15 prioritātes vērtējums — augsts risks; klasificē, NEBŪVĒ | ❌ nav klasifikācijas | Klasifikācija `docs/MI-RISKA-KLASIFIKACIJA.md` 5.2 — [US-15](US-15.md) | ✅ (nav būvēts) |
| GPAI API (Claude) vai atslēgvārdu imitācija, vienāds līgums | ❌ | Imitācija pēc noklusējuma; Claude API, ja ir `ANTHROPIC_API_KEY` (`AI_MODEL`); kļūda → imitācija | ✅ |
| Caurviju: pieejamība (EN 301 549 / WCAG 2.2 AA, MK 445, paziņojums) | 🟡 | Protokols un atradumi — [US-9](US-9.md) | ✅ (bez ekrānlasītāja testa) |
| Caurviju: MI akts — riska klase pirms izstrādes, marķējums, cilvēks apstiprina, žurnāls | ❌ | US-10 klasificēts pirms būvēšanas; marķējums, cilvēka apstiprinājums un žurnāls US-7 | ✅ |
| Caurviju: VDAR — minimāli dati, e-pasts tikai darbiniekam, testa dati izdomāti | ✅ | «Mans iesniegums» nerāda vārdu, e-pastu, iekšējos komentārus un MI žurnālu; uz API sūta tikai aprakstu vai jautājumu | ✅ |
| Vide: `tests/a11y_check.py` visas lapas | 🟡 tikai publiskās | `LOMA=` atbalsts ([S0.3](S0.3.md)) | ✅ |
| Vide: manuālie testi (tastatūra, 200 %, NVDA) | ❌ | Tastatūra un 200 % automatizēti; **NVDA nav veikts** | 🟡 |
| Vide: **git commit katrai vienībai** | ❌ | **Nav izdarīts** — commit netiek veikts bez lietotāja atļaujas | ❌ |
