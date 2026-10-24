# SAN-10: Strategia Social Commerce, Flussi WhatsApp Business e Calendario Lanci Promozionali Locali

**Progetto**: Just in Time di Benegiamo Andrea (E-Commerce Shopify)  
**Codice Identificativo Task**: SAN-10  
**Data di Redazione**: 24 Ottobre 2026  
**Autore / Ruolo**: Social Media Manager (`worker-jim-marketing`)  
**Stato**: Completato (Fase 3 - Flussi Operativi e Lancio Territoriale)  

---

## 1. Executive Summary & Architettura Omnicanale Phygital

Il presente documento definisce le linee guida operative, tecniche ed editoriali per trasformare la presenza social e di messaggistica istantanea di **Just in Time di Benegiamo Andrea** (Via Corsica 151, Muro Leccese - LE) nel motore di trazione dell'e-commerce Shopify.

L'approccio adottato è rigorosamente **phygital (Physical + Digital)**:
1. **Canali Social (Meta / Instagram / Facebook)**: generano scoperta, riprova sociale ed engagement attraverso il volto e la competenza di Andrea.
2. **Sincronizzazione Catalogo Shopify (Meta Commerce)**: permette l'acquisto diretto con tag di prodotto nei reel, nei caroselli e nelle stories.
3. **WhatsApp Business**: costituisce l'infrastruttura fiduciaria primaria per abbattere ogni attrito di conversione, supportare il *Click & Collect* in negozio ed erogare assistenza pre/post vendita in tempo reale.
4. **Local Marketing & Google Business Profile**: presidiano l'hinterland di Muro Leccese e del Salento centrale (Maglie, Poggiardo, Scorrano, Otranto, Tricase).

```
+---------------------------------------------------------------------------------------+
|                                 TRAFFICO LOCALE & SOCIAL                              |
|   - Meta Ads geolocalizzate (raggio 15km)        - Reel & Post Brand Voice (Andrea)   |
|   - Ricerca Google Maps / Local SEO              - Passaparola & Vetrine territoriali |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                           PUNTI DI ATTERRAGGIO & TOUCHPOINT                           |
|   - Vetrina Instagram / Facebook Shopping (Catalogo sincronizzato Shopify)            |
|   - Storefront Shopify Dawn (Scheda prodotto, Click & Collect 2h, Carrello)           |
+-------------------------------------------+-------------------------------------------+
                                            |
                    +-----------------------+-----------------------+
                    |                                               |
                    v                                               v
+---------------------------------------+   +---------------------------------------+
|        CONVERSIONE SHOPIFY            |   |     ASSISTENZA & CHAT WHATSAPP        |
| - Ordine online con ritiro in sede    |   | - Verifica compatibilità / ricambi    |
| - Spedizione espressa 24/48h          |   | - Preventivi riparazione laboratorio  |
| - Pagamento online o al banco         |   | - Assistenza pre e post-acquisto      |
+---------------------------------------+   +---------------------------------------+
```

---

## 2. Piano Operativo di Sincronizzazione Meta (Facebook & Instagram Shopping)

### 2.1 Prerequisiti & Commerce Eligibility Requirements
Per garantire l'approvazione immediata dello shop senza incorrere in blocchi da parte dei revisori automatici di Meta:
* **Connessione Account**: Associazione tra la Pagina Facebook ufficiale *Just in Time di Benegiamo Andrea* e l'account Instagram Professionale (`@justintime.muroleccese`).
* **Verifica Dominio**: Verifica DNS del dominio Shopify tramite record TXT inserito nel pannello DNS.
* **Commerce Eligibility**: Presenza sul sito Shopify di policy di reso, termini di servizio e informativa privacy esplicite e accessibili (già allestite nella Fase 2 in `pages-legal/`).
* **Trasparenza Prezzi e Valuta**: Prezzi visualizzati in Euro (€) comprensivi di IVA e condizioni chiare per i prodotti ricondizionati (Grado A+ e garanzia 12 mesi).

---

### 2.2 Architettura di Connessione con Shopify
La sincronizzazione avviene mediante il canale nativo Shopify: **Facebook & Instagram by Meta**.

1. **Meta Business Manager & Commerce Manager**:
   * Creazione / associazione del Business Manager intestato a "Just in Time di Benegiamo Andrea".
   * Attivazione del Catalogo Prodotti primario con sincronizzazione bidirezionale in tempo reale (Shopify -> Meta Commerce Manager).
2. **Meta Pixel & Conversions API (CAPI)**:
   * Attivazione della modalità *Maximum Data Sharing* nell'app Shopify, che combina il tracciamento lato browser (Meta Pixel) con il tracciamento lato server (Conversions API).
   * Eventi tracciati automaticamente: `ViewContent` (visualizzazione scheda prodotto), `AddToCart` (aggiunta al carrello), `InitiateCheckout` (avvio cassa) e `Purchase` (acquisto completato).
3. **Mappatura degli Attributi di Catalogo (Feed Sync)**:
   * **Google Product Category / Meta Taxonomy**: Mappatura secondo la tassonomia ufficiale (es. *Electronics > Computers > Laptops* per notebook; *Electronics > Storage > Solid State Drives* per SSD).
   * **Condition**: Valorizzazione automatica del campo `condition` (`new` per articoli nuovi, `refurbished` per notebook e dispositivi ricondizionati).
   * **Disponibilità**: `in stock` sincronizzato con la giacenza effettiva del magazzino Shopify, con disattivazione automatica del tag se il pezzo unico ricondizionato viene venduto.

---

### 2.3 Struttura della Vetrina Social (Instagram Shop & Facebook Shop)
All'interno di Instagram e Facebook, la vetrina sarà organizzata in collezioni curate, rispecchiando l'assortimento del negozio:

| Collezione Vetrina | Prodotti Inclusi | Obiettivo Commerciale |
| :--- | :--- | :--- |
| **I Consigliati da Andrea** | Notebook HP 250 G9, SSD Kingston 480GB, Kit Logitech MK270 | Bestseller pronti all'uso per famiglie, studenti e lavoratori |
| **Occasioni Ricondizionate** | Lenovo ThinkPad T480 Grado A+, monitor e workstation usate garantite | Offerta ad alto margine e convenienza economica |
| **Upgrade & Riparazioni** | Pacchetto Upgrade SSD + Clonazione, Servizio Diagnosi Guasto | Spinta ai servizi ad alto valore aggiunto del laboratorio |
| **Consumabili & Ufficio** | Toner HP 106A, Cartucce Epson 603XL, Risme Fabriano Copy 2 | Acquisto ricorrente ad alta frequenza per privati e PMI |

---

