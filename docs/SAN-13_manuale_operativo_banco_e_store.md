# SAN-13: Manuale Operativo di Gestione Store Shopify al Banco
## Guida Quotidiana e Procedure Standard per Andrea Benegiamo
**Punto Vendita e Laboratorio**: Just in Time — Via Corsica 151, 73036 Muro Leccese (LE)  
**Data di Rilascio**: 24 Ottobre 2026  
**Autore / Ruolo**: Online Store Operator (`worker-pam-operations`)  
**Codice Task**: SAN-13  
**Stato**: Approvato per Esercizio Operativo (Fase 4 - Go-Live)  

---

```
=========================================================================================
                           JUST IN TIME - MURO LECCESE (LE)
                  MANUALE OPERATIVO GESTIONE STORE SHOPIFY & BANCO
=========================================================================================
 Destinatari: Andrea Benegiamo (Titolare) & Addetti al Banco
 Recapiti Store: Tel & WhatsApp: +39 320 602 5789 | Email: info@justintimemuro.it
 Orari Negozio: Lun-Sab 08:30-13:00 / 16:30-20:00 (Giovedì pomeriggio e Domenica CHIUSO)
 Piattaforma: Shopify Store Admin (Desktop & App Mobile iOS/Android)
=========================================================================================
```

---

## 1. Introduzione & Ruolo dell'Omnicanalità Phygital

Il presente manuale è la guida pratica da tenere sempre a portata di mano al banco di **Via Corsica 151 a Muro Leccese**. Descrive in modo chiaro, sequenziale e senza gergo superfluo tutte le operazioni quotidiane necessarie per gestire lo store online Shopify in perfetta sinergia con il punto vendita fisico, il laboratorio di assistenza e i servizi integrati (Amazon Counter, MEPA, fornitura scuole e consumabili).

### La Regola d'Oro di Just in Time
> **"L'Informatica con il Tuo Tecnico di Fiducia a Portata di Click"**  
> Per il cliente di Muro Leccese e del Salento, lo store online non è un'entità astratta: è la vetrina digitale del banco di Andrea. La rapidità nel preparare l'ordine Click & Collect (entro 2 ore lavorative), la cura nell'imballaggio e la disponibilità umana al banco rappresentano il nostro vantaggio competitivo assoluto rispetto ai giganti del commercio elettronico.

---

## 2. La Routine Quotidiana di Gestione

Una corretta gestione richiede pochi minuti al giorno, suddivisi in tre momenti chiave:

```
+---------------------------------------------------------------------------------------+
|                               ROUTINE QUOTIDIANA AL BANCO                             |
+---------------------------------------------------------------------------------------+
|  08:30 - APERTURA MATTINA (10 min)                                                    |
|  - Accensione PC banco e apertura tab Shopify Admin (https://admin.shopify.com)       |
|  - Controllo ordini ricevuti durante la notte su Shopify Admin                        |
|  - Controllo messaggi WhatsApp Business (+39 320 602 5789)                            |
|  - Ispezione rapida scorte fisiche dei prodotti ad alta rotazione                     |
+---------------------------------------------------------------------------------------+
|  GIORNATA DI VENDITA & BANCO (08:30-13:00 / 16:30-20:00)                              |
|  - Presidio notifiche sonore / push su app mobile Shopify                             |
|  - Lavorazione ordini Click & Collect entro 2 ore dalla ricezione                     |
|  - Imballaggio spedizioni nazionali e consegna al corriere pomeridiano (SDA/GLS/BRT)  |
|  - Scarico immediato dal gestionale/Shopify dei pezzi venduti al banco fisico         |
+---------------------------------------------------------------------------------------+
|  20:00 - CHIUSURA SERA (10 min)                                                        |
|  - Riconciliazione ordini evasi e verifica ordini ancora in attesa di ritiro          |
|  - Chiusura cassa fisica (POS + Contanti) e quadrature corrispettivi fiscali          |
|  - Attivazione messaggio di assenza su WhatsApp Business                              |
+---------------------------------------------------------------------------------------+
```

---

## 3. Workflow 1: Ricezione Ordine & Smistamento Immediato

