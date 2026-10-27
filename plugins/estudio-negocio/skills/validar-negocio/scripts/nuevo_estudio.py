#!/usr/bin/env python3
"""Crea la estructura de carpetas y plantillas de un estudio de negocio.

Ejemplo:
  python3 nuevo_estudio.py "Cafetería de especialidad en Ruzafa" --dir estudios --modo estandar

No sobrescribe archivos existentes (salvo con --forzar), así que es seguro relanzarlo.
"""

import argparse
import datetime as dt
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import slug  # noqa: E402

PLANTILLAS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plantillas")

MODULOS = [  # carpeta, clave de módulo, título
    ("00-brief", "brief", "Brief"),
    ("01-mercado", "mercado", "Mercado"),
    ("02-cliente", "cliente", "Cliente y público objetivo"),
    ("03-palabras-clave", "palabras_clave", "Palabras clave y demanda"),
    ("04-competencia", "competencia", "Competencia"),
    ("05-estrategia", "estrategia", "Estrategia: DAFO, CAME y modelo de negocio"),
    ("06-viabilidad", "viabilidad", "Viabilidad económica"),
    ("07-marketing-ventas", "marketing_ventas", "Marketing y ventas"),
    ("08-producto-distribucion", "producto_distribucion", "Producto y distribución"),
    ("09-legal", "legal", "Legal y trámites"),
    ("10-veredicto", "veredicto", "Riesgos y veredicto"),
]

# (plantilla, destino relativo)
COPIAS = [
    ("brief.md", "00-brief/brief.md"),
    ("PROGRESO.md", "PROGRESO.md"),
    ("README-estudio.md", "README.md"),
    ("contexto-ia.md", "ia/contexto-ia.md"),
    ("persona.md", "02-cliente/personas.md"),
    ("guion-entrevista.md", "02-cliente/guion-entrevistas.md"),
    ("encuesta.md", "02-cliente/encuesta.md"),
    ("ficha-competidor.md", "04-competencia/fichas/_plantilla.md"),
    ("dafo.md", "05-estrategia/dafo.md"),
    ("lean-canvas.md", "05-estrategia/lean-canvas.md"),
    ("modelo-financiero.json", "06-viabilidad/supuestos.json"),
    ("puntuacion.json", "10-veredicto/puntuacion.json"),
    ("experimento.md", "10-veredicto/experimentos.md"),
]


def rellenar(texto, valores):
    for k, v in valores.items():
        texto = texto.replace("{{" + k + "}}", v)
    return texto


def escribir(ruta, contenido, forzar, creados):
    if os.path.exists(ruta) and not forzar:
        return
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    creados.append(ruta)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("idea", help="Nombre corto de la idea")
    ap.add_argument("--dir", default="estudios", help="Carpeta donde crear el estudio (por defecto: estudios)")
    ap.add_argument("--slug", help="Nombre de carpeta (por defecto se deriva de la idea)")
    ap.add_argument("--modo", default="estandar", choices=["express", "estandar", "profundo"])
    ap.add_argument("--forzar", action="store_true", help="Sobrescribir archivos existentes")
    a = ap.parse_args()

    nombre = a.slug or slug(a.idea)
    raiz = os.path.join(a.dir, nombre)
    hoy = dt.date.today().isoformat()
    valores = {"IDEA": a.idea, "FECHA": hoy, "MODO": a.modo, "SLUG": nombre}
    creados = []

    for plantilla, destino in COPIAS:
        origen = os.path.join(PLANTILLAS, plantilla)
        if not os.path.exists(origen):
            print(f"[aviso] falta la plantilla {plantilla}", file=sys.stderr)
            continue
        if plantilla.endswith(".json"):
            ruta = os.path.join(raiz, destino)
            if not os.path.exists(ruta) or a.forzar:
                os.makedirs(os.path.dirname(ruta), exist_ok=True)
                shutil.copyfile(origen, ruta)
                creados.append(ruta)
            continue
        with open(origen, encoding="utf-8") as f:
            escribir(os.path.join(raiz, destino), rellenar(f.read(), valores), a.forzar, creados)

    with open(os.path.join(PLANTILLAS, "informe-modulo.md"), encoding="utf-8") as f:
        plantilla_informe = f.read()
    for carpeta, clave, titulo in MODULOS:
        if clave != "brief":
            nombre_informe = {"marketing_ventas": "plan-gtm.md"}.get(clave, "informe.md")
            if clave == "veredicto":
                nombre_informe = "riesgos.md"
            escribir(os.path.join(raiz, carpeta, nombre_informe),
                     rellenar(plantilla_informe, dict(valores, MODULO=titulo)), a.forzar, creados)
        esqueleto = {"modulo": clave, "version_esquema": 1, "fecha": hoy, "modo": a.modo, "confianza": "baja",
                     "resumen": "", "hallazgos": [], "metricas": {}, "banderas_rojas": [], "banderas_amarillas": [],
                     "pendiente": [], "implicacion_decision": ""}
        escribir(os.path.join(raiz, carpeta, "datos.json"),
                 json.dumps(esqueleto, ensure_ascii=False, indent=2) + "\n", a.forzar, creados)

    escribir(os.path.join(raiz, "fuentes", "fuentes.json"), "[]\n", a.forzar, creados)
    escribir(os.path.join(raiz, "fuentes", "evidencias.jsonl"), "", a.forzar, creados)

    print(f"Estudio: {raiz}")
    print(f"Archivos creados: {len(creados)}" + ("" if creados else " (ya existían; usa --forzar para regenerar)"))
    for c in creados:
        print("  " + os.path.relpath(c, a.dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
