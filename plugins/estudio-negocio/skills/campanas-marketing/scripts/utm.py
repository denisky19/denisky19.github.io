#!/usr/bin/env python3
"""Genera enlaces con UTM coherentes para una campaña y los guarda en CSV.

Ejemplo:
  python3 utm.py --base https://ejemplo.com/bodas --campana bodas-2027 \
      --fuentes instagram:paid_social,facebook:paid_social,google:cpc,bodasnet:referral,bio:social \
      --contenidos video-boda-1,carrusel-packs --salida utm.csv
  python3 utm.py --selftest
"""
import argparse
import csv
import re
import sys
import unicodedata
import urllib.parse

MEDIO_DEFECTO = {"instagram": "social", "facebook": "social", "tiktok": "social", "google": "cpc",
                 "email": "email", "whatsapp": "messaging", "bio": "social", "linkedin": "social"}


def limpio(t):
    t = "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9_\-]+", "-", t.strip().lower()).strip("-")


def url_utm(base, fuente, medio, campana, contenido=None, termino=None):
    p = urllib.parse.urlparse(base)
    q = dict(urllib.parse.parse_qsl(p.query))
    q.update({"utm_source": limpio(fuente), "utm_medium": limpio(medio), "utm_campaign": limpio(campana)})
    if contenido:
        q["utm_content"] = limpio(contenido)
    if termino:
        q["utm_term"] = limpio(termino)
    return urllib.parse.urlunparse(p._replace(query=urllib.parse.urlencode(q)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base")
    ap.add_argument("--campana")
    ap.add_argument("--fuentes", default="instagram,facebook,google", help="fuente o fuente:medio, separadas por comas")
    ap.add_argument("--contenidos", default="", help="variantes de anuncio o enlace, separadas por comas")
    ap.add_argument("--salida", default="utm.csv")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        u = url_utm("https://x.com/bodas?ref=1", "Instagram", "paid social", "Bodas 2027", "Vídeo 1")
        assert "ref=1" in u and "utm_source=instagram" in u and "utm_medium=paid-social" in u and "utm_campaign=bodas-2027" in u, u
        assert "utm_content=video-1" in u, u
        print("selftest OK")
        return 0
    if not (a.base and a.campana):
        ap.error("indica --base y --campana")
    filas = []
    contenidos = [c for c in a.contenidos.split(",") if c.strip()] or [None]
    for f in a.fuentes.split(","):
        fuente, _, medio = f.strip().partition(":")
        medio = medio or MEDIO_DEFECTO.get(fuente.lower(), "referral")
        for c in contenidos:
            filas.append({"fuente": fuente, "medio": medio, "campana": a.campana, "contenido": c or "",
                          "url": url_utm(a.base, fuente, medio, a.campana, c)})
    with open(a.salida, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["fuente", "medio", "campana", "contenido", "url"])
        w.writeheader()
        w.writerows(filas)
    for f in filas:
        print(f["url"])
    print(f"\n{len(filas)} enlaces → {a.salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