### 2.4 Procedura Operativa di Product Tagging per il Personale
Affinché ogni contenuto pubblicato generi vendite tracciabili:
1. **Reel & Video brevi**: Taggare fino a un massimo di 3 prodotti coerenti mostrati nel video (es. nel reel sul salvataggio del PC, taggare il *Pacchetto Upgrade SSD Kingston* e il *Servizio Diagnosi*).
2. **Caroselli Informativi**: Inserire il tag prodotto specifico nella slide finale di riepilogo con call to action a toccare l'icona della borsa della spesa.
3. **Stories Giornaliere**: Utilizzare l'adesivo interattivo "Prodotto" posizionato in un punto ben visibile, abbinato a un sondaggio o box domande ("Vuoi rinnovare il tuo PC prima che ti lasci a piedi?").

---

## 3. Configurazione Flussi Operativi WhatsApp Business

WhatsApp Business è il canale di conversazione privilegiato per il bacino d'utenza salentino. Il numero dedicato ufficiale è: **+39 320 6025789**.

### 3.1 Profilo dell'Attività (Business Profile Setup)
* **Nome Attività**: Just in Time di Benegiamo Andrea
* **Descrizione**: Vendita computer, notebook nuovi e ricondizionati certificati, laboratorio assistenza tecnica rapida, consumabili stampa e forniture per ufficio/scuola. Ritiro gratuito in sede o spedizione rapida.
* **Indirizzo**: Via Corsica 151, 73036 Muro Leccese (LE)
* **Orari di Apertura**: Lunedì - Sabato: 08:30 - 13:00 / 16:30 - 20:00 (Giovedì pomeriggio chiuso, Domenica chiuso).
* **Sito Web**: Link diretto allo storefront Shopify.
* **Catalogo Integrato**: Vetrina dei 10 articoli e servizi principali con link diretto alla scheda prodotto Shopify.

---

### 3.2 Messaggi Automatici di Sistema

#### A) Messaggio di Benvenuto (Greeting Message)
*Attivazione: inviato automaticamente al primo contatto o dopo 14 giorni di inattività del cliente.*

> **Testo**:  
> "Ciao! Ti diamo il benvenuto da **Just in Time** (Muro Leccese) 👋  
> Sono Andrea. Come possiamo aiutarti oggi?  
>   
> 💻 **Assistenza o riparazione PC**: descrivici il problema o portalo in laboratorio in Via Corsica 151.  
> 📦 **Info su un prodotto o ordine online**: indicaci il modello o il codice ordine.  
> 🖨️ **Cartucce / Toner**: scrivici il modello della tua stampante per verificare subito la disponibilità.  
>   
> Se vuoi dare un'occhiata al nostro catalogo completo e verificare le disponibilità in tempo reale, visita: [Link Store Shopify]  
> Ti risponderemo nel minor tempo possibile!"

---

#### B) Messaggio di Assenza / Fuori Orario (Away Message)
*Attivazione: inviato automaticamente durante gli orari di chiusura del negozio e la domenica.*

> **Testo**:  
> "Grazie per aver scritto a **Just in Time**!  
> In questo momento il nostro laboratorio e il punto vendita sono chiusi 🚪  
>   
> I nostri orari:  
> 🕒 Lun-Mer, Ven-Sab: 08:30-13:00 / 16:30-20:00  
> 🕒 Giovedì: 08:30-13:00 (pomeriggio chiuso)  
>   
> Non preoccuparti: il nostro store online è sempre aperto 24/7! Puoi consultare i prodotti, prenotare un ritiro o bloccare un'offerta su: [Link Store Shopify]  
> Leggeremo il tuo messaggio alla riapertura e ti risponderemo subito. A presto!"

---

### 3.3 Set Completo di Risposte Rapide (Quick Replies / Shortcuts)
Per consentire ad Andrea e al collaboratore al banco di rispondere in 3 secondi a oltre l'80% delle richieste frequenti:

```markdown
1. Comando: /ritiro
Titolo: Istruzioni Ritiro Click & Collect
Testo:
"Ottima notizia! Il tuo ordine Just in Time è pronto per essere ritirato al banco 📦
Ci trovi a Muro Leccese in Via Corsica 151.
Puoi passare negli orari di apertura (08:30-13:00 / 16:30-20:00).
Mostra pure questo messaggio o il codice ordine al tuo arrivo. A tra poco!"

2. Comando: /riparazione
Titolo: Diagnosi & Preventivo Laboratorio
Testo:
"Ciao! Per i problemi tecnici offriamo una diagnosi professionale in laboratorio entro 24 ore lavorative 🛠️
Puoi portarci il tuo computer in Via Corsica 151: verificheremo hardware, temperature e sistema operativo e ti comunicheremo il preventivo esatto prima di qualsiasi intervento.
Il costo della diagnosi (20€ PC fisso / 25€ notebook) viene interamente scalato dal costo finale della riparazione se approvata!"

3. Comando: /upgrade
Titolo: Servizio Upgrade SSD + Clonazione
Testo:
"Il tuo computer è diventato lento? Non c'è bisogno di comprarne uno nuovo! 🚀
Con il nostro pacchetto 'Upgrade SSD Kingston 480GB + Installazione e Clonazione' (79,00€ tutto compreso):
- Duplichiamo esattamente i tuoi programmi, foto e file senza perdere nulla.
- Il tuo computer diventerà fino a 10 volte più scattante.
- Lavoro eseguito e riconsegnato in sole 24 ore!
Portalo pure in negozio per un controllo preliminare."

4. Comando: /toner
Titolo: Verifica Consumabili Stampa
Testo:
"Ciao! Per verificare se abbiamo la cartuccia o il toner giusto per te, puoi scriverci:
1. La marca e il modello esatto della tua stampante (oppure inviaci una foto della targhetta o della vecchia cartuccia).
Abbiamo sempre disponibili le referenze più diffuse (HP, Epson, Brother, Canon) sia originali che compatibili ad alta resa!"

5. Comando: /libri
Titolo: Prenotazione Libri Scolastici & Servizio Colibrì
Testo:
"La campagna libri di testo per le scuole secondarie del Salento è attiva da Just in Time! 📚
Puoi prenotare la lista completa senza alcun anticipo:
- Ti avviseremo noi via WhatsApp man mano che i testi arrivano.
- Su richiesta applichiamo le copertine protettive Colibrì su misura.
- Pagherai comodamente al ritiro in negozio.
Mandaci la foto dell'elenco o la classe/sezione per procedere!"

6. Comando: /spedizione
Titolo: Tracciamento e Tempistiche Spedizioni
Testo:
"Il tuo ordine è stato affidato al nostro corriere espresso 🚚
I tempi medi di consegna sono di 24/48 ore lavorative. Riceverai un'email e un SMS con il link di tracking per monitorare il pacco in ogni momento. Se hai bisogno di assistenza sulla consegna siamo a tua completa disposizione!"

7. Comando: /orari
Titolo: Orari e Posizione Geografica
Testo:
"Siamo a Muro Leccese (LE) in Via Corsica 151 📍
Link Google Maps: https://maps.app.goo.gl/justintime
Orari:
- Lunedì - Sabato: 08:30 - 13:00 / 16:30 - 20:00
- Giovedì pomeriggio: Chiuso
- Domenica: Chiuso"

8. Comando: /zeropensieri
Titolo: Configurazione PC Zero Pensieri
Testo:
"Con il nostro pacchetto 'Zero Pensieri' (40€ o incluso nelle nostre configurazioni speciali) ricevi il tuo nuovo computer:
- Aggiornato con l'ultima versione di Windows e driver stabili.
- Pulito da tutti i programmi spazzatura e pubblicità preinstallate.
- Con suite ufficio, antivirus, lettore PDF e strumenti pronti all'uso.
- Con eventuale travaso di tutti i tuoi dati dal vecchio PC!
Lo accendi ed è subito pronto per lavorare."

9. Comando: /ricondizionato
Titolo: Garanzia e Qualità Ricondizionati
Testo:
"Tutti i nostri notebook ricondizionati sono certificati 'Grado A+':
- Testati in laboratorio con oltre 25 controlli hardware accurati.
- Batteria verificata e igienizzazione professionale.
- Garanzia 12 mesi Just in Time direttamente presso il nostro laboratorio.
Prestazioni aziendali a meno di metà del prezzo del nuovo! Scopri i modelli disponibili qui: [Link Collezione Ricondizionati]"

10. Comando: /counter
Titolo: Servizio Fermopoint & Amazon Counter
Testo:
"Siamo punto di ritiro e reso ufficiale Amazon Counter e Fermopoint a Muro Leccese 📦
Puoi ritirare i tuoi pacchi durante tutti i nostri orari di apertura mostrando il codice a barre o il PIN di ritiro presente sulla tua app Amazon/corriere. Nessuna coda e massima flessibilità!"
```

