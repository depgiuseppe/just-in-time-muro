# Manuale Operativo & Specifiche Tecniche: Stack Locale Self-Hosted (Opzione B)
**Progetto**: E-Commerce & Gestionale Just in Time di Benegiamo Andrea  
**Sede Operativa**: Via Corsica 151, 73036 Muro Leccese (LE)  
**Ticket Task**: SAN-16 — Consolidamento e Completamento Stack Locale Self-Hosted  
**Responsabile Tecnico**: `worker-ryan-backend` (Backend & Full Stack Engineer)  
**Data di Rilascio**: 24 Ottobre 2026  
**Costo Licenze e Piattaforma**: **€0,00 / mese (Canone Zero perenne)**  

---

## 1. Visione d'Insieme & Obiettivi Raggiunti

La presente implementazione consolida ed estende lo **Stack Locale Self-Hosted (Opzione B)**, fornendo ad Andrea Benegiamo un ecosistema software autonomo, velocissimo e resiliente per la gestione integrata di:
1. **Storefront E-Commerce Locale & Prototipo Web**: navigazione catalogo, carrello reattivo, selezione Click & Collect / Spedizione corriere, checkout con notifica WhatsApp dinamica e tracciamento in tempo reale delle riparazioni.
2. **Pannello Gestionale al Banco (`/admin`)**: interfaccia web moderna per Andrea, accessibile dal browser del negozio per gestire ordini in arrivo, accettare dispositivi in riparazione con un click, stampare ricevute e talloncini banco, e monitorare giacenze.
3. **Data Access Layer (DAL) Python Unificato (`database/dal.py`)**: gestione thread-safe del database SQLite relazionale (`database/just_in_time.db`), con foreign keys attive, transazioni atomiche, validazione vincoli e decremento automatico delle scorte di magazzino.
4. **Server API REST Locale (`database/server.py`)**: server HTTP nativo ad alte prestazioni (zero dipendenze esterne, funziona su qualsiasi installazione Python 3 standard), con supporto completo a richieste GET, POST, PUT, OPTIONS (CORS abilitato) e rendering di ricevute stampabili in formato A4.
5. **Procedura di Avvio Semplificata**: file eseguibile con doppio click [`Avvia_Just_In_Time.command`](../Avvia_Just_In_Time.command) e script bash [`start_just_in_time.sh`](../start_just_in_time.sh) con apertura automatica del browser e controllo integrità del database.
6. **CLI di Amministrazione Avanzata (`database/manage.py`)**: comandi per interrogare ordini, schede riparazione, prezzi, giacenze magazzino e backup istantanei timestamped.

---

## 2. Architettura del Sistema Locale

```
+------------------------------------------------------------------------------------+
|                         CLIENTI & STOREFRONT WEB                                   |
|   index.html / preview/index.html (Portatile, Tablet, Smartphone cliente)         |
|   - Catalogo prodotti live via /api/products                                       |
|   - Carrello interattivo e checkout Click & Collect                                |
|   - Tracciamento live stato riparazione PC via /api/repairs/<ticket>              |
+------------------------------------------------------------------------------------+
                                      ▲  │
                       Fetch API JSON │  │ POST /api/orders
                                      │  ▼
+------------------------------------------------------------------------------------+
|               SERVER API REST & WEB STOREFRONT (database/server.py)                |
|                    Porta locale: http://127.0.0.1:8080                              |
|   - Endpoints: /api/products, /api/orders, /api/repairs, /api/books, /api/stats    |
|   - Generazione Ricevute HTML: /api/orders/.../receipt, /api/repairs/.../receipt   |
|   - Router Gestionale Banco: /admin                                                |
+------------------------------------------------------------------------------------+
               ▲                                                      ▲
               │ Metodi Python sincroni                               │ Accesso Browser
               ▼                                                      ▼
+-------------------------------------------+      +---------------------------------+
|   DATA ACCESS LAYER (database/dal.py)     |      | GESTIONALE AL BANCO (/admin)     |
|   - Categorie & Prodotti                  |      | Interfaccia Web per Andrea:     |
|   - Creazione ordini & scarico scorte     |      | - Cruscotto incassi & alert     |
|   - Laboratorio Riparazioni & Talloncini  |      | - Evasione ordini 1-click       |
|   - Prenotazione Testi Scolastici         |      | - Accettazione PC con stampa    |
+-------------------------------------------+      | - Controllo scorte magazzino    |
               ▲                                   +---------------------------------+
               │ SQL con PRAGMA foreign_keys = ON
               ▼
+------------------------------------------------------------------------------------+
|             DATABASE RELAZIONALE LOCALE (database/just_in_time.db)                 |
|   9 Tabelle: categories, products, product_variants, product_tags, customers,      |
|              orders, order_items, repair_tickets, book_reservations                |
+------------------------------------------------------------------------------------+
```

---

## 3. Specifiche Complete delle API REST Locale

