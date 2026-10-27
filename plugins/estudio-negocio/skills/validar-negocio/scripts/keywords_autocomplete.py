#!/usr/bin/env python3
"""Expande palabras clave con el autocompletado de Google, YouTube, Bing, DuckDuckGo y Amazon.

Sin claves de API. Usa endpoints públicos de sugerencias (no oficiales: pueden cambiar o
limitar peticiones). La presencia de una keyword en el autocompletado indica que tiene un
volumen mínimo de búsquedas; aparecer en varios motores y en posiciones altas sugiere más
popularidad. NO da volúmenes exactos: combínalo con Keyword Planner o Trends.

Ejemplos:
  python3 keywords_autocomplete.py "cafetería de especialidad" "café para llevar" --pais es
  python3 keywords_autocomplete.py "silla ergonómica" --motores google,amazon --modo preguntas
  python3 keywords_autocomplete.py --selftest
"""

import argparse
import json
import os
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import ErrorRed, avisar, escribir_csv, normalizar, obtener, sin_tildes  # noqa: E402

AMAZON = {  # país → (dominio de sugerencias, marketplace id)
    "es": ("completion.amazon.es", "A1RKKUPIHCS9HS"),
    "mx": ("completion.amazon.com.mx", "A1AM78C64UM0Y8"),
    "us": ("completion.amazon.com", "ATVPDKIKX0DER"),
    "uk": ("completion.amazon.co.uk", "A1F83G8C2ARO7P"),
    "gb": ("completion.amazon.co.uk", "A1F83G8C2ARO7P"),
    "de": ("completion.amazon.de", "A1PA6795UKMFR9"),
    "fr": ("completion.amazon.fr", "A13V1IB3VIYZZH"),
    "it": ("completion.amazon.it", "APJ6JRA9NG5V4"),
    "br": ("completion.amazon.com.br", "A2Q3Y263D00KWC"),
}

MODIFICADORES = {
    "es": {
        "prefijos": ["qué", "cómo", "cuánto cuesta", "cuál es el mejor", "dónde", "por qué",
                     "mejor", "comprar", "alternativa a", "se puede"],
        "sufijos": ["precio", "opiniones", "barato", "cerca de mí", "para", "vs", "online",
                    "sin", "con", "requisitos", "gratis", "ideas"],
        "alfabeto": list("abcdefghijklmnñopqrstuvwxyz"),
    },
    "en": {
        "prefijos": ["what", "how", "how much", "best", "where", "why", "buy", "alternative to",
                     "can i"],
        "sufijos": ["price", "reviews", "cheap", "near me", "for", "vs", "online", "without",
                    "with", "free", "ideas"],
        "alfabeto": list("abcdefghijklmnopqrstuvwxyz"),
    },
}

# Reglas de intención (se comparan sin tildes y en minúsculas).
REGLAS_INTENCION = [
    ("local", ["cerca de mi", "cerca de", "near me", "horario", "direccion", " en madrid",
               " en barcelona", " en valencia", " en sevilla", " en bilbao", " en malaga",
               " en zaragoza", " a domicilio"]),
    ("transaccional", ["comprar", "precio", "precios", "barato", "barata", "oferta", "ofertas",
                       "descuento", "tienda", "envio", "contratar", "presupuesto", "alquiler",
                       "reservar", "pedido", "cupon", "buy", "price", "cheap", "deal", "shop",
                       "coupon", "order", "hire", "cuanto cuesta", "tarifa", "tarifas"]),
    ("comercial", ["mejor", "mejores", "opiniones", "opinion", "comparativa", "comparar", " vs ",
                   " vs", "alternativa", "alternativas", "top ", "ranking", "review", "reviews",
                   "best", "versus", "merece la pena", "recomendacion"]),
    ("informacional", ["que es", "como ", "por que", "cuando", "quien", "guia", "tutorial",
                       "ideas", "significado", "requisitos", "what", "how", "why", "tips",
                       "consejos", "se puede", "para que sirve", "tipos de"]),
]


