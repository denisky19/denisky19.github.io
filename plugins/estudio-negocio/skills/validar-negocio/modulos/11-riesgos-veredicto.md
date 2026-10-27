# 11 · Riesgos, veredicto y experimentos

**Preguntas que responde:** ¿Funciona o no? ¿Con qué grado de seguridad? ¿Qué podría hacer que fracasara? ¿Qué hay que probar primero, cómo, con cuánto dinero y qué resultado haría seguir o parar?

Antes de puntuar, **piensa a fondo**. Pesa las señales más fuertes frente a las banderas rojas en lugar de promediarlas en un "depende": un fallo fatal puede pesar más que cinco señales buenas.

## 1. Abogado del diablo

Primero escribe el **mejor argumento a favor**, con evidencia. Después ataca la idea desde cinco perspectivas:
1. **Cliente**: ¿por qué no cambiaría de lo que usa hoy? ¿Por qué no lo aplazaría? ¿Qué le cuesta cambiar (dinero, tiempo, riesgo, confianza)?
2. **Competidor establecido**: ¿por qué sus clientes no se van? ¿Puede copiar la diferencia en 3 meses, bajar precios o bloquear el canal?
3. **Finanzas**: ¿qué 1–3 supuestos hacen frágil el modelo? ¿Se confunde facturación con beneficio, o beneficio con caja?
4. **Operaciones**: ¿qué se rompe con 10, 100 o 1.000 pedidos? ¿Cuellos de botella, calidad, devoluciones, dependencia del fundador?
5. **Regulación y entorno**: ¿qué cambio legal, de plataforma o económico lo hundiría?

Son perspectivas que simula un único analista: no las presentes como opiniones de expertos reales.

## 2. Pre-mortem (12 meses)

"Es dentro de un año y el negocio ha cerrado. ¿Por qué?" Escribe 5 causas plausibles y, para cada una:
- La **señal temprana** que lo avisaría.
- La **evidencia** que hoy la apoya o la contradice.
- El **experimento más barato** para comprobarlo.
- La **condición de parada o pivote**.

## 3. Matriz de riesgos

Tabla de probabilidad (1–5) × impacto (1–5), con mitigación, para los riesgos de mercado, cliente, competencia, producto, operaciones, financieros, legales y de equipo.

## 4. Puntuación (rúbrica)

Puntúa cada dimensión de 0 a 10 **según la evidencia** e indica una confianza (alta, media o baja) y su justificación con referencias. Si dudas entre dos niveles, **elige el más bajo** y anota la duda.

| # | Dimensión | Peso | 0–2 | 3–4 | 5–6 | 7–8 | 9–10 |
|---|---|---|---|---|---|---|---|
| 1 | **Dolor/necesidad** | 18 % | Nadie lo menciona o es una molestia menor | Menciones sueltas; las soluciones caseras "valen" | Quejas habituales en varias comunidades | Quejas frecuentes y emocionales; la gente se monta apaños | Ya pagan por soluciones malas o se las construyen |
| 2 | **Demanda y tendencia** | 12 % | Sin búsquedas o en claro declive | Plana o bajando | Estable, con búsquedas constantes | Creciendo de forma visible | Explosiva, de nicho a masiva |
| 3 | **Mercado alcanzable** | 10 % | El SOM no da ni para un sueldo | Justo para autoempleo con dificultades | Da para un negocio pequeño sano | Grande; permite crecer bastante | Muy grande y bien documentado |
| 4 | **Hueco competitivo** | 12 % | Líderes con clientes felices y opción gratuita | Saturado; solo quejas menores | Varios actores con debilidades reales | Soluciones actuales odiadas o un segmento desatendido | Necesidad clara sin solución buena |
| 5 | **Disposición a pagar** | 12 % | Se espera que sea gratis | Poca; muchas alternativas gratis | Hay productos de pago a precios modestos | Pagan de forma recurrente y se quejan del precio (prueba de que pagan) | Presupuestos B2B o precios premium aceptados |
| 6 | **Economía unitaria y financiación** | 16 % | Margen de contribución negativo o inversión inalcanzable | Equilibrio lejano o necesidad de caja muy superior a los recursos | Equilibrio alcanzable en el base, frágil en el pesimista | Equilibrio razonable y sensibilidad aceptable | Márgenes altos, poca inversión, recuperación rápida |
| 7 | **Acceso al cliente (distribución)** | 12 % | Sin canal identificable o con un CAC mayor que el margen | Canales caros o saturados | Al menos un canal plausible | Varios canales viables y comunidades receptivas | Viralidad natural o un canal propio difícil de copiar |
| 8 | **Ejecución (encaje del fundador, operaciones, legal)** | 8 % | Sin capacidades críticas, con bloqueo legal u operación imposible | Grandes carencias o regulación pesada | Carencias cubribles | Buen encaje y complejidad manejable | Ventaja injusta clara y complejidad baja |

