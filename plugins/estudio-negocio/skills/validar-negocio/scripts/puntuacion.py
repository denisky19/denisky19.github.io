#!/usr/bin/env python3
"""Calcula la puntuación ponderada y el veredicto de una idea de negocio.

Entrada: JSON con las 8 dimensiones puntuadas de 0 a 10 (ver plantillas/puntuacion.json).
Salida: puntuacion.md y puntuacion-resultado.json junto al archivo de entrada (o en --salida).

Rúbrica completa y anclas de cada nivel en modulos/11-riesgos-veredicto.md.

Ejemplos:
  python3 puntuacion.py estudios/mi-idea/10-veredicto/puntuacion.json
  python3 puntuacion.py --selftest
"""

import argparse
import json
import os
import sys

DIMENSIONES = [  # clave, nombre, peso
    ("dolor", "Dolor / necesidad", 0.18),
    ("demanda", "Demanda y tendencia", 0.12),
    ("mercado", "Mercado alcanzable", 0.10),
    ("hueco", "Hueco competitivo", 0.12),
    ("pago", "Disposición a pagar", 0.12),
    ("economia", "Economía unitaria y financiación", 0.16),
    ("distribucion", "Acceso al cliente (distribución)", 0.12),
    ("ejecucion", "Ejecución (fundador, operaciones, legal)", 0.08),
]
VEREDICTOS = {
    "ADELANTE": ("🟢", "ADELANTE: merece la pena validarlo con clientes reales gastando poco"),
    "AJUSTAR": ("🟡", "AJUSTAR o PIVOTAR antes de invertir"),
    "NO_SEGUIR": ("🔴", "NO SEGUIR en esta forma"),
}
ORDEN = ["NO_SEGUIR", "AJUSTAR", "ADELANTE"]


def evaluar(d):
    dims = d.get("dimensiones", {})
    usadas, faltan, suma_pesos, total = [], [], 0.0, 0.0
    for clave, nombre, peso in DIMENSIONES:
        info = dims.get(clave) or {}
        p = info.get("puntuacion")
        if p is None:
            faltan.append(nombre)
            continue
        p = max(0.0, min(10.0, float(p)))
        usadas.append({"clave": clave, "nombre": nombre, "peso": peso, "puntuacion": p,
                       "confianza": info.get("confianza", "baja"), "justificacion": info.get("justificacion", ""),
                       "evidencia": info.get("evidencia", [])})
        suma_pesos += peso
        total += p * peso
    if not usadas:
        raise ValueError("No hay ninguna dimensión puntuada")
    total = round(total / suma_pesos, 1)
    p = {u["clave"]: u["puntuacion"] for u in usadas}
    minimo = min(p.values())

    if total >= 7.0 and minimo >= 4:
        veredicto = "ADELANTE"
    elif total >= 5.0:
        veredicto = "AJUSTAR"
    else:
        veredicto = "NO_SEGUIR"
    motivos = []
    if total >= 7.0 and minimo < 4:
        motivos.append("Total ≥ 7 pero alguna dimensión < 4 → como mucho AJUSTAR.")

    def tope(max_veredicto, motivo):
        nonlocal veredicto
        if ORDEN.index(veredicto) > ORDEN.index(max_veredicto):
            veredicto = max_veredicto
        motivos.append(motivo)

    if p.get("dolor") is not None and p["dolor"] <= 2:
        tope("NO_SEGUIR", "Dolor ≤ 2: sin un problema real no hay negocio.")
    if d.get("bloqueo_legal"):
        tope("NO_SEGUIR", "Bloqueo legal confirmado: no seguir hasta resolverlo.")
    if p.get("economia") is not None and p["economia"] <= 2:
        tope("AJUSTAR", "Economía ≤ 2: el pivote debe cambiar el modelo económico.")
    if p.get("distribucion") is not None and p["distribucion"] <= 2:
        tope("AJUSTAR", "Distribución ≤ 2: el pivote debe resolver cómo llegar al cliente.")
    if p.get("pago") is not None and p["pago"] <= 2 and d.get("modelo_de_pago", True):
        tope("AJUSTAR", "Disposición a pagar ≤ 2 con un modelo de pago: hay que buscar otro modelo de ingresos.")

    bajas = sum(1 for u in usadas if u["confianza"] == "baja")
    fuentes = d.get("fuentes_solidas")
    insuficiente = bool(faltan) or bajas >= len(usadas) / 2 or (fuentes is not None and fuentes < 10)
    motivos_ev = []
    if faltan:
        motivos_ev.append("Dimensiones sin puntuar: " + ", ".join(faltan))
    if bajas >= len(usadas) / 2:
        motivos_ev.append(f"{bajas} de {len(usadas)} dimensiones con confianza baja")
    if fuentes is not None and fuentes < 10:
        motivos_ev.append(f"Solo {fuentes} fuentes sólidas (< 10)")

    debiles = sorted(usadas, key=lambda u: u["puntuacion"])[:3]
    emoji, texto = VEREDICTOS[veredicto]
    return {
        "puntuacion_total": total, "veredicto": veredicto, "emoji": emoji, "veredicto_texto": texto,
        "evidencia_insuficiente": insuficiente, "motivos_evidencia": motivos_ev,
        "reglas_aplicadas": motivos, "dimensiones": usadas,
        "dimensiones_mas_debiles": [u["nombre"] for u in debiles],
        "ambicion": d.get("ambicion", ""),
    }


