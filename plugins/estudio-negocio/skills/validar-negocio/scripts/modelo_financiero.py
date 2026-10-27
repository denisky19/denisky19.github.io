#!/usr/bin/env python3
"""Modelo económico por escenarios: margen, punto de equilibrio, caja, sensibilidad.

Entrada: JSON de supuestos (ver plantillas/modelo-financiero.json).
Salida (en --salida): modelo.md (informe), escenarios.csv (mes a mes), modelo.json (resumen).

Dos tipos de negocio:
  - "transaccional": ventas (unidades, tickets, servicios) al mes.
  - "suscripcion":  clientes que pagan una cuota mensual, con altas (nuevos) y bajas (churn).

Todas las cifras son SIN IVA y ANTES de impuestos sobre beneficios. No incluye amortizaciones
ni el desfase de cobros y pagos del IVA. Son escenarios condicionados a supuestos, no previsiones.

Ejemplos:
  python3 modelo_financiero.py supuestos.json --salida 06-viabilidad
  python3 modelo_financiero.py --selftest
"""

import argparse
import copy
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import escribir_csv, tabla_md  # noqa: E402

ESCENARIOS_DEFECTO = {
    "pesimista": {"volumen": 0.6, "precio": 0.95, "coste_variable": 1.1, "costes_fijos": 1.05, "cac": 1.3, "churn": 1.3},
    "base": {},
    "optimista": {"volumen": 1.3, "precio": 1.0, "coste_variable": 0.95, "costes_fijos": 1.0, "cac": 0.85, "churn": 0.8},
}
VARIABLES_SENSIBILIDAD = {
    "transaccional": ["precio", "volumen", "coste_variable", "costes_fijos"],
    "suscripcion": ["precio", "volumen", "coste_variable", "costes_fijos", "cac", "churn"],
}
NOMBRES = {"precio": "Precio", "volumen": "Volumen de ventas / altas", "coste_variable": "Coste variable unitario",
           "costes_fijos": "Costes fijos", "cac": "Coste de captación (CAC)", "churn": "Bajas mensuales (churn)"}


def suma(x):
    if isinstance(x, dict):
        return float(sum(v for v in x.values() if isinstance(v, (int, float))))
    return float(x or 0)


def validar(s):
    errores = []
    tipo = s.get("tipo", "transaccional")
    if tipo not in ("transaccional", "suscripcion"):
        errores.append("tipo debe ser 'transaccional' o 'suscripcion'")
    for campo in ("precio_medio_sin_iva", "coste_variable_unitario", "costes_fijos_mensuales", "inversion_inicial"):
        if campo not in s:
            errores.append(f"falta '{campo}'")
    if tipo == "transaccional" and "ventas_mes_inicial" not in s:
        errores.append("falta 'ventas_mes_inicial'")
    if tipo == "suscripcion":
        for campo in ("clientes_nuevos_mes_inicial", "churn_mensual_pct"):
            if campo not in s:
                errores.append(f"falta '{campo}'")
    est = s.get("estacionalidad")
    if est is not None and len(est) != 12:
        errores.append("estacionalidad debe tener 12 factores (enero…diciembre)")
    return errores


