#!/usr/bin/env python3
"""Busca locales en OpenStreetMap (Nominatim + Overpass) por zona y tipo. Gratis y sin clave.

Tipos predefinidos (se pueden combinar): clubs, bares_musica, cocteleria, beach, rooftop, eventos,
bodas, hoteles, bares, restaurantes, musica_en_vivo.

OSM es colaborativo: suele faltar parte de los locales y algunos datos están desactualizados.
Úsalo como esqueleto y completa con búsqueda web, directorios y Google Maps.
Respeta la política de uso: 1 petición por segundo a Nominatim y consultas razonables a Overpass.

Ejemplos:
  python3 buscar_locales_osm.py --zona "Girona" --tipos clubs,bares_musica,beach --salida osm_girona.csv
  python3 buscar_locales_osm.py --zona "Barcelona" --tipos clubs,rooftop,cocteleria
  python3 buscar_locales_osm.py --bbox 41.9,2.7,42.1,3.3 --tipos bodas,eventos
  python3 buscar_locales_osm.py --selftest
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import ErrorRed, avisar, escribir_csv, obtener, obtener_json  # noqa: E402

NOMINATIM = "https://nominatim.openstreetmap.org/search"
OVERPASS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter"]

NOMBRES_BODAS = "^(mas |masia|masía|finca|castell|castillo|can |cal |hacienda|celler)"
TIPOS = {
    "clubs": ['nwr["amenity"="nightclub"]'],
    "bares_musica": ['nwr["amenity"~"^(bar|pub)$"]["live_music"="yes"]',
                     'nwr["amenity"~"^(bar|pub)$"]["name"~"club|music|lounge|dj|vinyl|vinilo",i]'],
    "cocteleria": ['nwr["amenity"="bar"]["name"~"cocktail|coctel|cóctel|còctel|gin|mixolog",i]',
                   'nwr["amenity"="bar"]["cocktails"="yes"]'],
    "beach": ['nwr["amenity"~"^(bar|restaurant|nightclub|pub)$"]["name"~"beach|chiringuito|playa|platja|sunset",i]',
              'nwr["leisure"="beach_resort"]'],
    "rooftop": ['nwr["amenity"~"^(bar|restaurant)$"]["name"~"rooftop|terrat|terraza|terrassa|sky",i]',
                'nwr["rooftop"="yes"]'],
    "eventos": ['nwr["amenity"="events_venue"]', 'nwr["amenity"="conference_centre"]'],
    "bodas": [f'nwr["amenity"~"^(events_venue|restaurant)$"]["name"~"{NOMBRES_BODAS}",i]',
              f'nwr["tourism"~"^(hotel|guest_house|chalet)$"]["name"~"{NOMBRES_BODAS}",i]',
              'nwr["amenity"="events_venue"]'],
    "hoteles": ['nwr["tourism"="hotel"]'],
    "bares": ['nwr["amenity"~"^(bar|pub)$"]'],
    "restaurantes": ['nwr["amenity"="restaurant"]'],
    "musica_en_vivo": ['nwr["live_music"="yes"]'],
}


def area_de_zona(zona, pausa=1.1):
    """Devuelve ('area', id) o ('bbox', (s, w, n, e)) a partir de un nombre de lugar."""
    res = obtener_json(NOMINATIM, {"q": zona, "format": "json", "limit": 5, "accept-language": "es"}, pausa=pausa)
    if not res:
        raise ErrorRed(f"Nominatim no encontró «{zona}». Prueba con otro nombre o usa --bbox.")
    for r in res:
        if r.get("osm_type") == "relation":
            return "area", 3600000000 + int(r["osm_id"]), r.get("display_name", "")
    s, n, w, e = (float(x) for x in res[0]["boundingbox"])
    return "bbox", (s, w, n, e), res[0].get("display_name", "")


def construir_consulta(tipos, ambito):
    clase, valor = ambito
    filtros = []
    for t in tipos:
        for f in TIPOS[t]:
            filtros.append(f + ("(area.a);" if clase == "area" else f"({valor[0]},{valor[1]},{valor[2]},{valor[3]});"))
    cabecera = "[out:json][timeout:180];"
    if clase == "area":
        cabecera += f"area(id:{valor})->.a;"
    return cabecera + "(" + "".join(filtros) + ");out center tags;"


def primero(tags, *claves):
    for c in claves:
        if tags.get(c):
            return tags[c]
    return ""


def parse_overpass(datos, tipos_txt):
    filas, vistos = [], set()
    for el in datos.get("elements", []):
        clave = f"{el.get('type')}/{el.get('id')}"
        if clave in vistos:
            continue
        vistos.add(clave)
        t = el.get("tags", {})
        if not t.get("name"):
            continue
        lat = el.get("lat") or (el.get("center") or {}).get("lat")
        lon = el.get("lon") or (el.get("center") or {}).get("lon")
        calle = " ".join(x for x in (t.get("addr:street", ""), t.get("addr:housenumber", "")) if x)
        filas.append({
            "nombre": t.get("name", ""),
            "segmento": tipos_txt,
            "subtipo": primero(t, "amenity", "tourism", "leisure"),
            "direccion": calle,
            "municipio": primero(t, "addr:city", "addr:town", "addr:village"),
            "cp": t.get("addr:postcode", ""),
            "lat": lat, "lon": lon,
            "web": primero(t, "website", "contact:website", "url"),
            "email": primero(t, "email", "contact:email"),
            "telefono": primero(t, "phone", "contact:phone", "contact:mobile"),
            "instagram": primero(t, "contact:instagram", "instagram"),
            "otras_redes": primero(t, "contact:facebook", "facebook"),
            "horario": t.get("opening_hours", ""),
            "aforo": t.get("capacity", ""),
            "estilo": primero(t, "music", "music:genre"),
            "osm_url": f"https://www.openstreetmap.org/{el.get('type')}/{el.get('id')}",
            "fuentes": "OpenStreetMap",
        })
    filas.sort(key=lambda f: (f["municipio"], f["nombre"]))
    return filas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zona", help="Municipio, comarca, provincia o comunidad (p. ej. 'Girona', 'Baix Empordà', 'Catalunya')")
    ap.add_argument("--bbox", help="sur,oeste,norte,este (alternativa a --zona)")
    ap.add_argument("--tipos", default="clubs", help="Lista separada por comas: " + ", ".join(TIPOS))
    ap.add_argument("--salida", default="osm_locales.csv")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    tipos = [t.strip() for t in a.tipos.split(",") if t.strip()]
    malos = [t for t in tipos if t not in TIPOS]
    if malos:
        ap.error(f"tipos desconocidos: {malos}. Disponibles: {', '.join(TIPOS)}")
    try:
        if a.bbox:
            s, w, n, e = (float(x) for x in a.bbox.split(","))
            ambito, nombre = ("bbox", (s, w, n, e)), a.bbox
        elif a.zona:
            clase, valor, nombre = area_de_zona(a.zona)
            ambito = (clase, valor)
        else:
            ap.error("indica --zona o --bbox")
        consulta = construir_consulta(tipos, ambito)
        datos, ultimo = None, None
        for servidor in OVERPASS:
            try:
                datos = json.loads(obtener(servidor, {"data": consulta}, timeout=200, reintentos=1))
                break
            except (ErrorRed, json.JSONDecodeError) as e:
                ultimo = e
        if datos is None:
            raise ErrorRed(f"Overpass no respondió: {ultimo}")
    except ErrorRed as e:
        avisar(f"[error] {e}")
        return 2
    filas = parse_overpass(datos, ",".join(tipos))
    columnas = ["nombre", "segmento", "subtipo", "direccion", "municipio", "cp", "lat", "lon", "web", "email",
                "telefono", "instagram", "otras_redes", "horario", "aforo", "estilo", "osm_url", "fuentes"]
    escribir_csv(a.salida, filas, columnas)
    con_web = sum(1 for f in filas if f["web"])
    con_contacto = sum(1 for f in filas if f["email"] or f["telefono"] or f["instagram"])
    print(f"Zona: {nombre}\nTipos: {', '.join(tipos)}\nLocales: {len(filas)} · con web: {con_web} · con algún contacto: {con_contacto}")
    for f in filas[:25]:
        print(f"  - {f['nombre']} ({f['subtipo']}, {f['municipio'] or '¿municipio?'}) {f['web']}")
    print(f"\nCSV: {a.salida}  ·  Datos © colaboradores de OpenStreetMap (ODbL). Completa con otras fuentes.")
    return 0


def selftest():
    q = construir_consulta(["clubs", "beach"], ("area", 3600349053))
    assert q.startswith("[out:json]") and "area(id:3600349053)->.a;" in q and '["amenity"="nightclub"](area.a);' in q
    qb = construir_consulta(["clubs"], ("bbox", (41.9, 2.7, 42.1, 3.3)))
    assert '(41.9,2.7,42.1,3.3);' in qb
    datos = {"elements": [
        {"type": "node", "id": 1, "lat": 41.98, "lon": 2.82, "tags": {"name": "Sala Prueba", "amenity": "nightclub",
         "addr:street": "Carrer Major", "addr:housenumber": "5", "addr:city": "Girona", "website": "https://sala.example",
         "contact:instagram": "https://instagram.com/sala", "capacity": "400"}},
        {"type": "way", "id": 2, "center": {"lat": 42.0, "lon": 3.1}, "tags": {"name": "Beach Test", "amenity": "bar", "phone": "+34 972 000 000"}},
        {"type": "node", "id": 1, "lat": 41.98, "lon": 2.82, "tags": {"name": "Sala Prueba", "amenity": "nightclub"}},
        {"type": "node", "id": 3, "tags": {"amenity": "bar"}},
    ]}
    f = parse_overpass(datos, "clubs,beach")
    assert len(f) == 2, f
    sala = [x for x in f if x["nombre"] == "Sala Prueba"][0]
    assert sala["direccion"] == "Carrer Major 5" and sala["aforo"] == "400" and sala["instagram"].endswith("/sala")
    beach = [x for x in f if x["nombre"] == "Beach Test"][0]
    assert beach["lat"] == 42.0 and beach["telefono"] == "+34 972 000 000"
    print("selftest OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
