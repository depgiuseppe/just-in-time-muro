#!/usr/bin/env python3
"""
Inizializzazione e Seeding del Database Locale per Just in Time di Benegiamo Andrea
Importa categorie e prodotti direttamente dal catalogo validato e crea dati di test
per ordini, clienti, ticket di laboratorio e prenotazione libri.
"""

import os
import csv
import json
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "just_in_time.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")
COLLECTIONS_JSON = os.path.join(BASE_DIR, "catalog", "just_in_time_collections.json")
PRODUCTS_CSV = os.path.join(BASE_DIR, "catalog", "just_in_time_shopify_products.csv")

def init_database():
    print(f"--> Creazione database SQLite: {DB_PATH}")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Esecuzione schema SQL
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    print("✔ Schema tabelle creato con successo.")

    # 2. Inserimento Categorie da collections.json
    with open(COLLECTIONS_JSON, "r", encoding="utf-8") as f:
        col_data = json.load(f)

    category_map = {} # handle -> id
    for idx, col in enumerate(col_data.get("collections", []), 1):
        cursor.execute("""
            INSERT INTO categories (code, name, description, sort_order)
            VALUES (?, ?, ?, ?)
        """, (col["handle"], col["title"], col["description"], idx * 10))
        category_map[col["handle"]] = cursor.lastrowid

    print(f"✔ Inserite {len(category_map)} categorie principali.")

    # Mappatura tag -> categoria
    tag_to_cat = {
        "informatica": category_map.get("informatica-tecnologia"),
        "stampa": category_map.get("stampa-consumabili"),
        "scuola": category_map.get("scuola-cancelleria"),
        "servizi": category_map.get("servizi-assistenza-tecnica"),
        "promo:outlet": category_map.get("offerte-outlet")
    }

    # 3. Inserimento Prodotti e Varianti dal CSV Shopify
    products_seen = {} # handle -> product_id
    rows_inserted = 0

    with open(PRODUCTS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            handle = row["Handle"]
            title = row["Title"]
            body_html = row["Body (HTML)"]
            vendor = row["Vendor"]
            ptype = row["Type"]
            tags_str = row["Tags"]
            tags = [t.strip() for t in tags_str.split(",") if t.strip()]

            # Determina categoria primaria
            cat_id = None
            for t in tags:
                if t in tag_to_cat:
                    cat_id = tag_to_cat[t]
                    break
            if not cat_id:
                cat_id = category_map.get("informatica-tecnologia")

            # Inserisci o recupera prodotto base
            if handle not in products_seen:
                base_price = float(row["Variant Price"])
                comp_price = float(row["Variant Compare At Price"]) if row["Variant Compare At Price"] else None
                is_avail = 1 if "disp:immediata" in tags_str else 0
                lead_time = 2 if is_avail else 24
                req_ship = 1 if row["Variant Requires Shipping"].upper() == "TRUE" else 0
                condition = "Ricondizionato Grado A+" if "ricondizionato" in tags_str.lower() else "Nuovo"
                warranty = 12 if "ricondizionato" in tags_str.lower() else 24
                img_url = row["Image Src"]

                cursor.execute("""
                    INSERT INTO products (
                        category_id, handle, title, description_html, vendor,
                        product_type, base_price, compare_at_price, is_available_in_store,
                        lead_time_hours, requires_shipping, condition, warranty_months, image_url
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cat_id, handle, title, body_html, vendor,
                    ptype, base_price, comp_price, is_avail,
                    lead_time, req_ship, condition, warranty, img_url
                ))
                prod_id = cursor.lastrowid
                products_seen[handle] = prod_id

                # Inserisci Tags
                for t in tags:
                    cursor.execute("""
                        INSERT OR IGNORE INTO product_tags (product_id, tag)
                        VALUES (?, ?)
                    """, (prod_id, t))
            else:
                prod_id = products_seen[handle]

            # Inserisci Variante
            var_sku = row["Variant SKU"]
            var_title = row["Option1 Value"] if row["Option1 Value"] else "Standard"
            opt_name = row["Option1 Name"] if row["Option1 Name"] else None
            opt_val = row["Option1 Value"] if row["Option1 Value"] else None
            var_price = float(row["Variant Price"])
            var_comp = float(row["Variant Compare At Price"]) if row["Variant Compare At Price"] else None
            var_stock = int(row["Variant Inventory Qty"]) if row["Variant Inventory Qty"] else 0
            var_barcode = row["Variant Barcode"] if row["Variant Barcode"] else None
            var_weight = int(row["Variant Grams"]) if row["Variant Grams"] else 0

            cursor.execute("""
                INSERT INTO product_variants (
                    product_id, sku, title, option1_name, option1_value,
                    price, compare_at_price, stock_quantity, barcode, weight_grams
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prod_id, var_sku, var_title, opt_name, opt_val,
                var_price, var_comp, var_stock, var_barcode, var_weight
            ))
            rows_inserted += 1

    print(f"✔ Inseriti {len(products_seen)} prodotti univoci e {rows_inserted} varianti dal catalogo.")

    # 4. Inserimento Clienti Pilota (Territorio Salento)
    cursor.execute("""
        INSERT INTO customers (first_name, last_name, email, phone, address, city, fiscal_code, notes)
        VALUES 
        ('Marco', 'Verdi', 'marco.verdi@gmail.com', '+39 347 1234567', 'Via Roma 12', 'Muro Leccese', 'VRDMRC85M01E506X', 'Cliente abituale per cartucce e assistenza'),
        ('Elena', 'Russo', 'elena.russo@libero.it', '+39 338 9876543', 'Piazza Dante 5', 'Maglie', 'RSSLNE90A41E506Y', 'Genitore per prenotazione testi scolastici medie'),
        ('Studio Tecnico Ing. Greco', 'Greco', 'info@studiogreco.it', '+39 0836 12345', 'Via Corsica 80', 'Muro Leccese', '04589210753', 'Fornitura risme e toner per ufficio')
    """)
    cust_id_1 = 1
    cust_id_2 = 2
    cust_id_3 = 3
    print("✔ Inseriti 3 clienti campione locali.")

    # 5. Inserimento Ordine Esempio Click & Collect
    cursor.execute("""
        INSERT INTO orders (
            order_number, customer_id, delivery_type, pickup_location,
            order_status, payment_method, payment_status, subtotal,
            shipping_fee, total_amount, customer_notes, internal_notes
        ) VALUES (
            'JIT-2026-0001', ?, 'pickup', 'Via Corsica 151, Muro Leccese',
            'ready_for_pickup', 'pos_on_pickup', 'pending', 39.90,
            0.00, 39.90, 'Ritiro oggi pomeriggio verso le 17:30', 'Preparato in cassa da Andrea'
        )
    """, (cust_id_1,))
    order_id = cursor.lastrowid

    # Riga ordine SSD Kingston
    cursor.execute("""
        SELECT id, product_id, price FROM product_variants WHERE sku = 'JIT-KNG-A400-480'
    """)
    var_row = cursor.fetchone()
    if var_row:
        cursor.execute("""
            INSERT INTO order_items (
                order_id, product_id, variant_id, product_title, variant_title, sku, unit_price, quantity, subtotal
            ) VALUES (?, ?, ?, 'SSD Interno Kingston A400 480GB', 'Default Title', 'JIT-KNG-A400-480', 39.90, 1, 39.90)
        """, (order_id, var_row[1], var_row[0]))

    print("✔ Creato ordine pilota di test Click & Collect #JIT-2026-0001.")

    # 6. Inserimento Ticket di Laboratorio Assistenza
    cursor.execute("""
        INSERT INTO repair_tickets (
            ticket_number, customer_id, device_type, brand_model, serial_number,
            reported_issue, diagnosis_notes, advance_fee, estimated_cost, status
        ) VALUES (
            'LAB-2026-0012', ?, 'notebook', 'HP Pavilion 15-cw', '5CD9123XYZ',
            'Surriscaldamento anomalo e spegnimento improvviso dopo 10 minuti di utilizzo',
            'Ventola ostruita da lanugine e pasta termica completamente seccata. Richiesta pulizia interna.',
            25.00, 45.00, 'in_repair'
        )
    """, (cust_id_1,))
    print("✔ Creato ticket di laboratorio pilota #LAB-2026-0012.")

    # 7. Inserimento Prenotazione Libri Scolastici
    cursor.execute("""
        INSERT INTO book_reservations (
            reservation_code, customer_id, student_name, school_name, class_grade,
            book_list_text, colibri_covers_required, status
        ) VALUES (
            'LIB-2026-0001', ?, 'Matteo Russo', 'Istituto Comprensivo Statale Muro Leccese', 'Classe 1B Scuola Media',
            'Antologia Italiana (ISBN: 9788808123456), Matematica Vol. 1 (ISBN: 9788808987654), Storia e Geografia (ISBN: 9788842412345)',
            1, 'partially_arrived'
        )
    """, (cust_id_2,))
    print("✔ Creata prenotazione libri scolastici pilota #LIB-2026-0001.")

    conn.commit()
    conn.close()
    print("🎉 Database locale SQLite inizializzato e popolato con successo al 100%!")

if __name__ == "__main__":
    init_database()