def clasificar_intencion(keyword, ciudades=()):
    k = " " + sin_tildes(normalizar(keyword)) + " "
    for c in ciudades:
        if f" en {sin_tildes(c.lower())}" in k or f" {sin_tildes(c.lower())} " in k:
            return "local"
    for intencion, marcadores in REGLAS_INTENCION:
        for m in marcadores:
            if m in k:
                return intencion
    return "sin_clasificar"


# --- Parsers (separados para poder probarlos sin red) ---

def parse_google(texto):
    datos = json.loads(texto)
    return [s for s in datos[1] if isinstance(s, str)] if len(datos) > 1 else []


def parse_bing(texto):
    return parse_google(texto)


def parse_ddg(texto):
    datos = json.loads(texto)
    return [d.get("phrase", "") for d in datos if isinstance(d, dict) and d.get("phrase")]


def parse_amazon(texto):
    datos = json.loads(texto)
    return [s.get("value", "") for s in datos.get("suggestions", []) if s.get("value")]


def sugerencias(motor, consulta, pais, idioma, pausa):
    if motor == "google":
        t = obtener("https://suggestqueries.google.com/complete/search",
                    {"client": "firefox", "hl": idioma, "gl": pais, "q": consulta}, pausa=pausa)
        return parse_google(t)
    if motor == "youtube":
        t = obtener("https://suggestqueries.google.com/complete/search",
                    {"client": "firefox", "ds": "yt", "hl": idioma, "gl": pais, "q": consulta},
                    pausa=pausa)
        return parse_google(t)
    if motor == "bing":
        t = obtener("https://api.bing.com/osjson.aspx",
                    {"query": consulta, "market": f"{idioma}-{pais.upper()}"}, pausa=pausa)
        return parse_bing(t)
    if motor == "ddg":
        t = obtener("https://duckduckgo.com/ac/", {"q": consulta, "kl": f"{pais}-{idioma}"},
                    pausa=pausa)
        return parse_ddg(t)
    if motor == "amazon":
        dominio, mid = AMAZON.get(pais, AMAZON["es"])
        t = obtener(f"https://{dominio}/api/2017/suggestions",
                    {"mid": mid, "alias": "aps", "prefix": consulta}, pausa=pausa)
        return parse_amazon(t)
    raise ValueError(f"Motor desconocido: {motor}")


