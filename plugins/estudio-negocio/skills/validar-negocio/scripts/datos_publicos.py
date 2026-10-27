#!/usr/bin/env python3
"""Consulta estadísticas públicas y señales de interés sin claves de API.

Subcomandos:
  worldbank  Indicador del Banco Mundial por país          (ej.: SP.POP.TOTL, NY.GDP.PCAP.CD, IT.NET.USER.ZS)
  eurostat   Dataset de Eurostat con filtros               (ej.: demo_pjan geo=ES sex=T age=TOTAL)
  ine-tabla  Tabla del INE (España) por su ID              (el ID aparece en la URL de la tabla en ine.es: ?t=XXXXX)
  ine-serie  Serie del INE por su código                   (ej.: IPC251852)
  wikipedia  Visitas mensuales a un artículo de Wikipedia  (indicador de interés por un tema)
  gdelt      Volumen de noticias sobre un tema (últimos meses, por país o idioma)

Ejemplos:
  python3 datos_publicos.py worldbank SP.POP.TOTL --pais ES --anios 5
  python3 datos_publicos.py eurostat demo_pjan geo=ES sex=T age=TOTAL --ultimos 3
  python3 datos_publicos.py ine-tabla 50902 --nult 3 --contiene "Total"
  python3 datos_publicos.py wikipedia "Café de especialidad" --idioma es --meses 36
  python3 datos_publicos.py gdelt "café de especialidad" --pais SP --idioma spanish
  python3 datos_publicos.py --selftest

Cita siempre la fuente (organismo, tabla o indicador, fecha de consulta) en fuentes.json.
"""

import argparse
import datetime as dt
import itertools
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import ErrorRed, avisar, escribir_csv, obtener_json, tabla_md  # noqa: E402


# --- Banco Mundial ---

def parse_worldbank(datos):
    if not isinstance(datos, list) or len(datos) < 2 or datos[1] is None:
        msg = datos[0].get("message") if isinstance(datos, list) and datos and isinstance(datos[0], dict) else None
        raise ErrorRed(f"Banco Mundial sin datos: {msg or datos!r}"[:300])
    filas = []
    for d in datos[1]:
        filas.append({"pais": d.get("country", {}).get("value", ""), "indicador": d.get("indicator", {}).get("value", ""),
                      "anio": d.get("date", ""), "valor": d.get("value")})
    return filas


def cmd_worldbank(a):
    url = f"https://api.worldbank.org/v2/country/{a.pais}/indicator/{a.indicador}"
    filas = parse_worldbank(obtener_json(url, {"format": "json", "per_page": 100, "mrv": a.anios}))
    fuente = f"Banco Mundial, indicador {a.indicador} ({url})"
    return filas, ["pais", "indicador", "anio", "valor"], fuente


# --- Eurostat (JSON-stat 2.0) ---

def parse_jsonstat(datos):
    ids = datos.get("id", [])
    tamanos = datos.get("size", [])
    dims = datos.get("dimension", {})
    valores = datos.get("value", {})
    if isinstance(valores, list):
        valores = {str(i): v for i, v in enumerate(valores) if v is not None}
    categorias = []
    for d in ids:
        cat = dims[d]["category"]
        indice = cat.get("index", {})
        if isinstance(indice, list):
            orden = indice
        else:
            orden = [k for k, _ in sorted(indice.items(), key=lambda kv: kv[1])]
        etiquetas = cat.get("label", {})
        categorias.append([(c, etiquetas.get(c, c)) for c in orden])
    filas = []
    for pos, combinacion in enumerate(itertools.product(*categorias)):
        v = valores.get(str(pos))
        if v is None:
            continue
        fila = {}
        for d, (codigo, etiqueta) in zip(ids, combinacion):
            fila[d] = codigo if codigo == etiqueta else f"{codigo} ({etiqueta})"
        fila["valor"] = v
        filas.append(fila)
    assert len(categorias) == len(tamanos) or not tamanos
    return filas, ids


def cmd_eurostat(a):
    params = [("format", "JSON"), ("lang", "EN")]
    for f in a.filtros:
        if "=" not in f:
            raise SystemExit(f"Filtro mal formado: {f} (usa clave=valor)")
        k, v = f.split("=", 1)
        params.append((k, v))
    if a.ultimos:
        params.append(("lastTimePeriod", str(a.ultimos)))
    url = f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{a.dataset}?" + urllib.parse.urlencode(params)
    datos = obtener_json(url)
    filas, ids = parse_jsonstat(datos)
    fuente = f"Eurostat, dataset {a.dataset} — {datos.get('label', '')} (actualizado {datos.get('updated', '?')})"
    return filas, ids + ["valor"], fuente


