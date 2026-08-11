# -*- coding: utf-8 -*-
import re, unicodedata
from datetime import date, timedelta

MONTHS = ["", "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
          "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

ACCENT = {
    "music": "#B0C400", "cities": "#E6008A",
    "society": "#34A853", "ideas": "#6C4FE0",
}
CATLABEL = {"music": "Music", "cities": "Cities", "society": "Society", "ideas": "Ideas"}

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
     "image": "articles/demoralizzazione-italia-1963.jpg",
     "avatar": "articles/thomas-anderson.jpg"},
    {"slug": "society-tempio-futuro-perduto",
     "title": "LA RIVOLUZIONE DEL CLUBBING ITALIANO: IL TEMPIO DI MILANO",
     "desc": "Come un'ex officina tranviaria abbandonata è diventata una delle comunità culturali indipendenti più estese d'Italia.",
     "category": "society", "author": "Thomas Anderson", "date": date(2026, 7, 28),
     "href": "articles/society-tempio-futuro-perduto.html",
     "image": "articles/tempio-1.jpg",
     "avatar": "articles/thomas-anderson.jpg"},
    {"slug": "society-musica-finta-scena-italiana",
     "title": "LA MUSICA FATTA CON L'AI È FINTA COME LA SCENA ITALIANA DI OGGI",
     "desc": "L'Italia musicale del 2026 sembra un gigantesco talent permanente per persone che odiano la musica.",
     "category": "society", "author": "Thomas Anderson", "date": date(2026, 7, 28),
     "href": "articles/society-musica-finta-scena-italiana.html",
     "image": "articles/musica-2026-delia.jpg",
     "avatar": "articles/thomas-anderson.jpg"},
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
        <span class="card-avatar"><img src="{avatar}" alt=""></span>
        {author}
      </div>
    </div>
  </a>
'''

def page_filename(n):
    return "index.html" if n == 1 else "page-{}.html".format(n)

def pagination_nav(current):
    if n_pages <= 1:
        return ""
    items = []
    if current > 1:
        items.append('<a class="page-btn" href="{}">← Precedente</a>'.format(page_filename(current - 1)))
    else:
        items.append('<span class="page-btn disabled">← Precedente</span>')
    nums = []
    for n in range(1, n_pages + 1):
        cls = "page-num active" if n == current else "page-num"
        nums.append('<a class="{}" href="{}">{}</a>'.format(cls, page_filename(n), n))
    items.append('<div class="page-numbers">' + "".join(nums) + '</div>')
    if current < n_pages:
        items.append('<a class="page-btn" href="{}">Successivo →</a>'.format(page_filename(current + 1)))
    else:
        items.append('<span class="page-btn disabled">Successivo →</span>')
    return '<nav class="pagination">\n  ' + "\n  ".join(items) + '\n</nav>'

PAGE_TPL = '''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>INTERFERENCES — Culture Indipendenti{page_suffix}</title>
<meta name="description" content="INTERFERENCES è una piattaforma media internazionale dedicata alle culture indipendenti: musica, controculture, rigenerazione urbana, arte, filosofia, politica culturale, comunità, festival, architettura sociale e nuovi movimenti.">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="INTERFERENCES">
<meta property="og:title" content="INTERFERENCES — Culture Indipendenti">
<meta property="og:description" content="Musica, controculture, rigenerazione urbana, arte, filosofia, politica culturale, comunità, festival, architettura sociale, nuovi movimenti.">
<meta property="og:image" content="https://www.interferencesmag.com/interference-cover.png">
<meta property="og:url" content="https://www.interferencesmag.com/{page_url}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="INTERFERENCES — Culture Indipendenti">
<meta name="twitter:description" content="Musica, controculture, rigenerazione urbana, arte, filosofia, politica culturale, comunità, festival, architettura sociale, nuovi movimenti.">
<meta name="twitter:image" content="https://www.interferencesmag.com/interference-cover.png">

<link rel="stylesheet" href="style.css">
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <div class="logo"><a href="/"><img src="logo.png" alt="INTERFERENCES"></a></div>
  </div>
  <div class="wrap tagline-row">
    <span>Culture Indipendenti</span>
    <span>独立文化</span>
    <span>Independent Cultures</span>
    <span>Независимые культуры</span>
  </div>
</header>

<nav class="filters">
  <button class="filter-pill active" data-cat="all">See all</button>
  <button class="filter-pill" data-cat="music">Music</button>
  <button class="filter-pill" data-cat="cities">Cities</button>
  <button class="filter-pill" data-cat="society">Society</button>
  <button class="filter-pill" data-cat="ideas">Ideas</button>
  <button class="filter-pill dfree-toggle" id="dfree-toggle">distraction free</button>
</nav>

<main class="grid">
  <div class="grid-lines" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
{cards}</main>

{pagination}

<footer class="site-footer">
  <div>© 2026 Interference Media</div>
  <div>Musica — Città — Società — Idee{page_note}</div>
</footer>

<script src="script.js"></script>
</body>
</html>
'''

# Placeholder mode: every card links to the same shared article template
# until real editorial content is ready to replace it (see articles/template-articolo.html).
ARTICLE_HREF = "articles/template-articolo.html"

for n, page_articles in enumerate(pages, start=1):
    cards = ""
    for a in page_articles:
        image = a.get("image", "https://picsum.photos/seed/{}/900/700".format(a["slug"]))
        avatar = a.get("avatar", "https://i.pravatar.cc/64?u={}".format(slugify(a["author"])))
        cards += CARD_TPL.format(
            category=a["category"], href=a.get("href", ARTICLE_HREF), image=image,
            slug=a["slug"], title=a["title"], catlabel=CATLABEL[a["category"]],
            display_date=fmt_date(a["date"]), desc=a["desc"],
            author=a["author"], avatar=avatar,
        )
    html = PAGE_TPL.format(
        page_suffix="" if n == 1 else " — Pagina {}".format(n),
        page_url="" if n == 1 else page_filename(n),
        cards=cards, pagination=pagination_nav(n),
        page_note="" if n_pages <= 1 else " — Pagina {} di {}".format(n, n_pages),
    )
    with open(page_filename(n), "w", encoding="utf-8") as f:
        f.write(html)

print("Generate {} pagine ({} articoli totali, {} per pagina)".format(n_pages, len(ALL), PER_PAGE))
