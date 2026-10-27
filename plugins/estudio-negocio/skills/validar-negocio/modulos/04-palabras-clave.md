# 04 · Palabras clave y demanda en buscadores

**Preguntas que responde:** ¿La gente busca activamente una solución a esto? ¿Con qué palabras? ¿Cuánto y en qué épocas? ¿Quién ocupa hoy los primeros resultados? ¿Es viable captar clientes por SEO o anuncios de búsqueda?

> Si hay búsquedas, hay **demanda consciente**: la gente ya sabe que quiere algo. Si nadie busca, tendrás que **crear la demanda**, que es más caro y más lento. Esto pesa en el veredicto.

## Proceso

### 1. Semillas
Parte de las palabras que dio el usuario en la entrevista, del mapa de lenguaje del módulo 03 y de los términos que usan los competidores en sus títulos. Incluye:
- Problema ("me duele la espalda al teletrabajar").
- Solución genérica ("silla ergonómica").
- Categoría ("mobiliario oficina en casa").
- Alternativas y competidores ("[marca] opiniones", "alternativa a [marca]").
- Local ("[servicio] en [ciudad]", "[servicio] cerca de mí").

### 2. Expansión
- `scripts/keywords_autocomplete.py`: autocompletado de Google, YouTube, Bing, DuckDuckGo y Amazon, con variantes alfabéticas y de preguntas en español. Sin claves de API. Si una palabra aparece en el autocompletado de varios motores, hay un volumen mínimo de búsquedas.
- Conectores si existen: free-seo-mcp (autocompletado, Trends, Reddit), Ubersuggest o vidIQ (YouTube y TikTok). Ver `referencias/conectores.md`.
- WebSearch de cada semilla: recoge "Otras preguntas de los usuarios" y "Búsquedas relacionadas" cuando aparezcan.

### 3. Volumen y tendencia (estimaciones con su método)
Ninguna fuente gratuita da volúmenes exactos. Combina varias y etiqueta cada cifra con su método:

| Fuente | Qué da | Coste |
|---|---|---|
| Google Keyword Planner | Rangos de volumen mensual y CPC por país | Gratis con una cuenta de Google Ads (sin gastar) |
| Google Trends | Interés relativo 0–100, estacionalidad, regiones, consultas en ascenso | Gratis (web) |
| Autocompletado multimotor | Existencia y popularidad relativa (posición) | Gratis (script) |
| Bing Webmaster Tools | Impresiones reales de Bing por keyword | Gratis (requiere web verificada) |
| Wikipedia pageviews | Interés por un tema a lo largo del tiempo | Gratis (script) |
| Ubersuggest, AnswerThePublic, AlsoAsked | Volumen estimado y preguntas | Freemium con límites diarios |
| Google Search Console | Consultas reales que ya traen tráfico a tu web | Gratis (si ya tienes web) |

Si el usuario no puede abrir Keyword Planner, clasifica el volumen en **niveles** (muy alto, alto, medio, bajo o residual) según Trends y autocompletado, y dilo así. No inventes números.

### 4. Intención
Clasifica cada keyword (el script ya lo hace con reglas; revísalo):
- **Transaccional**: comprar, precio, barato, oferta, contratar, presupuesto, reservar.
- **Comercial**: mejor, opiniones, comparativa, vs, alternativa, top.
- **Local**: cerca de mí, en [ciudad], horario, dirección.
- **Informacional**: qué es, cómo, por qué, ideas, guía.
- **Navegacional**: nombre de una marca concreta.

Las transaccionales, comerciales y locales indican intención de pago. Su CPC en Keyword Planner indica lo que pagan los competidores por un clic, y por tanto la rentabilidad que obtienen de ese cliente.

### 5. Análisis de los resultados de búsqueda (SERP) de las 5–10 keywords clave
Busca cada una y clasifica los 10 primeros resultados: grandes marcas o marketplaces, comparadores o directorios, medios, pymes o webs especializadas, foros o contenido flojo, y el bloque de Google Maps si es una búsqueda local.
- **Dificultad alta**: dominan Amazon, grandes cadenas, comparadores o medios con mucha autoridad.
- **Media**: mezcla de especialistas medianos.
- **Baja**: foros, contenido antiguo o pobre, webs pequeñas. Es una oportunidad.
- Anota si hay **anuncios** arriba y cuántos. Muchos anunciantes indican que la keyword da dinero.

### 6. Agrupación y prioridad
Agrupa por tema y etapa del embudo (descubrimiento, comparación, compra). Prioriza 10–20 keywords combinando volumen, intención, dificultad y encaje. Para cada grupo propone **una página o contenido**, y valora si conviene captar ese tráfico con SEO, con anuncios o con ambos.

### 7. Otras búsquedas
- **Marketplaces**: autocompletado de Amazon y los más vendidos de la categoría.
- **Vídeo y social**: autocompletado de YouTube, TikTok Creative Center (hashtags y tendencias) y Pinterest Trends.
- **Búsqueda con IA**: pregunta a la propia búsqueda web "mejor [categoría] en [ciudad o país]" y anota qué marcas se recomiendan. Indica quién tiene hoy visibilidad.

## Conclusión que debe dar este módulo

- Nivel de **demanda consciente**: alta, media, baja o inexistente. Justifícalo.
- **Tendencia** (sube, estable o baja) y **estacionalidad** (meses pico).
- **Viabilidad del canal de búsqueda**: SEO realista o no, y si los anuncios de búsqueda parecen asumibles con el CPC estimado y el margen.
- Las 10–20 keywords prioritarias.

## Salidas

- `03-palabras-clave/informe.md`
- `03-palabras-clave/keywords.csv` con las columnas `keyword,cluster,intencion,volumen_estimado,nivel_volumen,metodo_volumen,cpc_estimado,dificultad,tendencia,fuentes,prioridad`
- `03-palabras-clave/datos.json` → `metricas`:
```json
{
  "demanda_consciente": "alta|media|baja|inexistente",
  "tendencia": "sube|estable|baja|desconocida",
  "estacionalidad": "",
  "keywords": [{"keyword": "", "intencion": "", "volumen_estimado": null, "nivel_volumen": "", "metodo_volumen": "", "cpc_estimado": null, "dificultad": "alta|media|baja", "prioridad": 1}],
  "viabilidad_seo": "", "viabilidad_sem": ""
}
```