def simular(s, esc):
    """Simula mes a mes un escenario. esc: multiplicadores por variable."""
    m = lambda k: float(esc.get(k, 1.0))  # noqa: E731
    tipo = s.get("tipo", "transaccional")
    meses = int(s.get("meses", 36))
    precio = float(s["precio_medio_sin_iva"]) * m("precio")
    cv = float(s["coste_variable_unitario"]) * m("coste_variable")
    comision = float(s.get("comision_cobro_pct", 0)) / 100
    cf = suma(s["costes_fijos_mensuales"]) * m("costes_fijos")
    inversion = suma(s["inversion_inicial"])
    est = s.get("estacionalidad") or [1.0] * 12
    rampa = s.get("rampa_inicial") or []
    mes_inicio = int(s.get("mes_inicio", 1))
    g = float(s.get("crecimiento_mensual_pct", 0)) / 100
    cap = s.get("capacidad_maxima_mes")
    caja = -inversion
    filas = []
    clientes = float(s.get("clientes_iniciales", 0))
    for mes in range(1, meses + 1):
        f_est = float(est[(mes_inicio - 1 + mes - 1) % 12])
        f_rampa = float(rampa[mes - 1]) if mes - 1 < len(rampa) else 1.0
        if tipo == "transaccional":
            unidades = float(s["ventas_mes_inicial"]) * (1 + g) ** (mes - 1) * f_est * f_rampa * m("volumen")
            if cap:
                unidades = min(unidades, float(cap))
            nuevos = None
            captacion = unidades * float(s.get("coste_captacion_por_venta", 0)) * m("cac")
            base_ingresos = unidades
        else:
            gn = float(s.get("crecimiento_nuevos_mensual_pct", s.get("crecimiento_mensual_pct", 0))) / 100
            churn = min(1.0, float(s["churn_mensual_pct"]) / 100 * m("churn"))
            nuevos = float(s["clientes_nuevos_mes_inicial"]) * (1 + gn) ** (mes - 1) * f_est * f_rampa * m("volumen")
            clientes = clientes * (1 - churn) + nuevos
            if cap:
                clientes = min(clientes, float(cap))
            unidades = clientes
            captacion = nuevos * float(s.get("cac", 0)) * m("cac")
            base_ingresos = clientes
        ingresos = base_ingresos * precio
        variables = base_ingresos * (cv + precio * comision)
        mc = ingresos - variables
        ebitda = mc - cf - captacion
        caja += ebitda
        filas.append({"mes": mes, "unidades_o_clientes": round(unidades, 2),
                      "nuevos_clientes": None if nuevos is None else round(nuevos, 2),
                      "ingresos": round(ingresos, 2), "costes_variables": round(variables, 2),
                      "margen_contribucion": round(mc, 2), "costes_fijos": round(cf, 2),
                      "captacion": round(captacion, 2), "ebitda": round(ebitda, 2), "caja_acumulada": round(caja, 2)})
    return filas, {"precio": precio, "cv": cv, "comision": comision, "cf": cf, "inversion": inversion}


def resumir(s, filas, p):
    tipo = s.get("tipo", "transaccional")
    mc_unit = p["precio"] - p["cv"] - p["precio"] * p["comision"]
    mc_pct = mc_unit / p["precio"] if p["precio"] else 0
    colchon = float(s.get("meses_colchon", 3)) * p["cf"]
    caja_min = min(0.0, min(f["caja_acumulada"] for f in filas), -p["inversion"])
    mes_eq = next((f["mes"] for f in filas if f["ebitda"] >= 0), None)
    mes_rec = next((f["mes"] for f in filas if f["caja_acumulada"] >= 0), None)
    anios = []
    for a in range(math.ceil(len(filas) / 12)):
        tramo = filas[a * 12:(a + 1) * 12]
        anios.append({"anio": a + 1, "ingresos": round(sum(f["ingresos"] for f in tramo)),
                      "margen_contribucion": round(sum(f["margen_contribucion"] for f in tramo)),
                      "ebitda": round(sum(f["ebitda"] for f in tramo)),
                      "caja_final": round(tramo[-1]["caja_acumulada"])})
    r = {
        "margen_contribucion_unitario": round(mc_unit, 2),
        "margen_contribucion_pct": round(mc_pct * 100, 1),
        "costes_fijos_mensuales": round(p["cf"], 2),
        "punto_equilibrio_unidades_mes": round(p["cf"] / mc_unit, 1) if mc_unit > 0 else None,
        "punto_equilibrio_ingresos_mes": round(p["cf"] / mc_pct, 2) if mc_pct > 0 else None,
        "mes_equilibrio_operativo": mes_eq,
        "mes_recuperacion_inversion": mes_rec,
        "caja_minima": round(caja_min, 2),
        "necesidad_financiacion": round(-caja_min + colchon, 2),
        "colchon": round(colchon, 2),
        "ebitda_acumulado": round(sum(f["ebitda"] for f in filas), 2),
        "anios": anios,
    }
    if tipo == "suscripcion":
        churn = float(s["churn_mensual_pct"]) / 100
        r["clientes_finales"] = filas[-1]["unidades_o_clientes"]
        if churn > 0 and mc_unit > 0:
            ltv = mc_unit / churn
            r["ltv"] = round(ltv, 2)
            cac = float(s.get("cac", 0))
            if cac > 0:
                r["ltv_cac"] = round(ltv / cac, 2)
                r["payback_cac_meses"] = round(cac / mc_unit, 1)
    if r["punto_equilibrio_unidades_mes"]:
        tramo2 = filas[12:24] if len(filas) >= 24 else filas[-12:]
        media = sum(f["unidades_o_clientes"] for f in tramo2) / len(tramo2)
        r["margen_seguridad_pct"] = round((media - r["punto_equilibrio_unidades_mes"]) / media * 100, 1) if media else None
    return r


