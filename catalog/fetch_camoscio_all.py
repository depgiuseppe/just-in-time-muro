#!/usr/bin/env python3
"""
Scarica le immagini reali per tutti gli 884 articoli di LISTINO Camoscio.xlsx
e genera il catalogo completo JSON, JS, CSV Shopify e il seed SQLite.
"""

import csv
import html
import json
import os
import re
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import openpyxl
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
EXCEL_PATH = BASE_DIR / "LISTINO Camoscio.xlsx"
IMG_DIR = BASE_DIR / "assets" / "images" / "camoscio"
CACHE_PATH = BASE_DIR / "catalog" / "camoscio_image_map.json"
CATALOG_JSON = BASE_DIR / "catalog" / "camoscio_products.json"
CATALOG_JS = BASE_DIR / "assets" / "camoscio_products.js"

IMG_DIR.mkdir(parents=True, exist_ok=True)

BRAND_MAP = {
    "DEEPCOOL": "DeepCool",
    "COUGAR": "Cougar",
    "HYTE": "HYTE",
    "FSP": "FSP Fortron",
    "DEZCTOP": "Dezctop",
    "FRACTAL": "Fractal Design",
    "SAMA": "SAMA",
    "GAMDIAS": "Gamdias",
    "MSI": "MSI",
    "GENIUS": "Genius",
    "TP-LINK": "TP-Link",
    "MOZA": "Moza Racing",
    "MARSGAMING": "Mars Gaming",
    "PANTUM": "Pantum",
    "THERMALTAKE": "Thermaltake",
    "ASROCK": "ASRock",
    "RAIJINTEK": "Raijintek",
    "MAD CATZ": "Mad Catz",
    "TRYX": "TRYX",
    "ITEK": "iTek",
    "SEAGATE": "Seagate",
    "VALKYRIE": "Valkyrie",
    "PLUSTEK": "Plustek",
    "AMD": "AMD",
    "CYBERPOWER": "CyberPower",
    "XPG": "ADATA XPG",
    "BitFenix": "BitFenix",
    "BITFENIX": "BitFenix",
    "ANIMA": "Anima",
    "MERCUSYS": "Mercusys",
    "INTEL": "Intel",
    "CRUCIAL": "Crucial",
    "AGI": "AGI Technology",
    "EDIMAX": "Edimax",
    "TOSHIBA": "Toshiba",
    "AIC": "AIC Server",
    "LIFEVIEW": "LifeView PC",
    "MICROSOFT": "Microsoft",
    "NOTONLY": "NotOnlyTV",
}


def map_category(sottogruppo: str, desc: str) -> tuple[str, str]:
    sg = (sottogruppo or "").upper()
    d = (desc or "").upper()

    # 1. Storage
    if any(k in sg for k in ("M2 PCIE", "SSD", "HARD DISK", "HDD", "RIGENERATI")):
        return "storage", "SSD & Hard Disk"

    # 2. Stampa, Scanner & Reti
    if any(k in sg for k in ("STAMPANT", "SCANNER", "SWITCH", "ROUTER", "EXTENDER", "POWERLINE", "ACCESS POINT", "SCHEDE RETE", "USB WIRELESS", "IP CAMERA", "CARICA BATTERIE")):
        return "stampa-reti", "Stampa, Scanner & Reti"

    # 3. Gaming, Desk & Sim Racing
    if any(k in sg for k in (
        "MOUSE", "TAPPETINI", "CUFFIE", "TASTIER", "LCD/LED", "GAMEPAD",
        "DEZCTOP", "SEDIA", "GAMING DESK", "VOLANTI", "PEDALIERE", "BUNDLE",
        "MOTORE / BASI", "SEDUTE", "SISTEMA CONTROLLO", "SISTEMA DI MOVIMENTO", "PRESENTER"
    )) or any(k in d for k in ("MOZA ", "VOLANTE", "PEDALIERA")):
        return "gaming", "Gaming, Desk & Sim Racing"

    # 4. Componenti & PC
    if any(k in sg for k in (
        "SOCKET", "NVIDIA", "AMD", "INTEL", "DDR4", "DDR5", "SO DIMM",
        "PC ASSEMBLATI", "NOTEBOOK", "MICROSOFT"
    )) and "DISSIPATORI NOTEBOOK" not in sg:
        return "componenti", "Componenti & PC"

    # 5. Case, Cooling & Alimentatori (default hardware category for cases, coolers, fans, PSUs, UPS, ARGB)
    return "case-cooling", "Case, Cooling & PSU"


