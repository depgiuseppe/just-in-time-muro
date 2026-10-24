#!/usr/bin/env python3
"""
Strumento di Gestione Semplice del Catalogo, Ordini e Riparazioni
Just in Time di Benegiamo Andrea (Muro Leccese)

Uso da terminale:
  python3 database/manage.py list                     (elenca tutti gli articoli nel database)
  python3 database/manage.py search <testo>           (cerca articoli per nome o codice SKU)
  python3 database/manage.py price <SKU> <prezzo>     (aggiorna il prezzo al volo)
  python3 database/manage.py stock <SKU> <qta>        (aggiorna la giacenza di magazzino)
  python3 database/manage.py feature <SKU> <1|0>      (imposta articolo in vetrina o standard)
  python3 database/manage.py add                      (procedura guidata per inserire un nuovo articolo)
  python3 database/manage.py orders                   (mostra gli ordini recenti e Click & Collect)
  python3 database/manage.py repairs                  (mostra le schede del laboratorio assistenza)
  python3 database/manage.py new-repair               (accettazione rapida PC/dispositivo al banco)
  python3 database/manage.py stats                    (cruscotto riassuntivo incassi e riparazioni)
  python3 database/manage.py backup                   (esegue copia di sicurezza del database)
  python3 database/manage.py sync-csv                 (risincronizza il database dal file CSV)
"""

import os
import sys
import shutil
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "just_in_time.db")

# Aggiungi cartella database al path per importare dal
sys.path.insert(0, os.path.join(BASE_DIR, "database"))
from dal import JustInTimeDAL

def get_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database non trovato in {DB_PATH}.")
        print("Esegui prima: python3 database/init_and_seed.py")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def list_products(query=None):
    conn = get_db()
    cursor = conn.cursor()
    sql = """
        SELECT p.id, pv.sku, p.title, c.name as category, pv.price, pv.stock_quantity, 
               p.is_featured, p.is_available_in_store
        FROM products p
        JOIN categories c ON p.category_id = c.id
        LEFT JOIN product_variants pv ON pv.product_id = p.id
        WHERE p.status = 'active'
    """
    params = []
    if query:
        sql += " AND (p.title LIKE ? OR pv.sku LIKE ? OR p.vendor LIKE ?)"
        w = f"%{query}%"
        params = [w, w, w]
    
    sql += " ORDER BY p.is_featured DESC, c.sort_order, p.id"
    rows = cursor.execute(sql, params).fetchall()

    print("\n" + "="*95)
    print(f"📦 CATALOGO PRODOTTI & MAGAZZINO — JUST IN TIME ({len(rows)} articoli)")
    print("="*95)
    print(f"{'ID':<4} | {'SKU':<20} | {'PREZZO':<9} | {'Q.TÀ':<5} | {'VETRINA':<8} | {'TITOLO':<40}")
    print("-"*95)

    for r in rows:
        sku = r['sku'] or "N/D"
        prezzo = f"€{r['price']:.2f}" if r['price'] is not None else "N/D"
        qta = str(r['stock_quantity']) if r['stock_quantity'] is not None else "0"
        vetrina = "⭐ SI" if r['is_featured'] else "no"
        titolo = (r['title'][:37] + '...') if len(r['title']) > 40 else r['title']
        print(f"{r['id']:<4} | {sku:<20} | {prezzo:<9} | {qta:<5} | {vetrina:<8} | {titolo:<40}")
    print("="*95 + "\n")
    conn.close()

def update_price(sku, new_price):
    try:
        price_val = float(new_price.replace(',', '.'))
    except ValueError:
        print(f"❌ Prezzo non valido: {new_price}. Usa ad esempio: 49.90")
        return

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE product_variants SET price = ? WHERE sku = ?", (price_val, sku))
    if cursor.rowcount == 0:
        print(f"❌ Nessun articolo trovato con SKU '{sku}'.")
    else:
        conn.commit()
        print(f"✔ Prezzo dell'articolo {sku} aggiornato a €{price_val:.2f} con successo.")
    conn.close()

