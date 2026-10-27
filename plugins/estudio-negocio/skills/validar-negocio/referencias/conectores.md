# Herramientas y conectores (gratuitos primero)

Regla: **no te limites a un buscador.** Para cada necesidad, usa la primera opción disponible de la cascada y combina varias vías. Al empezar, comprueba qué tienes y anótalo en `PROGRESO.md`. Si falta algo gratuito que cambiaría mucho la calidad, **sugiérelo una vez** con el comando de instalación y sigue con lo que haya.

Las condiciones de los planes gratuitos cambian: indícale al usuario que las confirme en la web del proveedor.

## 1. Cascada por necesidad

| Necesidad | 1ª opción | 2ª opción | 3ª opción |
|---|---|---|---|
| Búsqueda general | Búsqueda web integrada (WebSearch) | Conector Parallel Search, Exa o Tavily | MCP de DuckDuckGo |
| Leer una página entera | WebFetch | MCP Fetch o Firecrawl | Navegador (Playwright MCP) para páginas con JavaScript |
| Keywords y autocompletado | `scripts/keywords_autocomplete.py` | free-seo-mcp, Ubersuggest | Keyword Planner (el usuario) |
| Tendencias de búsqueda | free-seo-mcp (Trends) | Google Trends (pedir captura o CSV al usuario) | `datos_publicos.py wikipedia` y `gdelt` |
| Voz del cliente | `scripts/voz_cliente.py` (Reddit, HN, App Store) | reddit-mcp-buddy | WebSearch con `site:` en foros y reseñas |
| Estadística oficial | `scripts/datos_publicos.py` (INE, Eurostat, Banco Mundial) | MCP de Data Commons | WebFetch a las tablas del INE o Eurostat |
| Competidor (web) | `scripts/competidor_web.py` + WebFetch | Firecrawl | Navegador |
| Competidores locales | WebSearch "[negocio] en [zona]" + reseñas | Navegador en Google Maps | Apify (extractor de Google Maps, consume crédito) |
| Anuncios de los competidores | Navegador en Meta Ad Library, Google Ads Transparency y TikTok Creative Center | Pedir capturas al usuario | — |
| Guardar o compartir informes | Archivos locales (siempre) | Conector Google Drive | Claude Docs o Notion |
| Preguntar al usuario | AskUserQuestion (Claude Code) | Preguntas numeradas en el chat | — |
| Paralelizar la investigación | Agent (subagentes, en Claude Code) | Secuencial | — |

## 2. Herramientas integradas según la app

- **Claude Code** (terminal, escritorio o web): WebSearch, WebFetch, Bash (ejecuta `scripts/`), Agent (subagentes en paralelo), AskUserQuestion y los MCP que añadas con `claude mcp add`.
- **claude.ai, Claude Desktop y Cowork**: búsqueda web, ejecución de código (si está activada; puede tener la red restringida) y conectores en *Ajustes → Conectores*. Para subir la skill: *Ajustes → Capacidades → Skills* (archivo `.zip`).

## 3. Conectores del directorio de claude.ai útiles para este estudio

| Conector | Para qué | Coste |
|---|---|---|
| **Parallel Search** | Búsqueda y lectura web eficiente | Aparece como gratuito y sin autenticación en el directorio |
| **Exa** | Búsqueda web semántica (encontrar competidores "parecidos a…") | Plan gratuito con créditos |
| **Ubersuggest** | Keywords, volúmenes estimados, competidores SEO | Freemium (límites diarios) |
| **vidIQ** | Keywords y tendencias en YouTube, TikTok e Instagram | Freemium |
| **Google Drive** | Guardar el resumen y el HTML | Gratis |
| **Notion** y **Claude Docs** | Documentos vivos del estudio | Gratis o según el plan |
| Similarweb, Semrush, Ahrefs, Crunchbase, Meltwater, Supermetrics | Tráfico, SEO, empresas, medios | **De pago**: úsalos solo si el usuario ya los tiene |