# --- INE ---

def _fecha_ine(d):
    f = d.get("Fecha")
    if isinstance(f, (int, float)):
        return dt.datetime.fromtimestamp(f / 1000, dt.timezone.utc).strftime("%Y-%m-%d")
    if isinstance(f, str) and f:
        return f[:10]
    anio = d.get("Anyo", "")
    periodo = d.get("NombrePeriodo") or d.get("T3_Periodo") or d.get("FK_Periodo", "")
    return f"{anio} {periodo}".strip()


def parse_ine(datos, contiene=None):
    series = datos if isinstance(datos, list) else [datos]
    filas = []
    for s in series:
        nombre = s.get("Nombre", s.get("COD", ""))
        if contiene and contiene.lower() not in nombre.lower():
            continue
        for d in s.get("Data", []):
            filas.append({"serie": nombre.strip(), "periodo": _fecha_ine(d), "valor": d.get("Valor")})
    return filas


def cmd_ine_tabla(a):
    url = f"https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{a.id}"
    filas = parse_ine(obtener_json(url, {"nult": a.nult, "tip": "A"}), a.contiene)
    return filas, ["serie", "periodo", "valor"], f"INE, tabla {a.id} (https://www.ine.es/jaxiT3/Tabla.htm?t={a.id})"


def cmd_ine_serie(a):
    url = f"https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{a.codigo}"
    filas = parse_ine(obtener_json(url, {"nult": a.nult, "tip": "A"}))
    return filas, ["serie", "periodo", "valor"], f"INE, serie {a.codigo} ({url})"


# --- Wikipedia pageviews ---

def parse_pageviews(datos):
    return [{"mes": f"{i['timestamp'][:4]}-{i['timestamp'][4:6]}", "visitas": i.get("views", 0)}
            for i in datos.get("items", [])]


def tendencia(valores):
    """Compara la media del último tercio con la del primero."""
    valores = [v for v in valores if isinstance(v, (int, float))]
    if len(valores) < 6:
        return "datos insuficientes", None
    n = len(valores) // 3
    inicio, fin = sum(valores[:n]) / n, sum(valores[-n:]) / n
    if inicio == 0:
        return ("sube" if fin > 0 else "estable"), None
    cambio = (fin - inicio) / inicio * 100
    etiqueta = "sube" if cambio > 15 else "baja" if cambio < -15 else "estable"
    return etiqueta, round(cambio, 1)


