# Guida Tecnica Operativa: Importazione Catalogo e Allestimento Collezioni Shopify Partner
**Progetto**: Just in Time di Benegiamo Andrea (Muro Leccese, LE)  
**Destinatari**: Titolare dello store (Andrea Benegiamo), Store Operator, Team Tecnico  
**Ambiente**: Store di Sviluppo Shopify Partner / Store di Produzione  
**File di Riferimento**:
- Catalogo CSV: `catalog/just_in_time_shopify_products.csv` (17 varianti, 15 prodotti, 33 colonne standard)
- Architettura Collezioni: `catalog/just_in_time_collections.json` (5 macro-collezioni automatizzate)
- Script di Validazione: `catalog/validate_catalog.py` (controllo di integrità a 33 colonne)

---

## 1. Panoramica & Requisiti Preliminari

Questa guida fornisce i passaggi operativi puntuali per caricare e configurare l'intero catalogo prodotti e servizi di **Just in Time** su uno store Shopify (Partner Development Store o account commerciale), garantendo la perfetta integrità dei dati, la classificazione automatica e il supporto al modello ibrido **Click & Collect locale + Spedizione nazionale**.

### Prerequisiti:
1. **Accesso all'Admin Shopify**: Ruolo con permessi completi su *Prodotti*, *Collezioni*, *Impostazioni di Spedizione* e *Navigazione*.
2. **Ambiente Python 3** (locale): Per l'esecuzione preventiva dei test di conformità tramite `catalog/validate_catalog.py`.
3. **Immagini di Prodotto**: Il file CSV contiene URL CDN ad alta risoluzione (Unsplash prototipo). In fase di go-live definitivo, le immagini reali del punto vendita o dei cataloghi fornitori (Esprinet/Runner) potranno sostituire le attuali mantenendo inalterata la struttura.

---

## 2. Fase 1: Validazione Preliminare del File CSV

Prima di eseguire qualsiasi importazione, lanciare lo script di collaudo automatico per certificare l'assenza di errori di sintassi o campi fuori colonna:

```bash
python3 catalog/validate_catalog.py
```

### Esito Atteso:
* **33 colonne standard Shopify** allineate su ogni singola riga.
* **17 SKU univoci** (formato `JIT-XXX`).
* **15 handle unici** in formato web-friendly (slug kebab-case).
* **Corretta formattazione numerica**: prezzi con punto decimale (`549.00`), grammi interi (`1800`), quantità di magazzino.
* **Corretta impostazione dei flag di spedizione**: `Variant Requires Shipping = TRUE` per l'hardware fisico, `FALSE` per i servizi di laboratorio e la prenotazione libri.
* **100% di copertura del catalogo** nelle 5 collezioni automatizzate.

---

## 3. Fase 2: Procedura di Importazione Prodotti in Shopify

1. Accedere al pannello di amministrazione Shopify:  
   `https://admin.shopify.com/store/<nome-store>`
2. Nel menu laterale di sinistra, cliccare su **Prodotti** (`Products`).
3. In alto a destra, cliccare sul pulsante **Importa** (`Import`).
4. Nella finestra modale:
   - Cliccare su **Aggiungi file** (`Add file`) e selezionare il file `catalog/just_in_time_shopify_products.csv`.
   - **IMPORTANTE**: Se si tratta di un aggiornamento di un catalogo già importato, selezionare la casella:  
     ☑ *Sovrascrivi i prodotti esistenti con lo stesso handle* (`Overwrite any current products that have the same handle`).
5. Cliccare su **Carica e continua** (`Upload and continue`).
6. **Schermata di Anteprima**:
   - Verificare che Shopify riconosca correttamente i campi (Titolo, Fornitore, Prezzo, SKU, Varianti).
   - Verificare che la prima riga mostri il prodotto *Notebook HP 250 G9* con le due opzioni di configurazione:  
     1. `Base (Pronto all'uso)` a €549,00 (SKU: `JIT-HP250-BASE`)  
     2. `Pacchetto Zero Pensieri (+ Assistenza & Travaso)` a €589,00 (SKU: `JIT-HP250-ZEROPENSIERI`)
7. Cliccare su **Importa prodotti** (`Import products`).
8. L'operazione richiede circa 15-30 secondi. Al termine, apparirà una notifica verde di conferma con il totale di 15 prodotti importati con successo.

---

## 4. Fase 3: Allestimento delle Collezioni Automatizzate