## 4. Servidores MCP gratuitos para Claude Code o Desktop

Comandos para Claude Code (en Desktop, equivalente en `claude_desktop_config.json`). Revisa el repositorio de cada uno antes de instalar, porque los comandos pueden cambiar. Hay un ejemplo listo para copiar en `conectores/mcp-gratuitos.example.json` del plugin.

| MCP | Qué añade | Clave | Instalación |
|---|---|---|---|
| **free-seo-mcp** (github.com/JohnWayneeee/free-seo-mcp, MIT) | Autocompletado multimotor, Google Trends (comparar, relacionadas, por región), Reddit, sitemaps de competidores | No (Bing opcional) | `git clone https://github.com/JohnWayneeee/free-seo-mcp && cd free-seo-mcp && uv sync` y después `claude mcp add free-seo -- uv run --directory /ruta/free-seo-mcp free-seo-mcp` |
| **reddit-mcp-buddy** (MIT) | Navegar subreddits sin clave; la búsqueda completa requiere credenciales de Reddit | No para navegar | `claude mcp add --transport stdio reddit-mcp-buddy -s user -- npx -y reddit-mcp-buddy` |
| **Playwright MCP** (Microsoft) | Navegador real: Google Maps, bibliotecas de anuncios, páginas con JavaScript | No | `claude mcp add playwright -- npx @playwright/mcp@latest` |
| **Fetch** (servidor de referencia de MCP) | Leer URLs y convertirlas a Markdown | No | `claude mcp add fetch -- uvx mcp-server-fetch` |
| **DuckDuckGo** | Búsqueda alternativa sin clave | No | `claude mcp add ddg -- uvx duckduckgo-mcp-server` |
| **Data Commons** (Google) | Estadísticas públicas oficiales unificadas | Gratuita (según su documentación) | Paquete `datacommons-mcp` en PyPI; ver docs.datacommons.org/mcp |
| **Tavily** | Búsqueda y extracción para agentes | Gratuita con créditos mensuales | `claude mcp add --transport http tavily "https://mcp.tavily.com/mcp/?tavilyApiKey=TU_CLAVE"` |
| **Exa** | Búsqueda semántica | Gratuita con créditos | `claude mcp add --transport http exa https://mcp.exa.ai/mcp` |
| **Firecrawl** | Rastreo y extracción de webs completas | Gratuita con créditos | `claude mcp add firecrawl -e FIRECRAWL_API_KEY=TU_CLAVE -- npx -y firecrawl-mcp` |
| **Apify** | Miles de extractores (Google Maps, reseñas de Amazon, TikTok…) | Crédito gratuito mensual; cada extracción lo consume | `claude mcp add --transport http apify https://mcp.apify.com` |

## 5. Herramientas web gratuitas sin conector

Úsalas con el navegador (Playwright MCP) o pide al usuario una captura o exportación:
- Google Trends.
- Google Keyword Planner (cuenta de Ads sin gastar).
- Meta Ad Library, Google Ads Transparency Center, TikTok Creative Center y TikTok Ad Library, LinkedIn Ad Library.
- Similarweb (vista gratuita), Ahrefs (herramientas gratuitas), AnswerThePublic, AlsoAsked, SparkToro, Social Blade, BuiltWith, Wappalyzer.
- Wayback Machine.

## 6. Si la red está restringida

En algunos entornos (por ejemplo, sesiones en la nube con lista blanca de dominios), los scripts pueden fallar con `403` o con errores de DNS. En ese caso:
1. Dile al usuario **qué dominio** se bloqueó y que puede permitirlo en la configuración de red de su entorno.
2. Sigue con WebSearch y WebFetch, que suelen tener otra ruta de salida.
3. Anota en `PROGRESO.md` qué no se pudo consultar. **Nunca rellenes el hueco con datos inventados.**
