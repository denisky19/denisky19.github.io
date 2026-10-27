# Skills existentes para validar ideas de negocio, marketing y ventas

*Investigación del 27-10-2026. Fuentes: GitHub, directorio de plugins de Anthropic y búsquedas web. Comprueba la actividad y la licencia de cada proyecto antes de instalarlo: cambian con frecuencia.*

## Resumen

**Sí existen skills** para validar ideas y hacer marketing con Claude, y algunas son muy buenas. Pero ninguna reunía todo lo que se pedía:
- **En español**, con fuentes de **España y Latinoamérica** (INE, BORME, OEPM, DIRCE, Banco de España, INEGI, DANE…).
- **Todas las áreas** en un solo flujo: mercado, cliente, palabras clave, competencia, DAFO, viabilidad, marketing y ventas, producto, distribución y legal.
- **Preguntas al usuario** antes de investigar, para afinar la búsqueda.
- **Varias vías gratuitas** además del buscador: APIs públicas, conectores y MCP gratuitos.
- **Informes por carpetas** en dos capas: para humanos (Markdown + HTML) y para IAs (JSON + contexto compacto).

Por eso se creó [`plugins/estudio-negocio`](../plugins/estudio-negocio/), que reúne el método de los profesionales y lo mejor de estas skills, escrito desde cero.

## Skills de validación de ideas (todo en uno)

