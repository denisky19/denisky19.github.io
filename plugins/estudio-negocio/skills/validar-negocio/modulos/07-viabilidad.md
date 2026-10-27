# 07 · Viabilidad económica

**Preguntas que responde:** ¿Cuánto hay que invertir? ¿Cuánto se gana por cada venta? ¿Cuántas ventas hacen falta para no perder dinero? ¿Cuándo se llega a ese punto? ¿Cuánta caja hace falta para aguantar hasta entonces? ¿Qué pasa si las cosas van peor?

> Estos son **escenarios condicionados a supuestos, no predicciones**. Su valor está en descubrir qué supuestos deciden el resultado y cuánto margen de error aguanta el negocio.

## 0. Confirma los supuestos con el usuario (obligatorio)

Antes de calcular, enséñale la tabla de supuestos con su origen (`[FUNDADOR]`, `[DATO]`, `[ESTIMACIÓN]` o `[HIPÓTESIS]`) y pregúntale si los corrige. Son sus números y su dinero.

## 1. Unidad de venta y modelo de ingresos

Define qué se vende y cómo se cobra: unidad de producto, ticket medio de un local, hora o proyecto, suscripción mensual o comisión sobre transacciones (en un marketplace **el volumen de transacciones no es tu ingreso**: tu ingreso es la comisión).

## 2. Precio

Triangula tres métodos y explica la elección:
1. **Coste + margen**: es el suelo, nunca la estrategia.
2. **Competencia**: rango y mediana del módulo 05.
3. **Valor y disposición a pagar**: lo que el cliente gasta hoy en alternativas, las señales del módulo 03, el método Van Westendorp si hay encuesta y el CPC de las keywords.

En España los precios a particulares se anuncian **con IVA**. Modela los ingresos **sin IVA**: un precio de 12,10 € con un 21 % de IVA son 10 € de ingreso. Revisa el tipo de IVA del producto (21 %, 10 % o 4 %, según el caso).

## 3. Costes: lista de comprobación

**Variables por unidad o venta**: materia prima o mercancía, envases, envío y devoluciones, comisión de la pasarela de pago y del marketplace, mano de obra variable, licencias por uso, comisiones de venta y desperdicio o mermas.

**Fijos mensuales**:
- Alquiler y comunidad, suministros, seguros, gestoría.
- Software y herramientas, mantenimiento.
- Sueldos y Seguridad Social de la plantilla.
- **Cuota de autónomo y sueldo del fundador**: no pongas 0 €. Si el fundador no cobra, el negocio no es viable aunque dé beneficio: se está pagando con su tiempo.
- Marketing fijo, amortización de préstamos (en la caja) y otros.

**Inversión inicial**:
- Obra y acondicionamiento, mobiliario y equipamiento, informática.
- Stock inicial, fianzas (en locales suelen pedirse varios meses), licencias y tasas, constitución de la sociedad.
- Marca y diseño, web, lanzamiento.
- **Colchón de caja de 3–6 meses de costes fijos**.

Para cada coste importante busca **un precio real** (Idealista y Fotocasa para alquileres de locales, el convenio colectivo del sector para salarios, tarifas de proveedores y de mensajería). Anota la fuente.

## 4. Volumen de ventas: tres vías

1. **Demanda**: el SOM del módulo 02 repartido por meses.
2. **Embudo**: tráfico o visitas × conversión, con conversiones de referencia citadas y marcadas como hipótesis.
3. **Capacidad**: el máximo que se puede atender (mesas × rotación, horas facturables, producción). El volumen **nunca** puede superar la capacidad.

Usa la cifra más conservadora en el escenario base y aplica una curva de arranque realista: casi ningún negocio vende a pleno rendimiento el primer mes.

## 5. Modelo con el script

Rellena `plantillas/modelo-financiero.json` (copiado a `06-viabilidad/supuestos.json`) y ejecuta:

```bash
python3 <skill>/scripts/modelo_financiero.py estudios/<idea>/06-viabilidad/supuestos.json --salida estudios/<idea>/06-viabilidad
```

