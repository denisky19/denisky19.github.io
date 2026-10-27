#!/usr/bin/env python3
"""Extrae contactos PÚBLICOS de la web de cada cuenta: emails, teléfonos, redes, razón social y CIF.

Lee la portada y hasta N páginas de contacto, booking, eventos, bodas o aviso legal enlazadas desde ella.
Solo recoge datos publicados por la propia empresa. Revisa el resultado antes de usarlo.

Ejemplos:
  python3 extraer_contactos.py https://venue1.es https://venue2.com
  python3 extraer_contactos.py --csv cuentas.csv --salida cuentas_enriquecidas.csv   (usa la columna 'web')
  python3 extraer_contactos.py --selftest
"""

import argparse
import csv
import html as htmlmod
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import ErrorRed, avisar, escribir_csv, obtener  # noqa: E402

CLAVES_PAGINA = ["contact", "contacte", "contacto", "booking", "reserv", "event", "boda", "casament", "wedding",
                 "aviso-legal", "avis-legal", "legal", "privacidad", "privacitat", "nosotros", "about", "qui-som",
                 "quienes-somos", "empresa", "info"]
RE_EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
RE_EMAIL_OFUSCADO = re.compile(r"([A-Za-z0-9._%+\-]+)\s*(?:\[at\]|\(at\)| at |\[arroba\]|\(arroba\))\s*([A-Za-z0-9.\-]+)\s*(?:\[dot\]|\(dot\)| dot |\.)\s*([A-Za-z]{2,})", re.I)
RE_TEL = re.compile(r"(?:\+34[\s.\-]?)?(?:[6789]\d{2})[\s.\-]?\d{2,3}[\s.\-]?\d{2,3}[\s.\-]?\d{0,3}")
RE_CIF = re.compile(r"\b(?:CIF|NIF|N\.I\.F\.|C\.I\.F\.)?\s*[:\-]?\s*([ABCDEFGHJNPQRSUVW][\-\s]?\d{7}[0-9A-J]|\d{8}[A-Z])\b")
RE_RAZON = re.compile(r"(?:raz[oó]n social|titular|denominaci[oó]n social|ra[oó] social|empresa titular)\s*[:\-]?\s*([^\n<|]{3,90})", re.I)
RE_SOCIEDAD = re.compile(r"\b([A-ZÁÉÍÓÚÑÇ][\w&ÁÉÍÓÚÑÇáéíóúñç'·.\- ]{2,70}?,?\s+(?:S\.?L\.?U?\.?|S\.?A\.?U?\.?|S\.?C\.?P\.?|S\.?COOP\.?))(?=[\s,.;)]|$)")
REDES = {"instagram": "instagram.com/", "facebook": "facebook.com/", "tiktok": "tiktok.com/@",
         "linkedin": "linkedin.com/", "youtube": "youtube.com/", "whatsapp": "wa.me/"}
EMAIL_BASURA = ("example.", "sentry", "wixpress", "@2x", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
                "domain.com", "email.com", "tu@", "your@", "usuario@", "name@")


def limpiar_tel(t):
    d = re.sub(r"\D", "", t)
    if d.startswith("34") and len(d) == 11:
        d = d[2:]
    return d if len(d) == 9 and d[0] in "6789" else None