Tutti gli endpoint rispondono sulla porta `8080` (es. `http://127.0.0.1:8080`) e impostano automaticamente le intestazioni CORS `Access-Control-Allow-Origin: *`.

### 3.1 Statistiche & Cruscotto
* **`GET /api/stats`**
  * **Descrizione**: Restituisce metriche aggregate del negozio.
  * **Risposta (200 OK)**:
    ```json
    {
      "active_products": 15,
      "total_orders": 2,
      "pending_orders": 1,
      "total_revenue_eur": 79.80,
      "open_repairs_count": 2,
      "ready_repairs_count": 1,
      "open_book_reservations_count": 1,
      "low_stock_items_count": 1
    }
    ```

### 3.2 Catalogo Prodotti & Categorie
* **`GET /api/categories`**
  * **Descrizione**: Elenco delle categorie attive con conteggio prodotti associati.
* **`GET /api/products`**
  * **Parametri Query opzionali**:
    * `category`: codice categoria (es. `informatica-tecnologia`, `stampa-consumabili`, `servizi-assistenza-tecnica`).
    * `q`: ricerca libera su titolo, fornitore, descrizione o SKU.
    * `in_store`: `1` per visualizzare solo articoli con disponibilità immediata a Muro Leccese.
    * `featured`: `1` per visualizzare solo articoli in vetrina.
* **`GET /api/products/<handle_or_id>`**
  * **Descrizione**: Dettaglio scheda prodotto con elenco completo varianti, prezzi, giacenze e specifiche.

### 3.3 Gestione Ordini & Carrello
* **`GET /api/orders`**
  * **Parametri Query opzionali**: `status` (`pending`, `confirmed`, `ready_for_pickup`, `shipped`, `completed`, `cancelled`), `limit`.
* **`GET /api/orders/<id_or_number>`**
  * **Descrizione**: Dettagli completi dell'ordine, anagrafica cliente e righe d'acquisto.
* **`POST /api/orders`**
  * **Descrizione**: Crea un nuovo ordine, associa o crea l'anagrafica cliente, calcola spese di spedizione (€0 per ritiro in sede o ordini >= 79€, altrimenti €6.90) e decrementa automaticamente la giacenza magazzino (`product_variants.stock_quantity`).
  * **Payload di Esempio**:
    ```json
    {
      "customer": {
        "first_name": "Mario",
        "last_name": "Rossi",
        "phone": "+39 320 1234567",
        "email": "mario.rossi@gmail.com",
        "address": "Via Roma 10",
        "city": "Muro Leccese"
      },
      "items": [
        { "sku": "JIT-KNG-A400-480", "quantity": 1 }
      ],
      "delivery_type": "pickup",
      "payment_method": "pos_on_pickup",
      "notes": "Passo a ritirare nel pomeriggio",
      "decrement_stock": true
    }
    ```
  * **Risposta (201 Created)**: restituisce `order_number` (es. `JIT-20261024-0002`), subtotale, spese e totale ordine.
* **`PUT /api/orders/<id_or_number>`** (oppure `POST /api/orders/<id_or_number>/status`)
  * **Descrizione**: Aggiornamento stato avanzamento (`order_status`), stato pagamento (`payment_status`), note interne o codice lettera di vettura corriere (`tracking_code`).
* **`GET /api/orders/<id_or_number>/receipt`**
  * **Descrizione**: Genera e restituisce il documento HTML pronto per la stampa della ricevuta d'ordine o DDT per il ritiro/spedizione.

### 3.4 Laboratorio di Assistenza & Riparazioni PC
* **`GET /api/repairs`**
  * **Parametri Query**: `status`, `q`, `limit`.
* **`GET /api/repairs/<ticket_number>`**
  * **Descrizione**: Recupera la scheda tecnica con storico, dispositivo, difetto segnalato e preventivo. Utilizzato sia dal gestionale che dal widget storefront per i clienti.
* **`POST /api/repairs`**
  * **Descrizione**: Accettazione nuovo dispositivo al banco. Genera automaticamente il numero scheda sequenziale `LAB-YYYY-XXXX`.
  * **Payload di Esempio**:
    ```json
    {
      "customer": {
        "first_name": "Marco",
        "last_name": "Verdi",
        "phone": "+39 347 1234567",
        "email": "marco.verdi@gmail.com"
      },
      "device_type": "notebook",
      "brand_model": "HP Pavilion 15-cw",
      "serial_number": "5CD9123XYZ",
      "reported_issue": "Surriscaldamento anomalo e spegnimento",
      "advance_fee": 25.00,
      "estimated_cost": 45.00
    }
    ```
* **`PUT /api/repairs/<ticket_number>`** (oppure `POST /api/repairs/<ticket_number>/status`)
  * **Descrizione**: Avanzamento stato riparazione (`received` ➔ `diagnosing` ➔ `waiting_approval` ➔ `in_repair` ➔ `ready_for_pickup` ➔ `delivered`), aggiornamento diagnosi, costo finale e marcatura data di chiusura (`closed_at`).