def update_stock(sku, new_stock):
    try:
        stock_val = int(new_stock)
    except ValueError:
        print(f"❌ Quantità non valida: {new_stock}. Usa un numero intero (es. 5)")
        return

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE product_variants SET stock_quantity = ? WHERE sku = ?
    """, (stock_val, sku))
    if cursor.rowcount == 0:
        print(f"❌ Nessun articolo trovato con SKU '{sku}'.")
    else:
        cursor.execute("""
            UPDATE products 
            SET is_available_in_store = CASE WHEN ? > 0 THEN 1 ELSE 0 END
            WHERE id = (SELECT product_id FROM product_variants WHERE sku = ?)
        """, (stock_val, sku))
        conn.commit()
        print(f"✔ Giacenza di magazzino per {sku} aggiornata a {stock_val} pezzi.")
    conn.close()

def toggle_featured(sku, featured_val):
    is_feat = 1 if str(featured_val) in ['1', 'true', 'si', 'yes'] else 0
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products 
        SET is_featured = ?
        WHERE id = (SELECT product_id FROM product_variants WHERE sku = ?)
    """, (is_feat, sku))
    if cursor.rowcount == 0:
        print(f"❌ Nessun articolo trovato con SKU '{sku}'.")
    else:
        conn.commit()
        stato = "in vetrina (⭐ SI)" if is_feat else "standard (no)"
        print(f"✔ Articolo {sku} impostato come {stato}.")
    conn.close()

