-- =====================================================================
-- SCHEMA DATABASE LOCALE: Just in Time di Benegiamo Andrea
-- Piattaforma: SQLite 3 (Compatibile con PostgreSQL / MySQL con minimi adattamenti)
-- Data: 2026-10-24
-- =====================================================================

PRAGMA foreign_keys = ON;

-- 1. CATEGORIE / COLLEZIONI
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,                 -- es. 'informatica-tecnologia'
    name TEXT NOT NULL,                        -- es. 'Informatica & Tecnologia'
    description TEXT,
    sort_order INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. PRODOTTI & SCHEDE SERVIZIO
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    handle TEXT UNIQUE NOT NULL,               -- slug url univoco
    title TEXT NOT NULL,
    description_html TEXT,
    vendor TEXT NOT NULL,                      -- es. 'HP', 'Lenovo', 'Just in Time Lab'
    product_type TEXT NOT NULL,                -- es. 'Notebook', 'Toner', 'Servizio'
    base_price DECIMAL(10, 2) NOT NULL,
    compare_at_price DECIMAL(10, 2),
    is_available_in_store INTEGER DEFAULT 1,  -- 1 = disponibile subito a Muro Leccese
    is_featured INTEGER DEFAULT 0,            -- 1 = articolo in vetrina / evidenza in home
    lead_time_hours INTEGER DEFAULT 2,         -- ore per ritiro (2h, 24h, 48h)
    requires_shipping INTEGER DEFAULT 1,       -- 0 per servizi digitali e riparazioni
    condition TEXT DEFAULT 'Nuovo',            -- 'Nuovo', 'Ricondizionato Grado A+'
    warranty_months INTEGER DEFAULT 24,
    image_url TEXT,
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'draft', 'archived')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. VARIANTI PRODOTTO (Configurazioni, formati, tagli memoria)
CREATE TABLE IF NOT EXISTS product_variants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    sku TEXT UNIQUE NOT NULL,                  -- es. 'JIT-HP250-BASE'
    title TEXT NOT NULL DEFAULT 'Default Title',
    option1_name TEXT,
    option1_value TEXT,
    price DECIMAL(10, 2) NOT NULL,
    compare_at_price DECIMAL(10, 2),
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    barcode TEXT,                              -- EAN-13 o UPC
    weight_grams INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. TAG PRODOTTO (per ricerca e indicizzazione)
CREATE TABLE IF NOT EXISTS product_tags (
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    tag TEXT NOT NULL,
    PRIMARY KEY (product_id, tag)
);

-- 5. CLIENTI & CONTATTI
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT NOT NULL,                       -- fondamentale per comunicazioni WhatsApp
    address TEXT,
    city TEXT DEFAULT 'Muro Leccese',
    province TEXT DEFAULT 'LE',
    postal_code TEXT DEFAULT '73036',
    fiscal_code TEXT,                          -- per fatturazione e scontrino telematico
    vat_number TEXT,                           -- opzionale per clienti B2B
    privacy_consent INTEGER DEFAULT 1,         -- consenso GDPR art. 6
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 6. ORDINI (Click & Collect e Spedizioni)
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,         -- es. 'JIT-2026-0001'
    customer_id INTEGER REFERENCES customers(id) ON DELETE SET NULL,
    delivery_type TEXT NOT NULL CHECK(delivery_type IN ('pickup', 'shipping')),
    pickup_location TEXT DEFAULT 'Via Corsica 151, Muro Leccese',
    order_status TEXT NOT NULL DEFAULT 'pending' 
        CHECK(order_status IN ('pending', 'confirmed', 'ready_for_pickup', 'shipped', 'completed', 'cancelled')),
    payment_method TEXT NOT NULL 
        CHECK(payment_method IN ('cash_on_pickup', 'pos_on_pickup', 'bank_transfer', 'stripe', 'paypal')),
    payment_status TEXT NOT NULL DEFAULT 'pending' 
        CHECK(payment_status IN ('pending', 'paid', 'refunded')),
    subtotal DECIMAL(10, 2) NOT NULL,
    shipping_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    total_amount DECIMAL(10, 2) NOT NULL,
    tracking_code TEXT,                        -- lettera di vettura corriere
    customer_notes TEXT,
    internal_notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 7. DETTAGLIO RIGHE ORDINE
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
    variant_id INTEGER REFERENCES product_variants(id) ON DELETE SET NULL,
    product_title TEXT NOT NULL,
    variant_title TEXT,
    sku TEXT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    subtotal DECIMAL(10, 2) NOT NULL
);

-- 8. LABORATORIO DI ASSISTENZA & RIPARAZIONI PC
CREATE TABLE IF NOT EXISTS repair_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_number TEXT UNIQUE NOT NULL,        -- es. 'LAB-2026-0042'
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    device_type TEXT NOT NULL CHECK(device_type IN ('desktop', 'notebook', 'smartphone', 'printer', 'other')),
    brand_model TEXT NOT NULL,                 -- es. 'ASUS VivoBook 15'
    serial_number TEXT,
    reported_issue TEXT NOT NULL,              -- es. 'Schermo nero all avvio'
    diagnosis_notes TEXT,
    advance_fee DECIMAL(10, 2) DEFAULT 0.00,   -- acconto diagnosi (es. 20€ / 25€)
    estimated_cost DECIMAL(10, 2),
    final_cost DECIMAL(10, 2),
    status TEXT NOT NULL DEFAULT 'received' 
        CHECK(status IN ('received', 'diagnosing', 'waiting_approval', 'in_repair', 'ready_for_pickup', 'delivered', 'unrepairable')),
    received_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    closed_at DATETIME
);

-- 9. PRENOTAZIONI TESTI SCOLASTICI (Campagna Scuola Salento)
CREATE TABLE IF NOT EXISTS book_reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_code TEXT UNIQUE NOT NULL,     -- es. 'LIB-2026-0105'
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    student_name TEXT NOT NULL,
    school_name TEXT NOT NULL,                 -- es. 'Istituto Comprensivo Muro Leccese'
    class_grade TEXT NOT NULL,                 -- es. 'Classe 2B Medie'
    book_list_text TEXT NOT NULL,
    colibri_covers_required INTEGER DEFAULT 0, -- 1 = richiede copertine Colibri
    deposit_amount DECIMAL(10, 2) DEFAULT 0.00,
    status TEXT NOT NULL DEFAULT 'submitted' 
        CHECK(status IN ('submitted', 'ordered_supplier', 'partially_arrived', 'ready_for_pickup', 'completed', 'cancelled')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- INDICI DI PERFORMANCE
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_handle ON products(handle);
CREATE INDEX IF NOT EXISTS idx_variants_sku ON product_variants(sku);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(order_status);
CREATE INDEX IF NOT EXISTS idx_repair_tickets_status ON repair_tickets(status);