def barra(p):
    llenos = int(round(p))
    return "█" * llenos + "░" * (10 - llenos)


def informe_md(r, d):
    L = ["# Puntuación y veredicto", "",
         f"## {r['emoji']} {r['veredicto_texto']}",
         f"**Puntuación: {r['puntuacion_total']:.1f}/10**".replace(".", ",") + (" · ⚪ **EVIDENCIA INSUFICIENTE**" if r["evidencia_insuficiente"] else ""), ""]
    if r["reglas_aplicadas"]:
        L += ["Reglas aplicadas:"] + [f"- {m}" for m in r["reglas_aplicadas"]] + [""]
    if r["motivos_evidencia"]:
        L += ["Por qué la evidencia es insuficiente:"] + [f"- {m}" for m in r["motivos_evidencia"]] + [""]
    if r.get("ambicion"):
        L += [f"Ambición declarada: **{r['ambicion']}** (interpreta el mercado en función de ella).", ""]
    L += ["| Dimensión | Peso | Puntuación | | Confianza | Justificación (evidencia) |", "|---|---|---|---|---|---|"]
    for u in r["dimensiones"]:
        ev = f" ({', '.join(u['evidencia'])})" if u["evidencia"] else ""
        L.append(f"| {u['nombre']} | {u['peso'] * 100:.0f} % | {u['puntuacion']:g}".replace(".", ",") + f" | `{barra(u['puntuacion'])}` | {u['confianza']} | {u['justificacion']}{ev} |")
    L += ["", f"Dimensiones más débiles: {', '.join(r['dimensiones_mas_debiles'])}.", ""]
    for campo, titulo in (("argumento_a_favor", "Mejor argumento a favor"),
                          ("argumento_en_contra", "Mejor argumento en contra del veredicto"),
                          ("que_cambiaria_el_veredicto", "Qué evidencia cambiaría el veredicto")):
        if d.get(campo):
            L += [f"**{titulo}:** {d[campo]}", ""]
    L += ["Escala: 🟢 ≥ 7,0 sin dimensiones < 4 · 🟡 5,0–6,9 · 🔴 < 5,0. "
          "Un 🟢 significa «merece la pena gastar poco en comprobarlo», no «ya está validado»."]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada", nargs="?")
    ap.add_argument("--salida", help="Carpeta de salida (por defecto, la del archivo de entrada)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.entrada:
        ap.error("indica el JSON de puntuación")
    with open(a.entrada, encoding="utf-8") as f:
        d = json.load(f)
    r = evaluar(d)
    for campo in ("argumento_a_favor", "argumento_en_contra", "que_cambiaria_el_veredicto"):
        if d.get(campo):
            r[campo] = d[campo]
    carpeta = a.salida or os.path.dirname(os.path.abspath(a.entrada))
    md = informe_md(r, d)
    with open(os.path.join(carpeta, "puntuacion.md"), "w", encoding="utf-8") as f:
        f.write(md)
    with open(os.path.join(carpeta, "puntuacion-resultado.json"), "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
    print(md)
    return 0


def selftest():
    def caso(puntos, **extra):
        d = {"dimensiones": {k: {"puntuacion": v, "confianza": "media"} for k, v in puntos.items()}}
        d.update(extra)
        return evaluar(d)
    todos = lambda v: {k: v for k, _, _ in DIMENSIONES}  # noqa: E731
    assert abs(sum(p for _, _, p in DIMENSIONES) - 1.0) < 1e-9
    r = caso(todos(8))
    assert r["puntuacion_total"] == 8.0 and r["veredicto"] == "ADELANTE" and not r["evidencia_insuficiente"]
    p = todos(8); p["hueco"] = 3
    assert caso(p)["veredicto"] == "AJUSTAR"  # total alto pero una < 4
    p = todos(8); p["dolor"] = 2
    assert caso(p)["veredicto"] == "NO_SEGUIR"
    p = todos(8); p["economia"] = 2
    assert caso(p)["veredicto"] == "AJUSTAR"
    assert caso(todos(8), bloqueo_legal=True)["veredicto"] == "NO_SEGUIR"
    assert caso(todos(6))["veredicto"] == "AJUSTAR"
    assert caso(todos(4))["veredicto"] == "NO_SEGUIR"
    assert caso(todos(8), fuentes_solidas=5)["evidencia_insuficiente"]
    p = todos(8); del p["mercado"]
    r = caso(p)
    assert r["evidencia_insuficiente"] and r["puntuacion_total"] == 8.0
    p = todos(8); p["pago"] = 1
    assert caso(p, modelo_de_pago=False)["veredicto"] == "AJUSTAR"  # por la regla de < 4, no por la de pago
    md = informe_md(caso(todos(7)), {})
    assert "7,0/10" in md
    print("selftest OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
