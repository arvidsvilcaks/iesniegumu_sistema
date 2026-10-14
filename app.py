"""Iesniegumi — pašvaldības iesniegumu sistēma (mācību prototips, skat. BACKLOG.md)."""
import os
import re
import sqlite3
from datetime import datetime
from functools import wraps

from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for

import ai

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "macibu-uzdevums-nav-drosa-atslega")

LOMAS = {"iedzivotajs": "Iedzīvotājs", "darbinieks": "Darbinieks", "vaditajs": "Vadītājs", "sistema": "Sistēma"}
IZVELAMAS_LOMAS = ("iedzivotajs", "darbinieks", "vaditajs")
LOMAS_SAKUMLAPA = {"iedzivotajs": "iesniegt", "darbinieks": "saraksts", "vaditajs": "parskats"}

STATUSI = ["Jauns", "Apstrādē", "Atbildēts", "Noraidīts"]
STATUSA_PAREJAS = {"Jauns": ["Apstrādē"], "Apstrādē": ["Atbildēts", "Noraidīts"], "Atbildēts": [], "Noraidīts": []}
STATUSA_KLASE = {"Jauns": "jauns", "Apstrādē": "apstrade", "Atbildēts": "atbildets", "Noraidīts": "noraidits"}
NOTIKUMA_VEIDI = {"statuss": "Statuss", "komentars": "Komentārs", "atbilde": "Atbilde", "mi_ieteikums": "MI ieteikums"}

EPASTA_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NUMURA_RE = re.compile(r"^\d{4}-\d{4}$")
VIETTURA_RE = re.compile(r"\[[^\]\n]{1,60}\]")   # MI projekta vietturi, piem., [termiņš]

# Kājene un piekļūstamības paziņojums (3.2.6: palīdzība vienā vietā visās lapās). Izdomāti mācību dati.
KONTAKTI = {
    "iestade": "Novada pašvaldība",
    "talrunis": "+371 60 000 000",
    "epasts": "iesniegumi@novads.example.lv",
    "adrese": "Brīvības iela 1, Novads, LV-0000",
    "darba_laiks": "darba dienās 8.00–17.00",
}


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        # SQLite lower() nepazīst garumzīmes — meklēšanai izmanto Python
        g.db.create_function("lv_lower", 1, lambda s: s.lower() if s else "")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Tabulas, kas pievienotas pēc pirmās versijas — izveido arī esošā data.db, nezaudējot datus
MIGRACIJAS = """
CREATE TABLE IF NOT EXISTS mi_zurnals (
    id            INTEGER PRIMARY KEY,
    iesnieguma_id INTEGER NOT NULL REFERENCES iesniegumi(id) ON DELETE CASCADE,
    laiks         TEXT NOT NULL,
    loma          TEXT,
    darbiba       TEXT NOT NULL CHECK (darbiba IN ('ieteikums', 'izmantots', 'apstiprinats')),
    avots         TEXT,
    ieteikta_tema TEXT,
    redigets      INTEGER
);
"""


def init_db():
    """Izveido tabulas un sākumdatus, ja datubāzes vēl nav; esošai datubāzei piemēro migrācijas."""
    if os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as db:
            db.executescript(MIGRACIJAS)
        return
    with sqlite3.connect(DB_PATH) as db, open(SCHEMA_PATH, encoding="utf-8") as f:
        db.executescript(f.read())


def pieraksti_mi(db, iesnieguma_id, darbiba, avots=None, tema=None, redigets=None):
    db.execute(
        "INSERT INTO mi_zurnals (iesnieguma_id, laiks, loma, darbiba, avots, ieteikta_tema, redigets)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (iesnieguma_id, tagad(), session.get("loma"), darbiba, avots, tema, redigets),
    )


def tagad():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def pieraksti_notikumu(db, iesnieguma_id, veids, teksts, loma=None):
    db.execute(
        "INSERT INTO notikumi (iesnieguma_id, laiks, veids, loma, teksts) VALUES (?, ?, ?, ?, ?)",
        (iesnieguma_id, tagad(), veids, loma or session.get("loma"), teksts),
    )


def vajadziga_loma(*lomas):
    """Pieteikšanās nav — lomu pārbauda pēc sesijas."""
    def dekorators(f):
        @wraps(f)
        def ietvars(*args, **kwargs):
            if session.get("loma") not in lomas:
                return render_template("nav_piekluves.html", vajadzigas=[LOMAS[l] for l in lomas]), 403
            return f(*args, **kwargs)
        return ietvars
    return dekorators


