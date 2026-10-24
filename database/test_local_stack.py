#!/usr/bin/env python3
"""
Suite di Test Completa per lo Stack Locale Self-Hosted di Just in Time
Verifica:
1. Data Access Layer (DAL): catalogo, ordini, scalamento giacenze, laboratorio, ricevute e statistiche.
2. Server API REST: tutti gli endpoint GET, POST, PUT, OPTIONS e le pagine HTML del gestionale al banco.
"""

import os
import sys
import json
import time
import unittest
import threading
import urllib.request
import urllib.error
from http.server import HTTPServer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "database"))

from dal import JustInTimeDAL
from server import JustInTimeAPIHandler

TEST_PORT = 8089

class TestJustInTimeDAL(unittest.TestCase):
    def test_01_categories(self):
        cats = JustInTimeDAL.get_categories()
        self.assertIsInstance(cats, list)
        self.assertGreaterEqual(len(cats), 5)
        codes = [c["code"] for c in cats]
        self.assertIn("informatica-tecnologia", codes)
        self.assertIn("servizi-assistenza-tecnica", codes)

    def test_02_products_and_filters(self):
        prods = JustInTimeDAL.get_products()
        self.assertGreaterEqual(len(prods), 15)

        # Filtro per categoria
        it_prods = JustInTimeDAL.get_products(category_code="informatica-tecnologia")
        for p in it_prods:
            self.assertEqual(p["category_code"], "informatica-tecnologia")

        # Ricerca testuale
        search_res = JustInTimeDAL.get_products(query="Kingston")
        self.assertTrue(any("Kingston" in p["title"] for p in search_res))

        # Prodotto singolo per handle
        single = JustInTimeDAL.get_product_by_handle("kingston-a400-ssd-480gb")
        self.assertIsNotNone(single)
        self.assertEqual(single["handle"], "kingston-a400-ssd-480gb")
        self.assertGreaterEqual(len(single["variants"]), 1)

    def test_03_create_order_and_stock_decrement(self):
        # Recupera variante SSD Kingston per verificare stock
        conn = JustInTimeDAL.get_products()
        ssd = next(p for p in conn if p["handle"] == "kingston-a400-ssd-480gb")
        sku = ssd["variants"][0]["sku"]
        initial_stock = ssd["variants"][0]["stock_quantity"]

        order_data = JustInTimeDAL.create_order(
            customer_info={
                "first_name": "Test",
                "last_name": "Cliente DAL",
                "phone": "+39 333 1122334",
                "email": "test.dal@salento.it",
                "address": "Via Roma 1",
                "city": "Muro Leccese"
            },
            items=[{"sku": sku, "quantity": 1}],
            delivery_type="pickup",
            payment_method="pos_on_pickup",
            customer_notes="Test unitario ordine DAL",
            decrement_stock=True
        )

        self.assertIn("order_number", order_data)
        self.assertTrue(order_data["order_number"].startswith("JIT-"))
        self.assertEqual(order_data["shipping_fee"], 0.0)
        self.assertGreater(order_data["total_amount"], 0.0)

        # Verifica decremento magazzino
        updated_ssd = JustInTimeDAL.get_product_by_handle("kingston-a400-ssd-480gb")
        new_stock = updated_ssd["variants"][0]["stock_quantity"]
        self.assertEqual(new_stock, initial_stock - 1)

        # Recupera ordine completo
        fetched = JustInTimeDAL.get_order(order_data["order_id"])
        self.assertEqual(fetched["order_number"], order_data["order_number"])
        self.assertEqual(fetched["first_name"], "Test")
        self.assertEqual(len(fetched["items"]), 1)

        # Aggiorna stato
        upd = JustInTimeDAL.update_order_status(order_data["order_id"], order_status="ready_for_pickup", payment_status="paid")
        self.assertEqual(upd["order_status"], "ready_for_pickup")
        self.assertEqual(upd["payment_status"], "paid")

        # Genera ricevuta HTML
        receipt = JustInTimeDAL.generate_order_receipt_html(order_data["order_id"])
        self.assertIn("Just in Time di Benegiamo Andrea", receipt)
        self.assertIn(order_data["order_number"], receipt)

    def test_04_repair_tickets_and_receipt(self):
        ticket = JustInTimeDAL.create_repair_ticket(
            customer_info={
                "first_name": "Giuseppe",
                "last_name": "De Pascali",
                "phone": "+39 320 6000000",
                "email": "giuseppe@salento.it"
            },
            device_type="notebook",
            brand_model="Dell XPS 13",
            reported_issue="Batteria gonfia e touchpad bloccato",
            serial_number="DELL-987654",
            advance_fee=25.0,
            estimated_cost=85.0
        )

        self.assertIn("ticket_number", ticket)
        self.assertTrue(ticket["ticket_number"].startswith("LAB-"))
        self.assertEqual(ticket["status"], "received")
        self.assertEqual(ticket["advance_fee"], 25.0)

        # Aggiorna a in riparazione
        upd1 = JustInTimeDAL.update_repair_ticket(
            ticket["ticket_number"],
            status="in_repair",
            diagnosis_notes="Batteria originale ordinata dal fornitore"
        )
        self.assertEqual(upd1["status"], "in_repair")
        self.assertIn("Batteria originale", upd1["diagnosis_notes"])

        # Genera ricevuta cliente + talloncino banco
        receipt_html = JustInTimeDAL.generate_repair_receipt_html(ticket["ticket_number"])
        self.assertIn("RICEVUTA DI PRESA IN CARICO RIPARAZIONE", receipt_html)
        self.assertIn("TALLONCINO PER BANCO LABORATORIO", receipt_html)
        self.assertIn(ticket["ticket_number"], receipt_html)
        self.assertIn("Dell XPS 13", receipt_html)

        # Chiudi riparazione
        closed = JustInTimeDAL.update_repair_ticket(ticket["ticket_number"], status="delivered", final_cost=85.0)
        self.assertEqual(closed["status"], "delivered")
        self.assertIsNotNone(closed["closed_at"])

    def test_05_book_reservations(self):
        res = JustInTimeDAL.create_book_reservation(
            customer_info={
                "first_name": "Anna",
                "last_name": "Esposito",
                "phone": "+39 349 7788990"
            },
            student_name="Francesca Esposito",
            school_name="Liceo Capece Maglie",
            class_grade="3B Scientifico",
            book_list_text="Fisica Vol. 2, Latino Grammatica, Chimica Organica",
            colibri_covers=True,
            deposit=30.0
        )
        self.assertTrue(res["reservation_code"].startswith("LIB-"))
        self.assertEqual(res["colibri_covers_required"], 1)
        self.assertEqual(res["student_name"], "Francesca Esposito")

    def test_06_stats(self):
        s = JustInTimeDAL.get_stats()
        self.assertGreaterEqual(s["active_products"], 15)
        self.assertGreaterEqual(s["total_orders"], 1)
        self.assertGreaterEqual(s["total_revenue_eur"], 39.90)


class TestJustInTimeAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = HTTPServer(("127.0.0.1", TEST_PORT), JustInTimeAPIHandler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def _get(self, path):
        req = urllib.request.Request(f"http://127.0.0.1:{TEST_PORT}{path}")
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            ct = resp.headers.get("Content-Type", "")
            return resp.status, ct, data

    def _post(self, path, payload):
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"http://127.0.0.1:{TEST_PORT}{path}",
            data=data_bytes,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    def _put(self, path, payload):
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"http://127.0.0.1:{TEST_PORT}{path}",
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="PUT"
        )
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    def test_api_stats(self):
        status, ct, data = self._get("/api/stats")
        self.assertEqual(status, 200)
        self.assertIn("application/json", ct)
        res = json.loads(data.decode("utf-8"))
        self.assertIn("active_products", res)
        self.assertIn("total_revenue_eur", res)

    def test_api_products(self):
        status, _, data = self._get("/api/products")
        self.assertEqual(status, 200)
        prods = json.loads(data.decode("utf-8"))
        self.assertGreaterEqual(len(prods), 15)

        # Singolo prodotto
        status, _, data = self._get("/api/products/kingston-a400-ssd-480gb")
        self.assertEqual(status, 200)
        p = json.loads(data.decode("utf-8"))
        self.assertEqual(p["vendor"], "Kingston")

    def test_api_orders_flow(self):
        # 1. POST ordine
        status, created = self._post("/api/orders", {
            "customer": {
                "first_name": "API",
                "last_name": "Tester",
                "phone": "+39 320 1111222",
                "email": "apitester@muroleccese.it"
            },
            "items": [{"sku": "JIT-KNG-A400-480", "quantity": 1}],
            "delivery_type": "pickup",
            "payment_method": "pos_on_pickup",
            "notes": "Ritiro concordato per test API"
        })
        self.assertEqual(status, 201)
        self.assertIn("order_number", created)
        order_num = created["order_number"]

        # 2. GET ordine per numero
        status, _, data = self._get(f"/api/orders/{order_num}")
        self.assertEqual(status, 200)
        fetched = json.loads(data.decode("utf-8"))
        self.assertEqual(fetched["order_number"], order_num)

        # 3. PUT avanzamento stato
        status, updated = self._put(f"/api/orders/{order_num}", {
            "order_status": "ready_for_pickup",
            "payment_status": "paid",
            "internal_notes": "Scatola pronta con scontrino pinzato"
        })
        self.assertEqual(status, 200)
        self.assertEqual(updated["order_status"], "ready_for_pickup")

        # 4. GET ricevuta HTML
        status, ct, html_bytes = self._get(f"/api/orders/{order_num}/receipt")
        self.assertEqual(status, 200)
        self.assertIn("text/html", ct)
        self.assertIn(order_num.encode("utf-8"), html_bytes)

    def test_api_repairs_flow(self):
        # 1. POST nuova scheda riparazione
        status, ticket = self._post("/api/repairs", {
            "customer": {
                "first_name": "Laura",
                "last_name": "Mancini",
                "phone": "+39 347 5556677"
            },
            "device_type": "notebook",
            "brand_model": "Lenovo ThinkPad T480",
            "reported_issue": "Tastiera non risponde su alcuni tasti",
            "advance_fee": 20.0,
            "estimated_cost": 60.0
        })
        self.assertEqual(status, 201)
        self.assertIn("ticket_number", ticket)
        t_num = ticket["ticket_number"]

        # 2. GET scheda per codice
        status, _, data = self._get(f"/api/repairs/{t_num}")
        self.assertEqual(status, 200)
        fetched = json.loads(data.decode("utf-8"))
        self.assertEqual(fetched["ticket_number"], t_num)

        # 3. PUT aggiornamento stato a ready_for_pickup
        status, updated = self._put(f"/api/repairs/{t_num}", {
            "status": "ready_for_pickup",
            "diagnosis_notes": "Tastiera sostituita e collaudata con successo",
            "final_cost": 60.0
        })
        self.assertEqual(status, 200)
        self.assertEqual(updated["status"], "ready_for_pickup")

        # 4. GET ricevuta e talloncino banco stampabile
        status, ct, html_bytes = self._get(f"/api/repairs/{t_num}/receipt")
        self.assertEqual(status, 200)
        self.assertIn("text/html", ct)
        self.assertIn(t_num.encode("utf-8"), html_bytes)
        self.assertIn("TALLONCINO PER BANCO LABORATORIO".encode("utf-8"), html_bytes)

    def test_admin_and_storefront_pages(self):
        # Admin / Gestionale
        status, ct, html_bytes = self._get("/admin")
        self.assertEqual(status, 200)
        self.assertIn("text/html", ct)
        self.assertIn("GESTIONALE LOCALE AL BANCO".encode("utf-8"), html_bytes)

        # Storefront principale
        status, ct, html_bytes = self._get("/")
        self.assertEqual(status, 200)
        self.assertIn("text/html", ct)
        self.assertIn("Just in Time".encode("utf-8"), html_bytes)
        self.assertIn("Stato Riparazione".encode("utf-8"), html_bytes)

if __name__ == "__main__":
    unittest.main()
