#!/usr/bin/env python3
"""Genera el panel visual (informe.html) y el JSON consolidado para IAs (ia/estudio.json).

Lee los datos.json de cada carpeta del estudio, fuentes/fuentes.json y, si existen,
06-viabilidad/modelo.json y 10-veredicto/puntuacion-resultado.json.

Ejemplo:
  python3 generar_informe.py estudios/cafeteria-de-especialidad
"""

import argparse
import datetime as dt
import html
import json
import os
import re
import sys

CARPETAS = [
    ("00-brief", "brief", "Brief"),
    ("01-mercado", "mercado", "Mercado"),
    ("02-cliente", "cliente", "Cliente"),
    ("03-palabras-clave", "palabras_clave", "Palabras clave"),
    ("04-competencia", "competencia", "Competencia"),
    ("05-estrategia", "estrategia", "Estrategia"),
    ("06-viabilidad", "viabilidad", "Viabilidad"),
    ("07-marketing-ventas", "marketing_ventas", "Marketing y ventas"),
    ("08-producto-distribucion", "producto_distribucion", "Producto y distribución"),
    ("09-legal", "legal", "Legal"),
    ("10-veredicto", "veredicto", "Veredicto"),
]


def leer_json(ruta, defecto=None):
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return defecto
    except json.JSONDecodeError as e:
        print(f"[aviso] JSON inválido en {ruta}: {e}", file=sys.stderr)
        return defecto


def e(x):
    return html.escape("" if x is None else str(x))


def url_segura(u):
    return u if isinstance(u, str) and re.match(r"^https?://", u) else ""


def texto_item(x):
    if isinstance(x, dict):
        t = x.get("texto") or x.get("descripcion") or x.get("nombre") or json.dumps(x, ensure_ascii=False)
        ev = x.get("evidencia") or x.get("fuentes")
        return f"{t} ({', '.join(ev)})" if ev else t
    return str(x)


def num(v, dec=0, sufijo=""):
    if v is None or v == "":
        return "—"
    if isinstance(v, (int, float)):
        s = f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return s + sufijo
    return str(v)


def valor_metrica(m):
    if isinstance(m, dict):
        v = m.get("valor")
        u = m.get("unidad", "")
        if isinstance(v, (int, float)):
            if abs(v) >= 1e6:
                return f"{num(v / 1e6, 1)} M {u.replace('EUR', '€')}".strip()
            return f"{num(v)} {u.replace('EUR', '€')}".strip()
        return "—" if v is None else str(v)
    return num(m) if isinstance(m, (int, float)) else (str(m) if m else "—")


def cargar(raiz):
    modulos = {}
    for carpeta, clave, _ in CARPETAS:
        d = leer_json(os.path.join(raiz, carpeta, "datos.json"), {}) or {}
        modulos[clave] = d
    modelo = leer_json(os.path.join(raiz, "06-viabilidad", "modelo.json"))
    if modelo:
        modulos["viabilidad"].setdefault("modelo", modelo)
    punt = leer_json(os.path.join(raiz, "10-veredicto", "puntuacion-resultado.json"))
    if punt:
        met = modulos["veredicto"].setdefault("metricas", {})
        for k, v in punt.items():
            met.setdefault(k, v)
    fuentes = leer_json(os.path.join(raiz, "fuentes", "fuentes.json"), []) or []
    return modulos, fuentes


def nombre_idea(raiz, modulos):
    idea = (modulos.get("brief", {}).get("metricas") or {}).get("idea")
    if idea:
        return idea
    try:
        with open(os.path.join(raiz, "00-brief", "brief.md"), encoding="utf-8") as f:
            m = re.match(r"#\s*Brief:\s*(.+)", f.readline())
            if m:
                return m.group(1).strip()
    except FileNotFoundError:
        pass
    return os.path.basename(os.path.normpath(raiz)).replace("-", " ").capitalize()