def cmd_wikipedia(a):
    hoy = dt.date.today()
    fin = hoy.replace(day=1) - dt.timedelta(days=1)  # último mes completo
    inicio_mes = (fin.year * 12 + fin.month - 1) - (a.meses - 1)
    inicio = dt.date(inicio_mes // 12, inicio_mes % 12 + 1, 1)
    articulo = urllib.parse.quote(a.articulo.replace(" ", "_"), safe="")
    url = (f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{a.idioma}.wikipedia/"
           f"all-access/user/{articulo}/monthly/{inicio:%Y%m%d}00/{fin:%Y%m%d}00")
    filas = parse_pageviews(obtener_json(url))
    t, cambio = tendencia([f["visitas"] for f in filas])
    print(f"Tendencia (último tercio frente al primero): {t}" + (f" ({cambio:+} %)" if cambio is not None else ""))
    return filas, ["mes", "visitas"], f"Wikimedia Pageviews, {a.idioma}.wikipedia «{a.articulo}»"


# --- GDELT ---

def parse_gdelt(datos):
    filas = []
    for serie in datos.get("timeline", []):
        for p in serie.get("data", []):
            filas.append({"fecha": str(p.get("date", ""))[:8], "valor": p.get("value"), "serie": serie.get("series", "")})
    return filas


def cmd_gdelt(a):
    consulta = a.consulta if a.consulta.startswith('"') or " " not in a.consulta else f'"{a.consulta}"'
    if a.pais:
        consulta += f" sourcecountry:{a.pais}"
    if a.idioma:
        consulta += f" sourcelang:{a.idioma}"
    datos = obtener_json("https://api.gdeltproject.org/api/v2/doc/doc",
                         {"query": consulta, "mode": "timelinevol", "format": "json", "timespan": a.periodo})
    filas = parse_gdelt(datos)
    t, cambio = tendencia([f["valor"] for f in filas])
    print(f"Tendencia de cobertura (último tercio frente al primero): {t}" + (f" ({cambio:+} %)" if cambio is not None else ""))
    return filas, ["fecha", "valor", "serie"], f"GDELT DOC 2.0, consulta {consulta!r}, periodo {a.periodo} (valor = % de noticias monitorizadas)"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")

    def comunes(p):
        p.add_argument("--csv", help="Guardar resultados en CSV")
        p.add_argument("--max-filas", type=int, default=60, help="Filas a mostrar en pantalla")

    p = sub.add_parser("worldbank")
    p.add_argument("indicador")
    p.add_argument("--pais", default="ES", help="Código ISO2/ISO3 (ES, MX, AR…)")
    p.add_argument("--anios", type=int, default=10)
    comunes(p)

    p = sub.add_parser("eurostat")
    p.add_argument("dataset")
    p.add_argument("filtros", nargs="*", help="clave=valor (p. ej. geo=ES)")
    p.add_argument("--ultimos", type=int, default=5, help="Últimos N periodos")
    comunes(p)

    p = sub.add_parser("ine-tabla")
    p.add_argument("id")
    p.add_argument("--nult", type=int, default=5, help="Últimos N periodos")
    p.add_argument("--contiene", help="Filtrar series cuyo nombre contenga este texto")
    comunes(p)

    p = sub.add_parser("ine-serie")
    p.add_argument("codigo")
    p.add_argument("--nult", type=int, default=12)
    comunes(p)

    p = sub.add_parser("wikipedia")
    p.add_argument("articulo", help="Título exacto del artículo")
    p.add_argument("--idioma", default="es")
    p.add_argument("--meses", type=int, default=36)
    comunes(p)

    p = sub.add_parser("gdelt")
    p.add_argument("consulta")
    p.add_argument("--pais", help="Código FIPS del país de la fuente: SP=España, MX, AR, CO, CI=Chile, PE, US, UK")
    p.add_argument("--idioma", help="spanish, english, portuguese…")
    p.add_argument("--periodo", default="3m", help="Ventana temporal (p. ej. 1m, 3m). GDELT cubre los últimos meses")
    comunes(p)

    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.cmd:
        ap.print_help()
        return 1
    funciones = {"worldbank": cmd_worldbank, "eurostat": cmd_eurostat, "ine-tabla": cmd_ine_tabla,
                 "ine-serie": cmd_ine_serie, "wikipedia": cmd_wikipedia, "gdelt": cmd_gdelt}
    try:
        filas, columnas, fuente = funciones[a.cmd](a)
    except ErrorRed as e:
        avisar(f"[error] {e}")
        return 2
    print(f"Fuente: {fuente} · consultado {dt.date.today()}")
    print(f"Filas: {len(filas)}\n")
    if filas:
        print(tabla_md(filas[: a.max_filas], columnas))
        if len(filas) > a.max_filas:
            print(f"\n… {len(filas) - a.max_filas} filas más (usa --csv para guardarlas todas)")
    if a.csv:
        escribir_csv(a.csv, filas, columnas)
        print(f"\nCSV guardado en {a.csv}")
    return 0


def selftest():
    wb = [{"page": 1}, [{"country": {"value": "Spain"}, "indicator": {"value": "Population, total"}, "date": "2024", "value": 48619695}]]
    assert parse_worldbank(wb)[0]["valor"] == 48619695
    js = {"id": ["geo", "time"], "size": [1, 2],
          "dimension": {"geo": {"category": {"index": {"ES": 0}, "label": {"ES": "Spain"}}},
                        "time": {"category": {"index": {"2023": 0, "2024": 1}, "label": {"2023": "2023", "2024": "2024"}}}},
          "value": {"0": 100, "1": 110}}
    filas, ids = parse_jsonstat(js)
    assert filas == [{"geo": "ES (Spain)", "time": "2023", "valor": 100}, {"geo": "ES (Spain)", "time": "2024", "valor": 110}]
    ine = [{"Nombre": "Total Nacional. Total. ", "Data": [{"Fecha": 1704067200000, "Valor": 1.5}, {"Anyo": 2023, "FK_Periodo": 28, "Valor": 1.2}]}]
    f = parse_ine(ine, contiene="total nacional")
    assert f[0]["periodo"] == "2024-01-01" and f[1]["periodo"] == "2023 28"
    pv = {"items": [{"timestamp": "2024010100", "views": 10}, {"timestamp": "2024020100", "views": 12}]}
    assert parse_pageviews(pv)[1] == {"mes": "2024-02", "visitas": 12}
    assert tendencia([10, 10, 10, 10, 20, 20, 20, 20, 30])[0] == "sube"
    assert tendencia([10] * 9)[0] == "estable"
    gd = {"timeline": [{"series": "Volume Intensity", "data": [{"date": "20250101T000000Z", "value": 0.12}]}]}
    assert parse_gdelt(gd)[0] == {"fecha": "20250101", "valor": 0.12, "serie": "Volume Intensity"}
    print("selftest OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
