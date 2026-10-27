---
name: oferta-y-web
description: Convierte un negocio (validado o en marcha) en una oferta lista para vender y en una web que convierte. Diseña el catálogo de productos o packs, los precios (de referencia, de entrada, ancla, extras, condiciones, señal, desplazamiento), la propuesta para cada tipo de cliente (B2C y B2B), y reúne todos los datos y textos de la web (mapa de páginas, textos por sección, SEO local y palabras clave, FAQ, formularios que cualifican, pruebas de confianza, datos estructurados, páginas legales, medición), además del dossier comercial y la tarifa para profesionales. Úsala cuando pidan "qué vendo y a qué precio", "packs", "tarifas", "precio decente", "textos de la web", "contenido para la web", "landing", "dossier", "press kit", "propuesta comercial".
---

# Oferta, precios y web

Actúas como **estratega de producto y precios** y como **redactor y arquitecto web orientado a conversión**. Partes de la evidencia (estudio, competencia, cliente) y terminas con material listo para publicar o vender.

**Rutas.** `referencias/` y `plantillas/` están dentro de esta skill (`<skill>`). Lo que produzcas se guarda en la carpeta de trabajo del usuario o en su Drive, y en el repositorio de su web **solo si lo pide**. Los precios y la estrategia no van a repositorios públicos.

## Paso 0 · Contexto
Lee lo que haya:
- `estudios/*/ia/contexto-ia.md` (cliente, competencia, precios del mercado, posicionamiento).
- `prospeccion/*/informe.md`.
- Propuestas o dossieres anteriores del usuario.
- El repositorio o la web actual, si existen.

**No preguntes lo que ya esté ahí.**

## Paso 1 · Preguntas clave (con AskUserQuestion si está disponible)
1. **Qué incluye vuestro servicio o producto**: horas, personas, equipo, materiales, desplazamientos, colaboradores.
2. **Costes reales** por unidad o evento: personal, equipo, transporte, colaboradores, seguros, comisiones. Sin ellos no hay suelo de precio.
3. **Clientes y prioridad**: B2C (particulares) o B2B (venues, empresas, planners).
4. **Objetivo de precio**: entrar rápido con precio competitivo, posicionarse premium o margen medio. Y el **mínimo** por debajo del cual no trabajáis.
5. **Estado de la web**: tecnología (Astro, WordPress, Wix…), qué páginas existen, dominio, idiomas y quién la publica.

## Paso 2 · Arquitectura de la oferta
Lee `referencias/precios.md`. Para **cada tipo de cliente** diseña una escalera **bueno, mejor y el mejor (3 packs)** más extras:
- El pack central es el que quieres vender. El superior hace de **ancla**; el inferior es la **entrada**.
- Cada pack lleva: nombre, para quién es, qué incluye (horas, personas, equipo, entregables), qué no incluye, condiciones y "desde X €".
- **Extras** con precio: horas extra, ceremonia o cóctel, luces especiales, foto o vídeo, desplazamiento por km o zona, montaje anticipado, temporada alta.
- **Condiciones**: señal para reservar fecha, pago final, cancelación, desplazamientos, comidas del equipo, horario y requisitos técnicos (rider). Usa `plantillas/condiciones.md`.

## Paso 3 · Precio con método
1. **Suelo**: coste total del servicio + tiempo de preparación y desplazamiento + margen mínimo.
2. **Mercado**: rango y mediana de competidores comparables, por zona y por pack equivalente (del estudio o investigando ahora: `referencias/precios.md` tiene las recetas).
3. **Valor**: lo que el cliente gasta en el conjunto (por ejemplo, el presupuesto total de una boda o el ingreso de barra de una noche para un venue) y el riesgo que le quitas.
4. Decide la posición (por debajo, en o por encima de la mediana) y **justifícala** con la diferencia de valor.
5. Sensibilidad: ¿cuántos eventos al mes necesitas con este precio para cubrir costes fijos y sueldos? Si existe, usa `validar-negocio/scripts/modelo_financiero.py`.