Appena un cliente conclude un ordine sul sito Shopify, il sistema emette una notifica sonora sull'App Mobile Shopify e invia un'email all'indirizzo del negozio (`info@justintimemuro.it`).

### 3.1 Come interpretare la schermata dell'ordine su Shopify

Accedere a **Shopify Admin > Ordini** (`Orders`):

```
+-------------------------------------------------------------------------------------+
| Ordine #JIT-1042                                          Data: 24/10/2026, 09:15   |
| Cliente: Mario Rossi (Muro Leccese) - Cell: 340 1234567                             |
+-------------------------------------------------------------------------------------+
| Articoli ordinati:                                                                  |
| 1x Toner Compatibile Certificato HP 106A (W1106A) con Chip           € 24,90       |
| 1x Box 5 Risme Carta A4 Navigator Universal 80g                     € 26,50       |
+-------------------------------------------------------------------------------------+
| Stato Finanziario:      [ PAGATO ] (Shopify Payments / Carta di Credito)            |
|                         oppure                                                      |
|                         [ IN SOSPESO ] (Pagamento al ritiro in negozio)             |
|                                                                                     |
| Metodo di Consegna:     [ RITIRO IN NEGOZIO ] (Click & Collect Via Corsica 151)     |
|                         oppure                                                      |
|                         [ DA SPEDIRE ] (Spedizione Standard Corriere - Indirizzo)   |
+-------------------------------------------------------------------------------------+
```

### 3.2 Albero Decisionale di Smistamento

```
                           [ NUOVO ORDINE RICEVUTO ]
                                       |
                                       v
                     +-----------------------------------+
                     | Qual è la modalità di consegna?   |
                     +-----------------------------------+
                               /               \
                              /                 \
                             v                   v
              [ RITIRO IN SEDE ]            [ SPEDIZIONE CORRIERE ]
             (Click & Collect)              (Nazionale / Fuori Zona)
                     |                                   |
                     v                                   v
             Vedi WORKFLOW 2                     Vedi WORKFLOW 3
             (Prep. entro 2h)                    (Lettera di Vettura)
```

---

## 4. Workflow 2: Ritiro in Negozio (Click & Collect a Muro Leccese)

Il Click & Collect è il cuore della fiducia locale. Il cliente si aspetta che il prodotto sia pronto quando entra in negozio.

### Fasi Operative Dettagliate

#### Fase 2.1 — Prelievo a scaffale (Picking)
1. Stampare il riepilogo ordine (o consultarlo dallo smartphone/PC).
2. Recarsi allo scaffale o nel magazzino retrostante e prelevare gli articoli corrispondenti verificando attentamente:
   * **Codice cartuccia / toner**: verificare che la sigla corrisponda esattamente (es. HP 106A vs HP 107A).
   * **Notebook o PC**: verificare che sia la versione richiesta dal cliente (es. *Base* vs *Pacchetto Zero Pensieri con travaso dati*).
   * **Cancelleria**: verificare l'integrità delle confezioni e delle risme di carta.

#### Fase 2.2 — Confezionamento e Allocazione nel Rack Dedicato
1. Inserire gli articoli in una busta o scatola Just in Time.
2. Applicare una fascetta o post-it con:
   * **Numero Ordine** (es. `#JIT-1042`)
   * **Nome e Cognome Cliente** (es. *Mario Rossi*)
   * **Stato Pagamento**: `GIÀ PAGATO ONLINE` oppure `DA INCASSARE AL BANCO: € 51,40`.
3. Riporre la busta nello scaffale retro-banco **"RACK CLICK & COLLECT"**, ordinato alfabeticamente o per numero ordine.

#### Fase 2.3 — Notifica di "Pronto per il Ritiro" su Shopify
1. Su Shopify Admin aprire l'ordine `#JIT-1042`.
2. Nella sezione di evasione ritiro, cliccare sul pulsante **Segna come pronto per il ritiro** (`Ready for pickup`).
3. Il sistema invia istantaneamente al cliente un'email e un SMS automatici con le indicazioni di ritiro e gli orari di apertura del negozio.