@app.template_filter("datums")
def datums(vertiba):
    """2026-10-06 09:12 → 06.10.2026."""
    return datetime.strptime(vertiba[:10], "%Y-%m-%d").strftime("%d.%m.%Y.") if vertiba else ""


@app.template_filter("laiks")
def laiks(vertiba):
    """2026-10-06 09:12 → 06.10.2026. 09:12"""
    return datetime.strptime(vertiba[:16], "%Y-%m-%d %H:%M").strftime("%d.%m.%Y. %H:%M") if vertiba else ""


@app.template_filter("dienas")
def dienas(vertiba):
    if vertiba is None:
        return "nav datu"
    return f"{vertiba:.1f}".replace(".", ",") + " dienas"


@app.context_processor
def inject_globals():
    loma = session.get("loma")
    return {
        "loma": loma,
        "lomas_nosaukums": LOMAS.get(loma),
        "LOMAS": {k: LOMAS[k] for k in IZVELAMAS_LOMAS},
        "VISAS_LOMAS": LOMAS,
        "STATUSA_KLASE": STATUSA_KLASE,
        "NOTIKUMA_VEIDI": NOTIKUMA_VEIDI,
        "KONTAKTI": KONTAKTI,
        "MI_IESLEGTS": ai.ieslegts(),
    }


@app.route("/")
def index():
    temas = get_db().execute("SELECT id, nosaukums FROM temas ORDER BY nosaukums").fetchall()
    return render_template("index.html", temas=temas)


@app.post("/loma")
def izveleties_lomu():
    loma = request.form.get("loma")
    if loma not in IZVELAMAS_LOMAS:
        flash("Izvēlieties vienu no lomām.", "kluda")
        return redirect(url_for("index"))
    session["loma"] = loma
    flash(f"Izvēlētā loma: {LOMAS[loma]}.")
    return redirect(url_for(LOMAS_SAKUMLAPA[loma]))


# --- US-1: iesnieguma iesniegšana ---------------------------------------------

def validet_iesniegumu(dati, temu_id):
    """Atgriež {lauks: kļūdas teksts} lauku secībā (tā tās rāda kopsavilkumā)."""
    kludas = {}
    if not dati["vards"]:
        kludas["vards"] = "Ierakstiet vārdu un uzvārdu."
    elif len(dati["vards"]) > 100:
        kludas["vards"] = "Vārds un uzvārds nedrīkst būt garāks par 100 rakstzīmēm."
    if not dati["epasts"]:
        kludas["epasts"] = "Ierakstiet e-pasta adresi."
    elif not EPASTA_RE.match(dati["epasts"]) or len(dati["epasts"]) > 200:
        kludas["epasts"] = "Ierakstiet e-pasta adresi pareizā formātā, piemēram, vards@example.lv."
    if dati["tema"] not in temu_id:
        kludas["tema"] = "Izvēlieties iesnieguma tēmu."
    if len(dati["adrese"]) > 200:
        kludas["adrese"] = "Adrese nedrīkst būt garāka par 200 rakstzīmēm."
    if not dati["apraksts"]:
        kludas["apraksts"] = "Aprakstiet, par ko ir iesniegums."
    elif len(dati["apraksts"]) < 10:
        kludas["apraksts"] = "Aprakstam jābūt vismaz 10 rakstzīmes garam."
    elif len(dati["apraksts"]) > 2000:
        kludas["apraksts"] = "Apraksts nedrīkst būt garāks par 2000 rakstzīmēm."
    if not dati["piekrisana"]:
        kludas["piekrisana"] = "Lai iesniegtu iesniegumu, jāpiekrīt datu apstrādei."
    return kludas


def jauns_numurs(db):
    gads = datetime.now().year
    pedejais = db.execute(
        "SELECT MAX(CAST(substr(numurs, 6) AS INTEGER)) FROM iesniegumi WHERE numurs LIKE ?", (f"{gads}-%",)
    ).fetchone()[0] or 0
    return f"{gads}-{pedejais + 1:04d}"


