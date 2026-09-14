# -*- coding: utf-8 -*-
import re, unicodedata
from datetime import date, timedelta

MONTHS = ["", "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
          "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

ACCENT = {
    "music": "#B0C400", "cities": "#E6008A",
    "society": "#34A853", "ideas": "#6C4FE0", "interviews": "#FF96DE",
}
CATLABEL = {"music": "Music", "cities": "Cities", "society": "Society", "ideas": "Ideas", "interviews": "Interviews"}

AUTHORS = {
    "music": ["Chiara Ferretti", "Nadia Colombo", "Yusuf Demir"],
    "cities": ["Marco Divella", "Giulia Conte", "Tommaso Reali"],
    "society": ["Aisha Kone", "Sofia Lindqvist", "Omar El-Sayed"],
    "ideas": ["Leonardo Sacco", "Priya Nair", "Anton Weiss"],
}

BANK_P = {
    "music": [
        "La scena musicale europea continua a produrre format ibridi, in cui la componente sonora si intreccia sempre più con l'architettura degli spazi e con pratiche di comunità che superano il semplice ascolto.",
        "Le etichette indipendenti giocano un ruolo chiave in questo processo: distribuiscono risorse, competenze e reti di contatti a realtà che altrimenti resterebbero isolate, contribuendo a una scena più orizzontale.",
        "Non è un caso che molte delle innovazioni più interessanti arrivino da contesti periferici, dove il costo degli spazi permette sperimentazioni che nei centri urbani sarebbero economicamente insostenibili.",
    ],
    "cities": [
        "Il tema della rigenerazione urbana continua a dividere amministrazioni, cittadini e investitori, in un equilibrio delicato tra tutela della memoria industriale e necessità di nuove funzioni per gli spazi dismessi.",
        "Le esperienze più solide condividono un tratto comune: la partecipazione reale degli abitanti nella definizione degli usi, non solo nella fase di consultazione ma in quella di gestione quotidiana degli spazi.",
        "Resta il nodo della sostenibilità economica nel lungo periodo, che spesso costringe i progetti più radicali a scendere a compromessi con logiche di mercato.",
    ],
    "society": [
        "Le nuove forme di comunità che si osservano oggi nascono spesso dall'incrocio tra pratiche digitali e bisogno di prossimità fisica, in un equilibrio che le istituzioni faticano ancora a comprendere fino in fondo.",
        "Il rapporto tra visibilità mediatica e radicalità politica resta un nodo irrisolto per molti dei collettivi emergenti, spesso costretti a scegliere tra crescere e restare fedeli alla propria identità originaria.",
        "Osservare questi fenomeni richiede categorie nuove, capaci di uscire dagli schemi novecenteschi con cui siamo abituati a leggere i movimenti sociali.",
    ],
    "ideas": [
        "Il dibattito filosofico contemporaneo si trova sempre più spesso a dover rispondere a domande poste dalla tecnologia, prima ancora di aver risolto quelle ereditate dal Novecento.",
        "Molti pensatori invitano a diffidare tanto dell'entusiasmo acritico quanto del rifiuto totale: la via più feconda sembra essere quella di una critica che resti dentro i fenomeni che analizza.",
        "Le università e i centri di ricerca indipendenti giocano un ruolo sempre più importante nel tradurre questi dibattiti in un linguaggio accessibile a un pubblico più ampio.",
    ],
}

BANK_Q = {
    "music": [("La musica dal vivo resta l'unico luogo in cui una comunità si forma nello stesso istante in cui ascolta.", "Elena Ricci, curatrice musicale"),
              ("Non produciamo più dischi. Produciamo occasioni per stare insieme.", "Sam Delacroix, produttore")],
    "cities": [("Una città rigenerata bene si riconosce da chi continua a viverci, non da chi viene a fotografarla.", "Paolo Serra, urbanista"),
               ("Lo spazio pubblico è il primo indicatore della salute democratica di una città.", "Ines Duarte, architetta")],
    "society": [("Una comunità non si misura da quante persone ne fanno parte, ma da quante decisioni prende insieme.", "Sara Boujemaa, ricercatrice sociale"),
                ("Il conflitto, se ben gestito, è la forma più alta di cura di una comunità.", "David Ochoa, mediatore culturale")],
    "ideas": [("Pensare oggi significa soprattutto resistere alla tentazione di semplificare.", "Marta Hoffmann, filosofa"),
              ("Ogni nuova tecnologia ci costringe a riscrivere, almeno in parte, la domanda su cosa significhi essere umani.", "Julian Vance, teorico dei media")],
}

BANK_CLOSE = {
    "music": "Resta da vedere se queste pratiche riusciranno a strutturarsi in un modello economico stabile, o se continueranno a vivere ai margini, cambiando comunque, nel loro piccolo, il modo in cui pensiamo alla musica dal vivo.",
    "cities": "Il confronto tra queste esperienze suggerisce che non esiste un modello universale di rigenerazione: ogni intervento riuscito nasce da un equilibrio specifico tra contesto locale, tempi lunghi e volontà politica.",
    "society": "Che si tratti di energia, cura o consumo, il filo che lega queste esperienze è lo stesso: la ricerca di forme di autonomia collettiva in un momento storico che sembra spingere nella direzione opposta.",
    "ideas": "Non si tratta di trovare risposte definitive, quanto di tenere aperte domande che rischiano altrimenti di essere risolte troppo in fretta, con conseguenze pratiche non banali.",
}

NEW_ARTICLES = [
    # MUSIC (11)
    ("Radio indipendenti: la rinascita di un formato che sembrava morto", "Decine di piccole radio indipendenti stanno ricostruendo le scene musicali locali, una trasmissione alla volta.", "music"),
    ("Il ritorno del vinile nei quartieri periferici", "Negozi di dischi indipendenti aprono lontano dai centri storici, seguendo il pubblico più che il turismo.", "music"),
    ("Cori popolari: la coralità come pratica politica", "In diverse città europee i cori amatoriali tornano a essere spazi di aggregazione intergenerazionale.", "music"),
    ("Studi condivisi: il nuovo modello economico dei musicisti emergenti", "Sale prova e studi di registrazione gestiti in cooperativa riducono i costi d'ingresso per una nuova generazione di artisti.", "music"),
    ("Musica e migrazione: le scene sonore delle seconde generazioni", "Un viaggio tra i suoni che nascono all'incrocio tra tradizioni familiari e cultura urbana europea.", "music"),
    ("Il festival che non vende biglietti", "Un modello a donazione libera sta mettendo in discussione l'economia tradizionale degli eventi musicali.", "music"),
    ("Sale prova pubbliche: quando il Comune investe nella musica dal vivo", "Diverse amministrazioni locali finanziano spazi prova gratuiti per band emergenti.", "music"),
    ("Dentro il collettivo che produce colonne sonore per spazi pubblici", "Un gruppo di compositori progetta paesaggi sonori per parchi, stazioni e piazze.", "music"),
    ("La techno minimale torna nei centri sociali", "Un ritorno alle origini per una scena che negli ultimi anni si era spostata verso i grandi club commerciali.", "music"),
    ("Cantautorato e crisi abitativa: le nuove canzoni sulla casa", "Una generazione di cantautori scrive canzoni sul tema dell'abitare, tra sfratti e affitti brevi.", "music"),
    ("Le orchestre di quartiere: musica classica fuori dai teatri", "Piccole formazioni orchestrali portano il repertorio classico in cortili e biblioteche di quartiere.", "music"),
    # CITIES (11)
    ("Il quartiere che si è ricostruito attorno a una biblioteca", "A Rotterdam, un progetto di rigenerazione ha messo la lettura pubblica al centro della rinascita urbana.", "cities"),
    ("Superblocchi: il modello di Barcellona arriva in Italia", "Alcune città italiane sperimentano la pedonalizzazione a isolati per ridurre traffico e restituire spazio ai residenti.", "cities"),
    ("Le cooperative di abitanti che comprano i propri palazzi", "Un modello di proprietà collettiva prova a rispondere alla crisi degli affitti nei centri urbani.", "cities"),
    ("Tetti verdi e agricoltura urbana: Milano ripensa i cortili", "Una rete di cortili condominiali si trasforma in orti collettivi gestiti dai residenti.", "cities"),
    ("La stazione abbandonata diventata centro culturale", "Un ex scalo ferroviario a Bologna ospita oggi residenze artistiche e laboratori per il quartiere.", "cities"),
    ("Urbanistica tattica: interventi temporanei che cambiano le città per sempre", "Piccoli interventi reversibili stanno diventando lo strumento preferito di molte amministrazioni progressiste.", "cities"),
    ("Il porto industriale che è diventato un parco pubblico", "Ad Amburgo, la riconversione dell'area portuale mostra i limiti e i pregi della rigenerazione guidata da capitali privati.", "cities"),
    ("Chi decide il futuro di una piazza? Il caso di Napoli", "Un processo di progettazione partecipata coinvolge per mesi i residenti di un quartiere popolare.", "cities"),
    ("Le città dei 15 minuti, cinque anni dopo", "Un bilancio del modello urbanistico che promette servizi essenziali a distanza pedonale per tutti.", "cities"),
    ("Gentrificazione culturale: quando l'arte diventa un problema", "Le gallerie che animano un quartiere sono spesso le prime a doverlo lasciare, una volta rivalutato.", "cities"),
    ("Il mercato coperto che ha salvato un centro storico", "In una piccola città spagnola, la riapertura del mercato ha invertito lo spopolamento del centro.", "cities"),
    # SOCIETY (10)
    ("Le case del popolo del 2026: cosa resta del mutualismo", "Un viaggio tra le realtà che ancora oggi applicano i principi del mutuo soccorso ottocentesco.", "society"),
    ("Reti di cura: chi si prende cura di chi si prende cura", "Un'inchiesta sulle comunità informali che sostengono caregiver e operatori sociali.", "society"),
    ("Le nuove cooperative di consumo critico", "Gruppi di acquisto solidale si trasformano in vere e proprie reti economiche alternative.", "society"),
    ("Comunità energetiche: quando il quartiere produce la propria energia", "Decine di condomini italiani si organizzano per produrre e condividere energia rinnovabile.", "society"),
    ("Il collettivo che ripara oggetti invece di comprarne di nuovi", "Le repair cafe si moltiplicano come risposta pratica alla cultura dello scarto.", "society"),
    ("Genitorialità condivisa: le nuove reti di supporto tra famiglie", "In diverse città nascono gruppi informali che si scambiano tempo, spazi e competenze educative.", "society"),
    ("Le biblioteche di oggetti: possedere meno, condividere di più", "Dagli attrezzi da giardinaggio ai trapani, cresce il numero di biblioteche che prestano oggetti invece di libri.", "society"),
    ("Dentro un'assemblea di quartiere che decide davvero", "Un caso studio su un processo di bilancio partecipativo che ha coinvolto migliaia di residenti.", "society"),
    ("La nuova ondata di sindacalismo tra i lavoratori delle piattaforme", "Rider e lavoratori digitali si organizzano con strumenti presi in prestito dal sindacalismo tradizionale.", "society"),
    ("Comunità queer e spazio pubblico: una mappa in evoluzione", "Come cambiano i luoghi di ritrovo delle comunità LGBTQ+ nelle città europee.", "society"),
    # IDEAS (10)
    ("Decrescita, ancora: un'idea che non tramonta mai", "Perché il dibattito sulla decrescita continua a tornare, nonostante decenni di critiche.", "ideas"),
    ("Filosofia dello spreco: cosa dicono i rifiuti di una società", "Un percorso tra estetica, etica e gestione dei rifiuti nella città contemporanea.", "ideas"),
    ("Il tempo libero come campo di battaglia politico", "Come cambia il significato del tempo libero in una società always-on.", "ideas"),
    ("Postcolonialismo e musei: chi racconta la storia?", "Il dibattito sulla restituzione dei reperti coloniali arriva anche nei piccoli musei locali.", "ideas"),
    ("L'etica della lentezza in un mondo accelerato", "Filosofi e sociologi tornano a interrogarsi sul valore politico della lentezza.", "ideas"),
    ("Cosa significa ancora 'pubblico' nell'era delle piattaforme", "Una riflessione sul confine sempre più sottile tra spazio pubblico e spazio privato digitale.", "ideas"),
    ("L'immaginazione politica dopo la fine delle utopie", "Perché la capacità di immaginare futuri alternativi resta una risorsa scarsa e preziosa.", "ideas"),
    ("Estetica della riparazione: quando il difetto diventa valore", "Dal kintsugi giapponese alle pratiche contemporanee di riuso creativo.", "ideas"),
    ("Democrazia diretta e tecnologia: un matrimonio possibile?", "Diverse città sperimentano piattaforme digitali per il voto deliberativo locale.", "ideas"),
    ("Filosofia del confine: chi decide chi appartiene a un luogo", "Un percorso teorico tra cittadinanza, appartenenza e nuovi movimenti migratori.", "ideas"),
]

def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    return re.sub(r"[\s-]+", "-", text)

def fmt_date(d):
    return "{} {} {}".format(d.day, MONTHS[d.month], d.year)

# assign dates: start just before the existing oldest new-batch anchor, step back 3 days
start = date(2026, 6, 21)
cat_counters = {"music": 0, "cities": 0, "society": 0, "ideas": 0}
new_data = []
for i, (title, subtitle, cat) in enumerate(NEW_ARTICLES):
    d = start - timedelta(days=3 * i)
    author = AUTHORS[cat][cat_counters[cat] % len(AUTHORS[cat])]
    cat_counters[cat] += 1
    slug = cat + "-" + slugify(title)[:60].rstrip("-")
    new_data.append({
        "slug": slug, "title": title, "desc": subtitle, "category": cat,
        "author": author, "date": d,
    })

EXISTING = [
    {"slug": "music-festival-elettronica", "title": "Le nuove frontiere del suono: dentro i festival che reinventano la scena elettronica europea",
     "desc": "Spazi industriali riconquistati, comunità temporanee e nuove estetiche del suono.", "category": "music",
     "author": "Chiara Ferretti", "date": date(2026, 7, 8)},
    {"slug": "cities-torino-rigenerazione", "title": "Rigenerazione urbana a Torino: come un'ex fabbrica è diventata laboratorio di comunità",
     "desc": "Un caso studio di architettura sociale nato da un'occupazione, oggi regolarizzata.", "category": "cities",
     "author": "Marco Divella", "date": date(2026, 7, 6)},
    {"slug": "society-controculture-2026", "title": "Controculture 2026: chi sono i nuovi collettivi che riscrivono le regole",
     "desc": "Tra spazi autogestiti, nuovi linguaggi visivi e comunità digitali strutturate.", "category": "society",
     "author": "Aisha Kone", "date": date(2026, 7, 4)},
    {"slug": "ideas-filosofia-algoritmo", "title": "Filosofia e algoritmo: può un'intelligenza artificiale avere un'estetica?",
     "desc": "Un percorso tra teoria del gusto, machine learning e nuovi movimenti del pensiero.", "category": "ideas",
     "author": "Leonardo Sacco", "date": date(2026, 7, 2)},
    {"slug": "music-architetture-sonore", "title": "Architetture sonore: quando la musica diventa spazio pubblico",
     "desc": "Installazioni sonore permanenti e il nuovo dialogo tra composizione e architettura urbana.", "category": "music",
     "author": "Chiara Ferretti", "date": date(2026, 6, 29)},
    {"slug": "cities-berlino-lisbona-napoli", "title": "Berlino, Lisbona, Napoli: tre città, tre modelli di rigenerazione dal basso",
     "desc": "Un confronto tra approcci diversi alla cultura come motore di trasformazione urbana.", "category": "cities",
     "author": "Marco Divella", "date": date(2026, 6, 25)},
]

# Real, hand-written articles (unique href — NOT routed to the shared
# placeholder template like the demo content below).
REAL_ARTICLES = [
    {"slug": "ideas-demoralizzazione-arma-di-guerra",
     "title": "LA DEMORALIZZAZIONE COME ARMA DI GUERRA",
     "desc": "La guerra invisibile per il controllo della cultura.",
     "category": "ideas", "author": "Thomas Anderson", "date": date(2026, 7, 20),
     "href": "articles/ideas-demoralizzazione-arma-di-guerra.html",
     "image": "articles/demoralizzazione-italia-1963.jpg"},
    {"slug": "society-tempio-futuro-perduto",
     "title": "LA RIVOLUZIONE DEL CLUBBING ITALIANO: IL TEMPIO DI MILANO",
     "desc": "Come un'ex officina tranviaria abbandonata è diventata una delle comunità culturali indipendenti più estese d'Italia.",
     "category": "society", "author": "Anna Maria Rita dall'Ongaro", "date": date(2026, 7, 28),
     "href": "articles/society-tempio-futuro-perduto.html",
     "image": "articles/tempio-1.jpg"},
    {"slug": "society-musica-finta-scena-italiana",
     "title": "LA MUSICA FATTA CON L'AI È FINTA COME LA SCENA ITALIANA DI OGGI",
     "desc": "L'Italia musicale del 2026 sembra un gigantesco talent permanente per persone che odiano la musica.",
     "category": "society", "author": "Thomas Anderson", "date": date(2026, 7, 28),
     "href": "articles/society-musica-finta-scena-italiana.html",
     "image": "articles/musica-2026-delia.jpg"},
    {"slug": "ideas-forza-carattere-estetica",
     "title": "LA FORZA DEL CARATTERE HA LASCIATO POSTO ALL'ESTETICA",
     "desc": "Una civiltà che sostituisce la costruzione del carattere con la costruzione dell'immagine, produce individui dipendenti dalla validazione esterna.",
     "category": "ideas", "author": "Diogene di Sinope", "date": date(2026, 7, 29),
     "href": "articles/ideas-forza-carattere-estetica.html",
     "image": "articles/estetica-1-pubblicita-universita.jpg"},
    {"slug": "music-scuola-della-techno",
     "title": "LA PRIMA SCUOLA DELLA TECHNO AL MONDO È IN ITALIA",
     "desc": "Da Milano un progetto unico: migliaia di studenti, lezioni gratuite, ricerca culturale, workshop con artisti internazionali e un'idea radicale che trasforma la musica elettronica da semplice intrattenimento a patrimonio culturale.",
     "category": "music", "author": "Ada Scielbi", "date": date(2026, 7, 30),
     "href": "articles/music-scuola-della-techno.html",
     "image": "articles/scuola-techno-1-studio.jpg"},
    {"slug": "society-centri-sociali-italiani-morti",
     "title": "I CENTRI SOCIALI ITALIANI SONO MORTI. QUALCUNO AVREBBE DOVUTO DIRLO.",
     "desc": "Dal G8 di Genova a Macao, dal Leoncavallo al Tempio del Futuro Perduto: cosa resta oggi del movimento che per trent'anni ha rappresentato la resistenza politica e culturale italiana.",
     "category": "society", "author": "Diogene di Sinope", "date": date(2026, 7, 31),
     "href": "articles/society-centri-sociali-italiani-morti.html",
     "image": "articles/centri-sociali-2-sardone-macao.jpg"},
    {"slug": "music-italo-ghetto",
     "title": "SULLA TECHNO ORA SI CANTA IN ITALIANO. È UN NUOVO GENERE: SI CHIAMA ITALO GHETTO.",
     "desc": "Dopo quarant'anni di nostalgia e importazione di suoni stranieri, una nuova scena prova a costruire un linguaggio techno interamente italiano: dialetti, cantautorato, cultura rave e immaginario popolare dentro il dancefloor.",
     "category": "music", "author": "Mattia Losy", "date": date(2026, 8, 1),
     "href": "articles/music-italo-ghetto.html",
     "image": "articles/italo-ghetto-2-not-just-disco.jpg"},
    {"slug": "ideas-sinistra-reel-caroselli",
     "title": "LA SINISTRA ERA IL POPOLO DEI LIBRI E DELLA MILITANZA. OGGI È IL PUBBLICO DI REEL E CAROSELLI.",
     "desc": "Dalle riviste ai podcast, dagli avvocati social alle attiviste-brand: la sinistra ha sostituito il pensiero politico con contenuti rassicuranti, indignazioni seriali e carriere individuali perfettamente integrate nell'establishment.",
     "category": "ideas", "author": "Diogene di Sinope", "date": date(2026, 8, 2),
     "href": "articles/ideas-sinistra-reel-caroselli.html",
     "image": "articles/sinistra-reel-1-copertina-ai.png"},
    {"slug": "cities-sicurezza-milano-meme-elettorale",
     "title": "I PROBLEMI DI SICUREZZA DI MILANO NON SONO UN MEME ELETTORALE. E FORSE STIAMO GUARDANDO NELLA DIREZIONE SBAGLIATA.",
     "desc": "Tra Ministero dell'Interno, Prefetto, Comune e Commissione Sicurezza: chi ha davvero la responsabilità della sicurezza urbana a Milano, oltre lo slogan social contro il sindaco.",
     "category": "cities", "author": "Vincenzina da Porta Venezia", "date": date(2026, 8, 3),
     "href": "articles/cities-sicurezza-milano-meme-elettorale.html",
     "image": "articles/sicurezza-milano-4-tensione-milanoinmovimento.jpg"},
    {"slug": "interviews-oriental-techno-club-intervista",
     "title": "IL PRIMO CLUB ELETTRONICO 100% ASIATICO IN EUROPA: ORIENTAL TECHNO CLUB A MILANO",
     "desc": "Intervista al collettivo che ha trasformato la cultura elettronica asiatica in un ponte reale tra Asia ed Europa, tra musica, arti visive, performance e ritualità.",
     "category": "interviews", "author": "Anna Maria Rita dall'Ongaro", "date": date(2026, 8, 4),
     "href": "articles/interviews-oriental-techno-club-intervista.html",
     "image": "articles/otc-1-muro-nuta-sokol.jpg"},
    {"slug": "interviews-dolce-potente-intervista",
     "title": "DALLA PUGLIA, DA SOLA, IN AUTOBUS, INSEGUENDO UN SOGNO: INTERVISTA A DOLCE POTENTE",
     "desc": "Partendo dai quartieri popolari di Bari per arrivare ai recenti tour in Cina, in Europa e in Italia. Dolce Potente è ogni giorno di più un punto di riferimento per la nuova scena techno italiana.",
     "category": "interviews", "author": "Thomas Anderson", "date": date(2026, 8, 5),
     "href": "articles/interviews-dolce-potente-intervista.html",
     "image": "articles/dolce-potente-5-shanghai-2025.jpg"},
    {"slug": "ideas-festival-lunapark-territorio",
     "title": "FESTIVAL MODERNI, LUNAPARK IN DECLINO O RISORSE PER IL TERRITORIO?",
     "desc": "Una riflessione sulla proprietà dei grandi festival musicali europei, lo sfruttamento del territorio che li ospita e il provincialismo culturale italiano.",
     "category": "ideas", "author": "Francis Tutti", "date": date(2026, 8, 6),
     "href": "articles/ideas-festival-lunapark-territorio.html",
     "image": "articles/festival-territorio-1-persone-riunite.jpg"},
    {"slug": "interviews-elisa-bee-intervista",
     "title": "DALLA SARDEGNA AL BERGHAIN, PASSANDO PER IL TEMPIO: INTERVISTA A ELISA BEE",
     "desc": "Dalle prime serate in Sardegna ai dancefloor più prestigiosi d'Europa, fino al percorso artistico e umano che l'ha portata a diventare una delle figure più riconoscibili della nuova scena techno europea.",
     "category": "interviews", "author": "Mattia Losy", "date": date(2026, 8, 7),
     "href": "articles/interviews-elisa-bee-intervista.html",
     "image": "articles/elisa-bee-1-cimitero-monumentale.jpg"},
    {"slug": "ideas-discoteche-non-fanno-club-culture",
     "title": "LE DISCOTECHE COMMERCIALI NON FANNO CLUB CULTURE",
     "desc": "La crisi delle grandi discoteche commerciali non è un fenomeno passeggero, ma il sintomo dell'esaurimento di un modello economico e culturale che oggi tenta di rigenerarsi appropriandosi del clubbing, della techno e dell'hard techno.",
     "category": "ideas", "author": "Francesca Mondragone", "date": date(2026, 8, 8),
     "href": "articles/ideas-discoteche-non-fanno-club-culture.html",
     "image": "articles/discoteche-club-culture-1-bottiglie.jpg"},
]

# Only real articles appear on the site now (demo content retired).
ALL = list(REAL_ARTICLES)
ALL.sort(key=lambda a: a["date"], reverse=True)

ARTICLE_TEMPLATE = '''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — INTERFERENCE</title>
<meta name="description" content="{desc}">

<!-- Open Graph -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="INTERFERENCE">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://picsum.photos/seed/{slug}/1200/630">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://www.interferencemag.com/articles/{slug}.html">
<meta property="article:author" content="{author}">
<meta property="article:section" content="{catlabel}">
<meta property="article:published_time" content="{iso_date}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://picsum.photos/seed/{slug}/1200/630">

<link rel="stylesheet" href="../style.css">
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <div class="logo logo-small"><a href="../index.html"><img src="../logo.png" alt="INTERFERENCES"></a></div>
    <button class="filter-pill dfree-toggle" id="dfree-toggle">distraction free</button>
  </div>
</header>

<a class="article-back" href="../index.html">← Tutti i contenuti</a>

<div class="article-hero">
  <img src="https://picsum.photos/seed/{slug}/1600/900" alt="{title}">
</div>

<div class="article-head">
  <span class="article-category {category}">{catlabel}</span>
  <h1 class="article-title">{title}</h1>
  <p class="article-subtitle">{desc}</p>

  <div class="article-byline">
    <div>
      <div class="article-author">{author}</div>
      <div class="article-date">{display_date}</div>
    </div>
    <div class="share-bar">
      <button class="share-btn" title="WhatsApp" aria-label="Condividi su WhatsApp" onclick="shareArticle('whatsapp')"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12c0 1.85.5 3.58 1.36 5.07L2 22l5.06-1.33A9.94 9.94 0 0012 22c5.52 0 10-4.48 10-10S17.52 2 12 2zm5.2 14.2c-.22.62-1.28 1.18-1.77 1.24-.45.06-1.02.09-1.65-.1-.38-.12-.87-.28-1.5-.55-2.64-1.14-4.36-3.8-4.5-3.98-.13-.18-1.08-1.44-1.08-2.74 0-1.3.68-1.94.92-2.2.24-.26.53-.33.7-.33l.5.01c.16 0 .38-.06.6.46.22.53.75 1.83.82 1.96.07.13.11.29.02.47-.09.18-.14.29-.27.45-.13.15-.28.34-.4.46-.13.13-.27.27-.12.53.16.26.7 1.15 1.5 1.86 1.03.92 1.9 1.2 2.16 1.34.26.13.41.11.56-.07.16-.18.65-.76.83-1.02.18-.26.35-.21.59-.13.24.09 1.53.72 1.79.85.26.13.44.2.5.31.06.12.06.66-.16 1.28z"/></svg></button>
      <button class="share-btn" title="Telegram" aria-label="Condividi su Telegram" onclick="shareArticle('telegram')"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.9 3.6c-.28-.23-.7-.28-1.16-.1L2.7 10.4c-.5.19-.83.51-.85.85-.02.34.28.62.76.79l4.6 1.5 1.78 5.6c.13.4.4.62.72.62.2 0 .4-.09.58-.26l2.58-2.4 4.63 3.4c.2.15.42.23.63.23.16 0 .33-.05.47-.14.29-.19.47-.53.51-.93L22 4.5c.05-.44-.1-.75-.1-.9zM8.9 14.6l-1.16-3.65 9.9-6.13-8.74 9.78zm.98 4.35l-.6-1.9 1.55-1.44 1.87 1.37-2.82 1.97zm7.06-1.32l-4.55-3.34 6.6-7.4-2.05 10.74z"/></svg></button>
      <button class="share-btn" title="Facebook" aria-label="Condividi su Facebook" onclick="shareArticle('facebook')"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7.5h2.5l.4-3H13.5V8.5c0-.87.24-1.46 1.5-1.46h1.6V4.36C16.3 4.25 15.3 4.1 14.1 4.1c-2.5 0-4.2 1.53-4.2 4.33V10.5H7.4v3h2.5V21h3.6z"/></svg></button>
      <button class="share-btn" title="X" aria-label="Condividi su X" onclick="shareArticle('twitter')"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 3h3l-7.3 8.34L21.5 21h-6.6l-5.17-6.4L3.7 21H.7l7.8-8.9L2.5 3h6.76l4.68 5.86L17.5 3zm-1.16 16.2h1.83L7.75 4.7H5.8l10.54 14.5z"/></svg></button>
      <button class="share-btn" title="Condividi" aria-label="Condividi" onclick="shareArticle('native')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><line x1="8.3" y1="10.7" x2="15.8" y2="6.4"/><line x1="8.3" y1="13.3" x2="15.8" y2="17.6"/></svg></button>
      <button class="share-btn" id="copy-btn" title="Copia link" aria-label="Copia link" onclick="shareArticle('copy')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 17H7a5 5 0 010-10h2"/><path d="M15 7h2a5 5 0 010 10h-2"/><line x1="8" y1="12" x2="16" y2="12"/></svg></button>
    </div>
  </div>
</div>

<div class="article-body" style="--accent:{accent};">
  <p class="lead">{desc} {lead_extra}</p>

  <p>{p1}</p>

  <p>{p2}</p>

  <blockquote class="article-quote">
    "{quote_text}"
    <cite>— {quote_cite}</cite>
  </blockquote>
{gallery}
  <p>{closing}</p>
</div>

<div class="article-tags">{catlabel} — Interference</div>

<footer class="site-footer">
  <div>© 2026 Interference Media</div>
  <div>Musica — Città — Società — Idee</div>
</footer>

<script src="../script.js"></script>
</body>
</html>
'''

LEAD_EXTRA = {
    "music": "Un fenomeno che racconta molto di come sta cambiando il rapporto tra musica, spazio e comunità in Europa.",
    "cities": "Un caso che si aggiunge a una lista sempre più lunga di esperimenti urbani da monitorare con attenzione.",
    "society": "Una tendenza che si osserva ormai in diverse città europee, con forme e intensità diverse.",
    "ideas": "Una domanda che intreccia filosofia, politica e vita quotidiana più di quanto sembri a prima vista.",
}

GALLERY_TPL = '''
  <div class="article-gallery">
    <div class="article-image-block">
      <img src="https://picsum.photos/seed/{slug}-g1/900/700" alt="{title}">
    </div>
    <div class="article-image-block">
      <img src="https://picsum.photos/seed/{slug}-g2/900/700" alt="{title}">
    </div>
  </div>
'''

# Demo/placeholder article generation removed: the site now only contains
# real, hand-written articles (listed in REAL_ARTICLES above).

# ---------------------------------------------------------------------------
# Pagination: 12 cards per page
# ---------------------------------------------------------------------------

PER_PAGE = 12
pages = [ALL[i:i + PER_PAGE] for i in range(0, len(ALL), PER_PAGE)]
n_pages = len(pages)

CARD_TPL = '''  <a class="card" data-cat="{category}" href="{href}">
    <div class="card-media">
      <div class="card-image">
        <img src="{image}" alt="{title}" loading="lazy">
      </div>
      <span class="card-category">{catlabel}</span>
    </div>
    <div class="card-content">
      <span class="card-date">{display_date}</span>
      <h2 class="card-title">{title}</h2>
      <p class="card-desc">{desc}</p>
      <div class="card-meta">
        {author}
      </div>
    </div>
  </a>
'''

def page_filename(n):
    return "index.html" if n == 1 else "page-{}.html".format(n)

# ---------------------------------------------------------------------------
# Multi-language support (IT default at site root, EN/ZH/RU mirrored in
# their own subfolders). Article bodies stay Italian-only for now — the
# language switcher on every page links through to each language's
# homepage; homepage cards themselves show translated title/desc.
# ---------------------------------------------------------------------------

LANGS = ["it", "en", "zh", "ru"]
LANG_LABEL = {"it": "IT", "en": "EN", "zh": "中文", "ru": "RU"}
LANG_NAME = {"it": "Italiano", "en": "English", "zh": "中文", "ru": "Русский"}

UI_STRINGS = {
    "it": {"see_all": "Vedi tutti", "dfree": "distraction free",
           "footer": "Musica — Città — Società — Idee", "prev": "← Precedente", "next": "Successivo →",
           "page_note": " — Pagina {} di {}", "meta_desc": "INTERFERENCES è una piattaforma media internazionale dedicata alle culture indipendenti: musica, controculture, rigenerazione urbana, arte, filosofia, politica culturale, comunità, festival, architettura sociale e nuovi movimenti."},
    "en": {"see_all": "See all", "dfree": "distraction free",
           "footer": "Music — Cities — Society — Ideas", "prev": "← Previous", "next": "Next →",
           "page_note": " — Page {} of {}", "meta_desc": "INTERFERENCES is an international media platform dedicated to independent culture: music, counterculture, urban regeneration, art, philosophy, cultural politics, community, festivals, social architecture and new movements."},
    "zh": {"see_all": "查看全部", "dfree": "distraction free",
           "footer": "音乐 — 城市 — 社会 — 思想", "prev": "← 上一页", "next": "下一页 →",
           "page_note": " — 第 {} / {} 页", "meta_desc": "INTERFERENCES 是一个致力于独立文化的国际媒体平台:音乐、反文化、城市更新、艺术、哲学、文化政治、社区、艺术节、社会建筑与新兴运动。"},
    "ru": {"see_all": "Показать все", "dfree": "distraction free",
           "footer": "Музыка — Города — Общество — Идеи", "prev": "← Назад", "next": "Далее →",
           "page_note": " — Страница {} из {}", "meta_desc": "INTERFERENCES — международная медиаплатформа, посвящённая независимой культуре: музыка, контркультура, регенерация городов, искусство, философия, культурная политика, сообщества, фестивали, социальная архитектура и новые движения."},
}

MONTHS_EN = ["", "January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]
MONTHS_RU_GEN = ["", "января", "февраля", "марта", "апреля", "мая", "июня",
                 "июля", "августа", "сентября", "октября", "ноября", "декабря"]

def fmt_date_lang(d, lang):
    if lang == "en":
        return "{} {}, {}".format(MONTHS_EN[d.month], d.day, d.year)
    if lang == "zh":
        return "{}年{}月{}日".format(d.year, d.month, d.day)
    if lang == "ru":
        return "{} {} {}".format(d.day, MONTHS_RU_GEN[d.month], d.year)
    return fmt_date(d)

# Translated card title/desc per article slug. Falls back to the Italian
# REAL_ARTICLES copy for any language/slug not listed here yet.
TRANSLATIONS = {
    "ideas-demoralizzazione-arma-di-guerra": {
        "en": {"title": "DEMORALIZATION AS A WEAPON OF WAR", "desc": "The invisible war for the control of culture."},
        "zh": {"title": "士气瓦解:一种战争武器", "desc": "一场争夺文化控制权的无形战争。"},
        "ru": {"title": "ДЕМОРАЛИЗАЦИЯ КАК ОРУЖИЕ ВОЙНЫ", "desc": "Невидимая война за контроль над культурой."},
    },
    "society-tempio-futuro-perduto": {
        "en": {"title": "THE REVOLUTION OF ITALIAN CLUBBING: IL TEMPIO IN MILAN", "desc": "How an abandoned tram depot became one of Italy's largest independent cultural communities."},
        "zh": {"title": "意大利俱乐部文化的革命:米兰的Tempio", "desc": "一座废弃的有轨电车车库,如何变成意大利最大的独立文化社区之一。"},
        "ru": {"title": "РЕВОЛЮЦИЯ ИТАЛЬЯНСКОГО КЛАББИНГА: TEMPIO В МИЛАНЕ", "desc": "Как заброшенное трамвайное депо стало одним из крупнейших независимых культурных сообществ Италии."},
    },
    "society-musica-finta-scena-italiana": {
        "en": {"title": "AI-MADE MUSIC IS AS FAKE AS TODAY'S ITALIAN SCENE", "desc": "Italy's 2026 music scene looks like one giant permanent talent show for people who hate music."},
        "zh": {"title": "AI制作的音乐和今天的意大利乐坛一样虚假", "desc": "2026年的意大利音乐界,像一场为讨厌音乐的人举办的永久选秀。"},
        "ru": {"title": "МУЗЫКА, СОЗДАННАЯ ИИ, ТАКАЯ ЖЕ ФАЛЬШИВАЯ, КАК И СЕГОДНЯШНЯЯ ИТАЛЬЯНСКАЯ СЦЕНА", "desc": "Музыкальная Италия 2026 года напоминает гигантское неиссякаемое шоу талантов для людей, ненавидящих музыку."},
    },
    "ideas-forza-carattere-estetica": {
        "en": {"title": "STRENGTH OF CHARACTER HAS GIVEN WAY TO AESTHETICS", "desc": "A civilization that replaces character-building with image-building produces individuals dependent on external validation."},
        "zh": {"title": "性格的力量已让位于美学", "desc": "一个用塑造形象取代塑造性格的文明,只会制造出依赖外部认可的个体。"},
        "ru": {"title": "СИЛА ХАРАКТЕРА УСТУПИЛА МЕСТО ЭСТЕТИКЕ", "desc": "Цивилизация, заменяющая воспитание характера конструированием образа, порождает людей, зависимых от внешнего одобрения."},
    },
    "music-scuola-della-techno": {
        "en": {"title": "THE WORLD'S FIRST TECHNO SCHOOL IS IN ITALY", "desc": "From Milan, a unique project: thousands of students, free classes, cultural research, workshops with international artists, and a radical idea that turns electronic music from mere entertainment into cultural heritage."},
        "zh": {"title": "世界上第一所科技舞曲学校诞生在意大利", "desc": "来自米兰的独特项目:数千名学生、免费课程、文化研究、国际艺术家工作坊,以及一个将电子音乐从单纯娱乐转变为文化遗产的激进理念。"},
        "ru": {"title": "ПЕРВАЯ В МИРЕ ШКОЛА ТЕХНО НАХОДИТСЯ В ИТАЛИИ", "desc": "Уникальный проект из Милана: тысячи студентов, бесплатные занятия, культурные исследования, мастер-классы с международными артистами и радикальная идея, превращающая электронную музыку из развлечения в культурное наследие."},
    },
    "society-centri-sociali-italiani-morti": {
        "en": {"title": "ITALY'S SOCIAL CENTERS ARE DEAD. SOMEONE SHOULD HAVE SAID SO.", "desc": "From the Genoa G8 to Macao, from Leoncavallo to Tempio del Futuro Perduto: what's left today of the movement that for thirty years embodied Italian political and cultural resistance."},
        "zh": {"title": "意大利的社会中心已经死了。总得有人说出来。", "desc": "从热那亚G8峰会到Macao,从Leoncavallo到Tempio del Futuro Perduto:这场代表了意大利三十年政治文化抵抗运动的现状如何?"},
        "ru": {"title": "ИТАЛЬЯНСКИЕ СОЦИАЛЬНЫЕ ЦЕНТРЫ МЕРТВЫ. КТО-ТО ДОЛЖЕН БЫЛ ЭТО СКАЗАТЬ.", "desc": "От генуэзской G8 до Macao, от Leoncavallo до Tempio del Futuro Perduto: что осталось от движения, тридцать лет представлявшего итальянское политическое и культурное сопротивление."},
    },
    "music-italo-ghetto": {
        "en": {"title": "TECHNO IS NOW SUNG IN ITALIAN. IT'S A NEW GENRE CALLED ITALO GHETTO.", "desc": "After forty years of nostalgia and imported foreign sounds, a new scene tries to build an entirely Italian techno language: dialects, singer-songwriting, rave culture and popular imagery on the dancefloor."},
        "zh": {"title": "如今科技舞曲开始用意大利语演唱。这是一个新流派,名为Italo Ghetto。", "desc": "在四十年的怀旧与外来声音输入之后,一股新浪潮正尝试构建完全意大利化的科技舞曲语言:方言、创作歌曲、锐舞文化与大众意象在舞池中交融。"},
        "ru": {"title": "ТЕХНО ТЕПЕРЬ ПОЮТ НА ИТАЛЬЯНСКОМ. ЭТО НОВЫЙ ЖАНР — ITALO GHETTO.", "desc": "После сорока лет ностальгии и заимствованных иностранных звуков новая сцена пытается создать полностью итальянский техно-язык: диалекты, авторская песня, рейв-культура и народные образы на танцполе."},
    },
    "ideas-sinistra-reel-caroselli": {
        "en": {"title": "THE LEFT USED TO BE THE PEOPLE OF BOOKS AND MILITANCY. TODAY IT'S THE AUDIENCE OF REELS AND CAROUSELS.", "desc": "From magazines to podcasts, from social-media lawyers to activist-brands: the left has replaced political thought with reassuring content, serial outrage and individual careers perfectly integrated into the establishment."},
        "zh": {"title": "左翼曾是书籍与行动的信奉者。如今却成了Reels和轮播广告的观众。", "desc": "从杂志到播客,从社交媒体律师到活动家品牌:左翼用令人安心的内容、连续不断的愤慨和完全融入建制的个人事业,取代了政治思想。"},
        "ru": {"title": "ЛЕВЫЕ БЫЛИ НАРОДОМ КНИГ И БОРЬБЫ. СЕГОДНЯ ОНИ — АУДИТОРИЯ РИЛСОВ И КАРУСЕЛЕЙ.", "desc": "От журналов до подкастов, от юристов в соцсетях до брендов-активистов: левые заменили политическую мысль успокаивающим контентом, серийным возмущением и личными карьерами, идеально встроенными в истеблишмент."},
    },
    "cities-sicurezza-milano-meme-elettorale": {
        "en": {"title": "MILAN'S SECURITY PROBLEMS AREN'T AN ELECTION MEME. AND MAYBE WE'RE LOOKING IN THE WRONG DIRECTION.", "desc": "Between the Interior Ministry, the Prefect, the City Council and the Security Commission: who actually bears responsibility for urban security in Milan, beyond the social-media slogan against the mayor."},
        "zh": {"title": "米兰的治安问题不是竞选段子。或许我们一直看错了方向。", "desc": "在内政部、省长、市政府和治安委员会之间:除了针对市长的社交媒体口号,谁才真正对米兰的城市安全负责?"},
        "ru": {"title": "ПРОБЛЕМЫ БЕЗОПАСНОСТИ МИЛАНА — НЕ ПРЕДВЫБОРНЫЙ МЕМ. И, ВОЗМОЖНО, МЫ СМОТРИМ НЕ В ТУ СТОРОНУ.", "desc": "Между МВД, префектом, мэрией и комиссией по безопасности: кто на самом деле отвечает за городскую безопасность в Милане, помимо лозунга в соцсетях против мэра."},
    },
    "interviews-oriental-techno-club-intervista": {
        "en": {"title": "EUROPE'S FIRST 100% ASIAN ELECTRONIC CLUB: ORIENTAL TECHNO CLUB IN MILAN", "desc": "An interview with the collective that turned Asian electronic culture into a real bridge between Asia and Europe, through music, visual arts, performance and ritual."},
        "zh": {"title": "欧洲第一家100%亚洲风格电子俱乐部:米兰Oriental Techno Club", "desc": "专访这个团体,他们通过音乐、视觉艺术、表演与仪式,将亚洲电子文化变成连接亚洲与欧洲的真实桥梁。"},
        "ru": {"title": "ПЕРВЫЙ В ЕВРОПЕ ЭЛЕКТРОННЫЙ КЛУБ НА 100% АЗИАТСКИЙ: ORIENTAL TECHNO CLUB В МИЛАНЕ", "desc": "Интервью с коллективом, превратившим азиатскую электронную культуру в настоящий мост между Азией и Европой через музыку, визуальное искусство, перформанс и ритуал."},
    },
    "interviews-dolce-potente-intervista": {
        "en": {"title": "FROM PUGLIA, ALONE, BY BUS, CHASING A DREAM: AN INTERVIEW WITH DOLCE POTENTE", "desc": "Starting from the working-class neighborhoods of Bari to recent tours in China, Europe and Italy. Dolce Potente is becoming, day by day, a reference point for Italy's new techno scene."},
        "zh": {"title": "独自一人,从普利亚出发,乘大巴追逐梦想:专访Dolce Potente", "desc": "从巴里的平民社区起步,到近期的中国、欧洲和意大利巡演。Dolce Potente正日益成为意大利新一代科技舞曲的标杆人物。"},
        "ru": {"title": "ИЗ ПУЛЬИ, В ОДИНОЧКУ, НА АВТОБУСЕ, В ПОГОНЕ ЗА МЕЧТОЙ: ИНТЕРВЬЮ С DOLCE POTENTE", "desc": "От рабочих кварталов Бари до недавних туров по Китаю, Европе и Италии. Dolce Potente день ото дня становится ориентиром для новой итальянской техно-сцены."},
    },
    "ideas-festival-lunapark-territorio": {
        "en": {"title": "MODERN FESTIVALS: A DECLINING FUNFAIR, OR A RESOURCE FOR THE LAND?", "desc": "A reflection on the ownership of Europe's major music festivals, the exploitation of the territories that host them, and Italian cultural provincialism."},
        "zh": {"title": "现代音乐节:衰落的游乐场,还是地方的资源?", "desc": "对欧洲大型音乐节所有权、主办地遭受的剥削,以及意大利文化地方主义的反思。"},
        "ru": {"title": "СОВРЕМЕННЫЕ ФЕСТИВАЛИ: УГАСАЮЩИЙ ЛУНА-ПАРК ИЛИ РЕСУРС ДЛЯ ТЕРРИТОРИИ?", "desc": "Размышление о собственности крупных европейских музыкальных фестивалей, эксплуатации принимающих их территорий и итальянском культурном провинциализме."},
    },
    "interviews-elisa-bee-intervista": {
        "en": {"title": "FROM SARDINIA TO BERGHAIN, VIA IL TEMPIO: AN INTERVIEW WITH ELISA BEE", "desc": "From her first nights out in Sardinia to Europe's most prestigious dancefloors, the artistic and personal journey that made her one of the most recognizable figures in Europe's new techno scene."},
        "zh": {"title": "从撒丁岛到Berghain,途经Tempio:专访Elisa Bee", "desc": "从在撒丁岛的最初夜晚,到欧洲最负盛名的舞池,这段艺术与人生之旅让她成为欧洲新一代科技舞曲最具辨识度的人物之一。"},
        "ru": {"title": "ИЗ САРДИНИИ В BERGHAIN, ЧЕРЕЗ TEMPIO: ИНТЕРВЬЮ С ELISA BEE", "desc": "От первых вечеринок на Сардинии до самых престижных танцполов Европы — творческий и человеческий путь, сделавший её одной из самых узнаваемых фигур новой европейской техно-сцены."},
    },
    "ideas-discoteche-non-fanno-club-culture": {
        "en": {"title": "COMMERCIAL DISCOS DON'T MAKE CLUB CULTURE", "desc": "The crisis of the big commercial discos isn't a passing phase, but the symptom of an economic and cultural model running out of steam, now trying to regenerate itself by appropriating clubbing, techno and hard techno."},
        "zh": {"title": "商业迪厅制造不出俱乐部文化", "desc": "大型商业迪厅的危机并非一时现象,而是一种经济与文化模式走向枯竭的征兆——如今它试图通过挪用俱乐部文化、科技舞曲和硬核科技舞曲来重获新生。"},
        "ru": {"title": "КОММЕРЧЕСКИЕ ДИСКОТЕКИ НЕ СОЗДАЮТ КЛАБ-КУЛЬТУРУ", "desc": "Кризис крупных коммерческих дискотек — не временное явление, а симптом истощения экономической и культурной модели, которая сегодня пытается возродиться, присваивая клаббинг, техно и хард-техно."},
    },
}

def loc(path, lang):
    """Prefix an asset/article path with the extra '../' needed when the
    page being generated lives inside a /en /zh /ru subfolder."""
    return path if lang == "it" else "../" + path

def lang_link(current_lang, target_lang, page_fn):
    if current_lang == target_lang:
        return page_fn
    prefix = "" if current_lang == "it" else "../"
    if target_lang == "it":
        return prefix + page_fn
    return prefix + target_lang + "/" + page_fn

def lang_switcher_html(current_lang, page_fn):
    items = ""
    for L in LANGS:
        cls = ' class="active"' if L == current_lang else ""
        items += '      <a href="{}"{}>{}</a>\n'.format(lang_link(current_lang, L, page_fn), cls, LANG_NAME[L])
    return ('    <details class="lang-switcher">\n'
            '      <summary>{}</summary>\n'
            '      <div class="lang-menu">\n{}      </div>\n'
            '    </details>').format(LANG_LABEL[current_lang], items)

PRELOADER = ('<div id="site-preloader" aria-hidden="true">\n'
             '  <div class="preloader-word">INTERFERENCES</div>\n'
             '  <div class="preloader-bar"><span></span></div>\n'
             '</div>\n')

def pagination_nav(current, lang):
    if n_pages <= 1:
        return ""
    s = UI_STRINGS[lang]
    items = []
    if current > 1:
        items.append('<a class="page-btn" href="{}">{}</a>'.format(page_filename(current - 1), s["prev"]))
    else:
        items.append('<span class="page-btn disabled">{}</span>'.format(s["prev"]))
    nums = []
    for n in range(1, n_pages + 1):
        cls = "page-num active" if n == current else "page-num"
        nums.append('<a class="{}" href="{}">{}</a>'.format(cls, page_filename(n), n))
    items.append('<div class="page-numbers">' + "".join(nums) + '</div>')
    if current < n_pages:
        items.append('<a class="page-btn" href="{}">{}</a>'.format(page_filename(current + 1), s["next"]))
    else:
        items.append('<span class="page-btn disabled">{}</span>'.format(s["next"]))
    return '<nav class="pagination">\n  ' + "\n  ".join(items) + '\n</nav>'

PAGE_TPL = '''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>INTERFERENCES — Culture Indipendenti{page_suffix}</title>
<meta name="description" content="{meta_desc}">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="INTERFERENCES">
<meta property="og:title" content="INTERFERENCES — Culture Indipendenti">
<meta property="og:description" content="{meta_desc}">
<meta property="og:image" content="https://www.interferencesmag.com/interference-cover.png">
<meta property="og:url" content="https://www.interferencesmag.com/{page_url}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="INTERFERENCES — Culture Indipendenti">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="https://www.interferencesmag.com/interference-cover.png">

<link rel="stylesheet" href="{asset}style.css">
</head>
<body>

{preloader}
<header class="site-header">
  <div class="wrap">
    <div class="logo"><a href="/"><img src="{asset}logo.png" alt="INTERFERENCES"></a></div>
  </div>
  <div class="wrap tagline-row">
    <span>Culture Indipendenti</span>
    <span>独立文化</span>
    <span>Independent Cultures</span>
    <span>Независимые культуры</span>
  </div>
</header>

<nav class="filters">
  <button class="filter-pill active" data-cat="all">{see_all}</button>
  <button class="filter-pill" data-cat="music">Music</button>
  <button class="filter-pill" data-cat="cities">Cities</button>
  <button class="filter-pill" data-cat="society">Society</button>
  <button class="filter-pill" data-cat="ideas">Ideas</button>
  <button class="filter-pill" data-cat="interviews">Interviews</button>
{lang_switcher}
  <button class="filter-pill dfree-toggle" id="dfree-toggle">{dfree}</button>
</nav>

<main class="grid">
  <div class="grid-lines" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
{cards}</main>

{pagination}

<footer class="site-footer">
  <div>© 2026 Interference Media</div>
  <div>{footer}{page_note}</div>
</footer>

<script src="{asset}script.js"></script>
</body>
</html>
'''

# Placeholder mode: every card links to the same shared article template
# until real editorial content is ready to replace it (see articles/template-articolo.html).
ARTICLE_HREF = "articles/template-articolo.html"

import os

for lang in LANGS:
    s = UI_STRINGS[lang]
    outdir = "." if lang == "it" else lang
    if lang != "it":
        os.makedirs(outdir, exist_ok=True)

    for n, page_articles in enumerate(pages, start=1):
        cards = ""
        for a in page_articles:
            slug = a["slug"]
            tr = TRANSLATIONS.get(slug, {}).get(lang, {})
            title = tr.get("title", a["title"])
            desc = tr.get("desc", a["desc"])
            # Images always live in the shared root /articles/ folder (not
            # duplicated per language), so they always need the loc() prefix.
            image = loc(a.get("image", "https://picsum.photos/seed/{}/900/700".format(slug)), lang) \
                if not a.get("image", "").startswith("http") else a.get("image")
            # Articles themselves DO have a per-language translated copy
            # (en/articles/, zh/articles/, ru/articles/) once translated, so
            # for lang != "it" the homepage card should link straight to
            # that language's own copy rather than falling back to the
            # Italian original via loc().
            raw_href = a.get("href", ARTICLE_HREF)
            if raw_href.startswith("http"):
                href = raw_href
            elif lang == "it":
                href = raw_href
            else:
                href = raw_href  # e.g. "articles/{slug}.html" — already correct relative to lang subfolder
            cards += CARD_TPL.format(
                category=a["category"], href=href, image=image,
                slug=slug, title=title, catlabel=CATLABEL[a["category"]],
                display_date=fmt_date_lang(a["date"], lang), desc=desc,
                author=a["author"],
            )
        page_fn = page_filename(n)
        page_note = "" if n_pages <= 1 else s["page_note"].format(n, n_pages)
        html = PAGE_TPL.format(
            html_lang=lang,
            page_suffix="" if n == 1 else " — " + s["page_note"].format(n, n_pages).lstrip(" —"),
            page_url=(page_fn if lang == "it" else lang + "/" + page_fn),
            meta_desc=s["meta_desc"],
            asset=("" if lang == "it" else "../"),
            preloader=PRELOADER,
            see_all=s["see_all"], dfree=s["dfree"],
            lang_switcher=lang_switcher_html(lang, page_fn),
            cards=cards, pagination=pagination_nav(n, lang),
            footer=s["footer"], page_note=page_note,
        )
        with open(os.path.join(outdir, page_fn), "w", encoding="utf-8") as f:
            f.write(html)

print("Generate {} pagine x {} lingue ({} articoli totali, {} per pagina)".format(n_pages, len(LANGS), len(ALL), PER_PAGE))
