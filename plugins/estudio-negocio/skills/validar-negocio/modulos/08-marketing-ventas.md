# 08 · Marketing y ventas (go-to-market)

**Preguntas que responde:** ¿Cómo llegarán los primeros 100 clientes? ¿Por qué canales, con qué mensaje y a qué coste? ¿Cómo se convierte un interesado en comprador? ¿Qué hay que medir?

Este módulo **consume** los anteriores: segmento y lenguaje (03), keywords (04), canales y anuncios de los competidores (05), posicionamiento (06) y margen y CAC asumible (07). No inventes la estrategia desde cero.

## 1. Mensaje

- Propuesta de valor en una frase (del módulo 06).
- 3 mensajes clave, cada uno con su prueba (dato, testimonio o demostración).
- Respuestas a las 3–5 objeciones más probables (del módulo 03).
- Usa **las palabras del cliente** (mapa de lenguaje), no jerga interna.

## 2. Marketing mix

- **4P** (producto, precio, distribución, promoción) para producto.
- **7P** si es un servicio: añade personas, procesos y evidencia física (local, web, uniformes, materiales).

Resume cada P en 2–3 líneas coherentes con el posicionamiento.

## 3. Canales: método Bullseye (de *Traction*, Weinberg y Mares)

1. **Haz una lluvia de ideas** con los 19 canales de captación: PR, PR no convencional, anuncios en buscadores (SEM), anuncios en redes y display, publicidad offline, SEO, marketing de contenidos, email marketing, *engineering as marketing* (herramientas gratuitas), blogs e influencers del nicho, desarrollo de negocio (alianzas), venta directa, afiliados, plataformas existentes (marketplaces, tiendas de apps), ferias, eventos presenciales, conferencias y comunidad.
2. **Haz un ranking** de los 3–5 más prometedores según dónde está el cliente (03), qué funciona a los competidores (05: anuncios activos, tráfico, presencia) y el CAC que permite el margen (07).
3. **Diseña una prueba barata** para cada uno de los 3 primeros: presupuesto, duración y métrica de éxito.
4. **Concéntrate** en el canal que gane y no disperses el esfuerzo.

Canales típicos por arquetipo (detalle en `referencias/arquetipos.md`):
- **Local**: ficha de Google Business Profile y reseñas, SEO local, Instagram y TikTok locales, alianzas con negocios vecinos, buzoneo o cartelería segmentada, eventos de apertura y apps de reparto o reserva.
- **Ecommerce**: Meta Ads, Google Shopping, marketplaces, influencers o UGC, email y SMS, SEO de categoría.
- **SaaS B2B**: SEO de problema, contenido, LinkedIn, venta directa, partners e integraciones, marketplaces de apps.
- **Servicios profesionales**: recomendaciones, LinkedIn, alianzas con prescriptores (gestorías, colegios profesionales), contenido de autoridad y eventos.

**El coste de captar un cliente (CAC) que permite el negocio = margen de contribución por cliente (o LTV) / 3**, como referencia prudente. Compáralo con el coste real esperado del canal, usando el CPC del módulo 04 y conversiones de referencia marcadas como hipótesis.

## 4. Embudo y métricas (AARRR)

Para cada etapa (Adquisición, Activación, Retención, Referencia e Ingresos) define el **evento** que la marca, la **métrica** y un **objetivo inicial** (marcado `[HIPÓTESIS]` hasta que haya datos). Elige una **métrica norte** (*North Star*) que refleje el valor entregado al cliente.

## 5. Ventas

**B2C**: ¿compra impulsiva o meditada? Recorrido del cliente (descubre, compara, compra, usa, repite o recomienda), puntos de fricción, ofertas de lanzamiento, garantía, prueba gratuita o muestra y política de devoluciones.

**B2B**:
- ICP y quién decide.
- Lista de cuentas objetivo: cómo construirla (directorios sectoriales, LinkedIn, asociaciones, DIRCE para dimensionar).
- Secuencia de contacto, demo o propuesta.
- Duración del ciclo de venta y pipeline necesario para el objetivo:
```
clientes objetivo / tasa de cierre = oportunidades / tasa de conversión de contacto a oportunidad = contactos necesarios
```

En España la LSSI restringe el email comercial no solicitado, también a empresas. Antes de plantear emailing en frío, revisa los criterios de la AEPD y prioriza el contacto con base legítima (LinkedIn, eventos, recomendaciones, formularios).

## 6. Plan de los primeros 100 clientes

Acciones concretas, con nombres de comunidades, medios, eventos o socios encontrados en la investigación. Mal: "hacer redes sociales". Bien: "publicar en los 3 grupos de Facebook de madres de [barrio] encontrados (F21–F23) la oferta de inauguración; objetivo: 40 reservas".

## 7. Lanzamiento y plan de 90 días

Calendario semanal o quincenal con:
- **Preparación** (mensaje, web o ficha, primeras reseñas, lista de espera).
- **Lanzamiento** (oferta, evento, PR local o de nicho, comunidades).
- **Optimización** (medir, cortar lo que no funcione, doblar lo que sí).

Presupuesto por partida y KPI de control.

## Salidas

- `07-marketing-ventas/plan-gtm.md` (todo lo anterior)
- `07-marketing-ventas/datos.json` → `metricas`:
```json
{
  "mensaje_principal": "",
  "canales": [{"canal": "", "prioridad": 1, "por_que": "", "prueba": "", "presupuesto": 0, "metrica_exito": "", "cac_estimado": null, "fuentes": []}],
  "cac_maximo_asumible": null,
  "north_star": "",
  "embudo": [{"etapa": "adquisicion", "metrica": "", "objetivo": ""}],
  "presupuesto_lanzamiento": 0
}
```