#### Fase 2.4 — Messaggio WhatsApp di Cortesia (Best Practice di Fiducia)
Per dare un tocco personale tipico di Just in Time, inviare un messaggio WhatsApp rapido con il cellulare aziendale utilizzando la risposta rapida preimpostata `/ritiro`:

> *"Ciao Mario! Il tuo ordine Just in Time #JIT-1042 è pronto per essere ritirato al banco in Via Corsica 151 a Muro Leccese 📦. Puoi passare quando ti è più comodo negli orari di apertura (08:30-13:00 / 16:30-20:00). A tra poco!"*

#### Fase 2.5 — Accoglienza del Cliente e Consegna al Banco
1. Quando il cliente entra e dichiara il nome o mostra il messaggio:
   * Recuperare la busta dal Rack Click & Collect.
2. **Gestione del Pagamento**:
   * **Se l'ordine è già pagato online**: non richiedere alcun pagamento.
   * **Se l'ordine era "Pagamento al Ritiro"**:
     * Chiedere se preferisce contanti o carta/Bancomat (POS al banco).
     * Battere il documento commerciale (scontrino fiscale telematico) dal registratore di cassa per l'importo corrispondente.
3. Se l'ordine include materiale informatico o notebook, ricordare: *"Hai la garanzia diretta con noi: per qualsiasi dubbio sull'installazione o configurazione, chiamaci o scrivici su WhatsApp!"*.

#### Fase 2.6 — Chiusura dell'Ordine su Shopify
1. Riaprire l'ordine su Shopify Admin.
2. Cliccare su **Segna come ritirato** (`Mark as picked up`).
3. Se era previsto il pagamento al banco, cliccare su **Incassa pagamento** (`Collect payment` > `Mark as paid`).
4. L'ordine passa automaticamente allo stato **Evaso** (`Fulfilled`).

---

## 5. Workflow 3: Evasione Spedizioni con Corriere Espresso

Questo flusso si applica agli ordini con destinazione al di fuori dell'area di Muro Leccese o per clienti che hanno richiesto la spedizione a domicilio (tariffa fissa €6,90, gratuita sopra €79,00).

```
+------------------------------------------------------------------------------------+
|                  WORKFLOW SPEDIZIONE CORRIERE ESPRESSO (SDA/GLS/BRT)               |
+------------------------------------------------------------------------------------+
| 1. Controllo Pagamento -> L'ordine deve essere rigorosamente [ PAGATO ONLINE ]     |
| 2. Preparazione Collo   -> Imballaggio anti-urto protettivo specifico per categoria |
| 3. Creazione LDV        -> Generazione Lettera di Vettura su portale corriere      |
| 4. Evasione Shopify     -> Inserimento Tracking Number e click su "Evadi Articoli"  |
| 5. Consegna al Driver   -> Firma borderò passaggio corriere pomeridiano (ore 17:00)|
+------------------------------------------------------------------------------------+
```