CSS = """
:root{--bg:#f7f7f5;--card:#fff;--text:#1d1d1f;--muted:#5f6368;--line:#e3e3e0;--accent:#2f5dd3;
--ok:#1e8e3e;--warn:#c98a00;--bad:#c5221f;--na:#80868b;--chip:#eef1f8}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141416;--card:#1e1f22;--text:#ececec;
--muted:#a0a4ab;--line:#33353a;--accent:#8ab4f8;--ok:#5bb974;--warn:#f2b84b;--bad:#f28b82;--na:#9aa0a6;--chip:#2a2d34}}
:root[data-theme="dark"]{--bg:#141416;--card:#1e1f22;--text:#ececec;--muted:#a0a4ab;--line:#33353a;--accent:#8ab4f8;
--ok:#5bb974;--warn:#f2b84b;--bad:#f28b82;--na:#9aa0a6;--chip:#2a2d34}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:1080px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:1.7rem;margin:0 0 4px}h2{font-size:1.2rem;margin:0 0 12px}h3{font-size:1rem;margin:0 0 6px}
.muted{color:var(--muted)}.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;margin:16px 0}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}.kpi b{display:block;font-size:1.25rem}
.kpi span{color:var(--muted);font-size:.85rem}
.verdict{display:flex;gap:16px;align-items:center;flex-wrap:wrap}.badge{font-size:2.4rem;line-height:1}
.score{font-size:2rem;font-weight:700}.pill{display:inline-block;background:var(--chip);border-radius:999px;padding:2px 10px;margin:2px;font-size:.85rem}
.bar{height:10px;background:var(--line);border-radius:6px;overflow:hidden}.bar i{display:block;height:100%}
.dims{display:grid;grid-template-columns:minmax(140px,1.2fr) 3fr 50px;gap:8px 12px;align-items:center}
.swot{display:grid;grid-template-columns:1fr 1fr;gap:12px}.swot div{border-radius:10px;padding:12px;border:1px solid var(--line)}
.swot .f{border-top:4px solid var(--ok)}.swot .d{border-top:4px solid var(--warn)}.swot .o{border-top:4px solid var(--accent)}.swot .a{border-top:4px solid var(--bad)}
table{width:100%;border-collapse:collapse;font-size:.9rem}th,td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:600}.scroll{overflow-x:auto}ul{margin:6px 0;padding-left:20px}
details{border-top:1px solid var(--line);padding:8px 0}summary{cursor:pointer;font-weight:600}
a{color:var(--accent)}.red{color:var(--bad)}.amber{color:var(--warn)}footer{color:var(--muted);font-size:.85rem;margin-top:32px}
.toggle{float:right;background:var(--chip);color:var(--text);border:1px solid var(--line);border-radius:8px;padding:4px 10px;cursor:pointer}
@media (max-width:640px){.swot{grid-template-columns:1fr}.dims{grid-template-columns:1fr 2fr 40px}h1{font-size:1.4rem}}
"""

JS = """
(function(){var b=document.getElementById('tema');if(!b)return;b.onclick=function(){var r=document.documentElement;
var oscuro=r.getAttribute('data-theme')==='dark'||(!r.getAttribute('data-theme')&&matchMedia('(prefers-color-scheme: dark)').matches);
r.setAttribute('data-theme',oscuro?'light':'dark');};})();
"""


def color(p):
    return "var(--ok)" if p >= 7 else "var(--warn)" if p >= 5 else "var(--bad)"


def seccion(titulo, cuerpo):
    return f'<section class="card"><h2>{e(titulo)}</h2>{cuerpo}</section>' if cuerpo else ""


def tabla(filas, columnas):
    if not filas:
        return ""
    cab = "".join(f"<th>{e(t)}</th>" for _, t in columnas)
    cuerpo = ""
    for f in filas:
        celdas = []
        for clave, _ in columnas:
            v = f.get(clave, "") if isinstance(f, dict) else ""
            if isinstance(v, list):
                v = "; ".join(texto_item(x) for x in v)
            if clave in ("url", "enlace") and url_segura(v):
                celdas.append(f'<td><a href="{e(v)}" rel="noopener">{e(v)}</a></td>')
            else:
                celdas.append(f"<td>{e(v)}</td>")
        cuerpo += "<tr>" + "".join(celdas) + "</tr>"
    return f'<div class="scroll"><table><thead><tr>{cab}</tr></thead><tbody>{cuerpo}</tbody></table></div>'


def lista(items):
    items = [x for x in (items or []) if x]
    return "<ul>" + "".join(f"<li>{e(texto_item(x))}</li>" for x in items) + "</ul>" if items else ""


