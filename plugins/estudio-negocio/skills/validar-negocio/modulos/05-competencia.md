# 05 · Competencia

**Preguntas que responde:** ¿Contra quién compito de verdad? ¿Qué ofrecen, a qué precio y cómo captan clientes? ¿Qué odian sus clientes? ¿Dónde está el hueco? ¿Qué fuerza tiene cada actor del sector?

## 1. Identifica a todos los competidores, no solo a los obvios

| Tipo | Ejemplo para una app de recetas para celíacos |
|---|---|
| **Directos** | Otras apps de recetas sin gluten |
| **Indirectos** | Apps de recetas generales, blogs, cuentas de Instagram |
| **Sustitutos** | Comprar platos preparados sin gluten, comer fuera |
| **No hacer nada** | Seguir con las 5 recetas de siempre |
| **Análogos en otros países** | El líder en EE. UU. o Alemania, que muestra el modelo y lo que funciona |

Cómo encontrarlos: `mejor [categoría] [país/ciudad]`, `[categoría] opiniones`, `alternativas a [conocido]`, `[conocido] vs`, keywords del módulo 04 (quién sale arriba y quién se anuncia), Google Maps para negocios locales, Product Hunt, G2 o Capterra para software, Amazon (más vendidos) para producto, y asociaciones o ferias del sector.

Número de competidores a perfilar: Express 3–5, Estándar 5–8, Profundo 8–15.

## 2. Ficha por competidor

Usa `plantillas/ficha-competidor.md`. Rellena solo con lo **observado** y separa siempre lo observado, lo inferido y la implicación.

- **Qué venden y a quién**: propuesta de valor literal de su web (título y subtítulo).
- **Precio**: página de precios leída con WebFetch, carta, tarifas o precio en marketplaces. Anota la fecha. "Sin precio público" no significa ni caro ni gratis.
- **Tamaño y antigüedad**:
  - España: facturación y empleados con fragmentos gratuitos de Infoempresa, eInforma, Empresite o Axesor (búsqueda `"[razón social]" facturación empleados`); fecha de constitución y capital en BORME o LibreBOR; cuentas anuales en el Registro Mercantil (de pago, unos pocos euros).
  - Antigüedad de la web con `scripts/competidor_web.py` (primera captura en Wayback Machine).
- **Tracción**: nº de reseñas y valoración media (Google Maps, Trustpilot, tiendas de apps), seguidores (Social Blade), tráfico estimado (vista gratuita de Similarweb si es accesible) y ofertas de empleo (que indican crecimiento y prioridades).
- **Cómo captan clientes**:
  - Anuncios activos en la Meta Ad Library, el Google Ads Transparency Center y el TikTok Creative Center. Un anuncio activo durante meses suele indicar que es rentable.
  - Keywords en las que aparecen y contenido que publican.
  - Marketplaces, distribuidores y afiliados.
- **Tecnología y canal**: `scripts/competidor_web.py` detecta Shopify, WooCommerce, WordPress, Wix, PrestaShop, píxeles de anuncios, herramientas de email y chat, etc.
- **Qué opinan sus clientes**: reseñas de 1–3★ (huecos y quejas) y de 4★ (qué valoran y qué les falta). Cita literal con URL y fecha.
- **Fortalezas, debilidades y vulnerabilidad**: dónde podrías ganarle.

**Regla**: "no observado" no significa "no existe". Escribe "no observado en [páginas revisadas], a [fecha]". Nunca atribuyas motivos ("lo hacen porque…") salvo que lo hayan dicho públicamente.

## 3. Negocios locales

En un radio de influencia de 5–10 minutos andando o 10–15 en coche:
- Número de competidores y su ubicación (Google Maps).
- Valoración media y número de reseñas. El nº de reseñas es un indicador aproximado de afluencia.
- Horarios, precios o carta, especialización y huecos (horas, servicios o público no cubiertos).
- Locales cerrados recientemente (busca noticias y reseñas tipo "cerrado permanentemente"): son señales de alerta.

## 4. Análisis

- **Matriz comparativa** (`04-competencia/matriz.csv`): nombre, tipo, URL, propuesta, precio, modelo, segmento, tamaño, valoración, canales, fortaleza, debilidad y fuentes.
- **Mapa de posicionamiento**: elige dos ejes que importen al cliente (precio frente a especialización, rapidez frente a personalización…) y sitúa a todos. Puede ser una tabla o un diagrama en texto. Señala los espacios vacíos y explica **si están vacíos porque nadie los quiere**.
- **Las 5 fuerzas de Porter**: rivalidad, amenaza de entrantes (barreras), poder de proveedores, poder de clientes y sustitutos. Cada fuerza se califica como alta, media o baja con su justificación.
- **Benchmark de precios**: rango, mediana y dónde encajaría el usuario.
- **Hueco competitivo**: qué necesidad del módulo 03 no cubre bien nadie y si es suficientemente grande.
- **Battle card del competidor principal**: cuándo ganas tú, cuándo gana él, cómo responder a "¿y por qué no [competidor]?".

## Recetas de búsqueda

```
mejor [categoría] [ciudad/país] [año]
[categoría] comparativa precios
alternativas a [competidor]
[competidor] opiniones / reseñas / quejas / estafa
[competidor] facturación empleados
"[razón social]" BORME
[competidor] cierra / despidos / ronda de inversión
[competitor] pricing / reviews / alternatives / vs
[categoría] site:producthunt.com    (software)
[categoría] más vendidos amazon.es (producto)
```

## Salidas

- `04-competencia/informe.md`: mapa de competidores por tipo, resumen de fichas, matriz, posicionamiento, Porter, precios, hueco y battle card.
- `04-competencia/fichas/<competidor>.md`
- `04-competencia/matriz.csv`
- `04-competencia/datos.json` → `metricas`:
```json
{
  "intensidad_competitiva": "alta|media|baja",
  "competidores": [{"nombre": "", "url": "", "tipo": "directo|indirecto|sustituto|analogo", "precio": "", "modelo": "", "tamano": "", "valoracion": "", "fortalezas": [], "debilidades": [], "fuentes": []}],
  "porter": {"rivalidad": "", "entrantes": "", "proveedores": "", "clientes": "", "sustitutos": ""},
  "precios": {"min": null, "mediana": null, "max": null, "unidad": ""},
  "hueco": ""
}
```