@app.route("/iesniegt", methods=["GET", "POST"])
def iesniegt():
    db = get_db()
    temas = db.execute("SELECT id, nosaukums, apraksts FROM temas ORDER BY id").fetchall()
    dati = {"vards": "", "epasts": "", "tema": "", "adrese": "", "apraksts": "", "piekrisana": ""}
    kludas = {}

    if request.method == "POST":
        dati = {k: request.form.get(k, "").strip() for k in dati}
        kludas = validet_iesniegumu(dati, {str(t["id"]) for t in temas})
        if not kludas:
            numurs = jauns_numurs(db)
            laiks_tagad = tagad()
            cur = db.execute(
                "INSERT INTO iesniegumi (numurs, temas_id, vards, epasts, adrese, apraksts, izveidots, atjaunots)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (numurs, int(dati["tema"]), dati["vards"], dati["epasts"], dati["adrese"] or None,
                 dati["apraksts"], laiks_tagad, laiks_tagad),
            )
            pieraksti_notikumu(db, cur.lastrowid, "statuss", "Iesniegums reģistrēts ar statusu «Jauns».", "sistema")
            db.commit()
            # US-2: POST → redirect → GET; numuru nodod caur sesiju, ne URL
            session["pedejais_iesniegums"] = numurs
            return redirect(url_for("iesniegts"))

    return render_template("iesniegt.html", temas=temas, dati=dati, kludas=kludas), (400 if kludas else 200)


# --- US-2: apstiprinājums -------------------------------------------------------

@app.route("/iesniegts")
def iesniegts():
    numurs = session.get("pedejais_iesniegums")
    if not numurs:
        return redirect(url_for("iesniegt"))
    iesniegums = get_db().execute(
        "SELECT i.numurs, i.izveidots, t.nosaukums AS tema FROM iesniegumi i JOIN temas t ON t.id = i.temas_id"
        " WHERE i.numurs = ?", (numurs,)
    ).fetchone()
    if iesniegums is None:
        return redirect(url_for("iesniegt"))
    return render_template("iesniegts.html", iesniegums=iesniegums)


# --- US-3: iesniegumu saraksts --------------------------------------------------

@app.route("/saraksts")
@vajadziga_loma("darbinieks")
def saraksts():
    db = get_db()
    temas = db.execute("SELECT id, nosaukums FROM temas ORDER BY nosaukums").fetchall()
    filtri = {
        "statuss": request.args.get("statuss", ""),
        "tema": request.args.get("tema", ""),
        "q": request.args.get("q", "").strip(),
    }
    sql = ("SELECT i.numurs, i.izveidots, i.vards, i.statuss, t.nosaukums AS tema"
           " FROM iesniegumi i JOIN temas t ON t.id = i.temas_id WHERE 1 = 1")
    params = []
    if filtri["statuss"] in STATUSI:
        sql += " AND i.statuss = ?"
        params.append(filtri["statuss"])
    if filtri["tema"].isdigit():
        sql += " AND i.temas_id = ?"
        params.append(int(filtri["tema"]))
    if filtri["q"]:
        sql += (" AND instr(lv_lower(i.numurs || ' ' || i.vards || ' ' || coalesce(i.adrese, '') || ' ' || i.apraksts),"
                " ?) > 0")
        params.append(filtri["q"].lower())
    sql += " ORDER BY i.izveidots DESC"
    iesniegumi = db.execute(sql, params).fetchall()
    ir_filtri = any(filtri.values())
    return render_template("saraksts.html", iesniegumi=iesniegumi, temas=temas, statusi=STATUSI,
                           filtri=filtri, ir_filtri=ir_filtri)


# --- US-4: iesnieguma detaļas un apstrāde ---------------------------------------

def atrast_iesniegumu(numurs):
    iesniegums = get_db().execute(
        "SELECT i.*, t.nosaukums AS tema FROM iesniegumi i JOIN temas t ON t.id = i.temas_id WHERE i.numurs = ?",
        (numurs,),
    ).fetchone()
    if iesniegums is None:
        abort(404)
    return iesniegums


def raditi_detalas(iesniegums, kludas=None, ievade=None, statuss=200):
    notikumi = get_db().execute(
        "SELECT * FROM notikumi WHERE iesnieguma_id = ? ORDER BY laiks, id", (iesniegums["id"],)
    ).fetchall()
    numurs = iesniegums["numurs"]
    mi = session.get("mi") if session.get("mi", {}).get("numurs") == numurs else None
    melnraksts = session.get("mi_melnraksts") if session.get("mi_melnraksts", {}).get("numurs") == numurs else None
    ievade = dict(ievade or {})
    if melnraksts and "atbilde" not in ievade:
        ievade["atbilde"] = melnraksts["teksts"]
    return render_template(
        "detalas.html", i=iesniegums, notikumi=notikumi, parejas=STATUSA_PAREJAS[iesniegums["statuss"]],
        kludas=kludas or {}, ievade=ievade, mi=mi, ir_melnraksts=bool(melnraksts),
    ), statuss