---

### 3.4 Integrazione Tecnica con lo Storefront Shopify
* **Widget Fluttuante**: Snippet `whatsapp-widget.liquid` già integrato nel tema Dawn (in basso a destra, mobile responsive).
* **Messaggio Dinamico Precompilato**: Quando il cliente clicca il pulsante da una scheda prodotto, WhatsApp apre la conversazione precompilata:
  `"Ciao Andrea, vorrei informazioni su [Titolo Prodotto] (SKU: [SKU Prodotto]) visto su Just in Time"`
* **Pagina di Conferma Ordine (Thank You Page)**: Presenza del link:  
  *"Hai domande sul tuo ordine appena effettuato? Clicca qui per scrivere ad Andrea su WhatsApp indicando il tuo numero d'ordine"*.

---

## 4. Brand Voice, Tone of Voice e Linee Guida Editoriali

### 4.1 Identità & Personaggio
La voce del brand è quella di **Andrea Benegiamo**: il titolare, tecnico competente, appassionato di tecnologia e punto di riferimento fidato per le famiglie, i professionisti e gli studenti di Muro Leccese e del territorio circostante.

### 4.2 I Quattro Pilastri del Brand Voice
1. **Competenza Trasparente**: Andrea sa di cosa parla, spiega i motivi di una riparazione o di un consiglio d'acquisto senza nascondersi dietro formule commerciali ambigue.
2. **Semplicità e Chiarezza (Zero Fuffa)**: Evitare il gergo tecnico incomprensibile (es. "bus di memoria a 3200MHz in dual channel" diventa "memoria raddoppiata per farti aprire 20 schede senza rallentamenti").
3. **Calore e Prossimità Territoriale**: Andrea vive e lavora a Muro Leccese. Il tono è cordiale, diretto, educato e rassicurante, come un dialogo al banco del negozio.
4. **Onestà e Concretezza**: Se un computer vecchio non vale la pena di essere riparato, Andrea lo dice chiaramente al cliente proponendo la soluzione più economica o conveniente.

### 4.3 Matrice di Stile (Cosa dire vs Cosa evitare)

| Cosa Dire (In Target) | Cosa Evitare (Fuori Target) |
| :--- | :--- |
| "Non buttare il tuo vecchio PC: spesso basta un aggiornamento SSD per farlo tornare veloce come il primo giorno." | "Acquista ora per massimizzare il tuo throughput computazionale a benchmark record." |
| "Se hai dubbi, scrivimi su WhatsApp o passa in negozio in Via Corsica: vediamo insieme la soluzione migliore." | "Supporto clienti automatizzato tramite ticket system e chatbot." |
| "Notebook ricondizionato certificato: testato da noi con 25 controlli e coperto da 12 mesi di nostra garanzia diretta." | "Stock fallimentare a prezzi stracciati senza garanzia." |
| "Ritiro gratuito in negozio in 2 ore, oppure te lo portiamo a casa in 24 ore." | "Logistica esternalizzata con terzi parti non verificate." |

---

## 5. Piano Editoriale Operativo (Social Calendar Mensile - 4 Settimane)