def ejecutar(s):
    escenarios = s.get("escenarios") or ESCENARIOS_DEFECTO
    resultado, todas = {}, []
    for nombre, esc in escenarios.items():
        filas, p = simular(s, esc or {})
        resultado[nombre] = resumir(s, filas, p)
        for f in filas:
            todas.append({"escenario": nombre, **f})
    sens = sensibilidad(s, escenarios.get("base", {}) or {})
    avisos = generar_avisos(s, resultado)
    return resultado, todas, sens, avisos


def sensibilidad(s, base, delta=0.2):
    tipo = s.get("tipo", "transaccional")
    filas_base, p = simular(s, base)
    ref = resumir(s, filas_base, p)
    res = []
    for var in VARIABLES_SENSIBILIDAD[tipo]:
        fila = {"variable": NOMBRES[var]}
        for signo, etiqueta in ((-1, "menos"), (1, "mas")):
            esc = copy.deepcopy(base)
            esc[var] = float(esc.get(var, 1.0)) * (1 + signo * delta)
            r = resumir(s, *simular(s, esc))
            fila[f"ebitda_{etiqueta}"] = r["ebitda_acumulado"]
            fila[f"financiacion_{etiqueta}"] = r["necesidad_financiacion"]
        fila["rango_ebitda"] = round(abs(fila["ebitda_mas"] - fila["ebitda_menos"]), 2)
        res.append(fila)
    res.sort(key=lambda x: -x["rango_ebitda"])
    return {"delta_pct": delta * 100, "ebitda_acumulado_base": ref["ebitda_acumulado"],
            "necesidad_financiacion_base": ref["necesidad_financiacion"], "variables": res}


def generar_avisos(s, resultado):
    avisos = []
    base = resultado.get("base") or next(iter(resultado.values()))
    if base["margen_contribucion_unitario"] <= 0:
        avisos.append("🔴 Margen de contribución negativo o nulo: cada venta pierde dinero; vender más empeora el resultado.")
    elif base["margen_contribucion_pct"] < 20:
        avisos.append("🟠 Margen de contribución bajo (<20 %): poco espacio para pagar captación, errores o descuentos.")
    for nombre, r in resultado.items():
        if r["mes_equilibrio_operativo"] is None:
            avisos.append(f"⚠️ Escenario {nombre}: no alcanza el equilibrio operativo en el horizonte modelado.")
    if s.get("tipo") == "suscripcion" and base.get("ltv_cac") is not None and base["ltv_cac"] < 3:
        avisos.append(f"🟠 LTV/CAC = {base['ltv_cac']} (< 3, la referencia habitual).")
    if s.get("tipo") == "suscripcion" and base.get("payback_cac_meses") and base["payback_cac_meses"] > 12:
        avisos.append(f"🟠 Recuperar el CAC cuesta {base['payback_cac_meses']} meses (> 12, la referencia habitual).")
    cap = s.get("capacidad_maxima_mes")
    if cap and base.get("punto_equilibrio_unidades_mes") and base["punto_equilibrio_unidades_mes"] > float(cap):
        avisos.append("🔴 El punto de equilibrio supera la capacidad máxima: con esta estructura de costes nunca se cubren gastos.")
    if not any("fundador" in k.lower() or "autonomo" in k.lower() or "autónomo" in k.lower()
               for k in (s.get("costes_fijos_mensuales") or {})):
        avisos.append("⚠️ No hay partida de sueldo o cuota de autónomo del fundador en costes fijos: el resultado puede estar inflado.")
    return avisos