def extraer(html_texto, url_base):
    texto = htmlmod.unescape(re.sub(r"<[^>]+>", " ", html_texto))
    emails, tels, redes, enlaces = set(), set(), {}, []
    for m in re.finditer(r'href=["\']([^"\']+)["\']', html_texto, re.I):
        href = htmlmod.unescape(m.group(1)).strip()
        bajo = href.lower()
        if bajo.startswith("mailto:"):
            emails.add(urllib.parse.unquote(href[7:].split("?")[0]).strip().lower())
        elif bajo.startswith("tel:"):
            t = limpiar_tel(href[4:])
            if t:
                tels.add(t)
        else:
            absoluto = urllib.parse.urljoin(url_base, href)
            for red, patron in REDES.items():
                if patron in absoluto.lower() and red not in redes and "share" not in absoluto.lower():
                    redes[red] = absoluto.split("?")[0]
            enlaces.append(absoluto)
    for e in RE_EMAIL.findall(texto):
        emails.add(e.lower().rstrip("."))
    for u, d, tld in RE_EMAIL_OFUSCADO.findall(texto):
        emails.add(f"{u}@{d}.{tld}".lower())
    for t in RE_TEL.findall(texto):
        lt = limpiar_tel(t)
        if lt:
            tels.add(lt)
    emails = {e for e in emails if not any(b in e for b in EMAIL_BASURA)}
    cifs = {re.sub(r"[\-\s]", "", c) for c in RE_CIF.findall(texto) if not c.isdigit()}
    razon = ""
    m = RE_RAZON.search(texto)
    if m:
        razon = re.split(r"\s*(?:·|\||\bN\.?I\.?F\b|\bC\.?I\.?F\b|\bcon domicilio\b|\s-\s|—)", m.group(1), flags=re.I)[0].strip(" .,:;")
    else:
        m = RE_SOCIEDAD.search(texto)
        if m:
            razon = m.group(1).strip(" ,")
    return {"emails": emails, "telefonos": tels, "redes": redes, "cifs": cifs, "razon_social": razon, "enlaces": enlaces}


def paginas_candidatas(enlaces, url_base, maximo):
    dominio = urllib.parse.urlparse(url_base).netloc.replace("www.", "")
    vistas, res = set(), []
    for u in enlaces:
        p = urllib.parse.urlparse(u)
        if dominio not in p.netloc or p.scheme not in ("http", "https"):
            continue
        ruta = p.path.lower()
        limpio = f"{p.scheme}://{p.netloc}{p.path}"
        if limpio in vistas or limpio.rstrip("/") == url_base.rstrip("/"):
            continue
        if any(k in ruta for k in CLAVES_PAGINA):
            vistas.add(limpio)
            res.append(limpio)
    prioridad = lambda u: min([i for i, k in enumerate(CLAVES_PAGINA) if k in u.lower()] or [99])  # noqa: E731
    return sorted(res, key=prioridad)[:maximo]