@app.route("/iesniegumi/<numurs>")
@vajadziga_loma("darbinieks")
def detalas(numurs):
    return raditi_detalas(atrast_iesniegumu(numurs))


def uz_detalam(numurs):
    # Pēc darbības fokuss pāriet uz paziņojumu (#pazinojums), nevis pazūd lapas augšā
    return redirect(url_for("detalas", numurs=numurs) + "#pazinojums")


@app.post("/iesniegumi/<numurs>/statuss")
@vajadziga_loma("darbinieks")
def mainit_statusu(numurs):
    i = atrast_iesniegumu(numurs)
    jauns = request.form.get("statuss", "")
    if jauns not in STATUSA_PAREJAS[i["statuss"]]:
        return raditi_detalas(i, {"statuss": "Izvēlieties jauno statusu."}, statuss=400)
    if jauns == "Atbildēts" and not i["atbilde"]:
        return raditi_detalas(i, {"statuss": "Pirms statusa «Atbildēts» saglabājiet atbildi iedzīvotājam."}, statuss=400)
    db = get_db()
    laiks_tagad = tagad()
    pabeigts = laiks_tagad if jauns in ("Atbildēts", "Noraidīts") else None
    db.execute("UPDATE iesniegumi SET statuss = ?, atjaunots = ?, pabeigts = ? WHERE id = ?",
               (jauns, laiks_tagad, pabeigts, i["id"]))
    pieraksti_notikumu(db, i["id"], "statuss", f"Statuss mainīts no «{i['statuss']}» uz «{jauns}».")
    db.commit()
    flash(f"Statuss nomainīts uz «{jauns}».")
    return uz_detalam(numurs)


@app.post("/iesniegumi/<numurs>/komentars")
@vajadziga_loma("darbinieks")
def pievienot_komentaru(numurs):
    i = atrast_iesniegumu(numurs)
    teksts = request.form.get("komentars", "").strip()
    if not teksts:
        return raditi_detalas(i, {"komentars": "Ierakstiet komentāra tekstu."}, statuss=400)
    if len(teksts) > 2000:
        return raditi_detalas(i, {"komentars": "Komentārs nedrīkst būt garāks par 2000 rakstzīmēm."},
                              {"komentars": teksts}, 400)
    db = get_db()
    db.execute("UPDATE iesniegumi SET atjaunots = ? WHERE id = ?", (tagad(), i["id"]))
    pieraksti_notikumu(db, i["id"], "komentars", teksts)
    db.commit()
    flash("Komentārs pievienots vēsturei.")
    return uz_detalam(numurs)


@app.post("/iesniegumi/<numurs>/atbilde")
@vajadziga_loma("darbinieks")
def saglabat_atbildi(numurs):
    i = atrast_iesniegumu(numurs)
    teksts = request.form.get("atbilde", "").strip()
    if not teksts:
        return raditi_detalas(i, {"atbilde": "Ierakstiet atbildes tekstu."}, statuss=400)
    if len(teksts) > 5000:
        return raditi_detalas(i, {"atbilde": "Atbilde nedrīkst būt garāka par 5000 rakstzīmēm."},
                              {"atbilde": teksts}, 400)
    melnraksts = session.get("mi_melnraksts") if session.get("mi_melnraksts", {}).get("numurs") == numurs else None
    if melnraksts:
        # MI akts — cilvēka uzraudzība: MI projektu nevar saglabāt nepārbaudītu (obligāta rediģēšana)
        kludas = {}
        neaizpildits = VIETTURA_RE.findall(teksts)
        if neaizpildits:
            kludas["atbilde"] = (f"Atbildē ir neaizpildītas vietas kvadrātiekavās ({', '.join(neaizpildits[:3])}). "
                                 "Aizstājiet tās ar faktiem vai izdzēsiet.")
        if not request.form.get("mi_parbaudits"):
            kludas["mi_parbaudits"] = "Apliecinājiet, ka MI projekts ir pārbaudīts."
        if kludas:
            return raditi_detalas(i, kludas, {"atbilde": teksts}, 400)
    db = get_db()
    db.execute("UPDATE iesniegumi SET atbilde = ?, atjaunots = ? WHERE id = ?", (teksts, tagad(), i["id"]))
    pieraksti_notikumu(db, i["id"], "atbilde", teksts)
    if melnraksts:
        redigets = teksts != melnraksts["teksts"].strip()
        pieraksti_mi(db, i["id"], "apstiprinats", melnraksts.get("avots"), melnraksts.get("tema"), int(redigets))
        pieraksti_notikumu(db, i["id"], "mi_ieteikums",
                           "Darbinieks apliecināja pārbaudi un saglabāja atbildi, kas balstīta uz MI projektu "
                           f"({'rediģēta' if redigets else 'nemainīta'}).")
        session.pop("mi_melnraksts")
    db.commit()
    flash("Atbilde saglabāta.")
    return uz_detalam(numurs)


