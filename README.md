# Just in Time — Store & Laboratorio Informatico
### di Benegiamo Andrea • Muro Leccese (LE)

Benvenuti nel repository ufficiale del progetto web, e-commerce e gestionale di **Just in Time**, punto vendita e centro assistenza informatica situato in **Via Corsica 151, 73036 Muro Leccese (LE)**.

---

## 🏬 Chi Siamo & Servizi
- **Vendita Prodotti**: Computer desktop, notebook nuovi e ricondizionati garantiti, componentistica e accessori.
- **Stampa & Ufficio**: Consumabili originali e compatibili certificati (toner, cartucce inchiostro, risme carta Navigator).
- **Cancelleria & Scuola**: Forniture scolastiche, zaini Eastpak, servizio prenotazione testi scolastici Colibrì ad anticipo zero.
- **Laboratorio Tecnico**: Diagnosi guasti hardware, formattazione/ripristino Windows, travaso dati, upgrade SSD.
- **Punto Territoriale**: Amazon Counter, pagamento bollettini/PagoPA, ricariche e fornitore abilitato PA/Scuole su MEPA.

---

## 🚀 Architettura del Progetto
Questo repository contiene l'intera infrastruttura del negozio, progettata per operare sia su cloud sia in totale autonomia locale:

1. **Vetrina Web Interattiva (`index.html`)**:
   - Storefront moderno, responsive per smartphone e desktop.
   - Carrello integrato, calcolo spedizioni / ritiro gratuito in negozio.
   - Modulo di **Checkout & Selezione Pagamento** (Contanti o POS da banco, Carta Online / PayByLink, Bonifico).
   - Generazione automatica del messaggio d'ordine per **WhatsApp Business** (+39 320 602 5789).
2. **Database Locale SQLite (`database/just_in_time.db`)**:
   - Database serverless a zero costi di mantenimento (€0/mese).
   - Modello relazionale a 9 tabelle: prodotti, varianti, clienti, ordini, schede riparazione laboratorio e prenotazioni libri.
3. **Pannello di Gestione Rapida (`database/manage.py`)**:
   - Gestione da terminale per aggiornare prezzi, giacenze magazzino e impostare gli articoli in vetrina.
4. **Backend API REST (`database/server.py`)**:
   - Microserver Python a zero dipendenze per sincronizzare la vetrina con il database locale.
5. **Canale Alternativo Shopify (`catalog/` e `shopify-theme/`)**:
   - File CSV validato a 33 colonne standard Shopify e temi Liquid pronti per eventuale importazione su store Shopify.

---

## 🛠️ Come Avviare in Locale

### 1. Consultare o Modificare il Catalogo
```bash
# Elenca tutti gli articoli, prezzi, giacenze e stato vetrina
python3 database/manage.py list

# Modifica rapida prezzo o giacenza di un articolo
python3 database/manage.py price JIT-HP250-BASE 529.00
python3 database/manage.py stock JIT-HP250-BASE 5

# Metti un articolo in vetrina con badge in evidenza
python3 database/manage.py feature JIT-KNG-A400-480 1
```

### 2. Avviare il Server Locale
```bash
python3 database/server.py 8080
```
- Vetrina Web: `http://localhost:8080`
- API Prodotti JSON: `http://localhost:8080/api/products`
- Dashboard Statistiche: `http://localhost:8080/api/stats`

---

## 📁 Struttura delle Directory
```text
├── index.html                   # Vetrina web principale per hosting statico (Cloudflare/Vercel)
├── preview/                     # Copia della vetrina di anteprima
├── pages-legal/                 # Pagine legali conformi GDPR (Privacy, Termini, Ritiro in sede)
├── database/
│   ├── just_in_time.db          # Database SQLite relazionale
│   ├── schema.sql               # Definizione schema DDL (9 tabelle)
│   ├── dal.py                   # Data Access Layer Python
│   ├── server.py                # Server HTTP REST locale
│   ├── manage.py                # CLI per gestione catalogo e vetrina
│   └── init_and_seed.py         # Script inizializzazione e re-seed da CSV
├── catalog/
│   ├── just_in_time_shopify_products.csv  # Catalogo 15 prodotti / 17 varianti
│   ├── just_in_time_collections.json      # Struttura collezioni e tag
│   └── validate_catalog.py                # Suite di test e validazione catalogo
├── shopify-theme/               # Snippet Liquid (widget WhatsApp, trust badges)
└── docs/                        # Documentazione tecnica, piano di lancio, QA e sicurezza
```

---

## 📜 Informazioni Legali & Contatti
- **Ragione Sociale**: Just in Time di Benegiamo Andrea
- **Indirizzo**: Via Corsica 151, 73036 Muro Leccese (LE)
- **Telefono / WhatsApp**: +39 320 602 5789
- **Email**: `info@justintimemuro.it`
- **Membro ASSCOMM** (Associazione Commercianti Muro Leccese)