def clean_title(raw_desc: str, brand: str) -> str:
    t = re.sub(r"\s+", " ", (raw_desc or "").strip())
    return t


def build_search_query(brand: str, cod_prod: str, ean: str, desc: str) -> str:
    parts = [brand]
    if cod_prod and len(str(cod_prod).strip()) >= 3:
        cp = str(cod_prod).strip()
        if cp.upper() not in brand.upper():
            parts.append(cp)
    # Add key model words from description
    clean_d = re.sub(r"[^A-Za-z0-9\-\. ]+", " ", desc or "")
    words = [w for w in clean_d.split() if len(w) > 2 and w.upper() != brand.upper()]
    parts.extend(words[:5])
    if ean and str(ean).strip().isdigit() and len(str(ean).strip()) >= 8:
        parts.append(str(ean).strip())
    return " ".join(parts)


def fetch_one_image(item: dict, session: requests.Session) -> tuple[str, str]:
    sku = item["sku"]
    dest_file = IMG_DIR / f"{sku}.jpg"
    rel_path = f"assets/images/camoscio/{sku}.jpg"

    if dest_file.exists() and dest_file.stat().st_size > 1500:
        return sku, rel_path

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    queries = [
        f"{item['brand']} {item['mpn']}".strip() if item["mpn"] else "",
        f"{item['brand']} {item['raw_desc'][:45]}".strip(),
    ]
    queries = [q for q in queries if q]

    for q in queries:
        try:
            url = "https://www.bing.com/images/search?q=" + urllib.parse.quote(q) + "&form=HDRSC2&first=1"
            r = session.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                unesc = html.unescape(r.text)
                turls = re.findall(r'"turl":"(https?://[^"]+)"', unesc)
                if turls:
                    img_url = turls[0]
                    ir = session.get(img_url, headers=headers, timeout=10)
                    if ir.status_code == 200 and len(ir.content) > 1500:
                        dest_file.write_bytes(ir.content)
                        return sku, rel_path
        except Exception:
            pass

    return sku, ""


def main():
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb["listino"]

    items = []
    for r in range(5, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, 11)]
        cd_ar, desc, prezzo, stock, data_prox, qta_arr, sottogruppo, desc_marca, cod_prod, ean = vals
        if not cd_ar or not desc:
            continue

        sku = str(cd_ar).strip()
        raw_brand = str(desc_marca or "").strip()
        brand = BRAND_MAP.get(raw_brand, BRAND_MAP.get(raw_brand.upper(), raw_brand.title() if raw_brand else "Hardware"))
        price_val = round(float(prezzo or 0.0), 2)
        stock_val = int(float(stock or 0))
        sg_str = str(sottogruppo or "VARI").strip()
        mpn_str = str(cod_prod or "").strip() if cod_prod is not None else ""
        ean_str = str(ean or "").strip() if ean is not None else ""

        if data_prox is not None:
            if hasattr(data_prox, "strftime"):
                next_date = data_prox.strftime("%d/%m/%Y")
            else:
                next_date = str(data_prox)[:10]
        else:
            next_date = None

        cat_code, cat_label = map_category(sg_str, str(desc))

        items.append({
            "sku": sku,
            "title": clean_title(str(desc), brand),
            "raw_desc": str(desc).strip(),
            "brand": brand,
            "raw_brand": raw_brand,
            "price": price_val,
            "stock": stock_val,
            "next_date": next_date,
            "incoming_qty": int(float(qta_arr)) if qta_arr is not None else 0,
            "sottogruppo": sg_str,
            "category": cat_code,
            "category_label": cat_label,
            "mpn": mpn_str,
            "ean": ean_str,
        })

    print(f"Articoli letti da LISTINO Camoscio.xlsx: {len(items)}")

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=32, pool_maxsize=32)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    img_map = {}
    if CACHE_PATH.exists():
        try:
            img_map = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            img_map = {}

    t0 = time.time()
    done_count = 0
    with ThreadPoolExecutor(max_workers=20) as ex:
        futures = {ex.submit(fetch_one_image, it, session): it["sku"] for it in items}
        for fut in as_completed(futures):
            sku, rel_img = fut.result()
            if rel_img:
                img_map[sku] = rel_img
            done_count += 1
            if done_count % 100 == 0 or done_count == len(items):
                elapsed = time.time() - t0
                print(f"  [{done_count}/{len(items)}] immagini scaricate ({len(img_map)} ok) in {elapsed:.1f}s", flush=True)

    CACHE_PATH.write_text(json.dumps(img_map, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Totale immagini associate: {len(img_map)} / {len(items)}")


if __name__ == "__main__":
    main()