def add_product_interactive():
    conn = get_db()
    cursor = conn.cursor()
    categories = cursor.execute("SELECT id, name, code FROM categories ORDER BY sort_order").fetchall()

    print("\n--- INSERIMENTO NUOVO ARTICOLO ---")
    title = input("Titolo prodotto: ").strip()
    if not title:
        print("❌ Titolo obbligatorio.")
        return

    print("\nSeleziona Categoria:")
    for idx, c in enumerate(categories, 1):
        print(f"  {idx}) {c['name']} ({c['code']})")
    cat_choice = input(f"Scelta (1-{len(categories)}): ").strip()
    try:
        cat_id = categories[int(cat_choice) - 1]['id']
    except Exception:
        cat_id = categories[0]['id']

    vendor = input("Marca / Produttore (es. HP, Kingston, Buffetti): ").strip() or "Just in Time"
    sku = input("Codice SKU (univoco, es. JIT-MOUSE-01): ").strip()
    if not sku:
        sku = f"JIT-GEN-{int(os.times().system * 1000)}"

    price_str = input("Prezzo al pubblico in € (es. 19.90): ").strip()
    try:
        price = float(price_str.replace(',', '.'))
    except ValueError:
        price = 0.0

    stock_str = input("Giacenza iniziale in negozio (es. 5): ").strip() or "1"
    stock = int(stock_str)

    desc = input("Descrizione breve (opzionale): ").strip() or title
    img = input("URL immagine (opzionale, invio per default): ").strip() or "assets/images/prodotti/notebook-hp-250-g9-i5-16gb.jpg"

    handle = sku.lower().replace(" ", "-")

    cursor.execute("""
        INSERT INTO products (
            handle, title, description_html, category_id, vendor,
            product_type, is_featured, is_available_in_store, image_url, status
        ) VALUES (?, ?, ?, ?, ?, 'Articolo Negozio', 1, 1, ?, 'active')
    """, (handle, title, desc, cat_id, vendor, img))
    prod_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO product_variants (
            product_id, sku, title, price, stock_quantity, is_active
        ) VALUES (?, ?, 'Default', ?, ?, 1)
    """, (prod_id, sku, price, stock))

    conn.commit()
    conn.close()
    print(f"\n✔ Articolo '{title}' creato con successo nel Database Locale con SKU {sku} e Prezzo €{price:.2f}!\n")

def show_orders():
    orders = JustInTimeDAL.get_orders(limit=25)
    print("\n" + "="*95)
    print(f"🛒 ORDINI CLIENTI & CLICK & COLLECT — JUST IN TIME ({len(orders)} recenti)")
    print("="*95)
    print(f"{'ORDINE':<18} | {'DATA':<16} | {'CLIENTE':<20} | {'TIPO':<8} | {'TOTALE':<9} | {'STATO':<14}")
    print("-"*95)
    for o in orders:
        cust = f"{o.get('first_name', '')} {o.get('last_name', '')}".strip()
        date_str = (o.get('created_at') or '')[:16]
        tot = f"€{float(o['total_amount']):.2f}"
        print(f"{o['order_number']:<18} | {date_str:<16} | {cust[:20]:<20} | {o['delivery_type']:<8} | {tot:<9} | {o['order_status']:<14}")
    print("="*95 + "\n")

def show_repairs():
    repairs = JustInTimeDAL.get_repair_tickets(limit=25)
    print("\n" + "="*95)
    print(f"🔬 SCHEDE LABORATORIO ASSISTENZA — JUST IN TIME ({len(repairs)} recenti)")
    print("="*95)
    print(f"{'SCHEDA':<15} | {'DISPOSITIVO':<18} | {'CLIENTE':<18} | {'TEL':<14} | {'ACCONTO':<8} | {'STATO':<14}")
    print("-"*95)
    for r in repairs:
        cust = f"{r.get('first_name', '')} {r.get('last_name', '')}".strip()
        dev = f"{r['device_type'].upper()}: {r['brand_model']}"
        acc = f"€{r.get('advance_fee', 0.0):.2f}"
        print(f"{r['ticket_number']:<15} | {dev[:18]:<18} | {cust[:18]:<18} | {r.get('phone', '')[:14]:<14} | {acc:<8} | {r['status']:<14}")
    print("="*95 + "\n")

def new_repair_interactive():
    print("\n--- 🛠️ NUOVA ACCETTAZIONE DISPOSITIVO AL BANCO ---")
    first_name = input("Nome Cliente: ").strip() or "Cliente"
    last_name = input("Cognome Cliente: ").strip() or "Banco"
    phone = input("Telefono / WhatsApp (obbligatorio): ").strip()
    if not phone:
        print("❌ Recapito telefonico obbligatorio per notifiche di riparazione.")
        return
    email = input("Email (opzionale): ").strip()

    print("\nTipo dispositivo:")
    print("  1) Notebook / Portatile")
    print("  2) PC Desktop / Fisso")
    print("  3) Smartphone / Tablet")
    print("  4) Stampante")
    print("  5) Altro")
    dtype_choice = input("Scelta (1-5, invio per notebook): ").strip()
    dtype_map = {"1": "notebook", "2": "desktop", "3": "smartphone", "4": "printer", "5": "other"}
    device_type = dtype_map.get(dtype_choice, "notebook")

    brand_model = input("Marca e Modello (es. HP 15s, ASUS VivoBook): ").strip()
    if not brand_model:
        brand_model = "Dispositivo generico"

    serial = input("Matricola / Serial Number (se presente): ").strip()
    issue = input("Guasto / Problema riscontrato: ").strip()
    if not issue:
        issue = "Diagnosi generale e controllo hardware/software"

    advance_str = input("Acconto versato in cassa in € (es. 20.00, invio per 20): ").strip() or "20"
    try:
        advance = float(advance_str.replace(',', '.'))
    except ValueError:
        advance = 20.0

    ticket = JustInTimeDAL.create_repair_ticket(
        customer_info={"first_name": first_name, "last_name": last_name, "phone": phone, "email": email},
        device_type=device_type,
        brand_model=brand_model,
        reported_issue=issue,
        serial_number=serial,
        advance_fee=advance
    )
    print(f"\n✔ Scheda creata con successo: {ticket['ticket_number']}")
    print(f"  Visualizza ricevuta e talloncino: http://127.0.0.1:8080/api/repairs/{ticket['ticket_number']}/receipt\n")

def show_stats():
    s = JustInTimeDAL.get_stats()
    print("\n" + "="*60)
    print("📊 CRUSCOTTO JUST IN TIME (MURO LECCESE)")
    print("="*60)
    print(f"  • Articoli Attivi a Catalogo:     {s['active_products']}")
    print(f"  • Totale Ordini Registrati:       {s['total_orders']}")
    print(f"  • Ordini da Evadere / Preparare:  {s['pending_orders']}")
    print(f"  • Incassato Totale Vendite:       €{s['total_revenue_eur']:.2f}")
    print(f"  • Riparazioni PC Aperte nel Lab:  {s['open_repairs_count']} ({s['ready_repairs_count']} pronte al ritiro)")
    print(f"  • Prenotazioni Libri di Testo:    {s['open_book_reservations_count']}")
    print(f"  • Prodotti con Scorta Bassa:      {s['low_stock_items_count']}")
    print("="*60 + "\n")

def backup_db():
    backup_dir = os.path.join(BASE_DIR, "database", "backups")
    os.makedirs(backup_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(backup_dir, f"just_in_time_{ts}.db")
    shutil.copy2(DB_PATH, dest)
    print(f"✔ Backup del database creato con successo:")
    print(f"  {dest} ({os.path.getsize(dest)} bytes)")

def sync_csv():
    import subprocess
    script_seed = os.path.join(BASE_DIR, "database", "init_and_seed.py")
    print(f"--> Risincronizzazione dal file CSV tramite: {script_seed}")
    res = subprocess.run([sys.executable, script_seed])
    if res.returncode == 0:
        print("✔ Database locale risincronizzato con successo dal file CSV!")
    else:
        print("❌ Errore durante la risincronizzazione.")

def main():
    if len(sys.argv) < 2:
        list_products()
        print("Suggerimento comandi:")
        print("  python3 database/manage.py list")
        print("  python3 database/manage.py search <nome>")
        print("  python3 database/manage.py price <SKU> <prezzo>")
        print("  python3 database/manage.py stock <SKU> <quantita>")
        print("  python3 database/manage.py feature <SKU> 1")
        print("  python3 database/manage.py add")
        print("  python3 database/manage.py orders")
        print("  python3 database/manage.py repairs")
        print("  python3 database/manage.py new-repair")
        print("  python3 database/manage.py stats")
        print("  python3 database/manage.py backup")
        print("  python3 database/manage.py sync-csv\n")
        return

    cmd = sys.argv[1].lower()
    if cmd == "list":
        list_products()
    elif cmd == "search" and len(sys.argv) > 2:
        list_products(sys.argv[2])
    elif cmd == "price" and len(sys.argv) >= 4:
        update_price(sys.argv[2], sys.argv[3])
    elif cmd == "stock" and len(sys.argv) >= 4:
        update_stock(sys.argv[2], sys.argv[3])
    elif cmd == "feature" and len(sys.argv) >= 4:
        toggle_featured(sys.argv[2], sys.argv[3])
    elif cmd == "add":
        add_product_interactive()
    elif cmd == "orders":
        show_orders()
    elif cmd == "repairs":
        show_repairs()
    elif cmd == "new-repair":
        new_repair_interactive()
    elif cmd == "stats":
        show_stats()
    elif cmd == "backup":
        backup_db()
    elif cmd == "sync-csv":
        sync_csv()
    else:
        print(f"Comando non riconosciuto: {cmd}")
        print("Usa: list, search, price, stock, feature, add, orders, repairs, new-repair, stats, backup, sync-csv")

if __name__ == "__main__":
    main()
