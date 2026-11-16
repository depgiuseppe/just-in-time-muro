# PROMPT MASTER — E-Commerce & Configuratore PC "Just in Time" (Muro Leccese)

Usa questo Prompt Master come specifica unica e vincolante per qualsiasi aggiornamento, rigenerazione o manutenzione del sito **Just in Time di Benegiamo Andrea**.

---

## 1. Identità Aziendale & Contatti Reali
- **Negozio**: Just in Time di Benegiamo Andrea
- **Indirizzo**: Via Corsica 151, 73036 Muro Leccese (LE)
- **WhatsApp / Telefono**: `+39 320 602 5789`
- **Orari**: Lun-Sab `08:30-13:00` / `16:30-20:00`
- **Servizi territoriali**: Vendita Hardware & Gaming, Laboratorio Riparazioni PC/Notebook, Amazon Counter, Fornitore PA MEPA, Ricariche/Bollettini, Prenotazione Libri di Testo Scolastici (Medie e Superiori) con servizio copertinatura Colibrì System.

---

## 2. Tema Visivo & Layout (Vincolante)
- **Stile originale Just in Time**: mantenere sempre il tema identitario Blu Navy (`#0f4c81`) e Oro/Ambra (`#f59e0b`) con font `Plus Jakarta Sans` (non sostituire con layout minimalisti da template).
- **Struttura Home (`index.html`)**:
  - Top announcement bar (`Click & Collect`).
  - Header con logo, barra di ricerca globale, pulsanti rapidi (`🖥️ Configura PC`, `📚 Libri Scolastici`, `🔬 Stato Riparazione`, `🛒 Carrello`).
  - Hero Banner con 4 azioni principali affiancate:
    1. `Esplora il Catalogo`
    2. `Configura il tuo PC Pezzo per Pezzo`
    3. `Laboratorio & Riparazioni`
    4. **`Servizio Prenotazione Libri di Testo Scolastici (Medie e Superiori)`** (sempre in evidenza in alto accanto agli altri bottoni Hero).
  - Trust Badges (4 card), Catalogo Ufficiale & Servizi, Footer legale GDPR, Drawer Carrello laterale, Modale Checkout (Ritiro/Spedizione + WhatsApp), Modale Stato Riparazione, Modale Prenotazione Libri Scolastici, pulsante WhatsApp flottante.

---

## 3. Catalogo, Prezzi, Immagini & Disponibilità
- **Fonte dati**: `LISTINO Camoscio.xlsx` (884 articoli reali + servizi laboratorio/scuola).
- **Sicurezza GitHub**: `LISTINO Camoscio.xlsx` deve restare **solo in locale** ed essere sempre escluso dal repository pubblico via `.gitignore`.
- **Formula Prezzi Obbligatoria**:
  $$\text{Prezzo al Pubblico} = \text{Prezzo Netto Listino} \times 1{,}20 \text{ (ricarico 20\%)} \times 1{,}22 \text{ (IVA 22\%)}$$
- **Immagini locali**: tutte le immagini reali dei prodotti devono risiedere in locale in `assets/images/camoscio/<SKU>.jpg` (e `assets/images/prodotti/` per i servizi) con attributi HTML `width` e `height` espliciti per garantire `CLS = 0`.
- **Etichette Disponibilità (Regola "In arrivo")**:
  - Se `Stock > 0`: mostrare `Disponibile (N pz)`.
  - Se `Stock <= 0`: **non scrivere mai "Manca" o "Esaurito"**. Mostrare sempre **`In arrivo`** (con la data `DataProxCons` se presente in Excel, altrimenti `In arrivo (24/48h)`). Negli slot vuoti usare `Da scegliere`.
- **Categorie Catalogo**:
  - `CPU, Schede & PC`
  - `Raffreddamento & Ventole`
  - `Case & Chassis`
  - `Alimentatori & UPS`
  - `Gaming & Sim Racing`
  - `SSD & Hard Disk`
  - `Stampa, Reti & Scanner`
  - `📚 Libri Scolastici`
  - `Laboratorio & Riparazioni`
  - Con filtri dinamici a tendina per **Sottocategoria**, **Marca** e **Ordinamento / Solo disponibili**.

---

## 4. Servizio Prenotazione Libri Scolastici (Medie e Superiori)
- Accessibile sia dall'Hero (a fianco a *Esplora il Catalogo* e *Laboratorio & Riparazioni*) sia dall'Header.
- Modale interattivo ad **Anticipo Zero**:
  - Campi: Nome e Cognome Genitore/Studente, Cellulare/WhatsApp, Istituto Scolastico, Classe/Sezione, Elenco Libri / Codici ISBN.
  - Checkbox per foderatura protettiva trasparente **Colibrì System**.
  - Invio diretto con messaggio pre-compilato su WhatsApp ad Andrea (`+39 320 602 5789`) + salvataggio su API locale `/api/book_reservations` se attiva.