**Calcula** con `python3 <skill>/scripts/puntuacion.py estudios/<idea>/10-veredicto/puntuacion.json` (formato en `plantillas/puntuacion.json`). El script aplica los pesos, las reglas y las anulaciones, y escribe `puntuacion.md` y `puntuacion-resultado.json`.

## 5. Veredicto

| Resultado | Condición |
|---|---|
| 🟢 **ADELANTE, a validar con clientes reales** | Total ≥ 7,0 y ninguna dimensión < 4 |
| 🟡 **AJUSTAR o PIVOTAR antes de invertir** | Total entre 5,0 y 6,9, o ≥ 7,0 con alguna dimensión < 4 |
| 🔴 **NO SEGUIR en esta forma** | Total < 5,0 |
| ⚪ **EVIDENCIA INSUFICIENTE** | Bandera adicional: menos de ~10 fuentes sólidas, o la mitad o más de las dimensiones con confianza baja |

**Anulaciones** (se aplican sobre el total):
- Dolor ≤ 2 → 🔴, sea cual sea el total. Sin dolor no hay negocio.
- Bloqueo legal confirmado → 🔴 hasta resolverlo.
- Economía ≤ 2 → como mucho 🟡, y el pivote tiene que cambiar el modelo económico.
- Distribución ≤ 2 → como mucho 🟡, y el pivote tiene que resolver el acceso al cliente.
- Disposición a pagar ≤ 2 con un modelo de pago → como mucho 🟡, hacia otro modelo de ingresos.

Interpreta el mercado según la **ambición** del usuario: un 5 en mercado es bueno para autoempleo e insuficiente para una startup que quiera levantar capital.

El párrafo de veredicto debe incluir:
- La decisión.
- Las 3 razones principales.
- **El mejor argumento contra el propio veredicto**.
- **Qué evidencia lo cambiaría**.

Un veredicto 🟢 nunca significa "ya está validado". Significa "merece la pena **gastar poco** en comprobarlo con clientes reales".

## 6. Experimentos de validación (del más barato al más caro)

Para las hipótesis críticas (las variables que más pesan en la sensibilidad del módulo 07 y las dimensiones con confianza baja), diseña 3–5 experimentos con `plantillas/experimento.md`:

| Experimento | Coste típico | Plazo | Ejemplo de umbral de éxito (ajústalo al caso) |
|---|---|---|---|
| 10 entrevistas tipo Mom Test | 0 € | 1–2 semanas | ≥ 7/10 describen el problema sin que se lo sugieras; ≥ 3 ya gastan en resolverlo |
| Encuesta a ≥ 100 personas del segmento | 0–150 € | 1–2 semanas | ≥ 30 % con problema intenso y gasto actual |
| Landing + anuncios (*smoke test*) | 100–300 € | 1–2 semanas | CTR y coste por registro compatibles con el CAC asumible |
| Preventa o reserva con señal | 0–200 € | 2–4 semanas | ≥ X preventas reales al precio objetivo |
| Concierge o servicio manual a 3–5 clientes | Tiempo | 2–4 semanas | Pagan y repiten |
| Pop-up, mercadillo o feria | 50–500 € | 1 fin de semana | Ventas por hora y ticket medio frente a lo que necesita el modelo |
| Carta de intenciones o piloto B2B | 0 € | 2–6 semanas | ≥ 3 empresas firman o pagan un piloto |

Cada experimento lleva: la hipótesis que prueba, el método paso a paso, el presupuesto máximo, la duración, la **métrica**, el **umbral de éxito** y el **umbral de parada**.

## 7. Criterios de abandono y plan de 30 días

- **Criterios de abandono o pivote**: 5–7 condiciones medibles. Por ejemplo: "si tras 300 € en anuncios el coste por registro es > 15 €, replantear el canal o el segmento".
- **Plan de 30 días**:
  - Semana 1: entrevistas y encuesta.
  - Semana 2: experimento de demanda.
  - Semana 3: experimento de pago o MVP.
  - Semana 4: decisión.

  Cada semana tiene 3–5 tareas concretas, con plantillas o textos si hace falta.

## Salidas

- `10-veredicto/riesgos.md` (abogado del diablo, pre-mortem, matriz)
- `10-veredicto/puntuacion.json` (entrada) y `puntuacion.md` (salida del script)
- `10-veredicto/experimentos.md`, `criterios-abandono.md`, `plan-30-dias.md`
- `10-veredicto/datos.json` → `metricas`: copia `puntuacion-resultado.json` y añade:
```json
{
  "experimentos": [{"nombre": "", "hipotesis": "", "coste_max": 0, "plazo": "", "metrica": "", "umbral_exito": "", "umbral_parada": ""}],
  "criterios_abandono": [],
  "riesgos": [{"riesgo": "", "probabilidad": 0, "impacto": 0, "mitigacion": ""}],
  "argumento_a_favor": "", "argumento_en_contra": "", "que_cambiaria_el_veredicto": ""
}
```
