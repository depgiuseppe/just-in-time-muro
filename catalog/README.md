# Catalogo Prodotti & Collezioni Shopify — Just in Time

Questa directory contiene i dati e gli strumenti per l'allestimento del catalogo e-commerce dello store **Just in Time di Benegiamo Andrea** (Muro Leccese, LE).

## File Inclusi

1. **`just_in_time_shopify_products.csv`**  
   Dataset ufficiale a 33 colonne standard Shopify contenente il set pilota di 15 prodotti e 17 varianti (hardware nuovo, ricondizionato garantito, periferiche, consumabili originali e compatibili, cancelleria, pacchetti configurazione e schede servizio di laboratorio).
   - Conforme alle specifiche native di importazione Shopify.
   - Pesi in grammi configurati per il calcolo automatizzato delle tariffe corriere.
   - Gestione differenziata per articoli fisici (`Requires Shipping = TRUE`) e servizi/prenotazioni in laboratorio (`Requires Shipping = FALSE`).
   - Barcode EAN-13 reali e SKU standardizzati (`JIT-XXX`).

2. **`just_in_time_collections.json`**  
   Definizione delle 5 macro-collezioni automatizzate dello store e delle rispettive condizioni basate su tag (`informatica`, `stampa`, `scuola`, `servizi`, `promo:outlet`).

3. **`validate_catalog.py`**  
   Script Python di validazione e test automatico. Verifica la conformità delle 33 colonne per ogni riga, l'univocità degli SKU, la validità dei prezzi e la copertura delle collezioni.
   ```bash
   python3 catalog/validate_catalog.py
   ```

## Documentazione e Guida Operativa

Per le istruzioni dettagliate passo-passo sull'importazione nel pannello Shopify Partner, la configurazione delle collezioni e il setup del Click & Collect (Ritiro in sede), fare riferimento a:  
**[`docs/GUIDA_IMPORTAZIONE_SHOPIFY_PARTNER.md`](../docs/GUIDA_IMPORTAZIONE_SHOPIFY_PARTNER.md)**