---

## 5. Configuratore PC Custom (`#pcBuilderSection` / `configuratore.html`)
- **Sezione separata a parte (Toggle Apri/Chiudi)**:
  - Su `index.html` la sezione è **nascosta di default** (`display: none`).
  - **1° clic** su `🖥️ Configura PC`: apre il Configuratore PC e nasconde Hero/Catalogo.
  - **2° clic** su `🖥️ Configura PC` (o su `← Torna al Catalogo Completo`): chiude il Configuratore e ripristina la schermata principale.
- **Wizard Guidato in 10 Passi Anti-Dimenticanza**:
  1. Processore (CPU)
  2. Scheda Madre (filtrata automaticamente per Socket CPU)
  3. Memoria RAM (filtro DDR4/DDR5 + selettore `1x` o `2x Dual-Channel`)
  4. Dissipatore CPU (avviso se la CPU è senza ventola in scatola)
  5. SSD Primario (M.2 NVMe / SATA)
  6. Scheda Video (blocco grafica integrata se CPU serie `KF`)
  7. Case / Cabinet (evidenziazione supporto radiatore 360mm)
  8. Alimentatore (calcolo in tempo reale dei Watt stimati e margine consigliato)
  9. Extra (HDD archivio, Ventole ARGB, UPS gruppo di continuità)
  10. Monitor, Kit Tastiera/Mouse & Software
- **Filtro Disponibilità Rigoroso**: con `Solo disponibili subito` attivo, mostrare **solo** componenti con `stock > 0`.
- **3 Preset Pronti**: *Base Ufficio & Studio*, *Base Gaming AM5 2K/4K*, *Base Extreme 9800X3D*.
- **Checklist Finale "Non Dimenticare"**: spunte per *Assemblaggio Professionale & Test (+€35,00)* e *Licenza Windows 11 Pro 64-Bit (+€122,28)*.
- **Drag & Drop Bidirezionale (Desktop)**:
  - Trascinare un componente dalla lista al Riepilogo / Drop Zone per montarlo.
  - Trascinare un componente già montato nel Riepilogo verso la *Zona Smontaggio 🗑️* (o nella colonna sinistra) per toglierlo.
- **Azioni Finali**: Aggiungi tutti i pezzi al Carrello in 1 click, Invia configurazione su WhatsApp ad Andrea, Stampa / Salva Preventivo PDF.

---

## 6. Ottimizzazione Mobile (Smartphone `390px`)
- **Zero taglio o overflow a destra** (`scrollWidth === innerWidth` su `390px`):
  - Usare `grid-template-columns: minmax(0, 1fr)` e `min-width: 0; max-width: 100%;` su tutti i contenitori Grid/Flex del configuratore e delle tendine.
  - Testi lunghi e SKU con `overflow-wrap: anywhere`.
- **UX Smartphone**:
  - Categorie e barra dei 10 passaggi scorrevoli orizzontalmente (`overflow-x: auto`) con auto-centramento del passo attivo.
  - Nascosti su touchscreen gli avvisi e le maniglie Drag & Drop desktop.
  - **Barra Fissa in Basso (`#pcMobileStickyBar`)** nel Configuratore PC con totale aggiornato, contatore pezzi, Watt e tasto `📋 Riepilogo ↓`.
  - Lista opzioni senza doppio scroll interno (`max-height: none`) e pulsanti touch `min-height: 44px`.
  - Modali a 1 colonna e pannello `database/admin.html` responsive con tabelle scrollabili orizzontalmente.

---

## 7. Qualità, Deploy & Comunicazione Telegram
- **Controlli automatici `design-taste-frontend` (`taste-skill`)**:
  - `copy-lint.mjs`: `0 FAIL, 0 WARN` (niente parole fluff o punti esclamativi nel copy UI).
  - `perf.mjs` (`1440px` & `390px`): `0 FAIL`, `0` richieste rotte, `CLS ~0.000`.
- **Deploy su GitHub Pages**:
  - Repository pubblico: `https://github.com/depgiuseppe/just-in-time-muro` (Live: `https://depgiuseppe.github.io/just-in-time-muro/`).
  - Eseguire sempre `git push` da staging APFS locale (`/tmp/jit_repo.git`) con token `gh auth token` per evitare blocchi `mmap` di Google Drive.
  - Mantenere sempre sincronizzati `index.html`, `preview/index.html` e `configuratore.html`.
- **Telegram Real-time**:
  - Inviare ogni aggiornamento di stato su Telegram tramite `send_telegram_notification.py`.
  - Tenere attivo il listener `wait_for_telegram_message.py` in background per eseguire i comandi inviati da Telegram.