### 5.1 Regole di Imballaggio Tecnico (Standard di Sicurezza Just in Time)
* **Notebook e PC**: 
  * Utilizzare scatola rigida a doppia onda con almeno 5 cm di materiale ammortizzante (pluriball o cuscini d'aria) su tutti i lati.
  * Assicurarsi che l'alimentatore e il cavo di alimentazione siano separati dallo chassis del PC per evitare graffi sullo schermo o sulla scocca.
  * Apporre nastro da imballaggio di sicurezza e adesivo *"FRAGILE - APPARECCHIATURA ELETTRONICA"*.
* **Toner e Cartucce**:
  * Inserire ogni cartuccia o toner in una busta di plastica sigillata prima dell'imballo esterno, per scongiurare qualsiasi dispersione accidentale di polvere o inchiostro in caso di schiacciamento del pacco durante il trasporto.
* **Cancelleria e Risme**:
  * Proteggere gli angoli delle scatole di carta con paraspigoli di cartone rigido.

### 5.2 Generazione Lettera di Vettura (LDV)
1. Accedere al portale web del corriere espresso convenzionato (SDA, GLS o BRT).
2. Inserire i dati del destinatario copiandoli fedelmente dalla schermata dell'ordine Shopify:
   * Nome, Cognome, Indirizzo completo (con frazione, scala, interno se specificati).
   * Numero di cellulare del cliente (fondamentale per il preavviso di consegna tramite SMS).
   * Peso e dimensioni del collo.
3. Stampare la Lettera di Vettura adesiva e applicarla saldamente sul lato superiore del pacco, evitando di coprire i codici a barre con nastro adesivo riflettente.

### 5.3 Registrazione del Tracciamento su Shopify
1. Nella pagina dell'ordine su Shopify Admin, cliccare su **Evadi articoli** (`Fulfill items`).
2. Nel campo **Corriere**, selezionare il vettore (es. *GLS Italy*, *SDA*, *BRT*).
3. Nel campo **Codice di tracciamento** (`Tracking number`), incollare il codice LDV.
4. Lasciare spuntata la casella: ☑ *Invia dettagli di spedizione al cliente adesso*.
5. Cliccare su **Evadi articoli**.
6. Il cliente riceverà automaticamente l'email con il link diretto per seguire il percorso del pacco in tempo reale.

---

## 6. Workflow 4: Gestione Resi, Garanzie e Sostituzioni

La gestione tempestiva ed empatica di un problema tecnico trasforma un cliente dubbioso in un cliente fedele a vita.

```
+--------------------------------------------------------------------------------------+
|                     QUADRO NORMATIVO & GARANZIE JUST IN TIME                         |
+--------------------------------------------------------------------------------------+
| - Diritto di Recesso (Ripensamento): 14 giorni solari dalla consegna/ritiro          |
| - Garanzia Legale Privati (Codice del Consumo): 24 mesi su difetti di conformità    |
| - Garanzia Acquisti Professionali (P.IVA): 12 mesi                                   |
| - Garanzia Prodotti Ricondizionati Certificati Grado A+: 12 mesi diretta negozio     |
+--------------------------------------------------------------------------------------+
```

### 6.1 Protocollo Specifico TONER & CARTUCCE

I problemi più comuni riscontrati dagli utenti sui consumabili di stampa sono:
1. *Chip non riconosciuto dalla stampante* (messaggio di errore su display).
2. *Stampa sbiadita o righe orizzontali/verticali ripetute*.
3. *Perdita di polvere di toner all'interno della meccanica*.

#### Procedura Operativa al Banco:
```
[ CLIENTE RIPORTA TONER/CARTUCCIA AL BANCO ]
                     |
                     v
  1. Verifica Visiva (5 secondi)
     - È presente il sigillo di protezione arancione o la linguetta trasparente?
       (Spesso il cliente dimentica di rimuoverli prima dell'inserimento!)
                     |
                     v
  2. Verifica Contatti & Chip
     - I contatti in rame del chip sono sporchi di polvere o grasso?
     - Pulire delicatamente con panno in microfibra asciutto.
                     |
                     v
  3. Test su Stampante Muletto in Laboratorio (se disponibile il modello)
     - Se il consumabile non funziona:
                     |
                     v
  4. SOSTITUZIONE DIRETTA AL BANCO ("Zero Discussioni")
     - Prelevare un toner identico da scaffale e consegnarlo subito al cliente.
     - Spiegazione amichevole: "Nessun problema, capita nei lotti industriali.
       Te lo sostituisco immediatamente con uno testato!"
                     |
                     v
  5. Gestione Amministrativa e Reso Fornitore (RMA)
     - Riporre il pezzo difettoso nella scatola originale contrassegnata con marker "DIFETTOSO".
     - Incollare un post-it con la data e la motivazione (es. "Chip non letto").
     - Caricare la richiesta di reso sul portale del fornitore (Esprinet / Distributore)
       per ottenere la nota di accredito nel riassortimento successivo.
```

### 6.2 Protocollo Specifico PC, NOTEBOOK & HARDWARE

#### Caso A: Guasto o ripensamento entro 14 giorni dall'acquisto (DOA / Recesso)
1. Verificare l'integrità estetica e la presenza di tutti gli accessori originali (alimentatore, manuali, scatola originale).
2. Se il dispositivo presenta un difetto di fabbrica (DOA - *Dead on Arrival*):
   * Sostituzione immediata con un'unità nuova identica da magazzino (o rimborso integrale se esaurito).
3. Se il cliente si avvale del diritto di ripensamento (prodotto integro non gradito):
   * Eseguire il ripristino delle impostazioni di fabbrica per cancellare qualsiasi account personale del cliente.
   * Emettere buono acquisto o rimborso sullo stesso metodo di pagamento utilizzato (Shopify Payments / PayPal / contanti).

#### Caso B: Guasto hardware durante il periodo di garanzia (oltre 14 giorni)
1. **Presa in Carico Formale Laboratorio**:
   * Compilare la *Scheda di Ingresso Laboratorio Just in Time*.
   * Annotare: Seriale dispositivo, presenza di graffi/urti preesistenti, password di Windows (se acconsentita dal cliente per i test), descrizione puntuale del malfunzionamento.
   * Far firmare la clausola di liberatoria salvataggio dati (il cliente è responsabile del preventivo backup dei file personali).
2. **Diagnosi Tecnica (entro 24-48h)**:
   * Test hardware su memorie RAM, disco SSD/HDD e temperature processore.
3. **Instradamento dell'Intervento**:
   * **Notebook Nuovi (HP, Lenovo, Asus)**: Se il guasto è coperto da garanzia della casa madre, istruire la pratica RMA ufficiale con ritiro tramite corriere convenzionato del brand o riparazione in laboratorio Just in Time se autorizzati.
   * **Notebook Ricondizionati Just in Time (12 mesi)**: Intervento diretto in laboratorio con sostituzione immediata del componente difettoso (SSD, modulo RAM, ventola, schermo).
4. **Riconsegna al Cliente**:
   * Collaudo finale congiunto al banco e firma per ricevuta.

---

## 7. Workflow 5: Sincronizzazione Magazzino Fisico-Digitale

La sfida principale del commercio omnicanale è evitare l'**overselling** (vendere online un articolo che un altro cliente ha appena acquistato al banco un quarto d'ora prima).