def analizar_sitio(url, max_paginas=4, pausa=0.6):
    if not re.match(r"^https?://", url):
        url = "https://" + url
    dominio = urllib.parse.urlparse(url).netloc.replace("www.", "")
    total = {"emails": set(), "telefonos": set(), "redes": {}, "cifs": set(), "razon_social": ""}
    revisadas, error = [], ""
    try:
        html = obtener(url, timeout=20, pausa=pausa)
    except ErrorRed as e:
        return {"web": url, "error": str(e)[:200]}
    r = extraer(html, url)
    revisadas.append(url)
    paginas = paginas_candidatas(r["enlaces"], url, max_paginas)
    resultados = [r]
    for p in paginas:
        try:
            resultados.append(extraer(obtener(p, timeout=20, pausa=pausa), p))
            revisadas.append(p)
        except ErrorRed as e:
            error = str(e)[:120]
    for x in resultados:
        total["emails"] |= x["emails"]
        total["telefonos"] |= x["telefonos"]
        total["cifs"] |= x["cifs"]
        for k, v in x["redes"].items():
            total["redes"].setdefault(k, v)
        if not total["razon_social"] and x["razon_social"]:
            total["razon_social"] = x["razon_social"]
    propios = sorted(e for e in total["emails"] if dominio.split(":")[0] in e)
    otros = sorted(e for e in total["emails"] if e not in propios)
    return {
        "web": url,
        "email": "; ".join(propios + otros),
        "telefono": "; ".join(sorted(total["telefonos"])),
        "instagram": total["redes"].get("instagram", ""),
        "otras_redes": "; ".join(v for k, v in total["redes"].items() if k != "instagram"),
        "razon_social": total["razon_social"],
        "cif": "; ".join(sorted(total["cifs"])),
        "paginas_revisadas": " | ".join(revisadas),
        "error": error,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--csv", help="CSV de cuentas con una columna de web")
    ap.add_argument("--columna", default="web")
    ap.add_argument("--salida", default="contactos.csv")
    ap.add_argument("--max-paginas", type=int, default=4)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    filas_entrada = []
    if a.csv:
        with open(a.csv, encoding="utf-8") as f:
            filas_entrada = list(csv.DictReader(f))
    filas_entrada += [{a.columna: u} for u in a.urls]
    if not filas_entrada:
        ap.error("indica URLs o --csv")
    salida = []
    for i, fila in enumerate(filas_entrada, 1):
        web = (fila.get(a.columna) or "").strip()
        if not web:
            salida.append(fila)
            continue
        r = analizar_sitio(web, a.max_paginas)
        nueva = dict(fila)
        for k, v in r.items():
            if k == "web":
                continue
            if v and not (nueva.get(k) or "").strip():
                nueva[k] = v
            elif v and k in ("email", "telefono") and v not in nueva.get(k, ""):
                nueva[k] = nueva[k] + "; " + v
        if r.get("error"):
            nueva["error"] = r["error"]
        nueva["fuentes"] = "; ".join(x for x in ((fila.get("fuentes") or ""), "web propia") if x)
        salida.append(nueva)
        print(f"[{i}/{len(filas_entrada)}] {web} → emails: {r.get('email') or '-'} · tel: {r.get('telefono') or '-'}" + (f" · ⚠ {r['error'][:80]}" if r.get("error") else ""))
    columnas = list(dict.fromkeys([c for f in salida for c in f.keys()] +
                                  ["email", "telefono", "instagram", "otras_redes", "razon_social", "cif", "paginas_revisadas", "error"]))
    escribir_csv(a.salida, salida, columnas)
    print(f"\nCSV: {a.salida} (revisa los datos antes de contactar; son datos publicados por cada empresa)")
    return 0


def selftest():
    html = """<html><body><a href="mailto:Booking@SalaTest.es?subject=hola">Booking</a>
    <a href="tel:+34 972 11 22 33">Llámanos</a><a href="/contacto">Contacto</a><a href="/aviso-legal/">Aviso legal</a>
    <a href="https://www.instagram.com/salatest/?hl=es">IG</a><a href="https://facebook.com/sharer.php?u=x">share</a>
    <p>Eventos: eventos [at] salatest [dot] es · WhatsApp 655 44 33 22 · logo@2x.png</p>
    <p>Titular: OCIO NOCTURNO TEST, S.L. — CIF: B-17123456</p></body></html>"""
    r = extraer(html, "https://salatest.es/")
    assert "booking@salatest.es" in r["emails"] and "eventos@salatest.es" in r["emails"], r["emails"]
    assert not any("2x" in e for e in r["emails"])
    assert r["telefonos"] == {"972112233", "655443322"}, r["telefonos"]
    assert r["redes"] == {"instagram": "https://www.instagram.com/salatest/"}, r["redes"]
    assert r["cifs"] == {"B17123456"}, r["cifs"]
    assert r["razon_social"].startswith("OCIO NOCTURNO TEST"), r["razon_social"]
    cand = paginas_candidatas(r["enlaces"], "https://salatest.es/", 4)
    assert cand == ["https://salatest.es/contacto", "https://salatest.es/aviso-legal/"], cand
    r2 = extraer("<p>Empresa: Masia Exemple SL, NIF B12345674</p>", "https://x.cat")
    assert r2["razon_social"].startswith("Masia Exemple SL") or r2["cifs"] == {"B12345674"}
    assert extraer("<p>Raó social: VENUE TEST SL · NIF B17000000</p>", "https://v.cat")["razon_social"] == "VENUE TEST SL"
    print("selftest OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
