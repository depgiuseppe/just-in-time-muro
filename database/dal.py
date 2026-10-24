#!/usr/bin/env python3
"""
Data Access Layer (DAL) per Just in Time di Benegiamo Andrea
Interfaccia di accesso e manipolazione dati su database SQLite locale.
"""

import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "just_in_time.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

class JustInTimeDAL:
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
    def get_products(category_code=None, query=None, only_in_store=False):
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

            if query:
                sql += " AND (p.title LIKE ? OR p.vendor LIKE ? OR p.description_html LIKE ? OR pv.sku LIKE ?)"
                wildcard = f"%{query}%"
                params.extend([wildcard, wildcard, wildcard, wildcard])

            sql += " GROUP BY p.id ORDER BY p.id ASC"

            rows = conn.execute(sql, params).fetchall()
            products = []
            for r in rows:
                p_dict = dict(r)
                # Recupera varianti
                vars_rows = conn.execute("""
                    SELECT * FROM product_variants WHERE product_id = ? AND is_active = 1
                """, (p_dict["id"],)).fetchall()
                p_dict["variants"] = [dict(v) for v in vars_rows]
                products.append(p_dict)
            return products

    @staticmethod
    def get_product_by_handle(handle):
        with get_connection() as conn:
            row = conn.execute("""
                SELECT p.*, c.name as category_name, c.code as category_code
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.handle = ? AND p.status = 'active'
            """, (handle,)).fetchone()
            if not row:
                return None
            p_dict = dict(row)
            vars_rows = conn.execute("""
                SELECT * FROM product_variants WHERE product_id = ? AND is_active = 1
            """, (p_dict["id"],)).fetchall()
            p_dict["variants"] = [dict(v) for v in vars_rows]
            return p_dict

    @staticmethod
    def create_order(customer_info, items, delivery_type="pickup", payment_method="pos_on_pickup", customer_notes=""):
        with get_connection() as conn:
            cursor = conn.cursor()
            # 1. Recupera o crea cliente
            cursor.execute("SELECT id FROM customers WHERE email = ? OR phone = ?", 
                           (customer_info.get("email"), customer_info.get("phone")))
            existing = cursor.fetchone()
            if existing:
                customer_id = existing[0]
            else:
                cursor.execute("""
                    INSERT INTO customers (first_name, last_name, email, phone, address, city, fiscal_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    customer_info.get("first_name", "Cliente"),
                    customer_info.get("last_name", "Banco"),
                    customer_info.get("email"),
                    customer_info.get("phone", ""),
                    customer_info.get("address", ""),
                    customer_info.get("city", "Muro Leccese"),
                    customer_info.get("fiscal_code", "")
                ))
                customer_id = cursor.lastrowid

            # 2. Calcola totale righe
            subtotal = 0.0
            order_items_to_insert = []
            for it in items:
                sku = it["sku"]
                qty = it.get("quantity", 1)
                var_row = cursor.execute("""
                    SELECT pv.*, p.title as prod_title 
                    FROM product_variants pv
                    JOIN products p ON pv.product_id = p.id
                    WHERE pv.sku = ?
                """, (sku,)).fetchone()
                if not var_row:
                    raise ValueError(f"SKU non valido: {sku}")

                price = float(var_row["price"])
                row_subtotal = price * qty
                subtotal += row_subtotal
                order_items_to_insert.append((
                    var_row["product_id"], var_row["id"], var_row["prod_title"],
                    var_row["title"], sku, price, qty, row_subtotal
                ))

            # Spedizione
            shipping_fee = 6.90 if (delivery_type == "shipping" and subtotal < 79.0) else 0.00
            total_amount = subtotal + shipping_fee

            # Genera numero ordine univoco
            now_str = datetime.now().strftime("%Y%m%d%H%M%S")
            order_number = f"JIT-{now_str}"

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

            # Inserisci righe
            for item in order_items_to_insert:
                cursor.execute("""
                    INSERT INTO order_items (
                        order_id, product_id, variant_id, product_title,
                        variant_title, sku, unit_price, quantity, subtotal
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (order_id, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

            conn.commit()
            return {
                "order_id": order_id,
                "order_number": order_number,
                "subtotal": subtotal,
                "shipping_fee": shipping_fee,
                "total_amount": total_amount,
                "delivery_type": delivery_type,
                "items_count": len(order_items_to_insert)
            }

    @staticmethod
    def get_orders():
        with get_connection() as conn:
            orders = conn.execute("""
                SELECT o.*, c.first_name, c.last_name, c.phone, c.email
                FROM orders o
                LEFT JOIN customers c ON o.customer_id = c.id
                ORDER BY o.id DESC
            """).fetchall()
            result = []
            for ord_row in orders:
                o_dict = dict(ord_row)
                items = conn.execute("""
                    SELECT * FROM order_items WHERE order_id = ?
                """, (o_dict["id"],)).fetchall()
                o_dict["items"] = [dict(i) for i in items]
                result.append(o_dict)
            return result

    @staticmethod
    def get_repair_tickets():
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT r.*, c.first_name, c.last_name, c.phone
                FROM repair_tickets r
                JOIN customers c ON r.customer_id = c.id
                ORDER BY r.id DESC
            """).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_stats():
        with get_connection() as conn:
            total_products = conn.execute("SELECT COUNT(*) FROM products WHERE status = 'active'").fetchone()[0]
            total_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
            total_revenue = conn.execute("SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE payment_status = 'paid' OR order_status = 'ready_for_pickup'").fetchone()[0]
            open_repairs = conn.execute("SELECT COUNT(*) FROM repair_tickets WHERE status NOT IN ('delivered', 'unrepairable')").fetchone()[0]
            open_books = conn.execute("SELECT COUNT(*) FROM book_reservations WHERE status != 'completed'").fetchone()[0]
            return {
                "active_products": total_products,
                "total_orders": total_orders,
                "total_revenue_eur": float(total_revenue),
                "open_repairs_count": open_repairs,
                "open_book_reservations_count": open_books
            }

if __name__ == "__main__":
    dal = JustInTimeDAL()
    stats = dal.get_stats()
    print("Test DAL Just in Time Stats:", stats)
    categories = dal.get_categories()
    print(f"Categorie caricate: {len(categories)}")
    prods = dal.get_products()
    print(f"Prodotti caricati: {len(prods)}")