```
+--------------------------------------------------------------------------------------+
|               LE 3 REGOLE AUREE DI SINCRONIZZAZIONE MAGAZZINO                        |
+--------------------------------------------------------------------------------------+
| 1. VENDUTO AL BANCO = SCARICATO SUBITO                                               |
|    Ogni volta che vendi un prodotto fisico al banco (non ordinato online), scala      |
|    immediatamente la giacenza da Shopify tramite App Mobile o PC.                    |
|                                                                                      |
| 2. DISTINZIONE DI INVENTORY POLICY TRA PRODOTTI E SERVIZI                            |
|    - Hardware, PC, Toner, Carta: "Nega vendite sottoscorta" (Variant Policy: deny)   |
|    - Servizi Laboratorio, Diagnosi, Prenotazione Libri: (Variant Policy: continue)   |
|                                                                                      |
| 3. INVENTARIO CICLICO DEI 20 BESTSELLER IL VENERDÌ POMERIGGIO                        |
|    Bastano 15 minuti ogni venerdì per contare a vista i 20 prodotti più venduti.    |
+--------------------------------------------------------------------------------------+
```

### 7.1 Procedura di Scarico Rapido Vendita al Banco Fisico

Quando un cliente entra in negozio e acquista direttamente al banco un prodotto presente a catalogo (es. un *Notebook Lenovo ThinkPad T480 Ricondizionato* di cui abbiamo solo 2 pezzi):

#### Metodo 1: Dall'App Mobile Shopify sullo Smartphone del Banco (Consigliato - 15 secondi)
1. Aprire l'app **Shopify**.
2. Toccare l'icona **Prodotti** in basso.
3. Cercare il prodotto (es. `T480` o scansionare il codice a barre con la fotocamera).
4. Toccare la voce **Inventario** (`Inventory`) e scalare la quantità: da `2` a `1`.
5. Salvare. Lo store online e i cataloghi social Instagram/Facebook vengono aggiornati istantaneamente!

#### Metodo 2: Dal PC del Banco
1. Aprire la scheda **Shopify Admin > Prodotti > Inventario**.
2. Cercare lo SKU del prodotto venduto (es. `JIT-THINKPAD-T480`).
3. Modificare il campo giacenza sottraendo l'unità venduta.

