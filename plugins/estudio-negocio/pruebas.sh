#!/usr/bin/env bash
# Ejecuta todas las autopruebas del plugin (sin red).
set -e
cd "$(dirname "$0")/skills"
python3 validar-negocio/scripts/pruebas/prueba_integracion.py
for s in prospeccion-clientes/scripts/buscar_locales_osm.py prospeccion-clientes/scripts/extraer_contactos.py \
         prospeccion-clientes/scripts/crm.py campanas-marketing/scripts/utm.py; do
  python3 "$s" --selftest >/dev/null && echo "✓ $s --selftest"
done
echo "TODO OK"
