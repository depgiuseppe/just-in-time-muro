#!/usr/bin/env python3
"""
Server Web e API REST Locale per Just in Time di Benegiamo Andrea
Fornisce endpoint JSON completi per il catalogo, ordini, carrello e riparazioni
senza richiedere alcuna dipendenza esterna (usa solo la libreria standard di Python).
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

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        # Router API
        if path == "/api/stats":
            stats = JustInTimeDAL.get_stats()
            self._set_headers(200)
            self.wfile.write(json.dumps(stats, indent=2).encode("utf-8"))
            return

        elif path == "/api/categories":
            categories = JustInTimeDAL.get_categories()
            self._set_headers(200)
            self.wfile.write(json.dumps(categories, indent=2).encode("utf-8"))
            return

        elif path == "/api/products":
            category = qs.get("category", [None])[0]
            query = qs.get("q", [None])[0]
            only_store = qs.get("in_store", ["0"])[0] == "1"
            products = JustInTimeDAL.get_products(category_code=category, query=query, only_in_store=only_store)
            self._set_headers(200)
            self.wfile.write(json.dumps(products, indent=2).encode("utf-8"))
            return

        elif path.startswith("/api/products/"):
            handle = path.replace("/api/products/", "")
            prod = JustInTimeDAL.get_product_by_handle(handle)
            if prod:
                self._set_headers(200)
                self.wfile.write(json.dumps(prod, indent=2).encode("utf-8"))
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Prodotto non trovato"}).encode("utf-8"))
            return

        elif path == "/api/orders":
            orders = JustInTimeDAL.get_orders()
            self._set_headers(200)
            self.wfile.write(json.dumps(orders, indent=2).encode("utf-8"))
            return

        elif path == "/api/repairs":
            repairs = JustInTimeDAL.get_repair_tickets()
            self._set_headers(200)
            self.wfile.write(json.dumps(repairs, indent=2).encode("utf-8"))
            return

        # Default: servi file statici (es. preview/index.html)
        if path == "/":
            self.path = "/preview/index.html"
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/orders":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            try:
                data = json.loads(body)
                customer = data.get("customer", {})
                items = data.get("items", [])
                delivery = data.get("delivery_type", "pickup")
                payment = data.get("payment_method", "pos_on_pickup")
                notes = data.get("notes", "")

                result = JustInTimeDAL.create_order(customer, items, delivery, payment, notes)
                self._set_headers(201)
                self.wfile.write(json.dumps(result, indent=2).encode("utf-8"))
            except Exception as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Endpoint non trovato"}).encode("utf-8"))

def run_server():
    server = HTTPServer(("127.0.0.1", PORT), JustInTimeAPIHandler)
    print(f"🚀 Server API e Storefront Locale attivo su http://127.0.0.1:{PORT}")
    print(f"📖 Dashboard API: http://127.0.0.1:{PORT}/api/stats")
    print(f"🛍️ Catalogo API: http://127.0.0.1:{PORT}/api/products")
    print(f"🖥️ Storefront Web: http://127.0.0.1:{PORT}/preview/index.html")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Arresto server.")
        server.server_close()

if __name__ == "__main__":
    run_server()