### 7.2 Gestione dei Tre Livelli di Fornitura

| Livello Catalogo | Tipologia Prodotti | Politica Giacenza su Shopify | Gestione Operativa Riordino |
| :--- | :--- | :--- | :--- |
| **Livello 1: Fast-Moving** *(Giacenza Locale)* | Toner HP 106A, Epson 603XL, Risme Navigator, Kit tastiera/mouse, SSD 480GB | Tracciato rigoroso (`Variant Policy: deny`). Se arriva a 0 il sito mostra "Esaurito". | Soglia minima di allerta: quando rimangono 2 pezzi a scaffale, inserire nella lista d'ordine fornitore settimanale. |
| **Livello 2: Just-in-Time 24/48h** *(Distributore)* | Notebook nuovi HP/Lenovo, Router Wi-Fi 6, Stampanti multifunzione | Tracciato con stock cuscinetto o aggiornato sui lotti confermati dai grossisti (Esprinet, Brevi, Runner). | Ordine al distributore entro le ore 16:00 per ricezione merce la mattina successiva al banco. |
| **Livello 3: Servizi & Prenotazioni** | Diagnosi laboratorio, Formattazione, Upgrade SSD, Prenotazione libri scolastici | Vendita continua (`Variant Policy: continue`). Giacenza fittizia impostata a 999. | Nessun rischio di rottura di stock fisico; l'evasione coincide con l'esecuzione della prestazione. |

### 7.3 Cosa fare se un prodotto va in "Overselling" (Rottura accidentale di stock)
Se per una svista un prodotto viene venduto al banco e contemporaneamente ordinato online prima dello scarico:
1. **Non farsi prendere dal panico e non annullare brutalmente l'ordine**.
2. Verificare immediatamente sul portale B2B del distributore (Esprinet / Runner) se l'articolo è disponibile in consegna 24 ore.
3. Se l'articolo arriva il giorno seguente, contattare il cliente via WhatsApp entro 30 minuti con tono trasparente e cordiale:
   > *"Ciao [Nome], ti ringrazio per l'ordine! Il pezzo da te ordinato è attualmente in transito dal nostro hub fornitore e sarà pronto per il ritiro domani mattina alle 10:30 al banco. Ti avviseremo noi appena è posizionato nel nostro rack. Per ringraziarti dell'attesa, ti omaggiamo di un controllo diagnostico gratuito per il tuo computer!"*
4. Se il prodotto è fuori produzione o richiede giorni, proporre un'alternativa di pari o superiore valore (senza sovrapprezzo) oppure il rimborso istantaneo con un click da Shopify.

---

## 8. Prontuario Rapido da Banco ("Cheat Sheet" da Stampare)

Questa tabella sintetica può essere stampata e affissa accanto al registratore di cassa e al PC del banco.

```markdown
========================================================================================
                     TABELLA SINOTTICA RAPIDA PER GLI OPERATORI
========================================================================================
EVENTO / SITUAZIONE        DOVE CLICCARE SU SHOPIFY         COSA FARE AL BANCO
----------------------------------------------------------------------------------------
Nuovo Ordine Ricevuto      Admin > Ordini                   Verificare se Ritiro o Spedizione.
                           (Controllare notifica mobile)    Prelevare merce da scaffale.
----------------------------------------------------------------------------------------
Merce Click & Collect      Ordine > Cliccare su             Imbustare con etichetta #JIT-xxx.
pronta per il cliente      "Segna come pronto per ritiro"   Posizionare nel Rack Ritiro.
                                                            Inviare WhatsApp rapido /ritiro.
----------------------------------------------------------------------------------------
Cliente arriva al banco    Ordine > Cliccare su             Se già pagato: solo consegna.
e ritira l'ordine          "Segna come ritirato"            Se pagamento al ritiro: incassare
                                                            POS/contanti e fare scontrino.
----------------------------------------------------------------------------------------
Spedizione pronta          Ordine > "Evadi articoli"        Imballo anti-urto. Stampare LDV.
per il corriere            Inserire Tracking e Corriere     Affidare all'autista pomeridiano.
----------------------------------------------------------------------------------------
Venduto pezzo al banco     Admin > Prodotti > Inventario    Scalare subito la quantità venduta
(cliente senza ordine web) (oppure da App Mobile)           per proteggere lo stock online.
----------------------------------------------------------------------------------------
Toner difettoso riportato  Nessun click online immediato    Verificare linguetta protettiva.
dal cliente al banco                                        Sostituire subito con pezzo nuovo.
                                                            Accantonare difettoso per RMA.
----------------------------------------------------------------------------------------
Richiesta fattura SDI      Ordine > Note / Dettagli         Verificare P.IVA, SDI o PEC.
da azienda o scuola        (oppure gestionale fatturazione) Generare fattura elettronica.
========================================================================================
```