def construir_html(raiz, modulos, fuentes):
    idea = nombre_idea(raiz, modulos)
    brief = modulos["brief"].get("metricas") or {}
    ver = modulos["veredicto"].get("metricas") or {}
    mer = modulos["mercado"].get("metricas") or {}
    via = modulos["viabilidad"].get("metricas") or {}
    modelo = modulos["viabilidad"].get("modelo") or {}
    comp = modulos["competencia"].get("metricas") or {}
    kw = modulos["palabras_clave"].get("metricas") or {}
    cli = modulos["cliente"].get("metricas") or {}
    est = modulos["estrategia"].get("metricas") or {}
    gtm = modulos["marketing_ventas"].get("metricas") or {}
    leg = modulos["legal"].get("metricas") or {}
    prod = modulos["producto_distribucion"].get("metricas") or {}
    partes = []

    meta = " · ".join(e(x) for x in (brief.get("arquetipo"), brief.get("ambito"), brief.get("cliente_tipo"),
                                        brief.get("modelo_ingresos")) if x)
    partes.append(f'<header><button class="toggle" id="tema" type="button">◐ Tema</button><h1>{e(idea)}</h1>'
                  f'<div class="muted">{meta}{" · " if meta else ""}Generado {dt.date.today().isoformat()}</div></header>')

    # Veredicto
    if ver.get("puntuacion_total") is not None:
        dims = "".join(
            f'<div>{e(d["nombre"])} <span class="muted">({e(d.get("confianza", ""))})</span></div>'
            f'<div class="bar"><i style="width:{float(d["puntuacion"]) * 10:.0f}%;background:{color(float(d["puntuacion"]))}"></i></div>'
            f'<div><b>{num(d["puntuacion"], 1)}</b></div>' for d in ver.get("dimensiones", []))
        flags = ""
        if ver.get("evidencia_insuficiente"):
            flags += '<span class="pill">⚪ Evidencia insuficiente</span>'
        for r in ver.get("reglas_aplicadas", []):
            flags += f'<span class="pill">{e(r)}</span>'
        cuerpo = (f'<div class="verdict"><div class="badge">{e(ver.get("emoji", ""))}</div><div>'
                  f'<div class="score">{num(ver["puntuacion_total"], 1)}/10</div>'
                  f'<div>{e(ver.get("veredicto_texto", ver.get("veredicto", "")))}</div></div></div>'
                  f'<p>{flags}</p><div class="dims">{dims}</div>')
        for campo, titulo in (("argumento_a_favor", "A favor"), ("argumento_en_contra", "En contra"),
                              ("que_cambiaria_el_veredicto", "Qué lo cambiaría")):
            if ver.get(campo):
                cuerpo += f"<p><b>{titulo}:</b> {e(ver[campo])}</p>"
        partes.append(seccion("Veredicto", cuerpo))
    elif modulos["veredicto"].get("resumen"):
        partes.append(seccion("Veredicto", f"<p>{e(modulos['veredicto']['resumen'])}</p>"))

    # Cifras clave
    base = (modelo.get("escenarios") or {}).get("base") or {}
    kpis = [
        ("Mercado total (TAM)", valor_metrica(mer.get("tam")) if mer.get("tam") else None),
        ("Mercado alcanzable (SAM)", valor_metrica(mer.get("sam")) if mer.get("sam") else None),
        ("Mercado obtenible (SOM)", valor_metrica(mer.get("som")) if mer.get("som") else None),
        ("Fase del mercado", mer.get("fase_mercado")),
        ("Demanda en buscadores", kw.get("demanda_consciente")),
        ("Intensidad competitiva", comp.get("intensidad_competitiva")),
        ("Inversión inicial", num(via.get("inversion_inicial") or modelo.get("inversion_inicial"), 0, " €") if (via.get("inversion_inicial") or modelo.get("inversion_inicial")) else None),
        ("Margen de contribución", num(via.get("margen_contribucion_pct") or base.get("margen_contribucion_pct"), 1, " %") if (via.get("margen_contribucion_pct") or base.get("margen_contribucion_pct")) else None),
        ("Punto de equilibrio /mes", num(via.get("punto_equilibrio_ingresos_mes") or base.get("punto_equilibrio_ingresos_mes"), 0, " €") if (via.get("punto_equilibrio_ingresos_mes") or base.get("punto_equilibrio_ingresos_mes")) else None),
        ("Mes de equilibrio (base)", (via.get("mes_equilibrio") or {}).get("base") or base.get("mes_equilibrio_operativo")),
        ("Financiación necesaria (base)", num((via.get("necesidad_financiacion") or {}).get("base") or base.get("necesidad_financiacion"), 0, " €") if ((via.get("necesidad_financiacion") or {}).get("base") or base.get("necesidad_financiacion")) else None),
        ("Complejidad legal", leg.get("nivel_complejidad")),
    ]
    kp = "".join(f'<div class="kpi"><span>{e(t)}</span><b>{e(v)}</b></div>' for t, v in kpis if v not in (None, "", "—"))
    partes.append(seccion("Cifras clave", f'<div class="grid">{kp}</div>' if kp else ""))

    # Resúmenes por módulo
    res = ""
    for carpeta, clave, titulo in CARPETAS:
        d = modulos.get(clave) or {}
        if not (d.get("resumen") or d.get("banderas_rojas") or d.get("banderas_amarillas")):
            continue
        conf = f' <span class="muted">· confianza {e(d.get("confianza"))}</span>' if d.get("confianza") else ""
        cuerpo = f"<p>{e(d.get('resumen', ''))}</p>"
        if d.get("banderas_rojas"):
            cuerpo += '<div class="red"><b>🚩 Banderas rojas</b></div>' + lista(d["banderas_rojas"])
        if d.get("banderas_amarillas"):
            cuerpo += '<div class="amber"><b>⚠️ Banderas amarillas</b></div>' + lista(d["banderas_amarillas"])
        if d.get("implicacion_decision"):
            cuerpo += f"<p><b>Para tu decisión:</b> {e(d['implicacion_decision'])}</p>"
        enlace = f' · <a href="{e(carpeta)}/">abrir carpeta</a>'
        res += f"<details><summary>{e(titulo)}{conf}</summary>{cuerpo}<p class='muted'>{enlace}</p></details>"
    partes.append(seccion("Resumen por área", res))

    # DAFO
    dafo = est.get("dafo") or {}
    if any(dafo.get(k) for k in ("fortalezas", "debilidades", "oportunidades", "amenazas")):
        cuerpo = (f'<div class="swot"><div class="f"><h3>Fortalezas</h3>{lista(dafo.get("fortalezas"))}</div>'
                  f'<div class="d"><h3>Debilidades</h3>{lista(dafo.get("debilidades"))}</div>'
                  f'<div class="o"><h3>Oportunidades</h3>{lista(dafo.get("oportunidades"))}</div>'
                  f'<div class="a"><h3>Amenazas</h3>{lista(dafo.get("amenazas"))}</div></div>')
        if est.get("estrategia_principal"):
            cuerpo += f"<p><b>Estrategia principal:</b> {e(est['estrategia_principal'])}</p>"
        if est.get("propuesta_valor"):
            cuerpo += f"<p><b>Propuesta de valor:</b> {e(est['propuesta_valor'])}</p>"
        partes.append(seccion("DAFO", cuerpo))

    # Cliente
    personas = cli.get("personas") or []
    cuerpo = ""
    if cli.get("segmento_principal"):
        cuerpo += f"<p><b>Segmento principal:</b> {e(cli['segmento_principal'])}</p>"
    if personas:
        cuerpo += '<div class="grid">' + "".join(
            f'<div class="kpi"><h3>{e(p.get("nombre"))}</h3><div>{e(p.get("descripcion"))}</div>'
            + (f'<div class="muted"><b>JTBD:</b> {e(p.get("jtbd"))}</div>' if p.get("jtbd") else "")
            + (f'<div><b>Dolores:</b>{lista(p.get("dolores"))}</div>' if p.get("dolores") else "")
            + (f'<div class="muted"><b>Dónde está:</b> {e(", ".join(map(str, p.get("canales", []))))}</div>' if p.get("canales") else "")
            + "</div>" for p in personas) + "</div>"
    citas = cli.get("citas") or []
    if citas:
        cuerpo += "<h3>Lo que dicen (literal)</h3><ul>" + "".join(
            f'<li>«{e(c.get("texto"))}» <span class="muted">{e(c.get("fuente", ""))} {e(c.get("fecha", ""))}</span></li>' for c in citas[:10]) + "</ul>"
    partes.append(seccion("Cliente", cuerpo))

    # Competencia
    comps = comp.get("competidores") or []
    cuerpo = tabla(comps, [("nombre", "Nombre"), ("tipo", "Tipo"), ("precio", "Precio"), ("tamano", "Tamaño"),
                           ("valoracion", "Valoración"), ("fortalezas", "Fortalezas"), ("debilidades", "Debilidades"), ("url", "Web")])
    if comp.get("hueco"):
        cuerpo += f"<p><b>Hueco:</b> {e(comp['hueco'])}</p>"
    partes.append(seccion("Competencia", cuerpo))

    # Keywords
    kws = sorted(kw.get("keywords") or [], key=lambda k: (k.get("prioridad") is None, k.get("prioridad") or 0))[:20]
    cuerpo = tabla(kws, [("keyword", "Keyword"), ("intencion", "Intención"), ("volumen_estimado", "Volumen est."),
                         ("nivel_volumen", "Nivel"), ("dificultad", "Dificultad"), ("cpc_estimado", "CPC est."), ("prioridad", "Prioridad")])
    extra = " · ".join(f"{t}: {e(kw.get(k))}" for k, t in (("tendencia", "Tendencia"), ("estacionalidad", "Estacionalidad"),
                                                           ("viabilidad_seo", "SEO"), ("viabilidad_sem", "Anuncios de búsqueda")) if kw.get(k))
    partes.append(seccion("Palabras clave", (f"<p>{extra}</p>" if extra else "") + cuerpo))

    # Viabilidad (escenarios)
    esc = modelo.get("escenarios") or {}
    if esc:
        filas = []
        for nombre, r in esc.items():
            filas.append({"escenario": nombre, "mc": num(r.get("margen_contribucion_pct"), 1, " %"),
                          "pe": num(r.get("punto_equilibrio_ingresos_mes"), 0, " €"),
                          "mes": r.get("mes_equilibrio_operativo") or "no se alcanza",
                          "fin": num(r.get("necesidad_financiacion"), 0, " €"),
                          "ebitda": num(r.get("ebitda_acumulado"), 0, " €")})
        cuerpo = tabla(filas, [("escenario", "Escenario"), ("mc", "Margen contribución"), ("pe", "Equilibrio €/mes"),
                               ("mes", "Mes equilibrio"), ("fin", "Financiación necesaria"), ("ebitda", "EBITDA acumulado")])
        if modelo.get("variables_criticas"):
            cuerpo += f"<p><b>Variables críticas:</b> {e(', '.join(modelo['variables_criticas']))}</p>"
        cuerpo += lista(modelo.get("avisos"))
        partes.append(seccion("Viabilidad económica (sin IVA, antes de impuestos)", cuerpo))

    # Go-to-market
    canales = sorted(gtm.get("canales") or [], key=lambda c: c.get("prioridad") or 99)
    cuerpo = ""
    if gtm.get("mensaje_principal"):
        cuerpo += f"<p><b>Mensaje:</b> {e(gtm['mensaje_principal'])}</p>"
    cuerpo += tabla(canales, [("prioridad", "#"), ("canal", "Canal"), ("por_que", "Por qué"), ("prueba", "Prueba"),
                              ("presupuesto", "Presupuesto"), ("metrica_exito", "Éxito si")])
    if gtm.get("cac_maximo_asumible"):
        cuerpo += f"<p><b>CAC máximo asumible:</b> {e(gtm['cac_maximo_asumible'])}</p>"
    partes.append(seccion("Marketing y ventas", cuerpo))

    # Producto y distribución
    cuerpo = ""
    mvp = prod.get("mvp") or {}
    if mvp:
        cuerpo += f"<p><b>MVP ({e(mvp.get('tipo'))}):</b> {e(mvp.get('descripcion'))} — prueba: {e(mvp.get('hipotesis_que_prueba'))}</p>"
    cuerpo += tabla(prod.get("canales_distribucion") or [], [("canal", "Canal"), ("margen_canal_pct", "Margen canal %"),
                                                               ("recomendado", "Recomendado"), ("motivo", "Motivo")])
    partes.append(seccion("Producto y distribución", cuerpo))

    # Legal
    cuerpo = ""
    if leg:
        if leg.get("bloqueo_legal"):
            cuerpo += '<p class="red"><b>🚩 Bloqueo legal detectado</b></p>'
        if leg.get("forma_juridica_recomendada"):
            cuerpo += f"<p><b>Forma jurídica:</b> {e(leg['forma_juridica_recomendada'])}</p>"
        cuerpo += tabla(leg.get("tramites") or [], [("tramite", "Trámite"), ("organismo", "Organismo"),
                                                    ("coste_orientativo", "Coste"), ("plazo", "Plazo"), ("critico", "Crítico")])
    partes.append(seccion("Legal y trámites (orientativo)", cuerpo))

    # Riesgos y experimentos
    cuerpo = tabla(ver.get("riesgos") or [], [("riesgo", "Riesgo"), ("probabilidad", "Prob."), ("impacto", "Impacto"), ("mitigacion", "Mitigación")])
    if ver.get("experimentos"):
        cuerpo += "<h3>Experimentos (del más barato al más caro)</h3>" + tabla(
            ver["experimentos"], [("nombre", "Experimento"), ("hipotesis", "Hipótesis"), ("coste_max", "Coste máx."),
                                  ("plazo", "Plazo"), ("umbral_exito", "Éxito si"), ("umbral_parada", "Parar si")])
    if ver.get("criterios_abandono"):
        cuerpo += "<h3>Criterios de abandono</h3>" + lista(ver["criterios_abandono"])
    partes.append(seccion("Riesgos y próximos pasos", cuerpo))

    # Fuentes
    if fuentes:
        filas = "".join(
            f'<tr><td>{e(f.get("id"))}</td><td>' +
            (f'<a href="{e(f.get("url"))}" rel="noopener">{e(f.get("titulo") or f.get("url"))}</a>' if url_segura(f.get("url")) else e(f.get("titulo")))
            + f'</td><td>{e(f.get("editor"))}</td><td>{e(f.get("fecha_publicacion"))}</td><td>{e(f.get("nivel"))}</td></tr>'
            for f in fuentes)
        partes.append(seccion(f"Fuentes ({len(fuentes)})",
                              '<div class="scroll"><table><thead><tr><th>ID</th><th>Título</th><th>Editor</th>'
                              f'<th>Fecha</th><th>Nivel</th></tr></thead><tbody>{filas}</tbody></table></div>'))

    partes.append('<footer>Estudio basado en fuentes públicas a la fecha indicada. Las cifras etiquetadas como hipótesis '
                  'o estimación no son hechos. No sustituye el asesoramiento legal, fiscal ni financiero profesional. '
                  'Datos completos para IAs en <code>ia/estudio.json</code>.</footer>')
    cuerpo = "\n".join(p for p in partes if p)
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(idea)} · Estudio</title>'
            f'<style>{CSS}</style></head><body><main>{cuerpo}</main><script>{JS}</script></body></html>')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("estudio", help="Carpeta del estudio (estudios/<idea>)")
    a = ap.parse_args()
    raiz = a.estudio
    if not os.path.isdir(raiz):
        print(f"No existe la carpeta {raiz}", file=sys.stderr)
        return 2
    modulos, fuentes = cargar(raiz)
    idea = nombre_idea(raiz, modulos)
    os.makedirs(os.path.join(raiz, "ia"), exist_ok=True)
    consolidado = {"idea": idea, "generado": dt.datetime.now().isoformat(timespec="seconds"),
                   "modulos": modulos, "fuentes": fuentes}
    with open(os.path.join(raiz, "ia", "estudio.json"), "w", encoding="utf-8") as f:
        json.dump(consolidado, f, ensure_ascii=False, indent=2)
    with open(os.path.join(raiz, "informe.html"), "w", encoding="utf-8") as f:
        f.write(construir_html(raiz, modulos, fuentes))
    vacios = [t for c, k, t in CARPETAS if not (modulos.get(k) or {}).get("resumen") and k != "brief"]
    print(f"Generado: {os.path.join(raiz, 'informe.html')} y {os.path.join(raiz, 'ia', 'estudio.json')}")
    if vacios:
        print("Módulos sin resumen en datos.json (aparecerán vacíos): " + ", ".join(vacios))
    return 0


if __name__ == "__main__":
    sys.exit(main())
