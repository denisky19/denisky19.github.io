#!/usr/bin/env python3
"""CRM en CSV para prospección: unir fuentes, puntuar, agenda de seguimientos y resumen del embudo.

Subcomandos:
  unir     a.csv b.csv … --salida cuentas.csv   Une y desduplica (por dominio web o nombre+municipio)
  puntuar  cuentas.csv [--salida otro.csv]       Calcula puntuación y prioridad A/B/C (referencias/puntuacion-cuentas.md)
  agenda   cuentas.csv [--fecha AAAA-MM-DD]      Seguimientos de hoy y vencidos
  resumen  cuentas.csv                           Embudo por segmento, prioridad y estado

Ejemplo:
  python3 crm.py unir osm.csv busqueda.csv --salida cuentas.csv && python3 crm.py puntuar cuentas.csv
  python3 crm.py --selftest
"""

import argparse
import csv
import datetime as dt
import os
import re
import sys
import unicodedata
import urllib.parse

COLUMNAS = ("id,nombre,segmento,subtipo,municipio,comarca,provincia,direccion,web,email,telefono,instagram,otras_redes,"
            "decisor_cargo,decisor_nombre_publico,aforo,estilo,actividad_reciente,promotoras_residentes,via_acceso,"
            "contacto_calido,encaje,actividad,valor,accesibilidad,puntuacion,prioridad,estado,ultimo_contacto,"
            "siguiente_paso,fecha_siguiente_paso,notas,fuentes,verificado").split(",")
ESTADOS = ["nuevo", "investigado", "contactado", "respondio", "reunion", "propuesta", "piloto", "ganado", "perdido", "mas_adelante"]
PESOS = {"encaje": 0.35, "actividad": 0.25, "valor": 0.25, "accesibilidad": 0.15}
MULTIVALOR = ("email", "telefono", "otras_redes", "fuentes", "notas")


def leer(ruta):
    with open(ruta, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def escribir(ruta, filas):
    extra = [c for f in filas for c in f.keys() if c not in COLUMNAS]
    columnas = COLUMNAS + list(dict.fromkeys(extra))
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columnas, extrasaction="ignore")
        w.writeheader()
        for fila in filas:
            w.writerow({c: fila.get(c, "") for c in columnas})


