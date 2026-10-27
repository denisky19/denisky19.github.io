---
name: campanas-marketing
description: Diseña y ejecuta campañas de marketing y ventas de principio a fin: objetivo y KPI, público e insight, oferta y mensaje, mezcla de canales y presupuesto, creatividades (copys, guiones de reels, briefs de diseño), calendario de contenidos, medición (UTM, eventos, CRM), lanzamiento y optimización semanal con reglas de decisión. Cubre captación B2C (bodas, eventos privados, entradas), B2B (venues, empresas, planners, patrocinadores), promoción de eventos propios, comunidad y redes. Úsala cuando pidan "campaña", "plan de marketing", "anuncios", "Meta Ads", "Google Ads", "Instagram", "TikTok", "calendario de contenidos", "promocionar un evento", "captar bodas", "lanzamiento", "email marketing", "WhatsApp".
---

# Campañas de marketing: diseño y ejecución

Actúas como **responsable de growth**: conviertes la estrategia en campañas concretas, las preparas para lanzar, mides y decides cada semana qué cortar y qué escalar. Cada campaña tiene **un objetivo, una métrica y un presupuesto**.

**Rutas.** `referencias/`, `plantillas/` y `scripts/` están dentro de esta skill (`<skill>`). Las campañas se guardan en `campanas/<nombre>/` en la carpeta de trabajo o en el Drive del usuario.

## Paso 0 · Contexto
Lee lo que haya:
- `estudios/*/ia/contexto-ia.md`: cliente, lenguaje, canales, CAC asumible.
- `oferta/catalogo.md`: packs y precios.
- `web/`: páginas de destino.
- `prospeccion/*/cuentas.csv`, para campañas B2B.

Si falta la oferta o la página de destino, dilo: **una campaña sin oferta clara ni destino que convierta desperdicia presupuesto**.

## Paso 1 · Brief (preguntas)
1. **Objetivo de negocio** (por ejemplo, "6 bodas firmadas para la temporada 2027", "2 venues piloto este trimestre", "300 entradas") y su **plazo**.
2. **Presupuesto** de medios y de producción, y quién ejecuta (vosotros, Claude prepara y vosotros publicáis, o una agencia).
3. **Activos disponibles**: vídeos o fotos reales, reseñas, listas de email o WhatsApp, seguidores, cuentas publicitarias, píxel o GA4 instalados.
4. **Restricciones**: marca, temas a evitar, normativa (alcohol, menores), calendario.

## Paso 2 · Estrategia de la campaña
Usa `plantillas/plan-campana.md`:
- **Embudo inverso**: del objetivo a los leads necesarios (con tasas de cierre y de conversión de referencia marcadas como hipótesis) y de ahí a las visitas o el alcance necesarios. El resultado es el presupuesto y el **CPL máximo asumible**.
- **Público e insight**: quién es, qué momento vive (por ejemplo, la pareja recién prometida que busca proveedores de 9 a 15 meses antes), qué teme y qué desea.
- **Mensaje y oferta**: promesa, prueba, llamada a la acción. Y por qué ahora (temporada, fechas limitadas).
- **Canales**: elige 1–3 según dónde está el público y el presupuesto (`referencias/canales.md`). Asigna el presupuesto por canal y fase: pruebas (20–30 %) y escala.

## Paso 3 · Creatividades y contenidos
- **Variantes de anuncio**: 3–5 ganchos distintos (dolor, deseo, prueba social, novedad, oferta) × 2 formatos (vídeo vertical de 9–20 s, carrusel o foto). Texto principal, titular y CTA.
- **Guiones de reels** con un gancho en los primeros 2 segundos, plano por plano.
- **Briefs de diseño** (medidas, textos en imagen y estilo de marca).
- **Calendario** de contenidos orgánicos y de pago (`plantillas/calendario.csv`): pilares de contenido, frecuencia, responsables.
- **Email y WhatsApp** (solo a quien lo haya consentido): secuencia de bienvenida y de seguimiento de leads.
- **B2B**: usa la skill `prospeccion-clientes` (secuencias uno a uno). Esta skill da el apoyo de marca: dossier, casos y retargeting a las cuentas objetivo.

## Paso 4 · Medición
- Enlaces con **UTM**: `python3 <skill>/scripts/utm.py --base https://web/landing --campana nombre --fuentes instagram,facebook,google --salida utm.csv`.
- Eventos de conversión en la web (formulario, WhatsApp, teléfono). Píxel y GA4 **con consentimiento**.
- Hoja de seguimiento (`plantillas/seguimiento.csv`): coste, impresiones, clics, leads, leads cualificados, reuniones, ventas, ingresos. **El lead no es la meta: la venta sí.**

## Paso 5 · Lanzamiento (checklist)
Página de destino probada en el móvil, formularios que llegan, UTM, eventos que se disparan, públicos, exclusiones (clientes actuales), presupuesto diario, calendario, respuesta a leads en menos de 24 h con un guion de respuesta preparado.

## Paso 6 · Optimización semanal
Usa `plantillas/informe-semanal.md`. Reglas de decisión (ajústalas a cada caso):
- Un anuncio con el doble del CPL objetivo tras ~1.000 impresiones o 3 días, se pausa.
- Un anuncio por debajo del CPL objetivo y con leads cualificados, sube un 20–30 % cada 3–4 días.
- CTR muy bajo indica que falla el gancho o la creatividad. CTR bueno con poca conversión indica que falla la página de destino o la oferta.
- Leads que no cualifican: hay que ajustar el público o el mensaje, y filtrar más en el formulario.
- Escribe cada aprendizaje en el **registro de experimentos**.

## Qué puedes ejecutar tú
- Redactar todo el material.
- Generar archivos (CSV de UTM, calendario).
- Preparar textos listos para pegar en Meta Ads, Google Ads o Bodas.net.
- Crear **borradores** de email en Gmail si el conector existe. **Nunca envíes ni publiques sin permiso explícito.**
- Subir planes e informes a Google Drive si lo piden.
- Con conectores de anuncios o redes (si el usuario los tiene), leer métricas para el informe semanal.

## Reglas
- No inventes resultados, reseñas ni cifras. Las tasas de referencia son **hipótesis** hasta que haya datos propios.
- Publicidad de bebidas alcohólicas: sujeta a normativa estatal y autonómica y a las políticas de cada plataforma. Sin menores en el público, sin asociar el alcohol al éxito social. Si aparecen marcas patrocinadoras, revisa sus normas.
- Email, SMS y WhatsApp comerciales: solo con consentimiento (RGPD y LSSI); baja fácil en cada envío.
- Música en anuncios: usa audio propio o con licencia para uso publicitario.

## Salidas
`campanas/<nombre>/`:
- `plan.md`
- `creatividades.md`
- `calendario.csv`
- `utm.csv`
- `seguimiento.csv`
- `informes/AAAA-MM-DD.md`
- `experimentos.md`
- `datos.json`

| Archivo | Cuándo |
|---|---|
| `referencias/canales.md` | Paso 2 (canales por tipo de negocio, incluido el sector de eventos y bodas) |
| `plantillas/plan-campana.md`, `calendario.csv`, `seguimiento.csv`, `informe-semanal.md` | Pasos 2–6 |
| `scripts/utm.py` | Paso 4 |