Il calendario prevede **4 uscite settimanali fisse** (Lunedì, Mercoledì, Venerdì, Sabato) modulate sulle seguenti rubriche tematiche:
* **Lunedì (#IlConsiglioDelTecnico)**: Valore educativo, fiducia, trucchi e consigli pratici.
* **Mercoledì (#OccasioneDellaSettimana)**: Prodotto in vetrina, link shopping, focus convenienza e qualità.
* **Venerdì (#DietroLeQuinte)**: Laboratorio in azione, riparazioni, casi risolti, trasparenza.
* **Sabato (#WeekendInNegozio)**: Click & Collect locale, disponibilità immediata al banco, servizi utili.

---

### SETTIMANA 1: Fisiologia del PC & Ripartenza Rapida

#### Post 1 (Lunedì - Ore 13:30) | Rubrica: #IlConsiglioDelTecnico
* **Canale**: Instagram (Reel) + Facebook (Video con link)
* **Formato**: Reel verticale da 45 secondi
* **Regia & Visual**: Andrea in camicia o polo Just in Time al banco del laboratorio. Davanti a lui un vecchio hard disk meccanico e un nuovo SSD Kingston compatto. Tiene in mano l'hard disk, lo fa vedere e poi mostra la schermata del PC che si avvia in 10 secondi.
* **Copy per il post**:
  > Il tuo computer ci mette 5 minuti solo per aprirsi e farti navigare su Internet? 🐢  
  >   
  > Spesso pensiamo che un PC dopo 4 o 5 anni sia "da buttare". Nel 90% dei casi non è così: il vero collo di bottiglia è il vecchio disco rigido meccanico (l'hard disk a piattelli), che con il tempo si degrada e rallenta qualsiasi operazione.  
  >   
  > Con un semplice **aggiornamento a disco SSD**:  
  > ⚡ Il computer si avvia in meno di 15 secondi.  
  > ⚡ I programmi e i file si aprono istantaneamente.  
  > ⚡ Non perdi neanche una foto o un documento, perché nel nostro laboratorio cloniamo esattamente tutto ciò che hai.  
  >   
  > Portaci il tuo PC in Via Corsica 151 a Muro Leccese per una diagnosi gratuita dello stato del disco, oppure scopri il nostro pacchetto aggiornamento su: [Link Pacchetto Upgrade SSD]  
  >   
  > #JustInTime #MuroLeccese #RiparazionePC #ConsigliTech #Salento #AssistenzaComputer #Maglie #Poggiardo
* **Tag Prodotto**: `JIT-SRV-UPGRADE-SSD` (Pacchetto Upgrade SSD Kingston 480GB)
* **CTA**: "Scrivici su WhatsApp con il modello del tuo PC per verificare se è aggiornabile!"

---

#### Post 2 (Mercoledì - Ore 18:00) | Rubrica: #OccasioneDellaSettimana
* **Canale**: Instagram (Carosello 4 slide) + Facebook
* **Formato**: Carosello Grafico/Fotografico (Slide 1: Foto pulita del Lenovo ThinkPad T480 con badge "Grado A+"; Slide 2: Dettaglio tastiera retroilluminata e scocca in magnesio; Slide 3: Scheda tecnica sintetica; Slide 4: Garanzia 12 mesi e prezzo).
* **Copy per il post**:
  > Perché spendere 700€ per un computer economico in plastica fragile quando puoi avere una workstation aziendale a meno della metà? 💼  
  >   
  > Questa settimana in vetrina abbiamo un'occasione speciale: **Lenovo ThinkPad T480 Ricondizionato Grado A+**.  
  > Per chi non lo conoscesse, è il portatile aziendale per antonomasia: indistruttibile, tastiera con digitazione perfetta, scocca robusta e prestazioni impeccabili per lavoro, smart working e studio universitario.  
  >   
  > 🔍 **Caratteristiche principali**:  
  > • Processore Intel Core i5 Quad-Core  
  > • 16 GB di RAM (multitasking fluido senza blocchi)  
  > • Disco SSD ultraveloce da 256 GB  
  > • Schermo 14" Full HD antiriflesso  
  > • Doppia batteria per un'autonomia prolungata  
  > • **Garanzia 12 mesi Just in Time** direttamente nel nostro laboratorio  
  >   
  > 🏷️ Prezzo speciale: **289,00€** (anziché 349,00€). Solo 2 pezzi disponibili in negozio!  
  >   
  > Puoi acquistarlo online e ritirarlo subito al banco a Muro Leccese, o riceverlo a casa con spedizione assicurata.  
  > Tocca la foto per visualizzare i dettagli o scrivici in chat per bloccarlo!  
  >   
  > #ThinkPad #RicondizionatoGarantito #MuroLeccese #JustInTime #OfferteInformatica #SalentoTech #OccasioniLavoro
* **Tag Prodotto**: `JIT-THINKPAD-T480` (Notebook Lenovo ThinkPad T480)
* **CTA**: "Tocca i tag per acquistare o scrivici su WhatsApp per bloccare il tuo pezzo."

---

#### Post 3 (Venerdì - Ore 17:30) | Rubrica: #DietroLeQuinte
* **Canale**: Instagram (Reel) + Facebook
* **Formato**: Reel con riprese macro della pulizia interna ventola e sostituzione pasta termica.
* **Regia & Visual**: Ripresa dall'alto del banco da lavoro con luce tecnica. Si vede una ventola completamente intasata di polvere e la vecchia pasta termica secca. Poi montaggio dinamico con pulizia ad aria compressa, applicazione della nuova pasta termica argentata e test di temperatura a schermo che scende da 85°C a 42°C.
* **Copy per il post**:
  > Il tuo notebook diventa bollente e la ventola sembra un jet in fase di decollo? 🛫🔥  
  >   
  > Ecco cosa abbiamo trovato ieri aprendo questo portatile in laboratorio. Dopo 2-3 anni di utilizzo, polvere e pelucchi creano un vero e proprio "tappo" che impedisce all'aria di circolare. Inoltre la pasta termica, che trasferisce il calore dal processore al radiatore, si secca e perde efficacia.  
  >   
  > Il risultato? Il computer va in protezione termica, rallenta drasticamente per non bruciarsi e alla lunga rischia di danneggiare la scheda madre.  
  >   
  > Con una manutenzione completa in laboratorio:  
  > 🧽 Pulizia profonda e sanificazione del circuito di raffreddamento  
  > ❄️ Applicazione pasta termica professionale ad altissima conducibilità  
  > 🔇 Il PC torna silenzioso, fresco e scattante!  
  >   
  > Passa a trovarci in Via Corsica 151 a Muro Leccese per un controllo delle temperature.  
  >   
  > #LaboratorioInformatica #RiparazioniPC #MuroLeccese #ManutenzioneComputer #JustInTime #TecnicoDiFiducia #Salento
* **Tag Prodotto**: `JIT-SRV-DIAG-NOTE` (Servizio Diagnosi e Manutenzione Hardware Notebook)
* **CTA**: "Prenota una revisione del tuo notebook prima dell'estate o dei sessioni di studio!"

---

#### Post 4 (Sabato - Ore 10:30) | Rubrica: #WeekendInNegozio
* **Canale**: Instagram (Post Singolo + Story interattiva) + Facebook
* **Formato**: Foto reale del bancone di Just in Time con le shopping bag pronte e cartelli Click & Collect visibili.
* **Copy per il post**:
  > Sabato mattina: tempo di sbrigare commissioni e prepararsi per la settimana! ☀️  
  >   
  > Ti ricordiamo che sul nostro nuovo store online Just in Time puoi ordinare tutto ciò che ti serve comodamente dal divano e selezionare l'opzione **"Ritiro in sede a Muro Leccese"** al momento del checkout.  
  >   
  > I vantaggi?  
  > ✅ Zero spese di spedizione.  
  > ✅ Articoli riservati e preparati per te in massimo 2 ore.  
  > ✅ Puoi pagare online con carta/PayPal oppure saldare al banco al momento del ritiro (anche in contanti o bancomat).  
  > ✅ Consulenza diretta con Andrea per qualsiasi dubbio o configurazione.  
  >   
  > Siamo aperti oggi fino alle 13:00 e questo pomeriggio dalle 16:30 alle 20:00 in Via Corsica 151.  
  > Buon weekend a tutti!  
  >   
  > #ClickAndCollect #CommercioLocale #MuroLeccese #SpesaSottoCasa #JustInTime #ShoppingTerritoriale
* **Tag Prodotto**: `kit-wireless-logitech-mk270` (Kit Tastiera Mouse Logitech)
* **Story Interattiva**: Sondaggio: "Hai mai provato il ritiro al banco in 2 ore?" (Sì, comodissimo! / Ancora no, devo provare).

---

### SETTIMANA 2: Sicurezza Dati, Ufficio Smart e Pronti all'Uso

#### Post 5 (Lunedì - Ore 13:30) | Rubrica: #IlConsiglioDelTecnico
* **Canale**: Instagram (Carosello 5 slide) + Facebook
* **Formato**: Carosello Educational "3 errori da non fare mai con le tue foto e documenti di lavoro".
* **Contenuto**: Slide 1: Copertina impattante; Slide 2: Errore 1: Tenere i file solo sul desktop del PC; Slide 3: Errore 2: Usare una pennetta USB economica come unico backup (si bruciano all'improvviso!); Slide 4: Regola del 3-2-1 (copia locale + disco esterno + cloud); Slide 5: Come Just in Time ti aiuta a mettere al sicuro i tuoi ricordi.
* **Copy per il post**:
  > "Andrea, il computer non si accende più... dentro ho 10 anni di foto di famiglia e le fatture dell'ufficio! Si possono salvare?" 😰  
  >   
  > Questa è la frase che sentiamo più spesso in laboratorio e che ci stringe sempre il cuore. Troppo spesso pensiamo al backup solo *dopo* che il disco ha smesso di girare.  
  >   
  > Ecco 3 semplici regole d'oro da applicare oggi stesso:  
  > 1️⃣ La chiavetta USB non è un archivio sicuro: serve per trasportare file, non per conservarli a lungo termine.  
  > 2️⃣ Applica la regola del 3-2-1: 3 copie dei dati importanti, su 2 supporti differenti (es. PC + Hard Disk esterno dedicato), di cui 1 su cloud protetto.  
  > 3️⃣ Se il PC fa strani rumori metallici o si blocca all'avvio, SPEGNILO subito e non forzare riavvii continui per non graffiare i dischi magnetici.  
  >   
  > Se hai un disco danneggiato o vuoi configurare una procedura di salvataggio automatico senza pensieri, passa in laboratorio in Via Corsica 151 a Muro Leccese.  
  >   
  > #BackupDati #RecuperoDati #SicurezzaInformatica #MuroLeccese #JustInTime #ConsigliPratici
* **Tag Prodotto**: `JIT-SRV-FORMAT-STD` (Servizio Formattazione e Salvataggio Dati)
* **CTA**: "Salva questo post tra i preferiti per non dimenticarlo!"

---

#### Post 6 (Mercoledì - Ore 18:00) | Rubrica: #OccasioneDellaSettimana
* **Canale**: Instagram (Foto ambientata + Stories) + Facebook
* **Formato**: Foto di alta qualità del Notebook HP 250 G9 aperto su una scrivania ordinata con il packaging e il logo Just in Time.
* **Copy per il post**:
  > Se cerchi un notebook nuovo, veloce e solido per lavorare, gestire la contabilità o per lo studio, ecco la nostra prima scelta del mese: **HP 250 G9 15.6"**. 💻✨  
  >   
  > Niente processori lenti o plastiche scadenti: qui hai a disposizione un motore affidabile pronto per accompagnarti per i prossimi anni senza rallentamenti.  
  >   
  > ⚙️ **La nostra configurazione consigliata**:  
  > • Processore Intel Core i5 di 12a Generazione  
  > • Ben **16 GB di RAM** (niente blocchi anche con 50 documenti e tabelle aperte)  
  > • Disco SSD NVMe ultraveloce da 512 GB  
  > • Schermo 15.6'' Full HD antiriflesso  
  > • Windows 11 Pro già configurato e attivato  
  >   
  > 🛡️ **Il vantaggio esclusivo Just in Time**:  
  > Non ti consegniamo una scatola sigillata lasciandoti da solo tra configurazioni e aggiornamenti infiniti. Con la nostra opzione **"Zero Pensieri"**, prepariamo noi il computer: aggiornamenti installati, via programmi inutili precaricati, suite ufficio e antivirus configurati e, se lo desideri, trasferiamo tutti i tuoi dati dal vecchio computer!  
  >   
  > Disponibile subito in negozio a Muro Leccese o ordinabile online con spedizione rapida.  
  > Scoprilo cliccando sul tag prodotto o scrivici su WhatsApp!  
  >   
  > #NotebookHP #ComputerUfficio #MuroLeccese #SmartWorkingSalento #JustInTime #InformaticaFacile
* **Tag Prodotto**: `notebook-hp-250-g9-i5-16gb` (Notebook HP 250 G9 i5 16GB)
* **CTA**: "Disponibilità immediata in negozio: tocca il tag per scoprire il prezzo e la scheda completa."

---

#### Post 7 (Venerdì - Ore 17:30) | Rubrica: #DietroLeQuinte
* **Canale**: Instagram (Carosello Prima/Dopo) + Facebook
* **Formato**: Carousel Prima/Dopo di un PC desktop polveroso rimesso a nuovo con cablaggio ordinato, pulizia e nuovo SSD.
* **Copy per il post**:
  > Prima ➡️ Dopo: la trasformazione del venerdì in laboratorio! 🧼🔧  
  >   
  > Questo PC desktop ci è stato portato da un'azienda locale: si bloccava continuamente ed emetteva un forte rumore metallico.  
  >   
  > Ecco l'intervento eseguito da Andrea:  
  > 1. Smontaggio completo di alimentatore, dissipatore e ventole con pulizia a ultrasuoni e aria compressa.  
  > 2. Sostituzione pasta termica ceramica su processore e scheda video.  
  > 3. Eliminazione del vecchio hard disk difettoso e installazione di un SSD ad alte prestazioni.  
  > 4. Riorganizzazione completa dei cavi interni (cable management) per massimizzare il flusso d'aria fresca.  
  >   
  > Risultato? Silenziosità assoluta, temperature dimezzate e una macchina che ha ripreso a lavorare con la massima reattività, facendo risparmiare all'imprenditore il costo di una macchina nuova.  
  >   
  > La tecnologia va curata con passione e precisione artigianale. Ti aspettiamo in Via Corsica 151 a Muro Leccese per qualsiasi esigenza!  
  >   
  > #PrimaEDopo #RiparazioneHardware #MuroLeccese #LaboratorioTecnico #JustInTime #SostenibilitaTech
* **Tag Prodotto**: `servizio-diagnosi-riparazione-pc` (Diagnosi Guasto e Riparazione Hardware)
* **CTA**: "Hai un PC fisso che merita una rimessa a nuovo? Portacelo in negozio!"

---

#### Post 8 (Sabato - Ore 11:00) | Rubrica: #WeekendInNegozio
* **Canale**: Instagram (Post con grafica chiara) + Facebook
* **Formato**: Foto di Andrea con cartucce Epson e toner HP in mano, sorridente al banco.
* **Copy per il post**:
  > Quante volte capita di dover stampare un documento urgente il sabato mattina e... la stampante segnala "Livello inchiostro esaurito"? 🖨️🤦‍♂️  
  >   
  > Da Just in Time a Muro Leccese abbiamo un assortimento completo di **cartucce e toner originali e compatibili di alta qualità** per tutti i principali marchi: HP, Epson, Canon, Brother e Samsung.  
  >   
  > Non sei sicuro del modello esatto?  
  > Nessun problema:  
  > 📸 Fai una foto alla tua vecchia cartuccia o all'etichetta frontale della stampante.  
  > 📲 Mandacela su WhatsApp al 320 6025789.  
  > Ti confermeremo in 2 minuti se è disponibile a banco per il ritiro immediato!  
  >   
  > E per i formati più diffusi, puoi anche ordinare la tua scorta sul nostro shop online e ritirarla quando passi da Via Corsica 151.  
  >   
  > Siamo aperti oggi fino alle 13:00 e dalle 16:30 alle 20:00!  
  >   
  > #CartucceStampante #TonerHP #Inchiostri #MuroLeccese #JustInTime #StampaFacile #UfficioSalento
* **Tag Prodotto**: `toner-compatibile-hp-106a-w1106a` & `multipack-cartucce-epson-603xl-compatibile`
* **CTA**: "Hai bisogno di cartucce? Mandaci una foto del modello su WhatsApp!"

---

### SETTIMANA 3: Scuola, Studio e Cancelleria Intelligente

#### Post 9 (Lunedì - Ore 13:30) | Rubrica: #IlConsiglioDelTecnico
* **Canale**: Instagram (Reel) + Facebook
* **Formato**: Reel con Andrea che mostra come configurare un account protetto per i figli su Windows 11 (Family Safety) per evitare installazione di malware e acquisti accidentali.
* **Copy per il post**:
  > Tuo figlio usa il PC di casa per le ricerche scolastiche o per giocare? Ecco come proteggerlo (e proteggere i tuoi file di lavoro!) in soli 2 minuti 🛡️👦  
  >   
  > L'errore più comune è far utilizzare il computer con un unico account Amministratore condiviso. Bastano due clic sbagliati su un link per scaricare virus, estensioni pubblicitarie o cancellare cartelle importanti.  
  >   
  > Nel video di oggi Andrea ti mostra:  
  > 1. Come creare un account utente standard dedicato a tuo figlio.  
  > 2. Come attivare i filtri di navigazione per bloccare contenuti non adatti all'età.  
  > 3. Come impedire l'installazione di programmi senza l'inserimento del tuo PIN.  
  >   
  > Hai bisogno di una configurazione sicura o di un antivirus affidabile? Passa a trovarci in Via Corsica 151 a Muro Leccese, ti aiuteremo a configurare tutto a regola d'arte!  
  >   
  > #SicurezzaBambini #GenitoriSmart #Windows11 #MuroLeccese #JustInTime #ConsigliDelTecnico #ScuolaDigitale
* **CTA**: "Condividi questo video con un genitore a cui può essere utile!"

---

#### Post 10 (Mercoledì - Ore 18:00) | Rubrica: #OccasioneDellaSettimana
* **Canale**: Instagram (Post Carosello) + Facebook
* **Formato**: Carosello con Kit Logitech Wireless MK270 abbinato a mousepad ergonomico e risme di carta Fabriano Copy 2.
* **Copy per il post**:
  > La tua scrivania è soffocata da una giungla di cavi disordinati? Libera spazio e lavora in totale comodità! ⌨️🖱️  
  >   
  > Il **Kit Wireless Logitech MK270** è la soluzione più affidabile ed economica scelta da centinaia di nostri clienti per l'ufficio e la casa:  
  > 🔹 Connessione wireless a 2.4 GHz stabile fino a 10 metri senza alcun ritardo.  
  > 🔹 Un unico micro-ricevitore USB per mouse e tastiera (basta inserirlo ed è subito pronto).  
  > 🔹 Durata delle batterie straordinaria: fino a 36 mesi per la tastiera e 12 mesi per il mouse!  
  > 🔹 Tasti multimediali rapidi per volume, calcolatrice e musica.  
  >   
  > 🏷️ In offerta speciale su Just in Time a soli **29,90€**!  
  >   
  > Abbinalo alla nostra scorta di carta Fabriano Copy 2 (5 risme a soli 22,50€) e ritira tutto al banco a Muro Leccese senza costi di spedizione.  
  > Ordina online dal tag prodotto e passa a trovarci quando ti è più comodo!  
  >   
  > #Logitech #UfficioOrdinato #MuroLeccese #AccessoriPC #JustInTime #CancelleriaSalento
* **Tag Prodotto**: `kit-wireless-logitech-mk270` & `carta-a4-fabriano-copy-2-box-5-risme`
* **CTA**: "Tocca i prodotti per acquistare con ritiro immediato in sede!"

---

#### Post 11 (Venerdì - Ore 17:30) | Rubrica: #DietroLeQuinte
* **Canale**: Instagram (Reel) + Facebook
* **Formato**: Reel con Andrea che mostra il macchinario Colibrì System in azione per ricoprire un libro scolastico in 20 secondi.
* **Copy per il post**:
  > Ricordate quando per foderare i libri di scuola si usavano chilometri di scotch, forbici storte e rotoli adesivi pieni di bolle d'aria? 😅✂️  
  >   
  > Quei tempi sono finiti! Da Just in Time a Muro Leccese utilizziamo il sistema ufficiale **Colibrì System**:  
  > 📚 Copertine su misura per qualsiasi formato di libro (anche dizionari ed atlanti).  
  > 🛡️ Pellicola trasparente ultra-resistente, morbida al tatto e igienizzabile.  
  > ✂️ Saldatura termica perfetta senza usare un millimetro di colla: non rovina la copertina originale e si può rimuovere a fine anno scolastico!  
  >   
  > Ti ricordiamo che il nostro servizio di **prenotazione libri scolastici** per medie e superiori è attivo tutto l'anno con anticipo zero: puoi ordinare i tuoi testi, richiedere la copertinatura e ritirare tutto comodamente al banco.  
  >   
  > Scrivici su WhatsApp per info o ordini!  
  >   
  > #ColibriSystem #LibriScolastici #MuroLeccese #ScuolaSalento #JustInTime #CopertineLibri #Maglie #Poggiardo
* **Tag Prodotto**: `prenotazione-libri-scolastici` (Servizio Prenotazione Libri di Testo)
* **CTA**: "Inviaci la lista dei tuoi libri su WhatsApp per prenotarli in anticipo senza code!"

---

#### Post 12 (Sabato - Ore 10:30) | Rubrica: #WeekendInNegozio
* **Canale**: Instagram (Post Singolo) + Facebook
* **Formato**: Foto d'insieme della corsia scuola e ufficio con zaini, quaderni, penne e calcolatrici scientifiche.
* **Copy per il post**:
  > Dalla penna per gli appunti al notebook per la tesi di laurea: tutto ciò che serve al tuo studio e al tuo lavoro lo trovi a due passi da casa! 🎒✏️💻  
  >   
  > Just in Time non è solo informatica avanzata, ma il tuo punto di riferimento completo a Muro Leccese per:  
  > 📌 Cancelleria di qualità (Fabriano, Pilot, Stabilo, Oxford).  
  > 📌 Stampa documenti, fotocopie e invio file via email/WhatsApp.  
  > 📌 Fermopoint e Amazon Hub per ritirare i tuoi acquisti online.  
  > 📌 Assistenza e consulenza informatica personalizzata.  
  >   
  > Siamo aperti oggi in Via Corsica 151:  
  > 🕘 Mattina: 08:30 - 13:00  
  > 🕓 Pomeriggio: 16:30 - 20:00  
  >   
  > Passa a salutarci o ordina su: [Link Storefront Shopify] per il ritiro express!  
  >   
  > #CommercioDiProssimita #MuroLeccese #JustInTime #ScuolaEUfficio #SalentoServizi
* **CTA**: "Vieni a trovarci in negozio o scrivici per verificare la disponibilità dei tuoi articoli!"

---

### SETTIMANA 4: Efficienza Aziendale, PMI Locali e Supporto Continuo

#### Post 13 (Lunedì - Ore 13:30) | Rubrica: #IlConsiglioDelTecnico
* **Canale**: Instagram (Carosello 4 slide) + Facebook
* **Formato**: Carosello dedicato a commercianti, studi professionali e artigiani del Salento.
* **Titolo Cover**: "La tua stampante in ufficio stampa a righe o macchia i fogli? Ecco come risolvere."
* **Contenuto**: Guida pratica: 1. Ciclo di pulizia testine software; 2. Controllo rullo tamburo nei toner laser; 3. Perché usare consumabili testati evita danni ai meccanismi di trascinamento; 4. Come Just in Time fornisce forniture periodiche a canone agevolato per uffici e aziende locali.
* **Copy per il post**:
  > Per uno studio o un'attività commerciale, una stampante che si blocca prima di una consegna importante è un incubo 📄❌  
  >   
  > La maggior parte dei difetti di stampa (righe bianche, aloni neri o fogli incastrati) è dovuta a:  
  > 🔹 Inchiostro secco negli ugelli dopo periodi di inutilizzo (basta una pulizia profonda mirata).  
  > 🔹 Toner di qualità scadente che perdono polvere sui rulli di caricamento.  
  > 🔹 Risme di carta umida o con troppa grammatura che frena i rulli.  
  >   
  > In negozio a Muro Leccese testiamo ogni lotto di toner e cartucce per garantire massima brillantezza e zero residui. E se hai un'attività nel Salento, possiamo gestire noi la fornitura programmata di consumabili e carta, consegnandotela direttamente o preparandotela per il ritiro rapido.  
  >   
  > Contattaci su WhatsApp per una quotazione aziendale personalizzata!  
  >   
  > #UfficioSalento #ConsigliStampa #MuroLeccese #PMISalento #JustInTime #FornitureUfficio
* **Tag Prodotto**: `toner-compatibile-hp-106a-w1106a`
* **CTA**: "Chiedici una fornitura per il tuo ufficio con fattura elettronica immediata!"

---

#### Post 14 (Mercoledì - Ore 18:00) | Rubrica: #OccasioneDellaSettimana
* **Canale**: Instagram (Reel veloce da 30s) + Facebook
* **Formato**: Reel con focus sul disco SSD Kingston A400 480GB: unbox, dettagli connettore SATA 3 e confronto dimensioni.
* **Copy per il post**:
  > Il miglior investimento tecnologico con meno di 40 euro? Questo piccolo disco qui! ⚡📦  
  >   
  > Si chiama **Kingston A400 SSD 480GB** ed è il componente più richiesto nel nostro laboratorio di Muro Leccese.  
  >   
  > Perché fa la differenza?  
  > 🚀 Velocità di lettura fino a 500 MB/s (10 volte più veloce dei vecchi dischi meccanici).  
  > 🔇 Zero rumore, zero parti meccaniche in movimento, resistenza a urti e vibrazioni.  
  > 🔋 Consuma meno batteria se montato su un notebook.  
  >   
  > Disponibile subito a banco e sul nostro e-commerce a soli **39,90€** (prezzo lancio).  
  > Se sei capace di montarlo da solo, lo ritiri e lo installi in 10 minuti. Se invece vuoi che ce ne occupiamo noi con clonazione completa di tutti i tuoi dati, ci pensiamo in laboratorio in 24 ore!  
  >   
  > Ordinalo online toccando il tag o vieni a ritirarlo in Via Corsica 151.  
  >   
  > #KingstonSSD #UpgradePC #MuroLeccese #VelocizzareComputer #JustInTime #SalentoTech
* **Tag Prodotto**: `kingston-a400-ssd-480gb` (SSD Kingston A400 480GB)
* **CTA**: "Tocca il prodotto per acquistarlo o scrivici per abbinare l'installazione in laboratorio!"

---

#### Post 15 (Venerdì - Ore 17:30) | Rubrica: #DietroLeQuinte
* **Canale**: Instagram (Foto Storytelling) + Facebook
* **Formato**: Foto di Andrea con un cliente sorridente al banco (con liberatoria) mentre ritira il proprio PC riparato.
* **Copy per il post**:
  > La soddisfazione più grande del nostro lavoro? Vedere il sollievo negli occhi dei nostri clienti quando riconsegniamo un computer dato per "spacciato" perfettamente funzionante! 😊💻  
  >   
  > Questa mattina il signor Marco di Maglie è passato a ritirare il suo portatile, portato in laboratorio mercoledì con schermo nero dopo una caduta accidentale.  
  >   
  > Abbiamo sostituito il pannello LCD con un ricambio originale ad alta luminosità, eseguito i test di stabilità e riallineato le cerniere. Il tutto in meno di 48 ore e a una frazione del costo di un PC nuovo.  
  >   
  > Da Just in Time la tecnologia è prima di tutto un rapporto umano di fiducia e trasparenza: preventivo chiaro prima di cominciare, nessuna sorpresa sul prezzo finale e pezzi garantiti.  
  >   
  > Grazie a tutti voi per la fiducia che ci rinnovate ogni giorno a Muro Leccese e in tutto il Salento!  
  >   
  > #RecensioniClienti #Fiducia #MuroLeccese #Maglie #RiparazioniSalento #JustInTime #TecnicoInformatico
* **CTA**: "Hai avuto un problema simile? Scrivici su WhatsApp per una prima consulenza gratuita!"

---

#### Post 16 (Sabato - Ore 10:30) | Rubrica: #WeekendInNegozio
* **Canale**: Instagram (Post Grafico Riepilogo) + Facebook
* **Formato**: Grafica con la mappa stilizzata del Salento centrale e il punto focale a Muro Leccese con le icone dei servizi (Store Online, Click & Collect 2h, Spedizioni Espresse, WhatsApp Diretto).
* **Copy per il post**:
  > Il tuo negozio di tecnologia sotto casa, ora anche online 24 ore su 24! 🌐📍  
  >   
  > Che tu ti trovi a Muro Leccese, Maglie, Scorrano, Poggiardo, Cutrofiano, Otranto o in qualsiasi altro comune salentino, **Just in Time** è sempre con te:  
  >   
  > 🛒 **Store Online**: [Link Storefront Shopify]  
  > 📦 **Click & Collect Gratuito**: ordini online, salti la fila e ritiri in negozio quando vuoi.  
  > 🚚 **Spedizioni Espresse**: consegne rapide e sicure in 24/48 ore direttamente a casa tua o in ufficio.  
  > 💬 **WhatsApp Sempre Attivo**: risposte rapide da parte del nostro staff tecnico per qualsiasi informazione al 320 6025789.  
  >   
  > Passa a trovarci oggi in Via Corsica 151 a Muro Leccese: siamo aperti fino alle 13:00 e dalle 16:30 alle 20:00.  
  > Vi auguriamo un sereno e tecnologico fine settimana!  
  >   
  > #JustInTime #MuroLeccese #Salento #ECommerceLocale #TecnologiaDiProssimita #PhygitalStore
* **CTA**: "Salva il nostro numero WhatsApp in rubrica: potremmo servirti quando meno te lo aspetti!"

---

## 6. Calendario Lanci Promozionali Locali & Campagne Stagionali (Roadmap Annuale)

| Periodo | Nome Campagna | Focus Prodotti / Servizi | Meccanica Promozionale & Social |
| :--- | :--- | :--- | :--- |
| **Marzo - Maggio (Primavera)** | **"Rottama la Lentezza" (Spring Tech Upgrade)** | Pacchetto Upgrade SSD + Manutenzione PC + Notebook Ricondizionati | Campagna Reel con video comparativi di velocità prima/dopo. Buono sconto di 10€ sull'upgrade portando un vecchio computer o notebook. |
| **Luglio - Settembre (Estate / Autunno)** | **"Back to School & University Zero Code"** | Prenotazione Libri Scolastici, Copertine Colibrì, Zaini, Cancelleria, Notebook per studenti | Anticipo zero sui libri scolastici. Chi ordina la lista completa riceve il 15% di sconto su cancelleria e zaini + 20€ di buono per l'acquisto di un notebook. |
| **Novembre (Black Friday)** | **"Black Friday di Prossimità"** | Notebook HP nuovi, ThinkPad ricondizionati, stampanti, kit wireless | Offerte reali e trasparenti a quantità limitata con ritiro prioritario in negozio. Post con countdown e prenotazione in anteprima via WhatsApp. |
| **Dicembre (Natale)** | **"Regala Tecnologia Utile con Assistenza Inclusa"** | Notebook "Zero Pensieri", periferiche gaming, accessori tech, gift card Just in Time | Consegna con pacchetto regalo e configurazione già inclusa. Slogan: "Lo scarta sotto l'albero ed è già pronto per giocare o lavorare". |

---

## 7. Local Marketing & Google Business Profile Playbook

### 7.1 Ottimizzazione Scheda Google Business Profile (Google Maps)
La scheda *Just in Time di Benegiamo Andrea* (Via Corsica 151, Muro Leccese) rappresenta la prima porta d'accesso per chi cerca servizi nel raggio di 20 km.
1. **Pulsante Sito Web**: Puntamento diretto all'indirizzo dell'e-commerce Shopify.
2. **Sezione Prodotti di Google Maps**: Inserimento manuale/sincronizzato dei 10 bestseller (con foto, prezzo e link al checkout Shopify).
3. **Post Novità Settimanali su Google Maps**: Ripubblicazione automatica dei contenuti della rubrica `#IlConsiglioDelTecnico` e `#OccasioneDellaSettimana` per intercettare le ricerche organiche locali (es. "riparazione notebook Muro Leccese", "vendita computer usati Maglie", "cartucce stampante Poggiardo").

---

### 7.2 Il Funnel di Riprova Sociale: Recensioni a 5 Stelle
La fiducia è il fattore determinante per competere con i marketplace globali.
* **Review Booster al Banco Cassa**:
  * Espositore in plexiglass con QR code diretto alla scheda Google:  
    *"Ti sei trovato bene con Andrea? Inquadra e lascia una recensione a 5 stelle: per noi vale tantissimo!"*
  * Al momento del saldo, Andrea o il collaboratore invita calorosamente il cliente a lasciare due righe di feedback.
* **Follow-up Automatico WhatsApp / Email Post-Ritiro**:
  * 24 ore dopo il ritiro di una riparazione o di un ordine Click & Collect, viene inviato un messaggio automatico:  
    *"Ciao [Nome]! Come ti trovi con il tuo acquisto / con il tuo computer riparato? Se sei soddisfatto, ci faresti un regalo enorme lasciandoci una recensione qui: [Link Diretto Google Review]. Grazie da Andrea e dal team Just in Time!"*

---

### 7.3 Micro-Campagne Meta Ads Geotargettizzate (Micro-Budget €3-5/giorno)
Per amplificare i contenuti a fronte di una spesa contenuta e sostenibile:

```
+---------------------------------------------------------------------------------------+
| TARGETING GEOGRAFICO: Raggio 15 km da Muro Leccese                                    |
| Comuni inclusi: Muro Leccese, Maglie, Poggiardo, Scorrano, San Cassiano,              |
|                 Cutrofiano, Otranto, Cursi, Corigliano d'Otranto, Tricase             |
| Età: 25 - 64 anni | Interessi: Computer, Informatica, Piccola Impresa, Genitori       |
+---------------------------------------------------------------------------------------+
```

* **Campagna Always-On A (Lead Generation WhatsApp / Laboratorio)**:
  * Budget: 2,00€/giorno.
  * Creatività: Video Reel di Andrea sull'Upgrade SSD o sulla riparazione rapida.
  * Obiettivo: Clic sul pulsante WhatsApp per richiedere diagnosi o disponibilità.
* **Campagna Always-On B (Catalogo Vendita / Click & Collect)**:
  * Budget: 2,00€/giorno.
  * Creatività: Carosello dinamico del catalogo Shopify con i prodotti disponibili a banco.
  * Obiettivo: Traffico qualificato allo store Shopify con preferenza per il ritiro in sede.

---

## 8. Flusso di Approvazione e Governance ("Human-in-the-Loop")

In conformità al ruolo del Social Media Manager e alle direttive operative di Just in Time:
1. **Preparazione Batch Settimanale**: Il Social Media Manager predispone entro ogni giovedì i copy, le indicazioni visual, i tag prodotto e le risposte rapide per la settimana successiva.
2. **Revisione e Approvazione del Titolare**: Andrea Benegiamo visiona le bozze con 1 tap da smartphone su Meta Business Suite o via documento di riepilogo.
3. **Nessuna Pubblicazione Automatica Non Visionata**: Nessun post promozionale, offerta straordinaria o risposta a recensioni delicate viene pubblicata senza l'esplicito benestare di Andrea.
4. **Monitoraggio e Reportistica**: A fine mese viene generato un report sintetico contenente:
   * Numero di clic generati verso lo store Shopify da Instagram e Facebook.
   * Numero di conversazioni WhatsApp aperte tramite i pulsanti prodotto.
   * Ordini Click & Collect finalizzati con attribuzione social.

---

*Documento archiviato con successo nella repository ufficiale del progetto: `docs/SAN-10_flussi_social_commerce_e_whatsapp.md`.*
