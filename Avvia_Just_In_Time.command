#!/usr/bin/env bash
# ==============================================================================
# File di Avvio Diretto con Doppio Click per Mac (Finder)
# Just in Time di Benegiamo Andrea (Muro Leccese)
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

chmod +x "$DIR/start_just_in_time.sh"
"$DIR/start_just_in_time.sh"