def fmt(v, dec=0, sufijo=""):
    if v is None:
        return "no se alcanza"
    if isinstance(v, (int, float)):
        txt = f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return txt + sufijo
    return str(v)


def informe_md(s, resultado, sens, avisos):
    mon = s.get("moneda", "EUR")
    tipo = s.get("tipo", "transaccional")
    unidad = "clientes" if tipo == "suscripcion" else "ventas"
    L = ["# Modelo económico", "",
         f"> Tipo: **{tipo}** · horizonte {s.get('meses', 36)} meses · cifras en {mon} **sin IVA** y antes de impuestos.",
         "> Escenarios condicionados a supuestos `[CÁLCULO]` sobre entradas etiquetadas en `supuestos.json`; no son previsiones.", ""]
    if avisos:
        L += ["## Avisos", ""] + [f"- {a}" for a in avisos] + [""]
    def desglose(x):
        return (" → " + ", ".join(f"{k} {fmt(v)}" for k, v in x.items())) if isinstance(x, dict) else ""

    L += ["## Supuestos principales", "",
          f"- Precio medio sin IVA: {fmt(s['precio_medio_sin_iva'], 2)} {mon} · coste variable unitario: {fmt(s['coste_variable_unitario'], 2)} {mon} · comisión de cobro: {fmt(float(s.get('comision_cobro_pct', 0)), 1)} %",
          f"- Costes fijos mensuales: {fmt(suma(s['costes_fijos_mensuales']))} {mon}{desglose(s['costes_fijos_mensuales'])}",
          f"- Inversión inicial: {fmt(suma(s['inversion_inicial']))} {mon}{desglose(s['inversion_inicial'])}",
          ]
    if tipo == "transaccional":
        L.append(f"- Ventas el mes 1: {s['ventas_mes_inicial']} · crecimiento mensual {s.get('crecimiento_mensual_pct', 0)} % · capacidad máx. {s.get('capacidad_maxima_mes') or 'sin límite'}")
    else:
        L.append(f"- Altas el mes 1: {s['clientes_nuevos_mes_inicial']} · crecimiento de altas {s.get('crecimiento_nuevos_mensual_pct', s.get('crecimiento_mensual_pct', 0))} % · churn {s['churn_mensual_pct']} %/mes · CAC {s.get('cac', 0)} {mon}")
    if s.get("notas_supuestos"):
        L.append(f"- Notas: {s['notas_supuestos']}")
    L += ["", "## Resultados por escenario", ""]
    cols = list(resultado.keys())
    filas = [
        ("Margen de contribución unitario", lambda r: fmt(r["margen_contribucion_unitario"], 2, f" {mon}")),
        ("Margen de contribución %", lambda r: fmt(r["margen_contribucion_pct"], 1, " %")),
        (f"Punto de equilibrio ({unidad}/mes)", lambda r: fmt(r["punto_equilibrio_unidades_mes"], 1)),
        ("Punto de equilibrio (ingresos/mes)", lambda r: fmt(r["punto_equilibrio_ingresos_mes"], 0, f" {mon}")),
        ("Mes de equilibrio operativo", lambda r: fmt(r["mes_equilibrio_operativo"])),
        ("Mes en que se recupera la inversión", lambda r: fmt(r["mes_recuperacion_inversion"])),
        ("Caja mínima (peor momento)", lambda r: fmt(r["caja_minima"], 0, f" {mon}")),
        ("Necesidad de financiación (incl. colchón)", lambda r: fmt(r["necesidad_financiacion"], 0, f" {mon}")),
        ("Margen de seguridad (año 2)", lambda r: fmt(r.get("margen_seguridad_pct"), 1, " %")),
    ]
    if tipo == "suscripcion":
        filas += [("LTV", lambda r: fmt(r.get("ltv"), 0, f" {mon}")), ("LTV/CAC", lambda r: fmt(r.get("ltv_cac"), 2)),
                  ("Payback CAC (meses)", lambda r: fmt(r.get("payback_cac_meses"), 1)),
                  ("Clientes al final", lambda r: fmt(r.get("clientes_finales"), 0))]
    L.append("| Indicador | " + " | ".join(c.capitalize() for c in cols) + " |")
    L.append("|---|" + "---|" * len(cols))
    for nombre, f in filas:
        L.append(f"| {nombre} | " + " | ".join(f(resultado[c]) for c in cols) + " |")
    L += ["", "## Cuenta anual por escenario", ""]
    for c in cols:
        L.append(f"**{c.capitalize()}**\n")
        L.append(tabla_md([{k: fmt(v) if k != "anio" else v for k, v in a.items()} for a in resultado[c]["anios"]],
                          ["anio", "ingresos", "margen_contribucion", "ebitda", "caja_final"],
                          ["Año", "Ingresos", "Margen contribución", "EBITDA", "Caja final"]))
        L.append("")
    L += [f"## Sensibilidad (±{sens['delta_pct']:.0f} % sobre el escenario base)", "",
          f"EBITDA acumulado base: {fmt(sens['ebitda_acumulado_base'])} {mon} · necesidad de financiación base: {fmt(sens['necesidad_financiacion_base'])} {mon}", "",
          "| Variable (ordenada por impacto) | EBITDA acum. −20 % | EBITDA acum. +20 % | Financiación −20 % | Financiación +20 % |",
          "|---|---|---|---|---|"]
    for v in sens["variables"]:
        L.append(f"| {v['variable']} | {fmt(v['ebitda_menos'])} | {fmt(v['ebitda_mas'])} | {fmt(v['financiacion_menos'])} | {fmt(v['financiacion_mas'])} |")
    top = ", ".join(v["variable"] for v in sens["variables"][:3])
    L += ["", f"**Variables críticas a validar primero:** {top}.", "",
          "## Fórmulas", "",
          "- Margen de contribución unitario = precio sin IVA − coste variable − comisión de cobro",
          "- Punto de equilibrio = costes fijos mensuales / margen de contribución unitario",
          "- Necesidad de financiación = −(caja acumulada mínima, incluida la inversión) + colchón (meses_colchon × costes fijos)",
          "- Suscripción: LTV = margen mensual por cliente / churn · Payback CAC = CAC / margen mensual por cliente",
          "- El EBITDA incluye el gasto de captación variable; no incluye amortizaciones, intereses ni impuestos sobre beneficios.", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("supuestos", nargs="?", help="JSON de supuestos")
    ap.add_argument("--salida", default=".", help="Carpeta de salida")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.supuestos:
        ap.error("indica el archivo de supuestos")
    with open(a.supuestos, encoding="utf-8") as f:
        s = json.load(f)
    errores = validar(s)
    if errores:
        print("Errores en los supuestos:\n- " + "\n- ".join(errores), file=sys.stderr)
        return 2
    resultado, todas, sens, avisos = ejecutar(s)
    os.makedirs(a.salida, exist_ok=True)
    md = informe_md(s, resultado, sens, avisos)
    with open(os.path.join(a.salida, "modelo.md"), "w", encoding="utf-8") as f:
        f.write(md)
    escribir_csv(os.path.join(a.salida, "escenarios.csv"), todas,
                 ["escenario", "mes", "unidades_o_clientes", "nuevos_clientes", "ingresos", "costes_variables",
                  "margen_contribucion", "costes_fijos", "captacion", "ebitda", "caja_acumulada"])
    salida_json = {"moneda": s.get("moneda", "EUR"), "tipo": s.get("tipo", "transaccional"),
                   "inversion_inicial": suma(s["inversion_inicial"]),
                   "precio_medio_sin_iva": s["precio_medio_sin_iva"], "escenarios": resultado,
                   "sensibilidad": sens, "avisos": avisos,
                   "variables_criticas": [v["variable"] for v in sens["variables"][:3]]}
    with open(os.path.join(a.salida, "modelo.json"), "w", encoding="utf-8") as f:
        json.dump(salida_json, f, ensure_ascii=False, indent=2)
    print(md)
    print(f"\nArchivos: {a.salida}/modelo.md, escenarios.csv, modelo.json")
    return 0


def selftest():
    s = {"tipo": "transaccional", "meses": 24, "precio_medio_sin_iva": 10.0, "coste_variable_unitario": 4.0,
         "comision_cobro_pct": 0, "ventas_mes_inicial": 1000, "crecimiento_mensual_pct": 0,
         "costes_fijos_mensuales": {"alquiler": 3000, "sueldo_fundador": 3000}, "inversion_inicial": {"obra": 12000},
         "meses_colchon": 2, "escenarios": {"base": {}}}
    assert not validar(s)
    res, filas, sens, avisos = ejecutar(s)
    b = res["base"]
    # MC unit = 6; equilibrio = 6000/6 = 1000 uds; vende 1000 → EBITDA 0 cada mes
    assert b["margen_contribucion_unitario"] == 6.0 and b["punto_equilibrio_unidades_mes"] == 1000.0
    assert b["punto_equilibrio_ingresos_mes"] == 10000.0 and b["mes_equilibrio_operativo"] == 1
    assert b["caja_minima"] == -12000 and b["necesidad_financiacion"] == 12000 + 12000
    assert b["mes_recuperacion_inversion"] is None and b["margen_seguridad_pct"] == 0.0
    # Con 1500 ventas: EBITDA 3000/mes → recupera 12000 en el mes 4
    s2 = dict(s, ventas_mes_inicial=1500)
    b2 = ejecutar(s2)[0]["base"]
    assert b2["mes_recuperacion_inversion"] == 4 and b2["anios"][0]["ebitda"] == 36000
    # Capacidad
    s3 = dict(s, ventas_mes_inicial=5000, capacidad_maxima_mes=1200)
    assert ejecutar(s3)[1][0]["unidades_o_clientes"] == 1200
    # Suscripción: estado estacionario clientes = nuevos/churn
    sub = {"tipo": "suscripcion", "meses": 120, "precio_medio_sin_iva": 20, "coste_variable_unitario": 2,
           "comision_cobro_pct": 0, "clientes_nuevos_mes_inicial": 50, "churn_mensual_pct": 5, "cac": 100,
           "costes_fijos_mensuales": {"autonomo_y_sueldo_fundador": 2000}, "inversion_inicial": {"web": 5000},
           "escenarios": {"base": {}}}
    rs = ejecutar(sub)[0]["base"]
    assert abs(rs["clientes_finales"] - 1000) < 5, rs["clientes_finales"]
    assert rs["ltv"] == 360.0 and rs["ltv_cac"] == 3.6 and rs["payback_cac_meses"] == 5.6
    # Margen negativo → aviso rojo
    neg = dict(s, coste_variable_unitario=11)
    assert any("negativo" in x for x in ejecutar(neg)[3])
    # Sensibilidad ordenada y con 4 variables
    assert len(sens["variables"]) == 4 and sens["variables"][0]["rango_ebitda"] >= sens["variables"][-1]["rango_ebitda"]
    md = informe_md(s, res, sens, avisos)
    assert "Punto de equilibrio" in md and "Sensibilidad" in md
    print("selftest OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
