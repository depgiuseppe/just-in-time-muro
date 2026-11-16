#!/usr/bin/env python3
"""
Data Access Layer (DAL) per Just in Time di Benegiamo Andrea (Muro Leccese)
Gestione unificata e sicura di Catalogo, Ordini, Laboratorio Riparazioni e Prenotazioni.
Nessuna dipendenza esterna: SQLite3 nativo con foreign keys attive.
"""

import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "just_in_time.db")

COMPANY_INFO = {
    "name": "Just in Time di Benegiamo Andrea",
    "address": "Via Corsica 151",
    "city": "73036 Muro Leccese (LE)",
    "phone": "+39 320 602 5789",
    "email": "info@justintimesalento.it",
    "vat": "IT04589210753"
}

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

class JustInTimeDAL:

    # -------------------------------------------------------------
    # CATEGORIE & CATALOGO PRODOTTI
    # -------------------------------------------------------------

    @staticmethod
    def get_categories():
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT c.*, COUNT(p.id) as products_count
                FROM categories c
                LEFT JOIN products p ON p.category_id = c.id AND p.status = 'active'
                WHERE c.is_active = 1
                GROUP BY c.id
                ORDER BY c.sort_order ASC
            """).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_products(category_code=None, query=None, only_in_store=False, featured_only=False):
        with get_connection() as conn:
            sql = """
                SELECT p.*, c.name as category_name, c.code as category_code,
                       GROUP_CONCAT(t.tag, ', ') as tags_list,
                       MIN(pv.price) as min_price, MAX(pv.price) as max_price,
                       SUM(pv.stock_quantity) as total_stock
                FROM products p
                JOIN categories c ON p.category_id = c.id
                LEFT JOIN product_tags t ON t.product_id = p.id
                LEFT JOIN product_variants pv ON pv.product_id = p.id AND pv.is_active = 1
                WHERE p.status = 'active'
            """
            params = []

            if category_code and category_code != 'all':
                sql += " AND c.code = ?"
                params.append(category_code)

            if only_in_store:
                sql += " AND p.is_available_in_store = 1"

            if featured_only:
                sql += " AND p.is_featured = 1"

            if query:
                sql += " AND (p.title LIKE ? OR p.vendor LIKE ? OR p.description_html LIKE ? OR pv.sku LIKE ?)"
                wildcard = f"%{query}%"
                params.extend([wildcard, wildcard, wildcard, wildcard])

            sql += " GROUP BY p.id ORDER BY p.is_featured DESC, c.sort_order ASC, p.id ASC"

            rows = conn.execute(sql, params).fetchall()
            if not rows:
                return []

            all_vars = conn.execute("""
                SELECT * FROM product_variants WHERE is_active = 1 ORDER BY id ASC
            """).fetchall()
            vars_by_prod = {}
            for v in all_vars:
                vd = dict(v)
                vars_by_prod.setdefault(vd["product_id"], []).append(vd)

            products = []
            for r in rows:
                p_dict = dict(r)
                p_dict["variants"] = vars_by_prod.get(p_dict["id"], [])
                products.append(p_dict)
            return products

    @staticmethod
    def get_product_by_handle(handle):
        with get_connection() as conn:
            row = conn.execute("""
                SELECT p.*, c.name as category_name, c.code as category_code,
                       GROUP_CONCAT(t.tag, ', ') as tags_list
                FROM products p
                JOIN categories c ON p.category_id = c.id
                LEFT JOIN product_tags t ON t.product_id = p.id
                WHERE p.handle = ? AND p.status = 'active'
                GROUP BY p.id
            """, (handle,)).fetchone()
            if not row:
                return None
            p_dict = dict(row)
            vars_rows = conn.execute("""
                SELECT * FROM product_variants WHERE product_id = ? AND is_active = 1
                ORDER BY id ASC
            """, (p_dict["id"],)).fetchall()
            p_dict["variants"] = [dict(v) for v in vars_rows]
            return p_dict

    @staticmethod
    def get_product_by_id(product_id):
        with get_connection() as conn:
            row = conn.execute("""
                SELECT p.*, c.name as category_name, c.code as category_code
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.id = ?
            """, (product_id,)).fetchone()
            if not row:
                return None
            p_dict = dict(row)
            vars_rows = conn.execute("""
                SELECT * FROM product_variants WHERE product_id = ? AND is_active = 1
                ORDER BY id ASC
            """, (p_dict["id"],)).fetchall()
            p_dict["variants"] = [dict(v) for v in vars_rows]
            return p_dict

    # -------------------------------------------------------------
    # GESTIONE CLIENTI
    # -------------------------------------------------------------

    @staticmethod
    def find_or_create_customer(cursor, customer_info):
        email = (customer_info.get("email") or "").strip() or None
        phone = (customer_info.get("phone") or "").strip()
        first_name = (customer_info.get("first_name") or "Cliente").strip()
        last_name = (customer_info.get("last_name") or "Banco").strip()

        # Cerca per email o telefono
        existing = None
        if email and phone:
            existing = cursor.execute("SELECT id FROM customers WHERE email = ? OR phone = ?", (email, phone)).fetchone()
        elif email:
            existing = cursor.execute("SELECT id FROM customers WHERE email = ?", (email,)).fetchone()
        elif phone:
            existing = cursor.execute("SELECT id FROM customers WHERE phone = ?", (phone,)).fetchone()

        if existing:
            customer_id = existing[0]
            # Aggiorna indirizzo o codice fiscale se forniti
            if customer_info.get("address") or customer_info.get("fiscal_code"):
                cursor.execute("""
                    UPDATE customers 
                    SET address = COALESCE(NULLIF(?, ''), address),
                        city = COALESCE(NULLIF(?, ''), city),
                        fiscal_code = COALESCE(NULLIF(?, ''), fiscal_code)
                    WHERE id = ?
                """, (
                    customer_info.get("address", ""),
                    customer_info.get("city", "Muro Leccese"),
                    customer_info.get("fiscal_code", ""),
                    customer_id
                ))
            return customer_id

        cursor.execute("""
            INSERT INTO customers (first_name, last_name, email, phone, address, city, fiscal_code, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            first_name,
            last_name,
            email,
            phone,
            customer_info.get("address", ""),
            customer_info.get("city", "Muro Leccese"),
            customer_info.get("fiscal_code", ""),
            customer_info.get("notes", "")
        ))
        return cursor.lastrowid

    # -------------------------------------------------------------
    # GESTIONE ORDINI & CARRELLO
    # -------------------------------------------------------------

    @staticmethod
    def create_order(customer_info, items, delivery_type="pickup", payment_method="pos_on_pickup", customer_notes="", decrement_stock=True):
        if not items:
            raise ValueError("Il carrello non contiene articoli.")

        with get_connection() as conn:
            cursor = conn.cursor()

            # 1. Recupera o crea cliente
            customer_id = JustInTimeDAL.find_or_create_customer(cursor, customer_info)

            # 2. Calcola righe ordine e convalida giacenze
            subtotal = 0.0
            order_items_to_insert = []
            variants_to_decrement = []

            for it in items:
                sku = it.get("sku")
                if not sku:
                    raise ValueError("Articolo privo di codice SKU.")
                qty = int(it.get("quantity", 1))
                if qty <= 0:
                    raise ValueError(f"Quantità non valida per SKU {sku}: {qty}")

                var_row = cursor.execute("""
                    SELECT pv.*, p.title as prod_title, p.id as prod_id
                    FROM product_variants pv
                    JOIN products p ON pv.product_id = p.id
                    WHERE pv.sku = ?
                """, (sku,)).fetchone()
                if not var_row:
                    raise ValueError(f"SKU non valido: {sku}")

                price = float(var_row["price"])
                row_subtotal = round(price * qty, 2)
                subtotal += row_subtotal

                order_items_to_insert.append((
                    var_row["prod_id"], var_row["id"], var_row["prod_title"],
                    var_row["title"], sku, price, qty, row_subtotal
                ))

                if decrement_stock:
                    variants_to_decrement.append((var_row["id"], var_row["prod_id"], qty, var_row["stock_quantity"]))

            subtotal = round(subtotal, 2)
            # Spedizione: gratuita per pickup o per importi >= 79€
            shipping_fee = 6.90 if (delivery_type == "shipping" and subtotal < 79.0) else 0.00
            total_amount = round(subtotal + shipping_fee, 2)

            # Genera codice ordine
            now = datetime.now()
            count_today = cursor.execute("SELECT COUNT(*) FROM orders WHERE date(created_at) = date('now')").fetchone()[0]
            order_number = f"JIT-{now.strftime('%Y%m%d')}-{(count_today + 1):04d}"

            cursor.execute("""
                INSERT INTO orders (
                    order_number, customer_id, delivery_type, pickup_location,
                    order_status, payment_method, payment_status, subtotal,
                    shipping_fee, total_amount, customer_notes
                ) VALUES (?, ?, ?, 'Via Corsica 151, Muro Leccese', 'pending', ?, 'pending', ?, ?, ?, ?)
            """, (
                order_number, customer_id, delivery_type, payment_method,
                subtotal, shipping_fee, total_amount, customer_notes
            ))
            order_id = cursor.lastrowid

            # Inserimento righe
            for item in order_items_to_insert:
                cursor.execute("""
                    INSERT INTO order_items (
                        order_id, product_id, variant_id, product_title,
                        variant_title, sku, unit_price, quantity, subtotal
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (order_id, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

            # Decremento scorte e aggiornamento stato disponibilità
            if decrement_stock:
                for var_id, prod_id, qty, cur_stock in variants_to_decrement:
                    new_stock = max(0, cur_stock - qty)
                    cursor.execute("UPDATE product_variants SET stock_quantity = ? WHERE id = ?", (new_stock, var_id))
                    # Se la somma delle giacenze del prodotto è 0, segna is_available_in_store = 0
                    sum_stock = cursor.execute("SELECT SUM(stock_quantity) FROM product_variants WHERE product_id = ?", (prod_id,)).fetchone()[0] or 0
                    if sum_stock <= 0:
                        cursor.execute("UPDATE products SET is_available_in_store = 0 WHERE id = ?", (prod_id,))

            conn.commit()

            return {
                "order_id": order_id,
                "order_number": order_number,
                "customer_id": customer_id,
                "subtotal": subtotal,
                "shipping_fee": shipping_fee,
                "total_amount": total_amount,
                "delivery_type": delivery_type,
                "payment_method": payment_method,
                "items_count": len(order_items_to_insert),
                "created_at": now.isoformat()
            }

    @staticmethod
    def get_orders(status=None, limit=50):
        with get_connection() as conn:
            sql = """
                SELECT o.*, c.first_name, c.last_name, c.phone, c.email, c.address, c.city, c.fiscal_code
                FROM orders o
                LEFT JOIN customers c ON o.customer_id = c.id
            """
            params = []
            if status:
                sql += " WHERE o.order_status = ?"
                params.append(status)

            sql += " ORDER BY o.id DESC LIMIT ?"
            params.append(limit)

            orders = conn.execute(sql, params).fetchall()
            result = []
            for ord_row in orders:
                o_dict = dict(ord_row)
                items = conn.execute("""
                    SELECT * FROM order_items WHERE order_id = ? ORDER BY id ASC
                """, (o_dict["id"],)).fetchall()
                o_dict["items"] = [dict(i) for i in items]
                result.append(o_dict)
            return result

    @staticmethod
    def get_order(order_identifier):
        with get_connection() as conn:
            if str(order_identifier).isdigit():
                sql = "SELECT o.*, c.first_name, c.last_name, c.phone, c.email, c.address, c.city, c.fiscal_code FROM orders o LEFT JOIN customers c ON o.customer_id = c.id WHERE o.id = ?"
            else:
                sql = "SELECT o.*, c.first_name, c.last_name, c.phone, c.email, c.address, c.city, c.fiscal_code FROM orders o LEFT JOIN customers c ON o.customer_id = c.id WHERE o.order_number = ?"

            ord_row = conn.execute(sql, (order_identifier,)).fetchone()
            if not ord_row:
                return None
            o_dict = dict(ord_row)
            items = conn.execute("SELECT * FROM order_items WHERE order_id = ? ORDER BY id ASC", (o_dict["id"],)).fetchall()
            o_dict["items"] = [dict(i) for i in items]
            return o_dict

    @staticmethod
    def update_order_status(order_identifier, order_status=None, payment_status=None, internal_notes=None, tracking_code=None):
        valid_order_statuses = ('pending', 'confirmed', 'ready_for_pickup', 'shipped', 'completed', 'cancelled')
        valid_payment_statuses = ('pending', 'paid', 'refunded')

        if order_status and order_status not in valid_order_statuses:
            raise ValueError(f"Stato ordine non valido: {order_status}. Validi: {valid_order_statuses}")
        if payment_status and payment_status not in valid_payment_statuses:
            raise ValueError(f"Stato pagamento non valido: {payment_status}. Validi: {valid_payment_statuses}")

        with get_connection() as conn:
            cursor = conn.cursor()
            order = JustInTimeDAL.get_order(order_identifier)
            if not order:
                raise ValueError(f"Ordine non trovato: {order_identifier}")

            updates = []
            params = []
            if order_status:
                updates.append("order_status = ?")
                params.append(order_status)
            if payment_status:
                updates.append("payment_status = ?")
                params.append(payment_status)
            if internal_notes is not None:
                updates.append("internal_notes = ?")
                params.append(internal_notes)
            if tracking_code is not None:
                updates.append("tracking_code = ?")
                params.append(tracking_code)

            if not updates:
                return order

            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(order["id"])

            sql = f"UPDATE orders SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(sql, params)
            conn.commit()

            return JustInTimeDAL.get_order(order["id"])

    # -------------------------------------------------------------
    # LABORATORIO DI ASSISTENZA & RIPARAZIONI PC
    # -------------------------------------------------------------

    @staticmethod
    def get_repair_tickets(status=None, query=None, limit=50):
        with get_connection() as conn:
            sql = """
                SELECT r.*, c.first_name, c.last_name, c.phone, c.email, c.address, c.city
                FROM repair_tickets r
                JOIN customers c ON r.customer_id = c.id
                WHERE 1=1
            """
            params = []
            if status and status != 'all':
                sql += " AND r.status = ?"
                params.append(status)

            if query:
                sql += " AND (r.ticket_number LIKE ? OR r.brand_model LIKE ? OR r.reported_issue LIKE ? OR c.first_name LIKE ? OR c.last_name LIKE ? OR c.phone LIKE ?)"
                w = f"%{query}%"
                params.extend([w, w, w, w, w, w])

            sql += " ORDER BY r.id DESC LIMIT ?"
            params.append(limit)

            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_repair_ticket(ticket_identifier):
        with get_connection() as conn:
            if str(ticket_identifier).isdigit():
                sql = """
                    SELECT r.*, c.first_name, c.last_name, c.phone, c.email, c.address, c.city, c.fiscal_code
                    FROM repair_tickets r
                    JOIN customers c ON r.customer_id = c.id
                    WHERE r.id = ?
                """
            else:
                sql = """
                    SELECT r.*, c.first_name, c.last_name, c.phone, c.email, c.address, c.city, c.fiscal_code
                    FROM repair_tickets r
                    JOIN customers c ON r.customer_id = c.id
                    WHERE r.ticket_number = ?
                """
            row = conn.execute(sql, (ticket_identifier,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def create_repair_ticket(customer_info, device_type, brand_model, reported_issue, serial_number="", diagnosis_notes="", advance_fee=0.0, estimated_cost=None):
        valid_devices = ('desktop', 'notebook', 'smartphone', 'printer', 'other')
        if device_type not in valid_devices:
            raise ValueError(f"Tipo dispositivo non valido: {device_type}. Validi: {valid_devices}")
        if not brand_model or not reported_issue:
            raise ValueError("Marca/Modello e problema riscontrato sono obbligatori.")

        with get_connection() as conn:
            cursor = conn.cursor()
            customer_id = JustInTimeDAL.find_or_create_customer(cursor, customer_info)

            now = datetime.now()
            count_year = cursor.execute("SELECT COUNT(*) FROM repair_tickets WHERE strftime('%Y', received_at) = strftime('%Y', 'now')").fetchone()[0]
            ticket_number = f"LAB-{now.year}-{(count_year + 1):04d}"

            cursor.execute("""
                INSERT INTO repair_tickets (
                    ticket_number, customer_id, device_type, brand_model, serial_number,
                    reported_issue, diagnosis_notes, advance_fee, estimated_cost, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'received')
            """, (
                ticket_number, customer_id, device_type, brand_model.strip(),
                serial_number.strip() if serial_number else None,
                reported_issue.strip(),
                diagnosis_notes.strip() if diagnosis_notes else None,
                float(advance_fee or 0.0),
                float(estimated_cost) if estimated_cost is not None else None
            ))
            ticket_id = cursor.lastrowid
            conn.commit()

            return JustInTimeDAL.get_repair_ticket(ticket_id)

    @staticmethod
    def update_repair_ticket(ticket_identifier, status=None, diagnosis_notes=None, advance_fee=None, estimated_cost=None, final_cost=None, serial_number=None, reported_issue=None):
        valid_statuses = ('received', 'diagnosing', 'waiting_approval', 'in_repair', 'ready_for_pickup', 'delivered', 'unrepairable')
        if status and status not in valid_statuses:
            raise ValueError(f"Stato riparazione non valido: {status}. Validi: {valid_statuses}")

        with get_connection() as conn:
            cursor = conn.cursor()
            ticket = JustInTimeDAL.get_repair_ticket(ticket_identifier)
            if not ticket:
                raise ValueError(f"Scheda riparazione non trovata: {ticket_identifier}")

            updates = []
            params = []
            if status:
                updates.append("status = ?")
                params.append(status)
                if status in ('delivered', 'unrepairable') and not ticket.get("closed_at"):
                    updates.append("closed_at = CURRENT_TIMESTAMP")
            if diagnosis_notes is not None:
                updates.append("diagnosis_notes = ?")
                params.append(diagnosis_notes)
            if advance_fee is not None:
                updates.append("advance_fee = ?")
                params.append(float(advance_fee))
            if estimated_cost is not None:
                updates.append("estimated_cost = ?")
                params.append(float(estimated_cost))
            if final_cost is not None:
                updates.append("final_cost = ?")
                params.append(float(final_cost))
            if serial_number is not None:
                updates.append("serial_number = ?")
                params.append(serial_number.strip())
            if reported_issue is not None:
                updates.append("reported_issue = ?")
                params.append(reported_issue.strip())

            if not updates:
                return ticket

            params.append(ticket["id"])
            sql = f"UPDATE repair_tickets SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(sql, params)
            conn.commit()

            return JustInTimeDAL.get_repair_ticket(ticket["id"])

    # -------------------------------------------------------------
    # PRENOTAZIONE TESTI SCOLASTICI
    # -------------------------------------------------------------

    @staticmethod
    def get_book_reservations(status=None, limit=50):
        with get_connection() as conn:
            sql = """
                SELECT b.*, c.first_name, c.last_name, c.phone, c.email
                FROM book_reservations b
                JOIN customers c ON b.customer_id = c.id
                WHERE 1=1
            """
            params = []
            if status and status != 'all':
                sql += " AND b.status = ?"
                params.append(status)
            sql += " ORDER BY b.id DESC LIMIT ?"
            params.append(limit)
            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def create_book_reservation(customer_info, student_name, school_name, class_grade, book_list_text, colibri_covers=False, deposit=0.0):
        with get_connection() as conn:
            cursor = conn.cursor()
            customer_id = JustInTimeDAL.find_or_create_customer(cursor, customer_info)

            now = datetime.now()
            count_year = cursor.execute("SELECT COUNT(*) FROM book_reservations WHERE strftime('%Y', created_at) = strftime('%Y', 'now')").fetchone()[0]
            code = f"LIB-{now.year}-{(count_year + 1):04d}"

            cursor.execute("""
                INSERT INTO book_reservations (
                    reservation_code, customer_id, student_name, school_name,
                    class_grade, book_list_text, colibri_covers_required, deposit_amount, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'submitted')
            """, (
                code, customer_id, student_name.strip(), school_name.strip(),
                class_grade.strip(), book_list_text.strip(),
                1 if colibri_covers else 0, float(deposit or 0.0)
            ))
            res_id = cursor.lastrowid
            conn.commit()

            row = cursor.execute("""
                SELECT b.*, c.first_name, c.last_name, c.phone, c.email
                FROM book_reservations b
                JOIN customers c ON b.customer_id = c.id
                WHERE b.id = ?
            """, (res_id,)).fetchone()
            return dict(row)

    # -------------------------------------------------------------
    # RICEVUTE & MODULI STAMPABILI AL BANCO (HTML PRONTO PER STAMPA)
    # -------------------------------------------------------------

    @staticmethod
    def generate_repair_receipt_html(ticket_identifier):
        ticket = JustInTimeDAL.get_repair_ticket(ticket_identifier)
        if not ticket:
            return None

        status_labels = {
            'received': 'Dispositivo Ricevuto al Banco',
            'diagnosing': 'Diagnosi Tecnica in Corso',
            'waiting_approval': 'In Attesa Approvazione Preventivo',
            'in_repair': 'In Riparazione / Sostituzione Componenti',
            'ready_for_pickup': '✅ PRONTO PER IL RITIRO AL BANCO',
            'delivered': 'Consegnato al Cliente',
            'unrepairable': 'Non Riparabile'
        }
        status_label = status_labels.get(ticket['status'], ticket['status'])

        html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>Scheda Laboratorio #{ticket['ticket_number']} - {COMPANY_INFO['name']}</title>
  <style>
    @page {{ size: A4; margin: 15mm; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #1e293b;
      margin: 0;
      padding: 20px;
      line-height: 1.4;
      background: #f8fafc;
    }}
    .sheet {{
      max-width: 800px;
      margin: 0 auto;
      background: #fff;
      padding: 30px;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      border-bottom: 2px solid #0F4C81;
      padding-bottom: 15px;
      margin-bottom: 20px;
    }}
    .company-title {{
      font-size: 20px;
      font-weight: 800;
      color: #0F4C81;
      margin: 0;
    }}
    .company-sub {{
      font-size: 12px;
      color: #64748b;
      margin-top: 4px;
    }}
    .ticket-badge {{
      text-align: right;
    }}
    .ticket-num {{
      font-size: 24px;
      font-weight: 900;
      color: #0F4C81;
      letter-spacing: 1px;
    }}
    .ticket-status {{
      display: inline-block;
      padding: 4px 10px;
      background: #e0f2fe;
      color: #0369a1;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      margin-top: 4px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 15px;
      margin-bottom: 20px;
    }}
    .box {{
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 12px;
      background: #fdfdfd;
    }}
    .box-title {{
      font-size: 11px;
      text-transform: uppercase;
      font-weight: 800;
      color: #64748b;
      margin-bottom: 6px;
      letter-spacing: 0.5px;
    }}
    .box-content {{
      font-size: 14px;
      color: #0f172a;
    }}
    .table-details {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 20px;
      font-size: 13px;
    }}
    .table-details th, .table-details td {{
      padding: 8px 12px;
      border: 1px solid #e2e8f0;
      text-align: left;
    }}
    .table-details th {{
      background: #f1f5f9;
      font-weight: 700;
      color: #334155;
    }}
    .terms {{
      font-size: 10px;
      color: #64748b;
      border-top: 1px solid #e2e8f0;
      padding-top: 10px;
      margin-top: 20px;
      line-height: 1.3;
    }}
    .cut-line {{
      border-top: 2px dashed #94a3b8;
      margin: 30px 0 25px;
      position: relative;
      text-align: center;
    }}
    .cut-line span {{
      position: absolute;
      top: -10px;
      background: #fff;
      padding: 0 10px;
      font-size: 11px;
      color: #64748b;
      left: 50%;
      transform: translateX(-50%);
    }}
    .bench-tag {{
      border: 2px solid #0F4C81;
      padding: 15px;
      border-radius: 8px;
      background: #fafafa;
    }}
    .btn-print {{
      display: block;
      width: 100%;
      background: #0F4C81;
      color: #fff;
      padding: 12px;
      text-align: center;
      border-radius: 6px;
      text-decoration: none;
      font-weight: bold;
      margin-bottom: 20px;
      cursor: pointer;
      border: none;
    }}
    @media print {{
      body {{ background: #fff; padding: 0; }}
      .sheet {{ border: none; box-shadow: none; padding: 0; }}
      .btn-print {{ display: none; }}
    }}
  </style>
</head>
<body>
  <div class="sheet">
    <button class="btn-print" onclick="window.print()">🖨️ Stampa Ricevuta Cliente & Talloncino Laboratorio</button>

    <!-- SEZIONE 1: RICEVUTA CLIENTE -->
    <div class="header">
      <div>
        <h1 class="company-title">{COMPANY_INFO['name']}</h1>
        <div class="company-sub">{COMPANY_INFO['address']} • {COMPANY_INFO['city']}<br>Tel: {COMPANY_INFO['phone']} • P.IVA: {COMPANY_INFO['vat']}</div>
      </div>
      <div class="ticket-badge">
        <div class="ticket-num">{ticket['ticket_number']}</div>
        <div class="ticket-status">{status_label}</div>
        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Data: {ticket['received_at'][:16]}</div>
      </div>
    </div>

    <div style="font-weight: 800; font-size: 14px; margin-bottom: 12px; color: #0F4C81;">RICEVUTA DI PRESA IN CARICO RIPARAZIONE (Copia per il Cliente)</div>

    <div class="grid">
      <div class="box">
        <div class="box-title">Dati Cliente</div>
        <div class="box-content">
          <strong>{ticket['first_name']} {ticket['last_name']}</strong><br>
          Recapito WhatsApp/Tel: <strong>{ticket['phone']}</strong><br>
          {f"Email: {ticket['email']}<br>" if ticket['email'] else ""}
          {f"Indirizzo: {ticket['address']}, {ticket['city']}" if ticket['address'] else ""}
        </div>
      </div>
      <div class="box">
        <div class="box-title">Dispositivo in Assistenza</div>
        <div class="box-content">
          Tipologia: <strong>{ticket['device_type'].upper()}</strong><br>
          Marca e Modello: <strong>{ticket['brand_model']}</strong><br>
          {f"Matricola / Serial: <code>{ticket['serial_number']}</code>" if ticket['serial_number'] else "Matricola: Non indicata"}
        </div>
      </div>
    </div>

    <table class="table-details">
      <tr>
        <th style="width: 30%;">Problema Riscontrato</th>
        <td>{ticket['reported_issue']}</td>
      </tr>
      <tr>
        <th>Diagnosi / Intervento Tecnico</th>
        <td>{ticket['diagnosis_notes'] or "In fase di analisi presso il nostro banco tecnico."}</td>
      </tr>
      <tr>
        <th>Condizioni Economiche</th>
        <td>
          Acconto versato all'accettazione: <strong>€{ticket['advance_fee']:.2f}</strong><br>
          {f"Preventivo stimato: <strong>€{ticket['estimated_cost']:.2f}</strong> (inclusa IVA)<br>" if ticket['estimated_cost'] else "Preventivo: da concordare previa diagnosi approfondita.<br>"}
          {f"Costo finale a saldo: <strong>€{ticket['final_cost']:.2f}</strong><br>" if ticket['final_cost'] else ""}
        </td>
      </tr>
    </table>

    <div class="terms">
      <strong>Condizioni di Servizio:</strong><br>
      1. Il cliente dichiara che i dati presenti nel supporto sono stati preventivamente salvati; Just in Time declina ogni responsabilità per perdite accidentali di dati dovute a guasti fisici dei supporti magnetici o SSD.<br>
      2. Le riparazioni hardware godono di garanzia legale di 90 giorni sui componenti sostituiti a far data dalla consegna.<br>
      3. I dispositivi pronti per il ritiro devono essere ritirati entro 60 giorni dalla notifica WhatsApp/telefonica, trascorsi i quali verranno applicate le spese di custodia previste per legge.<br>
      4. Verifica stato online: collegati al nostro sito e inserisci il codice <strong>{ticket['ticket_number']}</strong> per seguire lo stato di avanzamento in tempo reale.
    </div>

    <!-- SEZIONE 2: TALLONCINO LABORATORIO APPLICABILE SULLO CHASSIS -->
    <div class="cut-line">
      <span>✂️ RITAGLIARE QUI — TALLONCINO PER BANCO LABORATORIO JUST IN TIME ✂️</span>
    </div>

    <div class="bench-tag">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div>
          <span style="font-size: 18px; font-weight: 900; color: #0F4C81;">SCHEDA BANCO: {ticket['ticket_number']}</span>
          <span style="margin-left: 10px; font-size: 12px; background: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 4px; font-weight: bold;">{ticket['device_type'].upper()}</span>
        </div>
        <div style="font-size: 13px; font-weight: bold;">Ingresso: {ticket['received_at'][:10]}</div>
      </div>
      <div style="font-size: 14px; margin-bottom: 6px;">
        <strong>Dispositivo:</strong> {ticket['brand_model']} {f"(S/N: {ticket['serial_number']})" if ticket['serial_number'] else ""}
      </div>
      <div style="font-size: 14px; margin-bottom: 6px;">
        <strong>Cliente:</strong> {ticket['first_name']} {ticket['last_name']} — 📞 <strong>{ticket['phone']}</strong>
      </div>
      <div style="font-size: 13px; background: #fff; border: 1px dashed #cbd5e1; padding: 8px; border-radius: 4px;">
        <strong>Difetto segnalato:</strong> {ticket['reported_issue']}<br>
        <strong>Acconto cassa:</strong> €{ticket['advance_fee']:.2f} | <strong>Stato:</strong> {ticket['status']}
      </div>
    </div>

  </div>
</body>
</html>"""
        return html

    @staticmethod
    def generate_order_receipt_html(order_identifier):
        order = JustInTimeDAL.get_order(order_identifier)
        if not order:
            return None

        status_labels = {
            'pending': 'In Elaborazione',
            'confirmed': 'Confermato',
            'ready_for_pickup': 'Pronto per il Ritiro al Banco',
            'shipped': 'Spedito con Corriere',
            'completed': 'Completato ed Evaso',
            'cancelled': 'Annullato'
        }
        pay_labels = {
            'pos_on_pickup': 'Pagamento al Ritiro (Contanti / POS)',
            'cash_on_pickup': 'Contanti al Ritiro',
            'stripe': 'Carta di Credito / PayByLink Online',
            'bank_transfer': 'Bonifico Bancario Anticipato',
            'paypal': 'PayPal'
        }

        items_rows = ""
        for it in order.get("items", []):
            items_rows += f"""
            <tr>
              <td><code>{it['sku']}</code></td>
              <td><strong>{it['product_title']}</strong><br><span style="font-size: 11px; color: #64748b;">{it['variant_title'] or ''}</span></td>
              <td style="text-align: center;">{it['quantity']}</td>
              <td style="text-align: right;">€{it['unit_price']:.2f}</td>
              <td style="text-align: right; font-weight: bold;">€{it['subtotal']:.2f}</td>
            </tr>
            """

        html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>Riepilogo Ordine #{order['order_number']} - {COMPANY_INFO['name']}</title>
  <style>
    @page {{ size: A4; margin: 15mm; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #1e293b;
      margin: 0;
      padding: 20px;
      background: #f8fafc;
    }}
    .sheet {{
      max-width: 800px;
      margin: 0 auto;
      background: #fff;
      padding: 30px;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      border-bottom: 2px solid #0F4C81;
      padding-bottom: 15px;
      margin-bottom: 20px;
    }}
    .btn-print {{
      display: block;
      width: 100%;
      background: #0F4C81;
      color: #fff;
      padding: 12px;
      text-align: center;
      border-radius: 6px;
      text-decoration: none;
      font-weight: bold;
      margin-bottom: 20px;
      cursor: pointer;
      border: none;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }}
    th, td {{
      padding: 10px;
      border-bottom: 1px solid #e2e8f0;
      text-align: left;
    }}
    th {{ background: #f1f5f9; font-size: 12px; text-transform: uppercase; }}
    .totals {{
      margin-top: 20px;
      float: right;
      width: 300px;
    }}
    .total-row {{
      display: flex;
      justify-content: space-between;
      padding: 6px 0;
    }}
    .total-final {{
      border-top: 2px solid #0F4C81;
      padding-top: 8px;
      font-size: 18px;
      font-weight: 800;
      color: #0F4C81;
    }}
    @media print {{
      body {{ background: #fff; padding: 0; }}
      .sheet {{ border: none; padding: 0; }}
      .btn-print {{ display: none; }}
    }}
  </style>
</head>
<body>
  <div class="sheet">
    <button class="btn-print" onclick="window.print()">🖨️ Stampa Documento di Spedizione / Ricevuta Ordine</button>
    <div class="header">
      <div>
        <h1 style="font-size: 20px; color: #0F4C81; margin: 0;">{COMPANY_INFO['name']}</h1>
        <div style="font-size: 12px; color: #64748b; margin-top: 4px;">{COMPANY_INFO['address']} • {COMPANY_INFO['city']}<br>Tel/WhatsApp: {COMPANY_INFO['phone']} • P.IVA: {COMPANY_INFO['vat']}</div>
      </div>
      <div style="text-align: right;">
        <div style="font-size: 22px; font-weight: 900; color: #0F4C81;">{order['order_number']}</div>
        <div style="font-size: 12px; font-weight: bold; color: #059669;">Stato: {status_labels.get(order['order_status'], order['order_status'])}</div>
        <div style="font-size: 11px; color: #64748b;">Data: {order['created_at'][:16]}</div>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
      <div style="border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px;">
        <div style="font-size: 11px; font-weight: bold; color: #64748b; text-transform: uppercase;">Destinatario / Cliente</div>
        <div style="font-size: 14px; margin-top: 4px;">
          <strong>{order.get('first_name', '')} {order.get('last_name', '')}</strong><br>
          Recapito: <strong>{order.get('phone', '')}</strong><br>
          {f"Email: {order.get('email')}<br>" if order.get('email') else ""}
          {f"C.F. / P.IVA: {order.get('fiscal_code')}<br>" if order.get('fiscal_code') else ""}
        </div>
      </div>
      <div style="border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px;">
        <div style="font-size: 11px; font-weight: bold; color: #64748b; text-transform: uppercase;">Modalità e Pagamento</div>
        <div style="font-size: 14px; margin-top: 4px;">
          Spedizione: <strong>{'Ritiro in sede (Via Corsica 151)' if order['delivery_type'] == 'pickup' else 'Consegna a domicilio con corriere'}</strong><br>
          {f"Indirizzo: {order.get('address', '')}, {order.get('city', '')}<br>" if order['delivery_type'] == 'shipping' else ""}
          Metodo Pagamento: <strong>{pay_labels.get(order['payment_method'], order['payment_method'])}</strong><br>
          Stato Pagamento: <strong>{order['payment_status'].upper()}</strong>
        </div>
      </div>
    </div>

    {f"<div style='background: #f8fafc; border: 1px dashed #cbd5e1; padding: 10px; border-radius: 6px; font-size: 13px; margin-bottom: 20px;'><strong>Note Cliente:</strong> {order['customer_notes']}</div>" if order.get('customer_notes') else ""}

    <table>
      <thead>
        <tr>
          <th>Codice SKU</th>
          <th>Descrizione Articolo</th>
          <th style="text-align: center;">Q.tà</th>
          <th style="text-align: right;">Prezzo Unit.</th>
          <th style="text-align: right;">Totale Riga</th>
        </tr>
      </thead>
      <tbody>
        {items_rows}
      </tbody>
    </table>

    <div class="totals">
      <div class="total-row">
        <span>Subtotale Merci:</span>
        <span>€{order['subtotal']:.2f}</span>
      </div>
      <div class="total-row">
        <span>Spese di Spedizione:</span>
        <span>{f"€{order['shipping_fee']:.2f}" if order['shipping_fee'] > 0 else "Gratis (€0,00)"}</span>
      </div>
      <div class="total-row total-final">
        <span>TOTALE ORDINE:</span>
        <span>€{order['total_amount']:.2f}</span>
      </div>
    </div>
    <div style="clear: both;"></div>

    <div style="margin-top: 40px; border-top: 1px solid #e2e8f0; padding-top: 15px; font-size: 11px; color: #94a3b8; text-align: center;">
      Grazie per aver acquistato da Just in Time di Benegiamo Andrea • Assistenza WhatsApp: {COMPANY_INFO['phone']}
    </div>
  </div>
</body>
</html>"""
        return html

    # -------------------------------------------------------------
    # CRUSCOTTO STATISTICHE
    # -------------------------------------------------------------

    @staticmethod
    def get_stats():
        with get_connection() as conn:
            total_products = conn.execute("SELECT COUNT(*) FROM products WHERE status = 'active'").fetchone()[0]
            total_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
            pending_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE order_status IN ('pending', 'confirmed')").fetchone()[0]
            total_revenue = conn.execute("SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE payment_status = 'paid' OR order_status = 'ready_for_pickup' OR order_status = 'completed'").fetchone()[0]
            open_repairs = conn.execute("SELECT COUNT(*) FROM repair_tickets WHERE status NOT IN ('delivered', 'unrepairable')").fetchone()[0]
            ready_repairs = conn.execute("SELECT COUNT(*) FROM repair_tickets WHERE status = 'ready_for_pickup'").fetchone()[0]
            open_books = conn.execute("SELECT COUNT(*) FROM book_reservations WHERE status != 'completed'").fetchone()[0]
            low_stock = conn.execute("SELECT COUNT(*) FROM product_variants WHERE stock_quantity <= 2 AND is_active = 1").fetchone()[0]

            return {
                "active_products": total_products,
                "total_orders": total_orders,
                "pending_orders": pending_orders,
                "total_revenue_eur": float(total_revenue),
                "open_repairs_count": open_repairs,
                "ready_repairs_count": ready_repairs,
                "open_book_reservations_count": open_books,
                "low_stock_items_count": low_stock
            }


if __name__ == "__main__":
    dal = JustInTimeDAL()
    stats = dal.get_stats()
    print("Test DAL Just in Time Stats:", stats)
    categories = dal.get_categories()
    print(f"Categorie caricate: {len(categories)}")
    prods = dal.get_products()
    print(f"Prodotti caricati: {len(prods)}")
    repairs = dal.get_repair_tickets()
    print(f"Schede laboratorio caricate: {len(repairs)}")