Genera:
- `modelo.md` con el margen de contribución, el punto de equilibrio, el mes de equilibrio por escenario, la necesidad máxima de financiación, los resultados por año, el LTV, el CAC y el payback si es una suscripción, y el análisis de sensibilidad.
- `escenarios.csv` (mes a mes).
- `modelo.json`.

Si no puedes ejecutar código, haz los mismos cálculos a mano con las fórmulas del apartado 6 y enséñalas.

## 6. Fórmulas clave

```
Margen de contribución unitario = precio sin IVA − costes variables unitarios
Margen de contribución %        = margen unitario / precio sin IVA
Punto de equilibrio (unidades/mes) = costes fijos mensuales / margen de contribución unitario
Punto de equilibrio (€/mes)        = costes fijos mensuales / margen de contribución %
Necesidad de financiación          = inversión inicial + pérdidas acumuladas hasta el equilibrio + colchón
Suscripción: LTV = cuota × margen % / churn mensual   ·   LTV/CAC (referencia habitual ≥ 3)
             Payback del CAC (meses) = CAC / (cuota × margen %)   (referencia habitual ≤ 12)
```

Si el margen de contribución es **negativo**, vender más empeora el resultado. Señálalo en rojo.

## 7. Sensibilidad y escenarios

- Escenarios **pesimista, base y optimista**, con sus supuestos explícitos.
- **Tornado**: impacto de ±20 % en el precio, el volumen, el coste variable, los costes fijos y el CAC o el churn. Indica las **3 variables que más mueven el resultado**, que son las que hay que validar primero (módulo 11).
- ¿Cuánto pueden caer las ventas antes de no cubrir costes? Es el margen de seguridad.

## 8. Comparación con referencias del sector

- **Banco de España**: Central de Balances, ratios sectoriales por CNAE (márgenes, rotación, endeudamiento). Gratis.
- Cuentas de competidores (Registro Mercantil o fragmentos de directorios de empresas).
- Reglas orientativas del sector (por ejemplo, en hostelería se suelen citar un coste de materia prima del 25–35 % y un alquiler que no debería pasar del 10–15 % de las ventas). Preséntalas como **orientativas** y con fuente si la hay.

## 9. Financiación

Calcula **cuánto** hace falta y **cuándo**. Después revisa opciones (España; verifica que estén vigentes y sus condiciones actuales):
- Fondos propios, familia y amigos.
- Capitalización del paro (pago único).
- Microcréditos y préstamos (ICO, MicroBank, banca), ENISA (préstamos participativos), CDTI (si hay I+D).
- Subvenciones autonómicas y municipales: búscalas en infosubvenciones.es (BDNS), donde se pueden filtrar y exportar las convocatorias, y en la web de la agencia de desarrollo de la comunidad autónoma.
- Bonificaciones en la cuota de autónomos para nuevas altas.
- Crowdfunding de recompensa o equity, business angels y aceleradoras.

Para otros países busca los equivalentes.

## Salidas

- `06-viabilidad/supuestos.json` (entrada del modelo)
- `06-viabilidad/modelo.md`, `escenarios.csv` y `modelo.json` (salidas del script)
- `06-viabilidad/informe.md`: supuestos con su origen, precio y su justificación, costes, inversión, resultados, sensibilidad, comparación con el sector, financiación y conclusión ("viable si…, no viable si…").
- `06-viabilidad/datos.json` → `metricas` (copia lo esencial de `modelo.json`):
```json
{
  "inversion_inicial": 0, "moneda": "EUR",
  "precio_medio_sin_iva": 0, "margen_contribucion_pct": 0,
  "costes_fijos_mensuales": 0,
  "punto_equilibrio_unidades_mes": 0, "punto_equilibrio_ingresos_mes": 0,
  "mes_equilibrio": {"pesimista": null, "base": null, "optimista": null},
  "necesidad_financiacion": {"pesimista": 0, "base": 0, "optimista": 0},
  "resultado_anual_base": [{"anio": 1, "ingresos": 0, "ebitda": 0}],
  "variables_criticas": [],
  "ltv_cac": null
}
```