| Skill | Qué hace | Puntos fuertes | Límites para este caso | Licencia |
|---|---|---|---|---|
| [ferdinandobons/startup-skill](https://github.com/ferdinandobons/startup-skill) (~1,2k ★) | `startup-design` (8 fases: research, estrategia, marca, producto, finanzas, validación), `startup-competitors`, `startup-positioning`, `startup-pitch` | Es la más completa. Investigación por oleadas con subagentes, protocolo de honestidad, puerta de entrevistas, `PROGRESS.md`, salida por carpetas, modo rápido | En inglés y pensada para startups tecnológicas. Sin fuentes locales ni salida JSON para IAs. Consume muchos tokens | MIT |
| [emotixco/claude-skills-founder](https://github.com/emotixco/claude-skills-founder) | 13 skills: `/validate-idea` (7 dimensiones, construir/pivotar/matar), competidores, personas, entrevistas, pricing, GTM, landing, pitch… | Comandos cortos y prácticos. Experimentos de < 2 semanas y < 200 $. Carpeta `founder/` compartida | Poca investigación web profunda; cada skill va por separado | MIT |
| [alexeybarinov/business-idea-stress-test](https://github.com/alexeybarinov/business-idea-stress-test) | 6 etapas: interrogatorio, validación temprana, mercado/cliente/competencia, finanzas, abogado del diablo, conclusión | Ledger de evidencia (F/E/C/H/U), fórmulas financieras rigurosas, pre-mortem, una pregunta cada vez | Sin scripts ni fuentes concretas; pensada para ChatGPT | MIT |
| [RohitWaghire/Deep-Market-Reasearch](https://github.com/RohitWaghire/Deep-Market-Reasearch) | Investigación y veredicto GO/PIVOT/KILL | Recetas de búsqueda por fase y rúbrica ponderada con reglas de anulación | Centrada en apps o SaaS; sin licencia publicada | — |
| [EmanuelVogt/skills](https://github.com/EmanuelVogt/skills), [veyralabsgroup/venture-analyst](https://github.com/veyralabsgroup/venture-analyst), [evgeniy038/hypothesis-validator](https://github.com/evgeniy038/hypothesis-validator), [sakshi-gupta-1/idea-teardown-skill](https://github.com/sakshi-gupta-1/idea-teardown-skill), [SensaiXo/kill-it-first](https://github.com/SensaiXo/kill-it-first) | Variantes de "estresar" una idea hasta un veredicto | Ideas útiles: separar hechos de suposiciones, varios revisores críticos | Proyectos pequeños y recientes | Varía |

## Colecciones de marketing, ventas y producto (para ejecutar después)

| Colección | Qué cubre | Cuándo usarla |
|---|---|---|
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 50+ skills: SEO, CRO, copywriting, anuncios, emails, precios, investigación de cliente, perfiles de competidores, lanzamientos, ventas… Comparten un documento de contexto de producto | Cuando el estudio da 🟢 y toca **ejecutar** el marketing. Puedes darle `ia/contexto-ia.md` como contexto. MIT |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Plugins oficiales de Anthropic: **marketing**, **sales**, **product-management**, **small-business** y otros | Campañas, briefs de competencia, llamadas comerciales, especificaciones de producto, gestión de pyme. Apache-2.0 |
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | ~65 skills de producto: market sizing, segmentos, personas, competidores, SWOT, PESTLE, Porter, Lean Canvas, pricing, GTM, beachhead, experimentos, pre-mortem | Profundizar en un marco concreto o en la gestión de producto. MIT |
| Directorio de plugins de Anthropic | **Product Marketing** (comunidad: ICP, personas, posicionamiento, mensajes), **market-researcher** (Anthropic FSI: panorama sectorial y competencia, orientado a inversión) | Posicionamiento B2B SaaS y análisis sectorial |
| [ishwarjha/claude-marketing-research-skill](https://github.com/ishwarjha/claude-marketing-research-skill), [BrianRWagner/ai-marketing-claude-code-skills](https://github.com/BrianRWagner/ai-marketing-claude-code-skills), [OneWave-AI/claude-skills](https://github.com/OneWave-AI/claude-skills), [w95/awesome-claude-corporate-skills](https://github.com/w95/awesome-claude-corporate-skills) | Colecciones amplias de marketing, avatar, posicionamiento y minería de Reddit | Ideas puntuales; calidad desigual |

## Conectores y MCP gratuitos encontrados

| Herramienta | Qué aporta | Coste |
|---|---|---|
| Parallel Search (directorio de claude.ai) | Búsqueda y lectura web | Gratis, sin autenticación |
| Exa, Tavily, Firecrawl | Búsqueda o rastreo para agentes | Créditos gratuitos (consulta las condiciones actuales) |
| Ubersuggest, vidIQ (conectores) | Keywords web y de YouTube/TikTok | Freemium |
| [free-seo-mcp](https://github.com/JohnWayneeee/free-seo-mcp) | Autocompletado, Google Trends, Reddit, sitemaps | Gratis (MIT) |
| [reddit-mcp-buddy](https://github.com/karanb192/reddit-mcp-buddy) | Navegar Reddit sin clave (la búsqueda completa requiere credenciales) | Gratis (MIT) |
| Data Commons MCP (Google) | Estadísticas públicas oficiales | Gratis |
| Playwright MCP, Fetch, DuckDuckGo | Navegador, lectura de URLs, búsqueda alternativa | Gratis |
| Apify | Extractores de Google Maps, reseñas de Amazon, TikTok… | Crédito gratuito mensual |
| Similarweb, Semrush, Ahrefs, Crunchbase, Meltwater | Tráfico, SEO, empresas, medios | **De pago** |

Nota: Google Trends no tiene una API pública abierta. La API oficial está en alfa con acceso por solicitud, y `pytrends` está archivado desde 2025. Por eso la skill usa free-seo-mcp, el navegador o una exportación manual.

## Qué se tomó de cada una (sin copiar texto)

| Idea | Origen | Dónde está en la nueva skill |
|---|---|---|
| Investigación por oleadas con subagentes, `PROGRESO.md` para reanudar, puerta de entrevistas, modo rápido | startup-skill | `SKILL.md` (pasos 0, 5) |
| Ledger de evidencia y separación entre volumen de transacciones, ingresos, beneficio y caja | business-idea-stress-test | Reglas de evidencia, `modulos/07` |
| Rúbrica ponderada con reglas de anulación y "en la duda, la nota baja" | Deep-Market-Research, startup-skill | `modulos/11`, `scripts/puntuacion.py` |
| Experimentos baratos con umbral de éxito y de parada | claude-skills-founder | `modulos/11`, `plantillas/experimento.md` |
| Observado / inferido / implicación; "no observado ≠ no existe" | marketingskills (competitor-profiling) | `modulos/05` |
| Documento de contexto compartido para otras skills | marketingskills (product-marketing) | `ia/contexto-ia.md` |

**Añadido nuevo**:
- Entrevista con "preguntas para afinar la búsqueda".
- Arquetipos de negocio (local, ecommerce, SaaS, servicios, marketplace, franquicia, fabricación, infoproducto).
- Catálogo de fuentes oficiales gratuitas por país.
- Módulos de palabras clave, distribución y legal.
- DAFO + CAME.
- Scripts sin claves de API (autocompletado multimotor, Reddit, HN, App Store, INE, Eurostat, Banco Mundial, Wikipedia, GDELT, ficha web de competidores, modelo financiero con sensibilidad, puntuación, panel HTML).
- Capa de datos JSON para IAs.

## Fuentes de esta investigación

- [GitHub topic: startup-validation](https://github.com/topics/startup-validation)
- [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
- [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)
- [phuryn/pm-skills](https://github.com/phuryn/pm-skills) · [Product Compass: PM Skills Marketplace](https://www.productcompass.pm/p/pm-skills-marketplace-claude)
- [ferdinandobons/startup-skill](https://github.com/ferdinandobons/startup-skill) · [emotixco/claude-skills-founder](https://github.com/emotixco/claude-skills-founder) · [alexeybarinov/business-idea-stress-test](https://github.com/alexeybarinov/business-idea-stress-test) · [RohitWaghire/Deep-Market-Reasearch](https://github.com/RohitWaghire/Deep-Market-Reasearch)
- [free-seo-mcp](https://github.com/JohnWayneeee/free-seo-mcp) · [reddit-mcp-buddy](https://github.com/karanb192/reddit-mcp-buddy)
- Sobre Google Trends y pytrends: [Scrapfly: alternativas a la API de Google Trends](https://scrapfly.io/blog/posts/google-trends-api-alternatives)
- Data Commons MCP: [InfoQ](https://www.infoq.com/news/2025/10/data-commons-mcp-server)
- Bibliotecas de anuncios gratuitas: [Atria: cómo encontrar los anuncios de la competencia](https://www.tryatria.com/blog/how-to-find-your-competitors-ads)
- API del INE: [Referencia de la API](https://ine.es/dyngs/DAB/index.htm?cid=1100)