def norm(t):
    t = "".join(c for c in unicodedata.normalize("NFD", (t or "").lower()) if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def clave(fila):
    web = (fila.get("web") or "").strip().lower()
    if web:
        host = urllib.parse.urlparse(web if "://" in web else "https://" + web).netloc.replace("www.", "")
        if host and not any(s in host for s in ("instagram.", "facebook.", "linktr.ee", "google.", "bodas.net")):
            return "dom:" + host
    return "nom:" + norm(fila.get("nombre")) + "|" + norm(fila.get("municipio"))


def fusionar(a, b):
    for k, v in b.items():
        v = (v or "").strip()
        if not v:
            continue
        actual = (a.get(k) or "").strip()
        if not actual:
            a[k] = v
        elif k in MULTIVALOR:
            partes = [p.strip() for p in re.split(r"[;|]", actual) if p.strip()]
            for p in re.split(r"[;|]", v):
                if p.strip() and p.strip().lower() not in (x.lower() for x in partes):
                    partes.append(p.strip())
            a[k] = "; ".join(partes)
    return a


def unir(rutas):
    cuentas = {}
    for ruta in rutas:
        for fila in leer(ruta):
            if not (fila.get("nombre") or "").strip():
                continue
            c = clave(fila)
            if c in cuentas:
                fusionar(cuentas[c], fila)
            else:
                cuentas[c] = dict(fila)
    filas = list(cuentas.values())
    for i, f in enumerate(sorted(filas, key=lambda x: (x.get("segmento", ""), x.get("municipio", ""), x.get("nombre", ""))), 1):
        f["id"] = f.get("id") or f"C{i:04d}"
        f["estado"] = f.get("estado") or "nuevo"
    return filas


def num(v):
    try:
        x = float(str(v).replace(",", "."))
        return x if 1 <= x <= 5 else None
    except (TypeError, ValueError):
        return None


def puntuar(filas):
    for f in filas:
        vals = {k: num(f.get(k)) for k in PESOS}
        if any(v is None for v in vals.values()):
            f["puntuacion"], f["prioridad"] = "", f.get("prioridad", "") or "sin_puntuar"
            continue
        p = round(sum(vals[k] * w for k, w in PESOS.items()), 2)
        f["puntuacion"] = f"{p:.2f}"
        f["prioridad"] = "C" if vals["encaje"] <= 2 else ("A" if p >= 4.0 else "B" if p >= 3.0 else "C")
    return filas


def agenda(filas, fecha):
    pendientes = []
    for f in filas:
        if f.get("estado") in ("ganado", "perdido"):
            continue
        d = (f.get("fecha_siguiente_paso") or "").strip()
        try:
            fd = dt.date.fromisoformat(d) if d else None
        except ValueError:
            fd = None
        if fd and fd <= fecha:
            pendientes.append((fd, f))
    return sorted(pendientes, key=lambda x: (x[0], x[1].get("prioridad", "Z")))


def resumen(filas):
    L = [f"Cuentas: {len(filas)}"]
    por = {}
    for f in filas:
        por.setdefault(f.get("segmento") or "(sin segmento)", []).append(f)
    L.append("\n| Segmento | Total | A | B | C | Contactadas | Respondieron | Reunión+ | Ganadas |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    avanzados = {"reunion", "propuesta", "piloto", "ganado"}
    for seg, fs in sorted(por.items()):
        cont = [f for f in fs if f.get("estado") not in ("", "nuevo", "investigado")]
        resp = [f for f in fs if f.get("estado") in {"respondio"} | avanzados]
        L.append(f"| {seg} | {len(fs)} | {sum(f.get('prioridad') == 'A' for f in fs)} | {sum(f.get('prioridad') == 'B' for f in fs)} | "
                 f"{sum(f.get('prioridad') == 'C' for f in fs)} | {len(cont)} | {len(resp)} | "
                 f"{sum(f.get('estado') in avanzados for f in fs)} | {sum(f.get('estado') == 'ganado' for f in fs)} |")
    cont = sum(f.get("estado") not in ("", "nuevo", "investigado") for f in filas)
    resp = sum(f.get("estado") in {"respondio"} | avanzados for f in filas)
    if cont:
        L.append(f"\nTasa de respuesta: {resp / cont * 100:.0f} % ({resp}/{cont})")
    sin_contacto = sum(not (f.get("email") or f.get("telefono") or f.get("instagram")) for f in filas)
    L.append(f"Sin ningún canal de contacto todavía: {sin_contacto}")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    u = sub.add_parser("unir"); u.add_argument("csvs", nargs="+"); u.add_argument("--salida", default="cuentas.csv")
    p = sub.add_parser("puntuar"); p.add_argument("csv"); p.add_argument("--salida")
    g = sub.add_parser("agenda"); g.add_argument("csv"); g.add_argument("--fecha")
    r = sub.add_parser("resumen"); r.add_argument("csv")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd == "unir":
        filas = unir(a.csvs)
        escribir(a.salida, filas)
        print(f"{len(filas)} cuentas únicas → {a.salida}")
    elif a.cmd == "puntuar":
        filas = puntuar(leer(a.csv))
        escribir(a.salida or a.csv, filas)
        cuenta = {k: sum(f.get("prioridad") == k for f in filas) for k in ("A", "B", "C", "sin_puntuar")}
        print(f"Prioridades: {cuenta} → {a.salida or a.csv}")
    elif a.cmd == "agenda":
        fecha = dt.date.fromisoformat(a.fecha) if a.fecha else dt.date.today()
        pend = agenda(leer(a.csv), fecha)
        print(f"Seguimientos hasta {fecha}: {len(pend)}")
        for fd, f in pend:
            vencido = " (VENCIDO)" if fd < fecha else ""
            print(f"- {fd}{vencido} [{f.get('prioridad', '')}] {f.get('nombre')} · {f.get('siguiente_paso')} · {f.get('via_acceso') or f.get('email') or f.get('instagram') or f.get('telefono')}")
    elif a.cmd == "resumen":
        print(resumen(leer(a.csv)))
    else:
        ap.print_help()
        return 1
    return 0


def selftest():
    import tempfile
    d = tempfile.mkdtemp()
    a, b = os.path.join(d, "a.csv"), os.path.join(d, "b.csv")
    with open(a, "w", encoding="utf-8") as f:
        f.write("nombre,municipio,web,email,fuentes,segmento\nSala Uno,Girona,https://www.salauno.es,info@salauno.es,OSM,clubs\nBar Dos,Roses,,,OSM,bares\n")
    with open(b, "w", encoding="utf-8") as f:
        f.write("nombre,municipio,web,email,fuentes,segmento,encaje,actividad,valor,accesibilidad,estado,fecha_siguiente_paso\n"
                "SALA UNO,Girona,salauno.es/contacto,booking@salauno.es,web,clubs,5,5,4,4,contactado,2026-01-10\n"
                "Bar Dos,Roses,,,búsqueda,bares,2,5,5,5,nuevo,\n"
                "Finca Tres,Pals,,,bodas.net,bodas,4,3,3,2,respondio,2026-01-20\n")
    filas = unir([a, b])
    assert len(filas) == 3, [f["nombre"] for f in filas]
    sala = [f for f in filas if f["nombre"] == "Sala Uno"][0]
    assert sala["email"] == "info@salauno.es; booking@salauno.es" and sala["fuentes"] == "OSM; web" and sala["id"].startswith("C")
    puntuar(filas)
    assert sala["puntuacion"] == "4.60" and sala["prioridad"] == "A"
    bar = [f for f in filas if f["nombre"] == "Bar Dos"][0]
    assert bar["prioridad"] == "C"  # encaje ≤ 2
    finca = [f for f in filas if f["nombre"] == "Finca Tres"][0]
    assert finca["prioridad"] == "B" and finca["puntuacion"] == "3.20"
    pend = agenda(filas, dt.date(2026, 1, 15))
    assert [f["nombre"] for _, f in pend] == ["Sala Uno"]
    texto = resumen(filas)
    assert "Tasa de respuesta: 50 %" in texto, texto
    salida = os.path.join(d, "c.csv")
    escribir(salida, filas)
    assert leer(salida)[0].keys() >= set(COLUMNAS)
    print("selftest OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