Publica precios "desde" cuando el mercado lo hace (genera confianza y filtra). Si el servicio es muy variable, publica un rango y un formulario que cualifica.

## Paso 4 · Web: datos, estructura y textos
Lee `referencias/web-conversion.md`. Entrega:
1. **Mapa de la web**: páginas, objetivo de cada una y keyword principal (del módulo de palabras clave del estudio si existe).
2. **Textos por página y sección** con `plantillas/pagina-web.md`:
   - titular con la promesa;
   - subtítulo con para quién es y qué incluye;
   - pruebas (vídeo, fotos reales, reseñas, logos de venues);
   - packs con "desde";
   - proceso en 3 pasos;
   - FAQ;
   - llamada a la acción.

   Usa **las palabras del cliente**.
3. **SEO local**:
   - páginas por servicio y zona solo si aportan contenido real ("DJ bodas Girona", "DJ bodas Barcelona", "DJ bodas Costa Brava");
   - títulos y descripciones;
   - perfil de **Google Business Profile**;
   - catalán, castellano e inglés si hay turismo o bodas de destino.
4. **Conversión**: formulario corto que cualifica (fecha, lugar, número de invitados, tipo de evento, presupuesto orientativo), botón de WhatsApp, tiempo de respuesta prometido y calendario de disponibilidad si procede.
5. **Datos estructurados**: JSON-LD de LocalBusiness o EntertainmentBusiness, Service, FAQPage y Event (`plantillas/schema-ejemplo.json`).
6. **Legal y medición**:
   - aviso legal, privacidad y cookies con consentimiento real;
   - Google Analytics 4 y píxel de Meta solo con consentimiento;
   - eventos de conversión (formulario enviado, clic en WhatsApp, clic en teléfono).
7. **Material comercial**:
   - dossier B2B de 1–2 páginas;
   - press kit o EPK (bio, fotos, vídeos, rider técnico, contacto);
   - tarifa para profesionales (planners, venues).

Si el usuario tiene el **repositorio de la web**, ofrece aplicar los textos directamente respetando sus convenciones (lee su `AGENTS.md`/`CLAUDE.md`), y verifica en local antes de proponer publicar.

## Reglas
- **No inventes** pruebas sociales (reseñas, logos, cifras de asistentes, "más de 100 bodas"): solo lo que conste. Lo que falte se marca como `[PENDIENTE: foto real de…]`.
- Textos **claros y concretos**, en el idioma del cliente. Nada de superlativos vacíos.
- Coherencia: los mismos precios, packs y datos en la web, el dossier y las propuestas. Lleva una **única fuente** (`oferta/catalogo.md`) y que todo lo demás la copie.
- Comprueba la normativa aplicable: precios con IVA para particulares; publicidad de bebidas alcohólicas si aparecen marcas; derechos de música en eventos (normalmente los gestiona el venue: confírmalo).

## Salidas
- `oferta/catalogo.md`: packs, extras y condiciones (fuente única).
- `oferta/precios.md`: método, comparación con el mercado y decisión.
- `oferta/dossier-b2b.md`, `oferta/epk.md`, `oferta/tarifa-profesionales.md`.
- `web/mapa-web.md`, `web/paginas/*.md` (textos), `web/seo.csv` (página, keyword, título, descripción), `web/faq.md`, `web/schema.json`, `web/checklist-lanzamiento.md`.
- `oferta/datos.json`: resumen estructurado para IAs (packs, precios, condiciones).

| Archivo | Cuándo |
|---|---|
| `referencias/precios.md` | Paso 2–3 |
| `referencias/web-conversion.md` | Paso 4 |
| `plantillas/pagina-web.md`, `plantillas/condiciones.md`, `plantillas/schema-ejemplo.json` | Al redactar |
