"""Utilidades compartidas por los scripts de la skill validar-negocio.

Solo usa la biblioteca estándar de Python (3.9+). Sin claves de API.
"""

import csv
import gzip
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = (
    "Mozilla/5.0 (compatible; validar-negocio-skill/1.0; "
    "investigacion de mercado; +https://github.com/denisky19/denisky19.github.io)"
)

_ultima_peticion = 0.0


class ErrorRed(Exception):
    """Fallo de red o HTTP con un mensaje legible."""


def obtener(url, params=None, pausa=0.0, timeout=20, reintentos=2, cabeceras=None, binario=False):
    """GET con reintentos, pausa entre peticiones y descompresión gzip.

    Devuelve texto (o bytes si binario=True). Lanza ErrorRed con un mensaje claro.
    """
    global _ultima_peticion
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    espera = pausa - (time.time() - _ultima_peticion)
    if espera > 0:
        time.sleep(espera)
    hdrs = {"User-Agent": USER_AGENT, "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"}
    if cabeceras:
        hdrs.update(cabeceras)
    ultimo_error = None
    for intento in range(reintentos + 1):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                _ultima_peticion = time.time()
                datos = resp.read()
                if resp.headers.get("Content-Encoding") == "gzip" or url.endswith(".gz"):
                    try:
                        datos = gzip.decompress(datos)
                    except OSError:
                        pass
                if binario:
                    return datos
                charset = resp.headers.get_content_charset() or "utf-8"
                return datos.decode(charset, errors="replace")
        except urllib.error.HTTPError as e:
            _ultima_peticion = time.time()
            ultimo_error = f"HTTP {e.code} en {url}"
            if e.code in (429, 500, 502, 503, 504) and intento < reintentos:
                time.sleep(2 * (intento + 1))
                continue
            break
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            _ultima_peticion = time.time()
            motivo = getattr(e, "reason", e)
            ultimo_error = f"No se pudo conectar con {urllib.parse.urlparse(url).netloc}: {motivo}"
            if intento < reintentos:
                time.sleep(1.5 * (intento + 1))
                continue
            break
    raise ErrorRed(
        ultimo_error
        + " · Si la red está restringida (403 del proxy o error de DNS), pide al usuario que permita "
        "ese dominio o usa la búsqueda web / WebFetch como alternativa."
    )


def obtener_json(url, params=None, **kw):
    texto = obtener(url, params=params, **kw)
    try:
        return json.loads(texto)
    except json.JSONDecodeError as e:
        raise ErrorRed(f"Respuesta no JSON de {url}: {texto[:200]!r}") from e


def normalizar(texto):
    """Minúsculas, sin espacios repetidos (conserva tildes y ñ)."""
    return re.sub(r"\s+", " ", (texto or "").strip().lower())


def sin_tildes(texto):
    return "".join(
        c for c in unicodedata.normalize("NFD", texto or "") if unicodedata.category(c) != "Mn"
    )


def slug(texto, maximo=60):
    s = sin_tildes(texto).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return (s[:maximo].rstrip("-")) or "estudio"


def escribir_csv(ruta, filas, columnas):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columnas, extrasaction="ignore")
        w.writeheader()
        for fila in filas:
            w.writerow({k: _a_texto(fila.get(k, "")) for k in columnas})


def _a_texto(v):
    if isinstance(v, (list, tuple, set)):
        return "; ".join(str(x) for x in v)
    return v


def tabla_md(filas, columnas, titulos=None):
    """Tabla Markdown simple a partir de una lista de diccionarios."""
    titulos = titulos or columnas
    lineas = ["| " + " | ".join(titulos) + " |", "|" + "---|" * len(columnas)]
    for fila in filas:
        celdas = []
        for c in columnas:
            v = _a_texto(fila.get(c, ""))
            v = "" if v is None else str(v)
            celdas.append(v.replace("|", "\\|").replace("\n", " "))
        lineas.append("| " + " | ".join(celdas) + " |")
    return "\n".join(lineas)


def avisar(msg):
    print(msg, file=sys.stderr)


def recortar(texto, n=600):
    texto = re.sub(r"\s+", " ", texto or "").strip()
    return texto if len(texto) <= n else texto[: n - 1].rstrip() + "…"