# --- US-7: MI ieteikums darbiniekam ----------------------------------------------

@app.post("/iesniegumi/<numurs>/mi")
@vajadziga_loma("darbinieks")
def mi_ieteikums(numurs):
    i = atrast_iesniegumu(numurs)
    if not ai.ieslegts():
        flash("MI ieteikumi ir izslēgti.", "kluda")
        return uz_detalam(numurs)
    rezultats = ai.ieteikums(i["apraksts"])
    session["mi"] = {"numurs": numurs, **rezultats}
    db = get_db()
    pieraksti_notikumu(db, i["id"], "mi_ieteikums",
                       f"Saņemts MI ieteikums (avots: {rezultats['avots']}); ieteiktā tēma «{rezultats['tema']}».")
    pieraksti_mi(db, i["id"], "ieteikums", rezultats["avots"], rezultats["tema"])
    db.commit()
    return redirect(url_for("detalas", numurs=numurs) + "#mi-virsraksts")


@app.post("/iesniegumi/<numurs>/mi/izmantot")
@vajadziga_loma("darbinieks")
def mi_izmantot(numurs):
    """Ievieto MI projektu atbildes laukā rediģēšanai. Nekas netiek saglabāts kā atbilde."""
    i = atrast_iesniegumu(numurs)
    mi = session.get("mi")
    if not ai.ieslegts() or not mi or mi.get("numurs") != numurs:
        flash("MI ieteikums vairs nav pieejams. Saņemiet jaunu ieteikumu.", "kluda")
        return uz_detalam(numurs)
    session["mi_melnraksts"] = {"numurs": numurs, "teksts": mi["atbildes_projekts"], "avots": mi["avots"],
                                "tema": mi["tema"]}
    db = get_db()
    pieraksti_notikumu(db, i["id"], "mi_ieteikums",
                       "MI atbildes projekts ievietots atbildes laukā rediģēšanai (vēl nav saglabāts).")
    pieraksti_mi(db, i["id"], "izmantots", mi["avots"], mi["tema"])
    db.commit()
    flash("MI projekts ievietots laukā «Atbildes teksts». Tas vēl nav saglabāts — pārbaudiet, rediģējiet "
          "un nospiediet «Saglabāt atbildi».")
    return uz_detalam(numurs)


# --- US-8: mans iesniegums ------------------------------------------------------

@app.route("/mans-iesniegums")
def mans_iesniegums():
    numurs = request.args.get("numurs", "").strip()
    kluda, iesniegums, pedejais = None, None, None
    if "numurs" in request.args:
        if not numurs:
            kluda = "Ierakstiet iesnieguma numuru."
        elif not NUMURA_RE.match(numurs):
            kluda = "Ierakstiet numuru formā GGGG-NNNN, piemēram, 2026-0001."
        else:
            db = get_db()
            iesniegums = db.execute(
                "SELECT i.id, i.numurs, i.statuss, i.atbilde, i.izveidots, t.nosaukums AS tema"
                " FROM iesniegumi i JOIN temas t ON t.id = i.temas_id WHERE i.numurs = ?", (numurs,)
            ).fetchone()
            if iesniegums is None:
                kluda = f"Iesniegums ar numuru {numurs} nav atrasts. Pārbaudiet numuru apstiprinājuma lapā."
            else:
                # Iedzīvotājam rāda tikai statusa notikumus — ne iekšējos komentārus, ne MI žurnālu
                pedejais = db.execute(
                    "SELECT laiks, teksts FROM notikumi WHERE iesnieguma_id = ? AND veids = 'statuss'"
                    " ORDER BY laiks DESC, id DESC LIMIT 1", (iesniegums["id"],)
                ).fetchone()
    return render_template("mans_iesniegums.html", numurs=numurs, kluda=kluda, i=iesniegums,
                           pedejais=pedejais), (400 if kluda else 200)


# --- US-10: čata palīgs iedzīvotājam --------------------------------------------

CATA_GARUMS = 6  # sesija ir sīkdatnē — glabā tikai pēdējos ierakstus


