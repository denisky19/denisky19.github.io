#!/usr/bin/env python3
"""Prueba de integración sin red: autopruebas de cada script y flujo completo de un estudio.

Uso:  python3 scripts/pruebas/prueba_integracion.py [--conservar]
Los datos del estudio de prueba son FICTICIOS: solo sirven para comprobar el formato.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ejecutar(*args, cwd=None):
    r = subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:], sep="\n")
        raise SystemExit(f"FALLO: {' '.join(args)} (código {r.returncode})")
    return r.stdout


def escribir_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def main():
    for s in ("keywords_autocomplete", "voz_cliente", "datos_publicos", "competidor_web",
              "modelo_financiero", "puntuacion"):
        salida = ejecutar(os.path.join(SCRIPTS, f"{s}.py"), "--selftest")
        assert "selftest OK" in salida, s
        print(f"✓ {s} --selftest")

    tmp = tempfile.mkdtemp(prefix="estudio-prueba-")
    try:
        ejecutar(os.path.join(SCRIPTS, "nuevo_estudio.py"), "Cafetería de prueba (FICTICIO)", "--dir", tmp)
        raiz = os.path.join(tmp, "cafeteria-de-prueba-ficticio")
        for rel in ("README.md", "PROGRESO.md", "00-brief/brief.md", "06-viabilidad/supuestos.json",
                    "10-veredicto/puntuacion.json", "ia/contexto-ia.md", "fuentes/fuentes.json",
                    "04-competencia/datos.json", "07-marketing-ventas/plan-gtm.md"):
            assert os.path.exists(os.path.join(raiz, rel)), rel
        print("✓ nuevo_estudio crea la estructura")
        # Relanzar no sobrescribe
        assert "ya existían" in ejecutar(os.path.join(SCRIPTS, "nuevo_estudio.py"), "Cafetería de prueba (FICTICIO)", "--dir", tmp)

        ejecutar(os.path.join(SCRIPTS, "modelo_financiero.py"), os.path.join(raiz, "06-viabilidad", "supuestos.json"),
                 "--salida", os.path.join(raiz, "06-viabilidad"))
        modelo = json.load(open(os.path.join(raiz, "06-viabilidad", "modelo.json"), encoding="utf-8"))
        assert set(modelo["escenarios"]) == {"pesimista", "base", "optimista"}
        assert modelo["escenarios"]["base"]["margen_contribucion_unitario"] > 0
        print("✓ modelo_financiero con la plantilla de supuestos")

        punt = json.load(open(os.path.join(raiz, "10-veredicto", "puntuacion.json"), encoding="utf-8"))
        valores = {"dolor": 6, "demanda": 6, "mercado": 5, "hueco": 5, "pago": 6, "economia": 5, "distribucion": 6, "ejecucion": 7}
        for k, v in valores.items():
            punt["dimensiones"][k].update(puntuacion=v, confianza="media", justificacion="FICTICIO", evidencia=["F1"])
        punt.update(fuentes_solidas=12, argumento_a_favor="FICTICIO a favor", argumento_en_contra="FICTICIO en contra")
        escribir_json(os.path.join(raiz, "10-veredicto", "puntuacion.json"), punt)
        ejecutar(os.path.join(SCRIPTS, "puntuacion.py"), os.path.join(raiz, "10-veredicto", "puntuacion.json"))
        res = json.load(open(os.path.join(raiz, "10-veredicto", "puntuacion-resultado.json"), encoding="utf-8"))
        assert res["veredicto"] == "AJUSTAR", res["veredicto"]
        print("✓ puntuacion → AJUSTAR con el caso de prueba")

        def modulo(carpeta, **campos):
            ruta = os.path.join(raiz, carpeta, "datos.json")
            d = json.load(open(ruta, encoding="utf-8"))
            d.update(campos)
            escribir_json(ruta, d)

        modulo("00-brief", metricas={"idea": "Cafetería de prueba (FICTICIO)", "arquetipo": "local", "ambito": "Barrio X",
                                     "cliente_tipo": "B2C", "modelo_ingresos": "venta por ticket"})
        modulo("01-mercado", resumen="FICTICIO: resumen de mercado.", confianza="media",
               metricas={"tam": {"valor": 2500000, "unidad": "EUR/año"}, "sam": {"valor": 900000, "unidad": "EUR/año"},
                         "som": {"valor": 160000, "unidad": "EUR/año"}, "fase_mercado": "madurez"},
               banderas_amarillas=["FICTICIO: competencia alta en la calle principal"])
        modulo("04-competencia", resumen="FICTICIO", metricas={"intensidad_competitiva": "alta", "hueco": "FICTICIO",
               "competidores": [{"nombre": "Competidor A <script>", "tipo": "directo", "precio": "2,10 €",
                                 "fortalezas": ["ubicación"], "debilidades": ["colas"], "url": "javascript:alert(1)"}]})
        modulo("05-estrategia", resumen="FICTICIO", metricas={"dafo": {"fortalezas": [{"texto": "Experiencia", "evidencia": ["F1"]}],
               "debilidades": ["Sin marca"], "oportunidades": ["Turismo"], "amenazas": ["Cadenas"]}})
        modulo("10-veredicto", resumen="FICTICIO", metricas={"experimentos": [{"nombre": "Pop-up", "coste_max": 300,
               "plazo": "1 fin de semana", "umbral_exito": "≥ 150 ventas", "umbral_parada": "< 60 ventas"}]})
        escribir_json(os.path.join(raiz, "fuentes", "fuentes.json"),
                      [{"id": "F1", "titulo": "Fuente ficticia", "url": "https://example.org", "nivel": "T1"}])

        ejecutar(os.path.join(SCRIPTS, "generar_informe.py"), raiz)
        html = open(os.path.join(raiz, "informe.html"), encoding="utf-8").read()
        for texto in ("Veredicto", "Cifras clave", "DAFO", "Competencia", "Viabilidad económica", "Fuentes (1)", "2,5 M €"):
            assert texto in html, texto
        assert "<script>alert" not in html and "Competidor A &lt;script&gt;" in html and 'href="javascript' not in html
        estudio = json.load(open(os.path.join(raiz, "ia", "estudio.json"), encoding="utf-8"))
        assert estudio["modulos"]["veredicto"]["metricas"]["veredicto"] == "AJUSTAR"
        assert estudio["modulos"]["viabilidad"]["modelo"]["escenarios"]
        print("✓ generar_informe crea informe.html (escapado) e ia/estudio.json")
        print(f"\nTODO OK · estudio de prueba en {raiz}")
    finally:
        if "--conservar" not in sys.argv:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
