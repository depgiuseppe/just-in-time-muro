# SAN-11: Report di Collaudo Formale e QA — Just in Time (Preview & Checkout)

**Progetto**: E-Commerce Shopify Just in Time di Benegiamo Andrea (Muro Leccese, LE)  
**Task ID**: `SAN-11`  
**Ruolo QA**: Dwight — QA and Test Engineer  
**Data Collaudo**: 24 Ottobre 2026  
**Ambiente di Test**: macOS / Google Chrome 155.0.8059.85 / Playwright Engine  
**Stato Finale**: **APPROVATO CON SUCCESSO (16/16 Test Superati, Bug Risolti)**

---

## 1. Obiettivo ed Ambito del Collaudo

Il presente documento certifica l'esecuzione del collaudo end-to-end e del controllo qualità formale per il rilascio del prototipo interattivo e del dataset di catalogo per il negozio **Just in Time di Benegiamo Andrea**.

### Ambito Verificato:
1. **Accuratezza e Integrità Dati Catalogo CSV** (`catalog/just_in_time_shopify_products.csv`):
   - Conformità alle 33 colonne standard Shopify.
   - Correttezza prezzi di vendita, prezzi di listino a confronto (*Compare At Price*), pesi, tassazione e tracciamento scorte.
   - Corrispondenza biunivoca con le schede prodotto esposte nel prototipo visuale.
2. **Reattività e Layout Mobile / Tablet / Desktop**:
   - Desktop (1440 × 900 px)
   - Tablet iPad (768 × 1024 px - breakpoint critico)
   - Mobile iPhone 14 (390 × 844 px)
3. **Flusso Carrello, Click & Collect e Checkout**:
   - Inserimento prodotti e apertura automatica Drawer.
   - Selezione modalità **Click & Collect** (Ritiro gratuito in negozio in Via Corsica 151, Muro Leccese a €0,00).
   - Calcolo automatico della spedizione con corriere espresso (€6,90 per ordini < €79,00; Gratuita per ordini ≥ €79,00).
   - Generazione del payload d'ordine WhatsApp per l'invio diretto ad Andrea.
4. **Conformità Percorsi Utente e Link Istituzionali/Legali** (`pages-legal/`).

---

## 2. Esito Sintetico dei Test

```mermaid
pie title Esito Test Suite QA (SAN-11)
    "Test Superati (PASS)" : 16
    "Test Falliti (FAIL)" : 0
```

| Categoria Collaudo | Casi di Test | PASS | FAIL | Esito |
| :--- | :---: | :---: | :---: | :---: |
| **Integrità & Prezzi CSV** | 17 righe / 15 prodotti | 17 | 0 | **100% Validato** |
| **Navigazione & Filtri UI** | 4 casi | 4 | 0 | **100% Validato** |
| **Carrello & Click & Collect** | 7 casi | 7 | 0 | **100% Validato** |
| **Responsive Mobile & Tablet** | 5 casi | 5 | 0 | **100% Validato** |
| **TOTALE** | **16** | **16** | **0** | **APPROVED** |

---

## 3. Analisi Dettagliata Anomalie Rilevate e Correzioni Applicate

Durante la fase di collaudo approfondito sono state scoperte tre anomalie, di cui una ad **Alta Criticità** sui dati CSV:

### BUG-01 [CRITICO]: Slittamento Colonne e Virgole Non Quotate nel CSV Catalogo
* **Gravità**: Bloccante per l'importazione Shopify.
* **Descrizione**: Il file `catalog/just_in_time_shopify_products.csv` conteneva un numero errato di colonne per riga (variabile tra 32 e 34 colonne rispetto alle 33 previste dall'intestazione):
  1. *Slittamento Opzioni*: Nelle righe a variante singola erano presenti solo 4 virgole separatrici tra `Option1 Value` e lo SKU anziché 5. Lo SKU finiva quindi nella colonna `Option3 Value`, spostando a cascata tutti i campi successivi (`Variant Grams` finiva in `Variant SKU`, `Variant Price` finiva in `Variant Fulfillment Service`, `Variant Compare At Price` finiva in `Variant Price`, ecc.).
  2. *Campi non quotati con virgole interne*:
     - La categoria `Electronics > Print, Copy, Scan & Fax > Printers` conteneva virgole senza doppi apici, generando 2 colonne spurie.
     - Le descrizioni SEO (*SEO Description*) dei record 3, 9 e 15 contenevano virgole non racchiuse tra apici.
* **Impatto sul Negozio**: Se importato grezzo, Shopify avrebbe scambiato i prezzi scontati con quelli pieni, impostato lo SKU numerico col peso, fallito la validazione numerica del Compare-At-Price e associato URL immagine al barcode.
* **Risoluzione Applicata**: Eseguito script di normalizzazione e correzione (`catalog/just_in_time_shopify_products.csv`). Ora tutte le 17 righe rispettano la struttura a 33 colonne standard, con quotatura RFC 4180 corretta.

### BUG-02 [MEDIO]: Conflitto tra Filtro Categorie e Ricerca Globale
* **Gravità**: Media (Esperienza Utente).
* **Descrizione**: Nel file `preview/index.html`, la funzione di ricerca filtrava i prodotti all'interno della sola `currentCategory` attiva. Se un utente selezionava ad esempio "Informatica & PC" e poi cercava "Toner" nella barra di ricerca dell'header, otteneva 0 risultati.
* **Risoluzione Applicata**: Aggiornato il listener dell'input `#searchInput`: non appena l'utente digita una query di ricerca, la categoria viene automaticamente reimpostata a `all` ("Tutti") e il relativo pulsante evidenziato, garantendo una ricerca globale su tutto il catalogo.

### BUG-03 [BASSO]: Link Pagine Legali nel Footer con Alert Placeholder
* **Gravità**: Bassa (Navigabilità).
* **Descrizione**: I link del footer (`Informativa Privacy`, `Cookie Policy`, `Termini di Vendita`, `Ritiro in Sede`) mostravano alert JavaScript anziché collegare le pagine HTML reali compilate in `pages-legal/`.
* **Risoluzione Applicata**: Aggiornati i tag `<a>` con puntamento relativo a `../pages-legal/` e target `_blank`.

---

## 4. Matrice di Test Eseguiti e Risultati

| ID Test | Descrizione e Percorso | Viewport / Ambiente | Risultato Atteso | Risultato Effettivo | Esito |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Caricamento Homepage e Griglia | Desktop (1440x900) | Header sticky, badges e 15 card renderizzate | Elementi visibili, nessun errore in console | **PASS** |
| **TC-02** | Filtro Categoria "Informatica & PC" | Desktop (1440x900) | Mostrati esattamente i 5 prodotti di categoria | 5 prodotti mostrati | **PASS** |
| **TC-03** | Ricerca Dinamica "Toner" | Desktop (1440x900) | Ricerca globale trova "Toner Compatibile HP 106A" | 1 prodotto mostrato | **PASS** |
| **TC-04** | Reset Filtri e Selezione "Tutti" | Desktop (1440x900) | Ripristino vista con 15 card totali | 15 card presenti | **PASS** |
| **TC-05** | Aggiunta al carrello Notebook HP 250 | Desktop (1440x900) | Aggiunta al carrello, badge a 1, apertura Drawer | Badge = 1, Drawer scivola a vista | **PASS** |
| **TC-06** | Default Click & Collect (€0,00) | Desktop (1440x900) | Opzione Ritiro in Sede spuntata, totale €549.00 | Totale = €549.00 (Sped. €0,00) | **PASS** |
| **TC-07** | Spedizione Corriere con Totale > €79 | Desktop (1440x900) | Spedizione gratis applicata (subtotal €549 > €79) | Totale = €549.00 (Spedizione gratis) | **PASS** |
| **TC-08** | Spedizione Corriere con Totale < €79 | Desktop (1440x900) | Penne (€5.90) + Corriere (€6.90) = €12.80 | Totale calcolato = €12.80 | **PASS** |
| **TC-09** | Switch a Ritiro in Sede per Totale < €79 | Desktop (1440x900) | Penne (€5.90) + Ritiro (€0.00) = €5.90 | Totale calcolato = €5.90 | **PASS** |
| **TC-10** | Trigger Simulazione Checkout | Desktop (1440x900) | Dialog con riepilogo e redirect WhatsApp | Popup formattato correttamente | **PASS** |
| **TC-11** | Chiusura Drawer Carrello | Desktop (1440x900) | Click su chiudi rimuove classe 'open' | Drawer chiuso regolarmente | **PASS** |
| **TC-12** | Layout Responsive Mobile (Hero & Header) | iPhone 14 (390x844) | Header collassato, pillole centrate, nessun overflow | Nessun overflow orizzontale | **PASS** |
| **TC-13** | Navigazione Categorie su Mobile | iPhone 14 (390x844) | Scroll/wrap categorie Stampa (3 prodotti) | 3 card renderizzate correttamente | **PASS** |
| **TC-14** | Responsive Drawer Carrello Mobile | iPhone 14 (390x844) | Larghezza drawer adattata allo schermo (<= 390px) | Larghezza = 390px esatti | **PASS** |
| **TC-15** | Visibilità Widget WhatsApp Mobile | iPhone 14 (390x844) | Pulsante galleggiante visibile con link diretto | Visibile e linkato a +39 320 602 5789 | **PASS** |
| **TC-16** | Layout Tablet Breakpoint 768px | iPad (768x1024) | Adattamento colonna e griglia fluida | Layout fluido e allineato | **PASS** |

---

## 5. Tabella di Corrispondenza Prezzi (CSV Rettificato vs Prototipo Web)

Tutti i 15 prodotti pilota sono stati comparati e validati al centesimo:

| SKU | Titolo Prodotto | Categoria | Prezzo Vendita | Prezzo Listino | Stato Verifica |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `JIT-HP250-BASE` | Notebook HP 250 G9 i5 16GB 512GB | Informatica | **€549,00** | €599,00 | **CONFORME** |
| `JIT-HP250-ZEROPENSIERI` | Notebook HP 250 G9 (Zero Pensieri) | Informatica | **€589,00** | €649,00 | **CONFORME** (CSV) |
| `JIT-THINKPAD-T480` | Notebook Lenovo ThinkPad T480 Grado A+ | Informatica | **€289,00** | €349,00 | **CONFORME** |
| `JIT-KNG-A400-480` | SSD Kingston A400 480GB SATA 3 | Informatica | **€39,90** | €49,90 | **CONFORME** |
| `JIT-LOGI-MK270` | Kit Tastiera + Mouse Logitech MK270 | Informatica | **€29,90** | €36,90 | **CONFORME** |
| `JIT-TPL-AX12` | Router Wi-Fi 6 TP-Link Archer AX12 | Informatica | **€44,90** | €54,90 | **CONFORME** |
| `JIT-EPS-603XL-BK` | Cartuccia Epson 603XL Nero Originale | Stampa | **€21,50** | €24,90 | **CONFORME** |
| `JIT-TON-HP106A-COMP` | Toner Compatibile HP 106A con Chip | Stampa | **€24,90** | €34,90 | **CONFORME** |
| `JIT-CAN-TS3350` | Stampante Multifunzione Canon PIXMA | Stampa | **€49,90** | €59,90 | **CONFORME** |
| `JIT-NAV-A4-BOX5` | Box 5 Risme Carta A4 Navigator 80g | Scuola/Uff | **€26,50** | €31,90 | **CONFORME** |
| `JIT-EAST-PAK-BLK` | Zaino Eastpak Padded Pak'r Nero 24L | Scuola | **€44,90** | €55,00 | **CONFORME** |
| `JIT-PIL-G2-TRIO` | Set 3 Penne Gel Pilot G-2 0.7mm | Cancelleria | **€5,90** | €7,20 | **CONFORME** |
| `JIT-SRV-DIAG-DESK` | Diagnosi & Riparazione PC Desktop | Servizi | **€20,00** | - | **CONFORME** |
| `JIT-SRV-DIAG-NOTE` | Diagnosi & Riparazione Notebook | Servizi | **€25,00** | - | **CONFORME** (CSV) |
| `JIT-SRV-FORMAT-STD` | Formattazione PC Windows + Backup | Servizi | **€45,00** | - | **CONFORME** |
| `JIT-SRV-UPGRADE-SSD` | Fornitura SSD 480GB + Clonazione | Servizi | **€79,00** | €95,00 | **CONFORME** |
| `JIT-SRV-LIBRI-TESTO` | Prenotazione Libri Scolastici | Scuola | **€0,00** | - | **CONFORME** |

---

## 6. Prove e Riscontri Visivi (Screenshot di Collaudo)

I riscontri fotografici sono archiviati nella directory `docs/qa/screenshots/`:
1. `01_desktop_home.png`: Render completo homepage su viewport desktop 1440x900.
2. `02_desktop_filter_informatica.png`: Filtraggio interattivo categoria Informatica & PC.
3. `03_desktop_search_toner.png`: Ricerca dinamica con reset automatico della categoria.
4. `04_desktop_cart_open.png`: Apertura drawer laterale carrello con Notebook HP e Click & Collect di default.
5. `05_desktop_cart_shipping_free.png`: Spedizione gratuita per carrello superiore alla soglia di €79,00.
6. `06_desktop_cart_shipping_charged.png`: Spedizione a €6,90 per ordini sotto soglia (es. penne a €5,90 -> totale €12,80).
7. `07_desktop_cart_pickup_pen.png`: Cambio metodo su Ritiro in Negozio con azzeramento spese di consegna.
8. `08_mobile_home_fold.png`: Layout sopra la piega su iPhone 14 (390px).
9. `09_mobile_fullpage.png`: Panoramica a tutta pagina su display mobile.
10. `10_mobile_category_stampa.png`: Selezione categoria Stampa da mobile.
11. `11_mobile_cart_drawer.png`: Drawer carrello a tutta larghezza (390px) responsive per touchscreen.
12. `12_tablet_view.png`: Breakpoint a 768px (iPad).

---

## 7. Giudizio Finale di Rilascio (QA Sign-Off)

Il prototipo `preview/index.html` e il catalogo normalizzato `catalog/just_in_time_shopify_products.csv` **soddisfano appieno tutti i requisiti di business, usabilità e integrità tecnica**:
- Il funnel d'acquisto Click & Collect valorizza la presenza locale e il negozio fisico di Muro Leccese.
- I prezzi, le descrizioni e i tag sono privi di discrepanze.
- La navigazione mobile è fluida e priva di difetti di rendering.

Si autorizza formalmente il passaggio alla **Fase 3: Provisioning Store Shopify Partner & Importazione Dati**.