def consultas_para(semilla, modo, idioma):
    mods = MODIFICADORES.get(idioma, MODIFICADORES["en"])
    consultas = [(semilla, "base")]
    if modo in ("preguntas", "completo"):
        consultas += [(f"{p} {semilla}", f"prefijo:{p}") for p in mods["prefijos"]]
        consultas += [(f"{semilla} {s}", f"sufijo:{s}") for s in mods["sufijos"]]
    if modo in ("alfabeto", "completo"):
        consultas += [(f"{semilla} {letra}", f"letra:{letra}") for letra in mods["alfabeto"]]
    return consultas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("semillas", nargs="*", help="Palabras clave semilla")
    ap.add_argument("--pais", default="es", help="Código de país (es, mx, us, ar, co…). Por defecto: es")
    ap.add_argument("--idioma", default=None, help="Idioma (es, en…). Por defecto: es salvo us/uk/gb")
    ap.add_argument("--motores", default="google,youtube,bing,ddg",
                    help="Lista separada por comas: google,youtube,bing,ddg,amazon")
    ap.add_argument("--modo", default="completo", choices=["basico", "preguntas", "alfabeto", "completo"])
    ap.add_argument("--ciudades", default="", help="Ciudades separadas por comas para detectar intención local")
    ap.add_argument("--salida", default="keywords_autocompletado.csv", help="Ruta del CSV de salida")
    ap.add_argument("--pausa", type=float, default=0.35, help="Segundos entre peticiones")
    ap.add_argument("--max-peticiones", type=int, default=600)
    ap.add_argument("--selftest", action="store_true", help="Prueba los parsers sin red")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.semillas:
        ap.error("indica al menos una semilla")

    pais = args.pais.lower()
    idioma = args.idioma or ("en" if pais in ("us", "uk", "gb") else "es")
    motores = [m.strip() for m in args.motores.split(",") if m.strip()]
    ciudades = [c.strip() for c in args.ciudades.split(",") if c.strip()]

    resultados = OrderedDict()
    peticiones = errores = 0
    motores_fallidos = {}
    for semilla in args.semillas:
        for consulta, origen in consultas_para(semilla, args.modo, idioma):
            for motor in motores:
                if motor in motores_fallidos and motores_fallidos[motor] >= 3:
                    continue
                if peticiones >= args.max_peticiones:
                    break
                peticiones += 1
                try:
                    lista = sugerencias(motor, consulta, pais, idioma, args.pausa)
                except (ErrorRed, ValueError, json.JSONDecodeError) as e:
                    errores += 1
                    motores_fallidos[motor] = motores_fallidos.get(motor, 0) + 1
                    if motores_fallidos[motor] == 3:
                        avisar(f"[aviso] {motor}: 3 fallos seguidos, lo desactivo. Último error: {e}")
                    continue
                motores_fallidos[motor] = 0
                for pos, kw in enumerate(lista, start=1):
                    clave = normalizar(kw)
                    if not clave:
                        continue
                    r = resultados.setdefault(clave, {
                        "keyword": clave, "motores": set(), "apariciones": 0,
                        "mejor_posicion": pos, "semilla": semilla, "consulta_origen": origen,
                    })
                    r["motores"].add(motor)
                    r["apariciones"] += 1
                    r["mejor_posicion"] = min(r["mejor_posicion"], pos)

    filas = []
    for r in resultados.values():
        r["n_motores"] = len(r["motores"])
        r["motores"] = ",".join(sorted(r["motores"]))
        r["intencion"] = clasificar_intencion(r["keyword"], ciudades)
        # Popularidad relativa (heurística): más motores, más apariciones y mejor posición.
        r["popularidad"] = round(r["n_motores"] * 3 + min(r["apariciones"], 10) + (11 - min(r["mejor_posicion"], 10)) * 0.5, 1)
        filas.append(r)
    filas.sort(key=lambda r: (-r["popularidad"], r["keyword"]))

    columnas = ["keyword", "intencion", "popularidad", "n_motores", "motores", "apariciones",
                "mejor_posicion", "semilla", "consulta_origen"]
    escribir_csv(args.salida, filas, columnas)

    print(f"# Autocompletado · país={pais} idioma={idioma} · motores={','.join(motores)}")
    print(f"Peticiones: {peticiones} · errores: {errores} · keywords únicas: {len(filas)}")
    if not filas:
        print("Sin resultados. Comprueba la conexión o prueba con otros motores (--motores).")
        return 1 if errores else 0
    conteo = {}
    for r in filas:
        conteo[r["intencion"]] = conteo.get(r["intencion"], 0) + 1
    print("Por intención: " + ", ".join(f"{k}={v}" for k, v in sorted(conteo.items(), key=lambda x: -x[1])))
    print("\nTop 30 (popularidad relativa, NO es volumen de búsquedas):")
    for r in filas[:30]:
        print(f"  {r['popularidad']:>5}  [{r['intencion']}] {r['keyword']}  ({r['motores']})")
    print(f"\nCSV guardado en: {args.salida}")
    return 0


def selftest():
    assert parse_google('["cafe",["cafe con leche","cafe solo"],[],{}]') == ["cafe con leche", "cafe solo"]
    assert parse_ddg('[{"phrase":"cafe de especialidad"},{"phrase":"cafe madrid"}]') == ["cafe de especialidad", "cafe madrid"]
    assert parse_amazon('{"suggestions":[{"value":"cafe en grano"},{"value":"cafetera"}]}') == ["cafe en grano", "cafetera"]
    casos = {
        "comprar café en grano": "transaccional",
        "mejor cafetera italiana": "comercial",
        "cafetería cerca de mí": "local",
        "qué es el café de especialidad": "informacional",
        "cafetería de especialidad": "sin_clasificar",
        "café de especialidad valencia": "local",
    }
    for kw, esperado in casos.items():
        obtenido = clasificar_intencion(kw, ciudades=["Valencia"])
        assert obtenido == esperado, (kw, obtenido, esperado)
    q = consultas_para("café", "completo", "es")
    assert q[0] == ("café", "base") and any(o == "letra:ñ" for _, o in q)
    print("selftest OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
