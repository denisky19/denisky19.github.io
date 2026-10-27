# 03 · Cliente y público objetivo

**Preguntas que responde:** ¿Quién tiene el problema con más intensidad? ¿Cómo lo resuelve hoy? ¿Qué le duele, con qué palabras lo dice y dónde está? ¿Pagaría, cuánto y quién decide la compra?

## 1. Segmentación

Haz una lista de 3–6 segmentos posibles y compáralos:

| Criterio | Pregunta |
|---|---|
| Dolor | ¿Cuánto le duele? ¿Es urgente? |
| Capacidad de pago | ¿Tiene dinero y costumbre de pagar por soluciones? |
| Accesibilidad | ¿Sé dónde encontrarlos y llegar a ellos barato? |
| Tamaño | ¿Hay suficientes en el ámbito? |
| Encaje | ¿Mis recursos y ventajas sirven para este segmento? |

Variables de segmentación:
- **B2C**: demográficas, geográficas, psicográficas (valores, estilo de vida) y **conductuales** (situación, frecuencia, momento de necesidad, que son las más útiles).
- **B2B**: sector (CNAE), tamaño, puesto que decide, madurez digital y momento (crecimiento, nueva normativa).

Elige un **segmento cabeza de playa** (beachhead): el más pequeño que puedas dominar primero. Ver `referencias/marcos-profesionales.md`.

## 2. Voz del cliente: escuchar antes de preguntar

Busca a los clientes hablando **sin que nadie les pregunte**. Es la evidencia más barata y honesta.

| Tipo de cliente | Dónde mirar |
|---|---|
| Consumidor general | Reseñas de 1–3★ en Google Maps, Amazon, Trustpilot y App Store/Google Play de los competidores. Comentarios de YouTube y TikTok. Reddit (r/spain, r/askspain, subreddits temáticos). Foros españoles (Forocoches, Mediavida, Enfemenino, foros sectoriales). Grupos de Facebook (lectura manual) |
| Ocio, viajes, hostelería | Tripadvisor, Google Maps, TheFork, Booking (reseñas) |
| Finanzas personales | Rankia, Reddit r/SpainFIRE, foros de bancos y aseguradoras |
| Padres y familia | Foros de crianza, grupos de colegio, Instagram |
| Pymes y autónomos | Foros de autónomos, grupos de LinkedIn, Reddit r/smallbusiness, r/autonomos, comunidades de gestorías |
| B2B y software | G2, Capterra (con versión española), Product Hunt, Hacker News, LinkedIn, ofertas de empleo (revelan dolores y herramientas) |
| Desarrolladores | GitHub issues, Stack Overflow, Hacker News, Discord |

**Herramientas**
- `scripts/voz_cliente.py`: Reddit, Hacker News y reseñas de App Store. Sin claves de API.
- WebSearch con nombre de sitio y operadores: `site:forocoches.com [tema]`, `[competidor] opiniones`, `[competidor] reseñas 1 estrella`, `"ojalá hubiera" [tema]`, `"alguien conoce" [tema]`, `"estoy harto de" [tema]`.
- WebFetch para leer hilos y páginas de reseñas completas.
- Conectores de Reddit o navegador si están instalados (ver `referencias/conectores.md`).

Para cada evidencia anota: cita literal breve, URL, fecha, plataforma, engagement (votos o respuestas), tipo de evidencia (queja, petición, alternativa usada, precio pagado o desencadenante) y segmento al que pertenece.

**Sesgos que debes declarar**: las reseñas sobrerrepresentan a los muy contentos y a los muy enfadados, Reddit es más técnico y escéptico, los foros tienen poca representatividad demográfica. No extrapoles porcentajes desde aquí; usa estas fuentes para **descubrir temas y lenguaje**.

## 3. Síntesis

- **Jobs To Be Done**: el trabajo funcional ("llevar la contabilidad sin errores"), el emocional ("dormir tranquilo con Hacienda") y el social ("parecer profesional ante mis clientes"). Formato: *Cuando [situación], quiero [motivación], para [resultado]*.
- **Dolores y ganancias** ordenados por frecuencia × intensidad.
- **Desencadenantes**: qué pasa justo antes de buscar una solución.
- **Alternativas actuales**, incluidas no hacer nada, Excel o un cuñado. Es el competidor real.
- **Proceso de compra**: quién inicia, quién influye, quién decide y quién paga; cuánto tarda; qué objeciones aparecen.
- **Señales de disposición a pagar**: cuánto pagan ya por soluciones peores, cuánto cuestan los competidores, quejas sobre el precio (que prueban que pagan) y CPC de las keywords (módulo 04).
- **Dónde están**: medios, redes, comunidades, eventos, influencers y asociaciones. Te servirá para el módulo 08.
- **Mapa de lenguaje**: palabras exactas que usan, que alimentan las keywords y el copy.

## 4. Personas (2–3 como máximo)

Usa `plantillas/persona.md`. Cada rasgo debe venir de la evidencia y llevar su etiqueta. Prohibido inventar nombres y fotos con rasgos sin base; si un rasgo es suposición, márcalo `[HIPÓTESIS]`.

## 5. Kit de investigación primaria (para que lo haga el usuario)

La investigación de escritorio no sustituye hablar con clientes. Entrega siempre:

- **Guion de entrevistas** según *The Mom Test* (`plantillas/guion-entrevista.md`): preguntar por el pasado y el comportamiento, nunca "¿te gustaría…?". Recomienda entre 5 y 10 entrevistas por segmento. Incluye dónde reclutar a esas personas.
- **Encuesta corta** (`plantillas/encuesta.md`, máximo 10 preguntas): filtro, comportamiento actual, gasto actual, intensidad del problema y sensibilidad al precio (Van Westendorp). Con 100 respuestas el margen de error de un porcentaje ronda ±10 puntos; menos de 30 respuestas solo da ideas, no porcentajes. Herramientas gratuitas: Google Forms y Tally.
- **Criterio de éxito**, por ejemplo: "4 de cada 5 entrevistados describen el problema sin que se lo sugieras y al menos 2 ya gastan dinero o tiempo en resolverlo".

## Salidas

- `02-cliente/informe.md` con: segmentos comparados, segmento cabeza de playa, JTBD, dolores y ganancias, desencadenantes, alternativas, proceso de compra, señales de disposición a pagar, dónde están, mapa de lenguaje y citas destacadas (5–10, literales, con URL y fecha).
- `02-cliente/personas.md`
- `02-cliente/guion-entrevistas.md`
- `02-cliente/encuesta.md`
- `02-cliente/evidencias.jsonl`: una línea por evidencia (el script la genera en parte).
- `02-cliente/datos.json` → `metricas`:
```json
{
  "segmento_principal": "",
  "segmentos": [{"nombre": "", "dolor": 0, "pago": 0, "accesibilidad": 0, "tamano": 0, "encaje": 0}],
  "personas": [{"nombre": "", "descripcion": "", "jtbd": "", "dolores": [], "alternativas": [], "canales": [], "disposicion_pago": ""}],
  "citas": [{"texto": "", "fuente": "F#", "url": "", "fecha": ""}],
  "senales_pago": [{"descripcion": "", "tipo": "comportamiento|declarado", "fuentes": []}]
}
```
