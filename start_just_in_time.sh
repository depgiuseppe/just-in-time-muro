#!/usr/bin/env bash
# ==============================================================================
# Script di Avvio Locale — Just in Time di Benegiamo Andrea (Muro Leccese)
# Piattaforma: macOS / Linux / Bash
# Canone Zero • Database Relazionale SQLite • Server API REST & Gestionale Banco
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "========================================================================"
echo "🏪 AVVIO AMBIENTE LOCALE JUST IN TIME (BENEGIAMO ANDREA - MURO LECCESE)"
echo "========================================================================"

# 1. Verifica presenza di Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Errore: Python 3 non risulta installato nel sistema."
    echo "   Scarica Python da https://www.python.org/downloads/ ed eseguilo di nuovo."
    exit 1
fi

PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✔ Python rilevato: versione $PY_VER (Libreria standard sufficiente, zero dipendenze)"

# 2. Controllo esistenza database SQLite
DB_FILE="$DIR/database/just_in_time.db"
if [ ! -f "$DB_FILE" ]; then
    echo "⚙️ Database non presente. Inizializzazione automatica e caricamento catalogo..."
    python3 "$DIR/database/init_and_seed.py"
else
    echo "✔ Database locale pronto: $DB_FILE"
fi

# 3. Apertura automatica del browser dopo 1 secondo di avvio
(
  sleep 1.2
  echo "🌐 Apertura automatica del browser..."
  if command -v open &> /dev/null; then
    open "http://127.0.0.1:8080/admin"
    open "http://127.0.0.1:8080/"
  elif command -v xdg-open &> /dev/null; then
    xdg-open "http://127.0.0.1:8080/admin"
    xdg-open "http://127.0.0.1:8080/"
  fi
) &

# 4. Avvio del Server API REST e Web Storefront
echo "🚀 Avvio server su http://127.0.0.1:8080 ..."
exec python3 "$DIR/database/server.py"
