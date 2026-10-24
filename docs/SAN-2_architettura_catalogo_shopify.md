# SAN-2: Architettura Catalogo, Tassonomia e Collezioni Shopify
**Progetto**: Just in Time di Benegiamo Andrea (E-Commerce Shopify)  
**Data**: 2026-10-24  
**Stato**: Completato (Fase 1 - Ricerca e Progettazione)

---

## 1. Struttura delle Collezioni Shopify

Shopify gestisce il catalogo mediante **Collezioni Automatizzate** (basate su tag e condizioni di prodotto) e **Collezioni Manuali** per promozioni o selezioni speciali.

### Mappa Principale dell'Albero delle Categorie

```
HOME
├── 1. INFORMATICA & TECNOLOGIA
│   ├── Computer & Notebook (Nuovo e Ricondizionato Garantito)
│   ├── Componenti PC (SSD, RAM, Alimentatori, Schede Video)
│   ├── Periferiche & Accessori (Mouse, Tastiere, Cuffie, Webcam, Monitor)
│   ├── Networking & Wi-Fi (Router, Switch, Range Extender, Cavi LAN)
│   └── Archiviazione (Hard Disk Esterni, Pendrive, Schede MicroSD)
│
├── 2. STAMPA & CONSUMABILI
│   ├── Cartucce Inkjet (Originali e Compatibili)
│   ├── Toner Laser (Originali e Compatibili Garantiti)
│   ├── Stampanti & Multifunzione (Casa e Ufficio)
│   └── Carta Speciale e Fotografica
│
├── 3. SCUOLA & CANCELLERIA
│   ├── Cancelleria Ufficio (Risme A4, Faldoni, Raccoglitori, Buste)
│   ├── Materiale Didattico & Scuola (Zaini, Astucci, Quaderni, Disegno Tecnico)
│   └── Libri di Testo (Servizio di prenotazione / lista scolastica)
│
├── 4. SERVIZI & ASSISTENZA TECNICA (Schede Servizio prenotabili)
│   ├── Diagnosi & Riparazione PC / Notebook
│   ├── Formattazione & Installazione Sistema Operativo + Backup Dati
│   ├── Pulizia Hardware e Sostituzione Pasta Termica
│   ├── Assemblaggio PC Gaming / Workstation su Misura
│   └── Richiesta Preventivo B2B / MEPA
│
└── 5. OFFERTE & OUTLET
    ├── Bestseller del Mese
    ├── Ricondizionati d'Occasione
    └── Fine Serie & Sottocosto
```

---

## 2. Definizione dei Campi Prodotto & Metafields Shopify

Per rendere la navigazione fluida e i filtri precisi su Shopify (usando l'app nativa *Search & Discovery*), ciascun prodotto utilizzerà una convenzione rigorosa di **Tag** e **Metafield**:

### Campi Standard:
* **Titolo**: [Marca] + [Modello] + [Caratteristica Principale] + [Colore/Variante]  
  *Es: "HP 250 G9 Notebook 15.6'' Intel Core i5 16GB RAM 512GB SSD Windows 11 Pro"*
* **Vendor (Fornitore)**: HP, Lenovo, ASUS, Kingston, Epson, Canon, Logitech, Buffetti, ecc.
* **Product Type**: Notebook, SSD, Toner, Cartuccia, Raccoglitore, Riparazione.
* **Tags Standardizzati**:
  * `disp:immediata` (disponibile in negozio a Muro Leccese)
  * `disp:ordine24h` (disponibile su ordinazione rapida)
  * `servizio:configurazione` (abbinabile a pacchetto installazione)
  * `promo:vetrina` (in evidenza in homepage)

### Metafields Custom (Shopify 2.0):
1. `custom.condizione`: Nuovo | Ricondizionato Grado A+ | Ricondizionato Grado A
2. `custom.garanzia_mesi`: 12 | 24 | 36
3. `custom.ritiro_negozio_ore`: 2 | 24 | 48
4. `custom.compatibilita_stampanti`: Elenco modelli compatibili (per toner/cartucce)
5. `custom.scheda_tecnica_pdf`: Link al manuale o datasheet PDF

---

## 3. Gestione Varianti e Servizi Aggiunti al Carrello
Shopify consente di associare varianti o opzioni con incremento di prezzo:
* **Esempio Prodotto Notebook**:
  * Variante Base: Notebook solo hardware.
  * + €29,00: Pacchetto "Ready to Work" (Aggiornamento Windows + Suite Ufficio + Antivirus + Pulizia Bloatware).
  * + €49,00: Pacchetto "Zero Pensieri" (Tutto il precedente + Travaso completo dati dal vecchio computer).