@app.route("/palidzigs", methods=["GET", "POST"])
def palidzigs():
    kluda = None
    if not ai.ieslegts():
        return render_template("palidzigs.html", cats=[], kluda=None, jautajums=""), (403 if request.method == "POST" else 200)
    if request.method == "POST":
        if request.form.get("darbiba") == "notirit":
            session.pop("cats", None)
            flash("Saruna notīrīta.")
            return redirect(url_for("palidzigs"))
        jautajums = request.form.get("jautajums", "").strip()
        if not jautajums:
            kluda = "Ierakstiet jautājumu."
        elif len(jautajums) > 500:
            kluda = "Jautājums nedrīkst būt garāks par 500 rakstzīmēm."
        else:
            atbilde = ai.cata_atbilde(jautajums)
            cats = session.get("cats", []) + [
                {"kas": "lietotajs", "teksts": jautajums},
                {"kas": "mi", "teksts": atbilde["atbilde"], "avots": atbilde["avots"]},
            ]
            session["cats"] = cats[-CATA_GARUMS:]
            return redirect(url_for("palidzigs") + "#pedeja-atbilde")
    return render_template("palidzigs.html", cats=session.get("cats", []), kluda=kluda,
                           jautajums=request.form.get("jautajums", "")), (400 if kluda else 200)


# --- US-5: pārskats vadītājam ---------------------------------------------------

@app.route("/parskats")
@vajadziga_loma("vaditajs")
def parskats():
    db = get_db()
    skaits = dict(db.execute("SELECT statuss, COUNT(*) FROM iesniegumi GROUP BY statuss").fetchall())
    pa_statusiem = [{"statuss": s, "skaits": skaits.get(s, 0)} for s in STATUSI]
    pa_temam = db.execute(
        "SELECT t.nosaukums, COUNT(i.id) AS skaits,"
        " AVG(julianday(i.pabeigts) - julianday(i.izveidots)) AS vid_dienas"
        " FROM temas t LEFT JOIN iesniegumi i ON i.temas_id = t.id"
        " GROUP BY t.id ORDER BY t.nosaukums"
    ).fetchall()
    kopa = db.execute(
        "SELECT COUNT(*) AS visi, COUNT(pabeigts) AS pabeigti,"
        " AVG(julianday(pabeigts) - julianday(izveidots)) AS vid_dienas FROM iesniegumi"
    ).fetchone()
    lielakais = max((r["skaits"] for r in pa_temam), default=0) or 1
    # MI uzraudzība (US-7 pasākums «kvalitātes izlases pārbaude reizi mēnesī»)
    mi_kopa = db.execute(
        "SELECT SUM(m.darbiba = 'ieteikums') AS ieteikumi, SUM(m.darbiba = 'izmantots') AS izmantoti,"
        " SUM(m.darbiba = 'apstiprinats') AS apstiprinati, SUM(m.darbiba = 'apstiprinats' AND m.redigets = 1) AS redigeti,"
        " SUM(m.darbiba = 'ieteikums' AND m.ieteikta_tema <> t.nosaukums) AS tema_atskiras"
        " FROM mi_zurnals m JOIN iesniegumi i ON i.id = m.iesnieguma_id JOIN temas t ON t.id = i.temas_id"
        " WHERE m.laiks >= datetime('now', 'localtime', '-30 days')"
    ).fetchone()
    mi_izlase = db.execute(
        "SELECT i.numurs, m.laiks, m.avots, m.ieteikta_tema, t.nosaukums AS tema, m.redigets, i.atbilde"
        " FROM mi_zurnals m JOIN iesniegumi i ON i.id = m.iesnieguma_id JOIN temas t ON t.id = i.temas_id"
        " WHERE m.darbiba = 'apstiprinats' AND m.laiks >= datetime('now', 'localtime', '-30 days')"
        " ORDER BY m.laiks DESC LIMIT 20"
    ).fetchall()
    return render_template("parskats.html", pa_statusiem=pa_statusiem, pa_temam=pa_temam, kopa=kopa,
                           lielakais=lielakais, mi_kopa=mi_kopa, mi_izlase=mi_izlase)


# --- US-6: piekļūstamības paziņojums --------------------------------------------

@app.route("/pieklustamiba")
def pieklustamiba():
    # Saturu papildina pēc testēšanas (veidne docs/PIEEJAMIBAS-PRASIBAS.md, 5. sadaļa)
    return render_template("pieklustamiba.html")


@app.errorhandler(404)
def nav_atrasts(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