Shopify popola le collezioni automaticamente in base ai **Tag** assegnati nel CSV.  
Accedere a **Prodotti > Collezioni** (`Collections`) e creare le seguenti 5 macro-collezioni (più la collezione vetrina):

### 1. Informatica & Tecnologia
* **Titolo**: `Informatica & Tecnologia`
* **Handle / URL**: `informatica-tecnologia`
* **Tipo di collezione**: **Automatizzata** (`Automated`)
* **Condizioni**: *I prodotti devono soddisfare tutti i criteri*
  * `Tag del prodotto` | `è uguale a` | `informatica`
* **Ordinamento predefinito**: *Più venduti* (`Best selling`)
* **Prodotti associati automaticamente**: 5 articoli (Notebook HP, ThinkPad Ricondizionato, Kingston SSD, Kit Logitech MK270, Router TP-Link).

### 2. Stampa & Consumabili
* **Titolo**: `Stampa & Consumabili`
* **Handle / URL**: `stampa-consumabili`
* **Tipo di collezione**: **Automatizzata**
* **Condizioni**:
  * `Tag del prodotto` | `è uguale a` | `stampa`
* **Ordinamento predefinito**: *Manuale* (con cartucce e toner in evidenza)
* **Prodotti associati automaticamente**: 3 articoli (Cartuccia Epson 603XL, Toner Compatibile HP 106A, Stampante Canon TS3350).

### 3. Scuola & Cancelleria
* **Titolo**: `Scuola & Cancelleria`
* **Handle / URL**: `scuola-cancelleria`
* **Tipo di collezione**: **Automatizzata**
* **Condizioni**:
  * `Tag del prodotto` | `è uguale a` | `scuola`