---

## 9. FAQ e Risoluzione Emergenze al Banco

### D: Il cliente arriva al banco dicendo di aver fatto l'ordine, ma non trovo la busta nel rack.
**R:** Chiedi cortesemente il nome o controlla l'App Shopify nella scheda *Tutti gli ordini*. Spesso l'ordine è stato effettuato solo 5 minuti prima ed è ancora nello stato *Non evaso*. Recupera l'articolo direttamente a scaffale in presenza del cliente e completa l'evasione al banco senza fargli percepire alcun disguido.

### D: Il cliente ritira l'ordine ma vuole cambiare un articolo (es. mouse con filo anziché kit wireless).
**R:** Nessun problema! Apri l'ordine su Shopify e clicca su **Modifica** (`Edit order`). Aggiungi il nuovo articolo scelto e rimuovi quello precedente. Se c'è una differenza di prezzo in eccesso, incassala al banco tramite POS o contanti; se è a favore del cliente, emetti il rimborso parziale con un click sullo strumento di rimborso dell'ordine.

### D: Un cliente ordina online con pagamento al ritiro ma non si presenta per giorni.
**R:** 
* Dopo **3 giorni lavorativi**: inviare un promemoria amichevole su WhatsApp (*"Ciao! Ti ricordiamo che il tuo ordine ti aspetta al banco di Muro Leccese"*).
* Dopo **7 giorni lavorativi** senza risposta: aprire l'ordine su Shopify, cliccare su **Altre azioni > Annulla ordine** (`Cancel order`), selezionando la motivazione *"Cliente non ha ritirato"*. La merce torna automaticamente disponibile a inventario.

### D: Come gestire la fattura elettronica per professionisti, aziende locali o scuole?
**R:** Se il cliente ha inserito la Partita IVA, il Codice Univoco SDI o l'indirizzo PEC nelle note dell'ordine o nei campi anagrafici, emettere la relativa fattura elettronica tramite il software di fatturazione collegato a Just in Time entro i termini di legge (12 giorni dall'operazione per fattura immediata).

---

## 10. Rubrica Contatti di Emergenza & Link Rapidi

| Canale / Servizio | Riferimento / URL | Note Operative |
| :--- | :--- | :--- |
| **Pannello Shopify Admin** | `https://admin.shopify.com` | Accessibile da PC banco o app smartphone |
| **Assistenza Tecnica Shopify** | Assistenza Partner 24/7 via Chat | Per anomalie gateway o checkout |
| **Portale Corriere Espresso** | Portale Spedizioni Web (SDA / GLS / BRT) | Creazione LDV, ritiro pacchi e svincolo giacenze |
| **Grossista Esprinet** | Portale B2B Esprinet Club | Hardware, notebook, accessori con consegna 24h |
| **Grossista Runner / Brevi** | Portale B2B Clienti | Componentistica PC, SSD e networking |
| **Fornitore Toner Compatibili** | Portale Ordini Fornitore Consumabili | Riassortimento e pratiche RMA toner difettosi |
| **WhatsApp Assistenza Clienti** | `+39 320 602 5789` | Cellulare aziendale Just in Time Muro Leccese |
| **Email Ufficiale Store** | `info@justintimemuro.it` | Ricezione notifiche ordini e comunicazioni clienti |

---
*Manuale operativo redatto in conformità alle direttive omnicanale della Fase 4 del Progetto Just in Time di Benegiamo Andrea.*  
*Store Operations Specialist (`worker-pam-operations`) — Munder Difflin Hive.*
