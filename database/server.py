#!/usr/bin/env python3
"""
Server Web e API REST Locale per Just in Time di Benegiamo Andrea (Muro Leccese)
Fornisce endpoint REST completi per:
- Catalogo prodotti e categorie
- Creazione e avanzamento ordini (Click & Collect / Spedizioni)
- Gestione schede laboratorio riparazioni con generazione ricevute e talloncini banco
- Prenotazioni testi scolastici
- Cruscotto statistiche e pannello gestionale locale per Andrea (/admin)

Nessuna dipendenza esterna: solo Python Standard Library (http.server, json, urllib).
"""

import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Assicura import locale di dal.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dal import JustInTimeDAL

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8080

class JustInTimeAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def _send_json(self, status=200, data=None):
        payload = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(payload)

    def _send_html(self, status=200, html_content=""):
        payload = html_content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        # ---------------------------------------------------------
        # ROUTE GESTIONALE / ADMIN
        # ---------------------------------------------------------
        if path in ("/admin", "/gestionale", "/admin/"):
            admin_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "admin.html")
            if os.path.exists(admin_file):
                with open(admin_file, "r", encoding="utf-8") as f:
                    self._send_html(200, f.read())
                return

        # ---------------------------------------------------------
        # ENDPOINT API REST
        # ---------------------------------------------------------
        if path == "/api/stats":
            stats = JustInTimeDAL.get_stats()
            self._send_json(200, stats)
            return

        elif path == "/api/categories":
            categories = JustInTimeDAL.get_categories()
            self._send_json(200, categories)
            return

        elif path == "/api/products":
            category = qs.get("category", [None])[0]
            query = qs.get("q", [None])[0]
            only_store = qs.get("in_store", ["0"])[0] in ("1", "true")
            featured = qs.get("featured", ["0"])[0] in ("1", "true")
            products = JustInTimeDAL.get_products(category_code=category, query=query, only_in_store=only_store, featured_only=featured)
            self._send_json(200, products)
            return

        elif path.startswith("/api/products/"):
            handle_or_id = path.replace("/api/products/", "").strip("/")
            prod = None
            if handle_or_id.isdigit():
                prod = JustInTimeDAL.get_product_by_id(int(handle_or_id))
            if not prod:
                prod = JustInTimeDAL.get_product_by_handle(handle_or_id)

            if prod:
                self._send_json(200, prod)
            else:
                self._send_json(404, {"error": "Prodotto non trovato", "key": handle_or_id})
            return

        elif path == "/api/orders":
            status = qs.get("status", [None])[0]
            limit = int(qs.get("limit", [50])[0])
            orders = JustInTimeDAL.get_orders(status=status, limit=limit)
            self._send_json(200, orders)
            return

        elif path.startswith("/api/orders/"):
            subpath = path.replace("/api/orders/", "").strip("/")
            if subpath.endswith("/receipt"):
                order_key = subpath.replace("/receipt", "")
                receipt_html = JustInTimeDAL.generate_order_receipt_html(order_key)
                if receipt_html:
                    self._send_html(200, receipt_html)
                else:
                    self._send_json(404, {"error": "Ordine non trovato per ricevuta"})
                return
            else:
                order = JustInTimeDAL.get_order(subpath)
                if order:
                    self._send_json(200, order)
                else:
                    self._send_json(404, {"error": "Ordine non trovato", "key": subpath})
                return

        elif path == "/api/repairs":
            status = qs.get("status", [None])[0]
            query = qs.get("q", [None])[0]
            limit = int(qs.get("limit", [50])[0])
            repairs = JustInTimeDAL.get_repair_tickets(status=status, query=query, limit=limit)
            self._send_json(200, repairs)
            return

        elif path.startswith("/api/repairs/"):
            subpath = path.replace("/api/repairs/", "").strip("/")
            if subpath.endswith("/receipt"):
                ticket_key = subpath.replace("/receipt", "")
                receipt_html = JustInTimeDAL.generate_repair_receipt_html(ticket_key)
                if receipt_html:
                    self._send_html(200, receipt_html)
                else:
                    self._send_json(404, {"error": "Scheda riparazione non trovata per ricevuta"})
                return
            else:
                ticket = JustInTimeDAL.get_repair_ticket(subpath)
                if ticket:
                    self._send_json(200, ticket)
                else:
                    self._send_json(404, {"error": "Scheda riparazione non trovata", "key": subpath})
                return

        elif path == "/api/books":
            status = qs.get("status", [None])[0]
            limit = int(qs.get("limit", [50])[0])
            books = JustInTimeDAL.get_book_reservations(status=status, limit=limit)
            self._send_json(200, books)
            return

        # ---------------------------------------------------------
        # DEFAULT: SERVI FILE STATICI (STOREFRONT INDEX.HTML)
        # ---------------------------------------------------------
        if path == "/":
            # Se esiste preview/index.html o index.html
            if os.path.exists(os.path.join(BASE_DIR, "preview", "index.html")):
                self.path = "/preview/index.html"
            elif os.path.exists(os.path.join(BASE_DIR, "index.html")):
                self.path = "/index.html"

        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Payload JSON non valido"})
            return

        # 1. Creazione Ordine dal carrello
        if path == "/api/orders":
            try:
                customer = data.get("customer", {})
                items = data.get("items", [])
                delivery = data.get("delivery_type", "pickup")
                payment = data.get("payment_method", "pos_on_pickup")
                notes = data.get("notes", "")
                decrement = data.get("decrement_stock", True)

                result = JustInTimeDAL.create_order(
                    customer_info=customer,
                    items=items,
                    delivery_type=delivery,
                    payment_method=payment,
                    customer_notes=notes,
                    decrement_stock=decrement
                )
                self._send_json(201, result)
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        # 2. Aggiornamento stato ordine via POST
        elif path.startswith("/api/orders/") and path.endswith("/status"):
            order_key = path.replace("/api/orders/", "").replace("/status", "").strip("/")
            try:
                updated = JustInTimeDAL.update_order_status(
                    order_identifier=order_key,
                    order_status=data.get("order_status"),
                    payment_status=data.get("payment_status"),
                    internal_notes=data.get("internal_notes"),
                    tracking_code=data.get("tracking_code")
                )
                self._send_json(200, updated)
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        # 3. Creazione Nuova Scheda Riparazione Laboratorio
        elif path == "/api/repairs":
            try:
                customer = data.get("customer", {})
                device_type = data.get("device_type")
                brand_model = data.get("brand_model")
                reported_issue = data.get("reported_issue")
                serial_number = data.get("serial_number", "")
                diagnosis = data.get("diagnosis_notes", "")
                advance_fee = float(data.get("advance_fee", 0.0) or 0.0)
                est_cost = float(data.get("estimated_cost")) if data.get("estimated_cost") is not None else None

                ticket = JustInTimeDAL.create_repair_ticket(
                    customer_info=customer,
                    device_type=device_type,
                    brand_model=brand_model,
                    reported_issue=reported_issue,
                    serial_number=serial_number,
                    diagnosis_notes=diagnosis,
                    advance_fee=advance_fee,
                    estimated_cost=est_cost
                )
                self._send_json(201, ticket)
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        # 4. Aggiornamento scheda riparazione via POST
        elif path.startswith("/api/repairs/") and path.endswith("/status"):
            ticket_key = path.replace("/api/repairs/", "").replace("/status", "").strip("/")
            try:
                updated = JustInTimeDAL.update_repair_ticket(
                    ticket_identifier=ticket_key,
                    status=data.get("status"),
                    diagnosis_notes=data.get("diagnosis_notes"),
                    advance_fee=data.get("advance_fee"),
                    estimated_cost=data.get("estimated_cost"),
                    final_cost=data.get("final_cost"),
                    serial_number=data.get("serial_number"),
                    reported_issue=data.get("reported_issue")
                )
                self._send_json(200, updated)
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        # 5. Creazione Prenotazione Libri Scolastici
        elif path == "/api/books":
            try:
                customer = data.get("customer", {})
                student = data.get("student_name", "")
                school = data.get("school_name", "")
                grade = data.get("class_grade", "")
                books_text = data.get("book_list_text", "")
                colibri = bool(data.get("colibri_covers", False))
                deposit = float(data.get("deposit_amount", 0.0) or 0.0)

                res = JustInTimeDAL.create_book_reservation(
                    customer_info=customer,
                    student_name=student,
                    school_name=school,
                    class_grade=grade,
                    book_list_text=books_text,
                    colibri_covers=colibri,
                    deposit=deposit
                )
                self._send_json(201, res)
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        self._send_json(404, {"error": "Endpoint POST non trovato", "path": path})

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Payload JSON non valido"})
            return

        if path.startswith("/api/orders/"):
            order_key = path.replace("/api/orders/", "").strip("/")
            try:
                updated = JustInTimeDAL.update_order_status(
                    order_identifier=order_key,
                    order_status=data.get("order_status"),
                    payment_status=data.get("payment_status"),
                    internal_notes=data.get("internal_notes"),
                    tracking_code=data.get("tracking_code")
                )
                self._send_json(200, updated)
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        elif path.startswith("/api/repairs/"):
            ticket_key = path.replace("/api/repairs/", "").strip("/")
            try:
                updated = JustInTimeDAL.update_repair_ticket(
                    ticket_identifier=ticket_key,
                    status=data.get("status"),
                    diagnosis_notes=data.get("diagnosis_notes"),
                    advance_fee=data.get("advance_fee"),
                    estimated_cost=data.get("estimated_cost"),
                    final_cost=data.get("final_cost"),
                    serial_number=data.get("serial_number"),
                    reported_issue=data.get("reported_issue")
                )
                self._send_json(200, updated)
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        self._send_json(404, {"error": "Endpoint PUT non trovato", "path": path})


def run_server(port=PORT):
    server = HTTPServer(("127.0.0.1", port), JustInTimeAPIHandler)
    print("=" * 80)
    print("🚀 JUST IN TIME — SERVER LOCALE SELF-HOSTED (OPZIONE B A CANONE ZERO)")
    print("=" * 80)
    print(f"📍 Storefront E-Commerce:    http://127.0.0.1:{port}/")
    print(f"🛠️ Pannello Gestionale Banco: http://127.0.0.1:{port}/admin")
    print(f"📊 Cruscotto Statistiche:    http://127.0.0.1:{port}/api/stats")
    print(f"📦 API Catalogo Prodotti:    http://127.0.0.1:{port}/api/products")
    print(f"🧾 API Ordini & Carrello:    http://127.0.0.1:{port}/api/orders")
    print(f"🔬 API Laboratorio Assist.:  http://127.0.0.1:{port}/api/repairs")
    print("=" * 80)
    print("Premi Ctrl+C per arrestare il server in sicurezza.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Arresto server locale Just in Time completato.")
        server.server_close()


if __name__ == "__main__":
    p = PORT
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        p = int(sys.argv[1])
    run_server(p)