* **Ordinamento predefinito**: *Più venduti*
* **Prodotti associati automaticamente**: 4 articoli (Box Risme Navigator A4, Zaino Eastpak Padded Pak'r, Set Penne Pilot G-2, Prenotazione Libri di Testo).

### 4. Servizi & Laboratorio Tecnico
* **Titolo**: `Servizi & Laboratorio Tecnico`
* **Handle / URL**: `servizi-assistenza-tecnica`
* **Tipo di collezione**: **Automatizzata**
* **Condizioni**:
  * `Tag del prodotto` | `è uguale a` | `servizi`
* **Ordinamento predefinito**: *Manuale*
* **Prodotti associati automaticamente**: 3 schede servizio (Diagnosi PC/Notebook, Formattazione e Antivirus, Upgrade SSD con Clonazione).

### 5. Offerte & Ricondizionati d'Occasione
* **Titolo**: `Offerte & Ricondizionati d'Occasione`
* **Handle / URL**: `offerte-outlet`
* **Tipo di collezione**: **Automatizzata**
* **Condizioni**: *I prodotti devono soddisfare qualsiasi criterio* (`Any condition`)
  * `Tag del prodotto` | `è uguale a` | `promo:outlet`
  * *oppure* `Tag del prodotto` | `è uguale a` | `promo:bestseller`
* **Ordinamento predefinito**: *Prezzo: dal più basso al più alto*
* **Prodotti associati automaticamente**: ThinkPad T480 Ricondizionato Grado A+ e Pacchetto Upgrade SSD.

### 6. Vetrina Homepage (In Evidenza)
* **Titolo**: `In Evidenza in Negozio`
* **Handle / URL**: `vetrina-home`
* **Condizione**: `Tag del prodotto` | `è uguale a` | `vetrina:home`

---

## 5. Fase 4: Configurazione Ritiro in Sede (Click & Collect) & Spedizioni

Il modello di business Just in Time fa del negozio fisico di Muro Leccese il proprio punto di forza fiduciario.

### A. Configurazione Click & Collect (Gratuito in Negozio):
1. In Shopify Admin, andare su **Impostazioni > Spedizione e consegna** (`Settings > Shipping and delivery`).
2. Scendere alla sezione **Ritiro in sede** (`Local pickup`).
3. Cliccare sulla sede principale del negozio:
   - **Nome sede**: *Just in Time - Negozio & Laboratorio*
   - **Indirizzo**: *Via Corsica 151, 73036 Muro Leccese (LE)*
   - Spuntare: ☑ *Questa sede offre il ritiro in sede*.
   - **Tempo di preparazione previsto**: Selezionare *Di solito è pronto in 2 ore* (per articoli contrassegnati con `disp:immediata`).
   - **Istruzioni per il ritiro**:  
     ```text
     Riceverai una notifica email e un messaggio WhatsApp non appena il tuo ordine sarà pronto per il ritiro presso il nostro punto vendita in Via Corsica 151 a Muro Leccese. Porta con te il numero d'ordine o il messaggio di conferma.
     Orari: Lun-Ven 09:00-13:00 / 16:30-20:00, Sab 09:00-13:00.
     ```

### B. Configurazione Tariffe di Spedizione Corriere Espresso:
1. Nella sezione **Spedizione generale**:
   - Creare una tariffa per l'Italia continentale e isole:
     - **Tariffa Base Standard (Corriere Espresso 24/48h)**: €6,90 per ordini fino a €88,99.
     - **Spedizione Gratuita**: €0,00 per carrelli pari o superiori a €89,00.
   - **Scaglioni di peso per articoli voluminosi**:  
     Poiché il file CSV include il peso reale in grammi (es. 12.500g per il Box 5 risme Navigator), è possibile definire una tariffa calibrata per colli pesanti (>10 kg: €9,90).

---

## 6. Fase 5: Gestione Speciale Servizi e Prenotazioni

I 4 articoli di servizio (`Variant Requires Shipping = FALSE`) presentano particolarità operative gestite come segue:

1. **Diagnosi e Riparazione Hardware (`JIT-SRV-DIAG-DESK` / `JIT-SRV-DIAG-NOTE`)**:
   - Al checkout il cliente seleziona il dispositivo (Desktop €20 / Notebook €25).
   - Non viene addebitata alcuna spesa di spedizione.
   - Il cliente riceve la conferma d'ordine con l'invito a consegnare la macchina presso il laboratorio di Muro Leccese.
2. **Pacchetto Upgrade SSD con Clonazione Dati (`JIT-SRV-UPGRADE-SSD`)**:
   - Venduto a prezzo promozionale di €79,00 (anziché €95,00). Include la fornitura dell'SSD Kingston 480GB e la manodopera.
3. **Servizio Prenotazione Libri di Testo Scolastici (`JIT-SRV-LIBRI-TESTO`)**:
   - Prezzo impostato a **€0,00**.
   - `Variant Taxable = FALSE` (Regime speciale IVA editoria art. 74).
   - Nel carrello, abilitare il blocco **"Note sull'ordine"** (configurabile da Personalizzazione Tema > Cart page) con etichetta:  
     *"Indica qui la scuola, la classe, la sezione e se desideri la copertinatura protettiva Colibrì"*.
   - Il cliente prenota a zero euro e paga al momento del ritiro in negozio all'arrivo dei libri.

---

## 7. Fase 6: Checklist di Collaudo Operativo

Completata l'importazione, verificare i seguenti 10 punti di controllo prima di comunicare il rilascio:

| # | Elemento di Controllo | Esito Atteso | Stato |
|---|---|---|:---:|
| 1 | **Conteggio Prodotti** | 15 prodotti distinti presenti in `Prodotti` | [ ] OK |
| 2 | **Conteggio Varianti** | 17 varianti totali attive con SKU dedicati | [ ] OK |
| 3 | **Stato Pubblicazione** | Tutti i prodotti impostati su `Attivo` (`Status = active`) | [ ] OK |
| 4 | **Variante Notebook HP** | Menu a tendina funzionante con Base (€549) e Pacchetto Zero Pensieri (€589) | [ ] OK |
| 5 | **Popolamento Collezioni** | Tutte le 5 collezioni mostrano i rispettivi prodotti associati | [ ] OK |
| 6 | **Click & Collect** | Disponibile opzione "Ritiro in sede a Muro Leccese" al checkout | [ ] OK |
| 7 | **Esclusione Spedizione Servizi** | I servizi a carrello non richiedono indirizzo né costi di spedizione | [ ] OK |
| 8 | **Immagini di Prodotto** | Immagini visibili correttamente sia in griglia che nella scheda singola | [ ] OK |
| 9 | **Campi SEO** | Titoli SEO e Meta descrizioni popolati e senza caratteri corrotti | [ ] OK |
| 10 | **Prezzi di Confronto** | Badge "Offerta" visibile su articoli con `Variant Compare At Price` (HP, ThinkPad, SSD) | [ ] OK |

---
*Documento redatto dall'Online Store Operator (`worker-pam-store-operator`) per il progetto Just in Time di Benegiamo Andrea.*