* **`GET /api/repairs/<ticket_number>/receipt`**
  * **Descrizione**: Genera il documento A4 stampabile a doppia sezione:
    1. **Ricevuta per il Cliente**: dettagli dispositivo, problema riscontrato, acconto versato, condizioni di garanzia 90 giorni sui ricambi e QR/link per monitoraggio online.
    2. **Talloncino per il Banco Laboratorio (con linea tratteggiata per ritaglio)**: talloncino sintetico da applicare fisicamente sullo chassis del computer o dispositivo sul banco di lavoro di Andrea.

### 3.5 Prenotazione Testi Scolastici
* **`GET /api/books`**: elenco prenotazioni con dettagli studente, scuola e testi.
* **`POST /api/books`**: inserimento prenotazione (con opzione copertine Colibrì).

---

## 4. Guida Operativa per Andrea al Banco di Muro Leccese

### 4.1 Come Avviare il Gestionale Ogni Mattina
1. Accendi il computer del negozio.
2. Fai **doppio click** sull'icona [`Avvia_Just_In_Time.command`](../Avvia_Just_In_Time.command).
3. Il terminale verificherà l'ambiente in 1 secondo e aprirà in automatico due schede nel tuo browser predefinito:
   * **Scheda 1**: Il **Pannello Gestionale Banco** (`http://127.0.0.1:8080/admin`).
   * **Scheda 2**: Lo **Storefront Web** (`http://127.0.0.1:8080/`).

### 4.2 Gestione degli Ordini Click & Collect in 3 Click
1. Quando un cliente ordina dal sito o invia la conferma su WhatsApp, l'ordine compare istantaneamente nel tab **"🛒 Ordini & Click & Collect"**.
2. Prepara gli articoli a scaffale e clicca **"✅ Pronto al Ritiro"**: lo stato passerà a verde.
3. Quando il cliente entra in negozio in Via Corsica 151 per ritirare, clicca **"📦 Consegnato & Saldato"** e premi **"🖨️ Ricevuta"** per stampare il riepilogo su carta o salvarlo in PDF.

### 4.3 Accettazione Riparazione PC e Stampa Ricevuta
1. Quando un cliente porta un PC guasto al banco:
   * Clicca su **"🛠️ Laboratorio Riparazioni"** e premi il pulsante blu **"➕ Nuova Accettazione al Banco"**.
   * Inserisci nome, cognome, numero WhatsApp, tipo dispositivo (Notebook, Fisso, Smartphone...), difetto riferito ed eventuale acconto incassato (es. 20€ o 25€).
   * Clicca su **"Registra e Genera Ricevuta"**.
2. Il sistema apre subito l'anteprima di stampa:
   * Consegna la parte superiore (Ricevuta Cliente) al cliente.
   * Ritaglia la parte inferiore lungo la linea tratteggiata e applicala con un nastro o pinzetta sullo chassis del computer sul tuo banco di lavoro.
3. Il cliente può collegarsi al sito in qualunque momento e inserire il numero scheda (es. `LAB-2026-0012`) cliccando sul pulsante **"🔬 Stato Riparazione"** in alto: vedrà lo stato aggiornato in tempo reale senza dover chiamare in negozio!

### 4.4 Backup del Database in Caso di Manutenzione
Per mettere al sicuro tutti i dati, basta aprire il terminale ed eseguire:
```bash
python3 database/manage.py backup
```
Il comando crea una copia istantanea del file `.db` all'interno della cartella `database/backups/just_in_time_AAAAMMGG_HHMMSS.db`.

---

## 5. Risultati del Collaudo e Suite di Test Automatizzati

È stata creata la suite di test [`database/test_local_stack.py`](../database/test_local_stack.py) comprendente 11 test integrati end-to-end:
* `test_01_categories`: verifica corretta tassonomia e conteggio articoli attivi.
* `test_02_products_and_filters`: test filtri per categoria, ricerca full-text e lookup per slug univoco (`kingston-a400-ssd-480gb`).
* `test_03_create_order_and_stock_decrement`: creazione ordine con verifica matematica di azzeramento spese di spedizione per ritiro in sede e decremento reale delle giacenze varianti nel database.
* `test_04_repair_tickets_and_receipt`: ciclo di vita completo della scheda riparazione (`received` ➔ `in_repair` ➔ `delivered`), generazione talloncino banco e tracciamento data chiusura.
* `test_05_book_reservations`: verifica conformità vincoli e stato prenotazione libri didattici con copertine Colibrì.
* `test_06_stats`: verifica cruscotto e coerenza somme fatturato.
* `test_api_stats`, `test_api_products`, `test_api_orders_flow`, `test_api_repairs_flow`, `test_admin_and_storefront_pages`: test HTTP reali con avvio server multi-thread, verifica codici HTTP 200/201, header CORS, content-type JSON e rendering documenti HTML.

**Esito Esecuzione**:
```
Ran 11 tests in 0.862s
OK (100% Passed)
```
