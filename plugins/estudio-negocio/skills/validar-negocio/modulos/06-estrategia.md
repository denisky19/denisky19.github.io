# 06 · Estrategia: DAFO, CAME, modelo de negocio y posicionamiento

**Preguntas que responde:** Con lo que sabemos del exterior (mercado, cliente y competencia) y del interior (recursos del usuario), ¿qué estrategia tiene más posibilidades? ¿Cómo se gana dinero y por qué nos elegirían?

Todo lo que se escriba aquí debe **apoyarse en hallazgos de los módulos anteriores** (cita sus identificadores, por ejemplo `M3`, `C5` o `K2`). Una estrategia sin evidencia es una opinión.

## 1. DAFO (FODA en Latinoamérica)

| | Positivo | Negativo |
|---|---|---|
| **Interno** (depende del usuario) | **Fortalezas**: recursos, habilidades, contactos, ventajas de coste, ubicación | **Debilidades**: lo que falta (experiencia, capital, equipo, marca) |
| **Externo** (no depende) | **Oportunidades**: tendencias, huecos, cambios legales, debilidades de los competidores | **Amenazas**: competidores fuertes, regulación, sustitutos, ciclo económico, dependencia de plataformas |

Reglas:
- Entre 3 y 6 puntos por cuadrante, concretos y con su evidencia. Mal: "buena calidad". Bien: "el fundador tiene 8 años como jefe de cocina en [sector] [FUNDADOR]; los competidores reciben quejas de calidad irregular (12 de 40 reseñas de 1–3★) [DATO F7]".
- Las fortalezas y debilidades se valoran **en comparación con los competidores**, no en abstracto.
- Lo interno es del usuario; lo externo, del mercado. No los mezcles.

## 2. CAME (estrategias a partir del DAFO)

| | Oportunidades | Amenazas |
|---|---|---|
| **Fortalezas** | **Explotar** (estrategia ofensiva, FO): usar fortalezas para aprovechar oportunidades | **Mantener/Afrontar** (estrategia defensiva, FA): usar fortalezas para neutralizar amenazas |
| **Debilidades** | **Corregir** (reorientación, DO): corregir debilidades para aprovechar oportunidades | **Afrontar** (supervivencia, DA): minimizar debilidades y evitar amenazas |

Para cada cuadrante, 1–3 acciones concretas. Señala cuál es la **estrategia principal** recomendada.

## 3. Lean Canvas (siempre)

Usa `plantillas/lean-canvas.md`. Tiene 9 bloques:
1. Problema (top 3 y alternativas actuales).
2. Segmentos de clientes y *early adopters*.
3. Propuesta de valor única.
4. Solución.
5. Canales.
6. Fuentes de ingresos.
7. Estructura de costes.
8. Métricas clave.
9. Ventaja injusta.

Marca cada bloque como `[VALIDADO]` o `[HIPÓTESIS]`.

En modo Profundo, o si el usuario lo pide, añade el **Business Model Canvas** (Osterwalder), cuyo enfoque está más en socios, actividades y recursos clave.

## 4. Propuesta de valor

- **Value Proposition Canvas**: tareas, dolores y ganancias del cliente (del módulo 03) frente a productos, aliviadores de dolor y creadores de ganancia.
- **Frase de valor**: "Para [segmento] que [necesidad], [producto] es un [categoría] que [beneficio clave]. A diferencia de [alternativa], [diferencia principal]."
- **Pruebas**: qué evidencia sostiene cada promesa.

## 5. Posicionamiento (método de April Dunford)

1. **Alternativas competitivas**: qué haría el cliente si no existieras (módulo 05).
2. **Atributos únicos**: qué tienes tú que ellos no.
3. **Valor**: qué consigue el cliente gracias a esos atributos.
4. **Clientes que más lo valoran**: el segmento cabeza de playa.
5. **Categoría de mercado**: el contexto en el que te presentas para que el valor sea obvio.
6. (Opcional) **Tendencia** relevante que refuerza el mensaje.

## 6. Diferenciación tipo Océano Azul (opcional, útil en mercados saturados)

Matriz ERRC: qué factores del sector **Eliminar**, **Reducir**, **Incrementar** y **Crear**. Comprueba que el resultado sigue siendo algo por lo que el cliente pagaría.

## 7. Ventaja competitiva sostenible

Para cada ventaja que se alegue, comprueba si es **valiosa, rara, difícil de imitar** y si el negocio está **organizado** para aprovecharla (VRIO). Si cualquier competidor puede copiarla en 3 meses, no es una ventaja sostenible; dilo.

## 8. Opciones estratégicas

Si la evidencia apunta a que la idea original es débil pero hay algo cerca, propone **2–3 variantes** (otro segmento, otro canal, otro modelo de ingresos, una versión más pequeña o una más especializada) y explica qué evidencia las apoya.

## Salidas

- `05-estrategia/dafo.md` (DAFO + CAME; plantilla `plantillas/dafo.md`)
- `05-estrategia/lean-canvas.md`
- `05-estrategia/propuesta-valor.md`
- `05-estrategia/posicionamiento.md`
- `05-estrategia/informe.md` (resumen y estrategia recomendada)
- `05-estrategia/datos.json` → `metricas`:
```json
{
  "dafo": {"fortalezas": [], "debilidades": [], "oportunidades": [], "amenazas": []},
  "came": {"corregir": [], "afrontar": [], "mantener": [], "explotar": []},
  "estrategia_principal": "",
  "propuesta_valor": "",
  "posicionamiento": {"alternativas": [], "atributos_unicos": [], "valor": "", "segmento": "", "categoria": ""},
  "lean_canvas": {"problema": [], "segmentos": [], "propuesta_unica": "", "solucion": [], "canales": [], "ingresos": [], "costes": [], "metricas": [], "ventaja_injusta": ""},
  "variantes": [{"nombre": "", "descripcion": "", "evidencia": []}]
}
```
Cada elemento del DAFO puede ser un texto o un objeto `{"texto": "", "evidencia": ["F3", "C2"]}`.
