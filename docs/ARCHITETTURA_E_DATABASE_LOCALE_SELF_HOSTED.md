# Architettura Database Locale & Stack Alternativo Self-Hosted
**Progetto**: E-Commerce & Gestionale Just in Time di Benegiamo Andrea  
**Sede**: Via Corsica 151, 73036 Muro Leccese (LE)  
**Tecnologia Database**: SQLite 3 (Database relazionale locale su file singolo)  
**Data di Rilascio**: 24 Ottobre 2026  
**Autore**: Michael (`god`), Orchestratore Hive  

---

## 1. Perché l'Alternativa a Shopify? (I Vantaggi della Soluzione Locale)

Se Andrea preferisce **non utilizzare Shopify**, la motivazione principale è quasi sempre economica e di controllo strategico:

| Fattore | Piattaforma Shopify | Database Locale & Stack Autonomo (Self-Hosted) |
| :--- | :--- | :--- |
| **Canone Fisso Mensile** | Da **29€ a 39€/mese** (~348€ - 468€ all'anno ricorrenti). | **€0,00/mese** (Nessun canone o licenza software). |
| **Commissioni Transazione** | Fino al **2.0% extra** su ogni vendita se non si usa Shopify Payments. | **0.0% di commissioni piattaforma** (solo tariffe POS fisico o Stripe standard). |
| **Proprietà dei Dati** | Dati memorizzati sui server cloud proprietari di Shopify. | **Sovranità al 100%**: il file database risiede sul computer del negozio a Muro Leccese. |
| **Gestione Riparazioni & Libri** | Richiede app terze a pagamento mensile (es. 10-20$/mese per ticketing). | **Integrata nativamente**: tabelle dedicate per ticket riparazione PC e prenotazioni testi scolastici. |
| **Funzionamento Offline** | Richiede sempre connessione internet attiva. | **Funziona anche senza connessione internet** al banco di Via Corsica 151. |

---

## 2. Struttura del Database Relazionale Locale (`just_in_time.db`)

Il database è stato implementato nel file [`database/just_in_time.db`](file:///Users/giuseppedepascali/Library/CloudStorage/GoogleDrive-depgiuseppe84@gmail.com/Il%20mio%20Drive/AI_CODE/Sito%20Andrea/database/just_in_time.db), strutturato secondo lo schema SQL [`database/schema.sql`](file:///Users/giuseppedepascali/Library/CloudStorage/GoogleDrive-depgiuseppe84@gmail.com/Il%20mio%20Drive/AI_CODE/Sito%20Andrea/database/schema.sql) e già popolato con il catalogo completo tramite [`database/init_and_seed.py`](file:///Users/giuseppedepascali/Library/CloudStorage/GoogleDrive-depgiuseppe84@gmail.com/Il%20mio%20Drive/AI_CODE/Sito%20Andrea/database/init_and_seed.py).

### Diagramma Entità-Relazione (ERD)

```
+------------------+         +-----------------------+         +----------------------+
|    categories    | 1     N |       products        | 1     N |   product_variants   |
|------------------|---------|-----------------------|---------|----------------------|
| id (PK)          |         | id (PK)               |         | id (PK)              |
| code (UNIQUE)    |         | category_id (FK)      |         | product_id (FK)      |
| name             |         | handle (UNIQUE)       |         | sku (UNIQUE)         |
| description      |         | title                 |         | title                |
| sort_order       |         | vendor                |         | price                |
+------------------+         | product_type          |         | compare_at_price     |
                             | base_price            |         | stock_quantity       |
                             | is_available_in_store |         | barcode              |
                             | lead_time_hours       |         | weight_grams         |
                             +-----------------------+         +----------------------+
                                         | 1
                                         |
                                         | N
                             +-----------------------+
                             |     product_tags      |
                             |-----------------------|
                             | product_id (FK)       |
                             | tag                   |
                             +-----------------------+

+------------------+         +-----------------------+         +----------------------+
|    customers     | 1     N |        orders         | 1     N |     order_items      |
|------------------|---------|-----------------------|---------|----------------------|
| id (PK)          |         | id (PK)               |         | id (PK)              |
| first_name       |         | order_number (UNIQUE) |         | order_id (FK)        |
| last_name        |         | customer_id (FK)      |         | product_id (FK)      |
| email            |         | delivery_type         |         | variant_id (FK)      |
| phone            |         | order_status          |         | product_title        |
| address, city    |         | payment_method        |         | sku, unit_price      |
| fiscal_code      |         | total_amount          |         | quantity, subtotal   |
+------------------+         +-----------------------+         +----------------------+
         | 1                                 
         |                                   
         +---------------+ 1                 
         | N             | N                 
+------------------+  +----------------------+
|  repair_tickets  |  |  book_reservations   |
|------------------|  |----------------------|
| id (PK)          |  | id (PK)              |
| ticket_number    |  | reservation_code     |
| customer_id (FK) |  | customer_id (FK)     |
| device_type      |  | student_name         |
| brand_model      |  | school_name, class   |
| reported_issue   |  | book_list_text       |
| diagnosis_notes  |  | colibri_covers_req   |
| estimated_cost   |  | deposit_amount       |
| status           |  | status               |
+------------------+  +----------------------+
```

---

## 3. Le 9 Tabelle Chiave e i Dati Già Precaricati

1. **`categories` (5 categorie)**:
   * *Informatica & Tecnologia*, *Stampa & Consumabili*, *Scuola & Cancelleria*, *Servizi & Assistenza Tecnica*, *Offerte & Outlet*.
2. **`products` (15 articoli pilota)**:
   * Notebook HP, ThinkPad ricondizionato, SSD Kingston, Kit Logitech, Router Wi-Fi 6, Cartucce Epson, Toner HP, Stampante Canon, Risme Navigator, Zaino Eastpak, Penne Pilot e schede servizio.
3. **`product_variants` (17 varianti)**:
   * SKU univoci (es. `JIT-HP250-BASE`, `JIT-HP250-ZEROPENSIERI`), prezzi, giacenze e codici a barre.
4. **`product_tags` (94 associazioni)**:
   * Tag per filtri e disponibilità rapida (`disp:immediata`, `vetrina:home`, `promo:outlet`).
5. **`customers`**:
   * Anagrafica clienti con nome, recapito WhatsApp, indirizzo e Codice Fiscale.
6. **`orders` & `order_items`**:
   * Gestione ordini con distinzione automatica tra Click & Collect (spese €0,00) e corriere espresso (spese €6,90, gratis sopra i 79€).
7. **`repair_tickets` (Laboratorio PC)**:
   * Tracciamento delle riparazioni con numero scheda (es. `LAB-2026-0012`), stato avanzamento (*ricevuto*, *in diagnosi*, *attesa ricambi*, *pronto per il ritiro*), acconto versato e preventivo finale.
8. **`book_reservations` (Scuola & Didattica)**:
   * Portale prenotazione testi scolastici per le scuole del Salento, studente, classe e opzione copertine protettive Colibrì.

---

## 4. Come Utilizzare il Database al Banco (Strumenti Disponibili)

### Opzione A: Tramite Interfaccia Grafica Gratuita (Consigliato per Andrea)
Andrea può aprire e gestire il database visualmente scaricando un software gratuito e leggero:
* **TablePlus** o **DBeaver** o **DB Browser for SQLite** (100% gratuito per Mac e Windows):
  * Permette di vedere tabelle, filtrare prodotti, aggiornare i prezzi e segnare gli ordini come "ritirati" come fosse un foglio Excel avanzato.

### Opzione B: Tramite il Data Access Layer Python (`database/dal.py`)
Per sviluppatori o script automatizzati, il file [`database/dal.py`](file:///Users/giuseppedepascali/Library/CloudStorage/GoogleDrive-depgiuseppe84@gmail.com/Il%20mio%20Drive/AI_CODE/Sito%20Andrea/database/dal.py) espone funzioni pronte:
```python
from database.dal import JustInTimeDAL

# Recupera catalogo
prodotti = JustInTimeDAL.get_products(category_code='informatica-tecnologia')

# Crea un nuovo ordine dal carrello web o WhatsApp
nuovo_ordine = JustInTimeDAL.create_order(
    customer_info={'first_name': 'Mario', 'last_name': 'Rossi', 'phone': '+39 320 0000000'},
    items=[{'sku': 'JIT-KNG-A400-480', 'quantity': 1}],
    delivery_type='pickup'
)
print("Ordine creato:", nuovo_ordine['order_number'])
```

### Opzione C: Tramite il Server API REST Locale (`database/server.py`)
Avviando con un comando:
```bash
python3 "database/server.py"
```
Il server si attiva su `http://127.0.0.1:8080` e mette a disposizione endpoint JSON universali:
* `GET /api/products` — Elenco prodotti con filtri categoria e ricerca testuale
* `GET /api/categories` — Macro-collezioni con conteggio articoli
* `GET /api/orders` — Storico ordini e righe carrello
* `POST /api/orders` — Ricezione ordini dal carrello web
* `GET /api/repairs` — Stato schede di riparazione laboratorio
* `GET /api/stats` — Cruscotto con fatturato, ordini e riparazioni aperte

---

## 5. Front-End Alternativi Collegabili a Questo Database

Se non si usa Shopify, il sito web e-commerce può essere realizzato e ospitato a costo quasi nullo scegliendo una di queste 3 strade:

1. **Storefront Jamstack / Astro / Next.js (Hosting Gratuito su Vercel / Cloudflare Pages)**:
   * Velocità fulminea, design moderno identico al nostro prototipo [`preview/index.html`](file:///Users/giuseppedepascali/Library/CloudStorage/GoogleDrive-depgiuseppe84@gmail.com/Il%20mio%20Drive/AI_CODE/Sito%20Andrea/preview/index.html).
   * Gli ordini inviano una notifica WhatsApp diretta ad Andrea e salvano i dati nel database SQLite.
   * **Costo hosting**: **0€/mese** (nel piano hobby di Vercel/Cloudflare).
2. **WooCommerce / WordPress su Hosting Italiano Economico**:
   * Spesa di circa **3€ - 5€/mese** su provider come SiteGround o Serverplan.
   * Importazione del catalogo tramite lo schema SQL o CSV standard.
3. **Piattaforma WhatsApp Commerce Pura**:
   * Il prototipo [`preview/index.html`](file:///Users/giuseppedepascali/Library/CloudStorage/GoogleDrive-depgiuseppe84@gmail.com/Il%20mio%20Drive/AI_CODE/Sito%20Andrea/preview/index.html) funge da catalogo digitale interattivo: il cliente seleziona i prodotti e il carrello genera un ordine preformattato che invia ad Andrea su WhatsApp con un click. Nessun canone, zero intermediari.

---

## 6. Riepilogo per la Decisione di Andrea

* **Se scegli Shopify**: Hai un pannello di controllo pronto all'uso, app mobile nativa e zero manutenzione tecnica, ma con un costo fisso di circa 30€/mese.
* **Se NON usi Shopify (Soluzione Locale/Self-Hosted)**: Hai il database SQLite già pronto, creato e popolato in [`database/just_in_time.db`](file:///Users/giuseppedepascali/Library/CloudStorage/GoogleDrive-depgiuseppe84@gmail.com/Il%20mio%20Drive/AI_CODE/Sito%20Andrea/database/just_in_time.db), integrato con il laboratorio di assistenza e la cartolibreria, a **costo fisso pari a ZERO**.
