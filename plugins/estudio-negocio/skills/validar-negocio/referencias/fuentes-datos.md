# Catálogo de fuentes gratuitas por área

Leyenda de acceso:
- 🔎 por búsqueda web.
- 📄 leyendo la página con WebFetch.
- 🐍 con un script de `scripts/`.
- 🔌 con un conector o MCP.
- 🖐️ manual o con navegador (el usuario o un MCP de navegador).

Leyenda de nivel: T1 oficial o primaria · T2 secundaria fiable · T3 opinión.

Las URLs y condiciones cambian: si una falla, búscala por su nombre.

---

## 1. Estadística oficial y datos de mercado

### España
| Fuente | Qué aporta | Acceso | Nivel |
|---|---|---|---|
| **INE**: ine.es | Población, hogares, empresas, consumo, precios, turismo | 📄 🐍 (`datos_publicos.py ine-tabla`) | T1 |
| INE: **Encuesta de Presupuestos Familiares (EPF)** | Gasto medio por hogar y persona por grupo de consumo; base del cálculo top-down B2C | 📄 🐍 | T1 |
| INE: **Padrón continuo** y cifras de población por municipio | Población por municipio, edad y sexo; secciones censales | 📄 🐍 | T1 |
| INE: **Atlas de Distribución de Renta de los Hogares** | Renta media por municipio, distrito y **sección censal**; clave para negocios locales | 📄 | T1 |
| INE: **DIRCE** | Nº de empresas por actividad (CNAE), tamaño y provincia; base del cálculo B2B | 📄 🐍 | T1 |
| INE: Encuesta TIC en hogares | Uso de Internet y compra online por perfil | 📄 | T1 |
| INE: Comercio minorista, turismo (FRONTUR, EGATUR, ocupación hotelera) | Coyuntura sectorial | 📄 🐍 | T1 |
| **datos.gob.es** y portales de datos abiertos autonómicos o municipales | Datos locales: licencias, censos de locales, aforos, movilidad | 📄 🔎 | T1 |
| **CNMC** (data.cnmc.es) | Comercio electrónico trimestral por sector de actividad | 📄 | T1 |
| **Banco de España**: Central de Balances, *Ratios sectoriales* | Márgenes, rentabilidad y estructura financiera por CNAE; benchmark para viabilidad | 📄 🖐️ | T1 |
| ONTSI | Estudios de comercio electrónico y digitalización | 📄 | T1–T2 |
| CIS | Barómetros de opinión y hábitos | 📄 | T1 |
| Asociaciones sectoriales (Hostelería de España, AECOC, ANGED, FIAB, Adigital, AMETIC, colegios profesionales…) | Tamaño del sector, anuarios, tendencias | 🔎 📄 | T2 |
| IAB Spain (estudios de redes sociales y ecommerce), AIMC (EGM), DataReportal (*Digital [año] Spain*) | Uso de redes y medios, perfiles digitales | 🔎 📄 | T2 |
| Mercasa: *Alimentación en España* | Consumo y distribución alimentaria por producto | 📄 | T2 |
| Observatorio Cetelem, GEM España, El Referente | Consumo, emprendimiento, ecosistema startup | 🔎 📄 | T2 |

### Europa y mundo
| Fuente | Qué aporta | Acceso | Nivel |
|---|---|---|---|
| **Eurostat** | Estadísticas comparables UE: consumo, empresas, ecommerce, demografía | 📄 🐍 (`eurostat`) | T1 |
| **Banco Mundial** (data.worldbank.org) | Indicadores macro por país | 🐍 (`worldbank`) | T1 |
| OCDE (data-explorer.oecd.org), FMI | Macro, productividad, sectores | 📄 | T1 |
| **Data Commons** (datacommons.org) | Estadísticas públicas unificadas (ONU, censos…) | 📄 🔌 (MCP de Data Commons) | T1 |
| Our World in Data | Series largas y gráficos | 📄 | T1–T2 |
| UN Comtrade | Importaciones y exportaciones por producto (HS) y país | 📄 🖐️ | T1 |
| Google Dataset Search | Buscador de conjuntos de datos | 🔎 🖐️ | — |
| Statista (parte gratuita) | Cifras sueltas; cita la fuente original que indique | 🔎 | T2 (verifica el origen) |

### Latinoamérica
| País | Estadística | Gasto de hogares | Empresas y directorios |
|---|---|---|---|
| México | INEGI | ENIGH | **DENUE** (directorio geolocalizado de negocios; tiene API con token gratuito), Censos Económicos |
| Colombia | DANE | ENPH | RUES (registro de empresas), Confecámaras |
| Argentina | INDEC | ENGHo | Registros provinciales |
| Chile | INE Chile | EPF | Registro de Empresas y Sociedades, SII (estadísticas de empresas) |
| Perú | INEI | ENAHO | SUNAT (padrón RUC) |
| Brasil | IBGE (API SIDRA) | POF | Receita Federal (datos abiertos de CNPJ) |
| Regional | CEPALSTAT, BID | — | — |

---

## 2. Demanda, búsquedas y tendencias

| Fuente | Qué aporta | Acceso |
|---|---|---|
| **Google Trends** | Interés relativo, estacionalidad, regiones, consultas en ascenso | 🖐️ 🔌 (free-seo-mcp) |
| **Google Keyword Planner** | Rangos de volumen y CPC por país (cuenta de Google Ads, sin gastar) | 🖐️ |
| **Autocompletado** de Google, YouTube, Bing, DuckDuckGo y Amazon | Keywords reales y popularidad relativa | 🐍 (`keywords_autocomplete.py`) 🔌 |
| Wikipedia pageviews | Interés por un tema en el tiempo | 🐍 (`wikipedia`) |
| GDELT | Volumen de noticias sobre un tema (últimos meses), por país o idioma | 🐍 (`gdelt`) |
| Bing Webmaster Tools | Impresiones de keywords (requiere web verificada) | 🖐️ 🔌 |
| Google Search Console | Consultas reales de tu web | 🖐️ 🔌 |
| Ubersuggest, AnswerThePublic, AlsoAsked | Volúmenes estimados y preguntas (freemium) | 🖐️ 🔌 (Ubersuggest) |
| Exploding Topics, Glimpse | Temas emergentes | 🔎 🖐️ |
| TikTok Creative Center, Pinterest Trends, YouTube | Tendencias sociales y de vídeo | 🖐️ 🔌 (vidIQ) |
| Amazon (más vendidos y novedades) | Demanda de producto por categoría | 📄 🖐️ |

---

## 3. Voz del cliente

| Fuente | Ideal para | Acceso |
|---|---|---|
| **Reddit** (r/spain, r/askspain, r/SpainFIRE, r/autonomos, temáticos; en inglés para análogos) | Dolores, alternativas, lenguaje | 🐍 (`voz_cliente.py reddit`) 🔌 🔎 |
| **Foros españoles**: Forocoches, Mediavida, Rankia, Enfemenino, foros sectoriales | Consumidor español sin filtros | 🔎 (con `site:`) 📄 |
| **Reseñas**: Google Maps, Trustpilot, Amazon.es, TripAdvisor, TheFork, Booking | Quejas y valor percibido de los competidores | 🔎 📄 🖐️ |
| **Tiendas de apps**: App Store y Google Play | Quejas de 1–3★ sobre apps competidoras | 🐍 (`voz_cliente.py appstore`) 📄 |
| **G2, Capterra, Product Hunt, Hacker News** | B2B y software | 🐍 (`hn`) 🔎 📄 |
| YouTube y TikTok (comentarios) | B2C, lenguaje | 🖐️ 🔌 |
| LinkedIn, grupos de Facebook, Discord, Telegram | B2B y comunidades | 🖐️ |
| Ofertas de empleo (InfoJobs, LinkedIn, Indeed) | Dolores B2B, herramientas usadas, crecimiento de los competidores | 🔎 📄 |
| SparkToro (consultas gratuitas limitadas) | Dónde pasa el tiempo una audiencia | 🖐️ |
| **Primaria**: entrevistas y encuestas (Google Forms, Tally) | Validar comportamiento y precio | Usuario |

---

## 4. Competencia

| Fuente | Qué aporta | Acceso |
|---|---|---|
| Webs de los competidores (inicio, precios, características, aviso legal) | Propuesta, precio, razón social | 📄 🐍 (`competidor_web.py`) |
| **Google Maps** y Páginas Amarillas | Competidores locales, reseñas, horarios | 🔎 🖐️ 🔌 (navegador o Apify) |
| **BORME** (boe.es) y LibreBOR | Constitución, capital, administradores, cambios | 🔎 📄 |
| Infoempresa, eInforma, Empresite, Axesor, Infocif (fragmentos gratuitos) | Facturación y empleados aproximados | 🔎 📄 |
| Registro Mercantil (registradores.org) | Cuentas anuales oficiales (de pago, pocos euros) | 🖐️ |
| **Meta Ad Library**, **Google Ads Transparency Center**, **TikTok Creative Center** y TikTok Ad Library, LinkedIn Ad Library | Anuncios activos y su antigüedad | 🖐️ 🔌 (navegador) |
| Similarweb (vista gratuita), Ahrefs (herramientas gratuitas), Ubersuggest | Tráfico y keywords estimados | 🖐️ 🔌 |
| BuiltWith, Wappalyzer | Tecnología de la web | 🖐️ 🐍 (detección básica) |
| **Wayback Machine** | Antigüedad e historial de la web y de los precios | 🐍 📄 |
| Crunchbase y Dealroom (parte gratuita), El Referente | Rondas e inversores | 🔎 📄 |
| Social Blade | Seguidores y crecimiento en redes | 🖐️ |
| Amazon, Etsy, Miravia, Wallapop | Precios y número de vendedores | 📄 🖐️ |

---

## 5. Costes y referencias para la viabilidad

| Fuente | Qué aporta |
|---|---|
| Idealista y Fotocasa (informes y anuncios de locales u oficinas) | Alquiler por m² y zona |
| Convenios colectivos (BOE y REGCON) e INE (Encuesta de Estructura Salarial) | Salarios del sector |
| Seguridad Social y Agencia Tributaria | Cotizaciones, cuotas de autónomo, impuestos (vigentes) |
| Banco de España (ratios sectoriales) | Márgenes y estructura de costes típicos por CNAE |
| Tarifas públicas de proveedores, mayoristas, mensajería y pasarelas de pago | Costes variables |
| Calculadoras de comisiones de los marketplaces | Coste del canal |

---

## 6. Legal, marca y trámites

| Fuente | Qué aporta |
|---|---|
| **PAE / CIRCE** (paeelectronico.es), Portal PYME (Ministerio de Industria) | Formas jurídicas, creación de empresas en línea, guías de trámites |
| **BOE** (incluida la API de datos abiertos) | Normativa estatal |
| Boletines autonómicos y ordenanzas municipales | Licencias y usos del suelo |
| **OEPM** (localizador de marcas), **TMview** (EUIPO), WIPO Global Brand Database | Disponibilidad de la marca |
| Google Patents, Espacenet, OEPM | Patentes y diseños |
| **AEPD** | Protección de datos, cookies, comunicaciones comerciales |
| Agencia Tributaria y Seguridad Social | Altas, IAE, IVA, RETA |
| AESAN y consejerías de sanidad | Requisitos alimentarios y sanitarios |
| Cámaras de Comercio (camara.es) | Ventanilla única y asesoramiento |

## 7. Financiación y ayudas (España)

| Fuente | Qué aporta |
|---|---|
| **Sistema Nacional de Publicidad de Subvenciones (infosubvenciones.es, BDNS)** | Convocatorias de ayudas de todas las Administraciones (búsqueda y exportación desde la web) |
| ENISA, CDTI, ICO, MicroBank | Préstamos participativos, I+D, líneas ICO, microcréditos |
| Agencias autonómicas de desarrollo y ayuntamientos | Ayudas al emprendimiento local |
| SEPE | Capitalización del paro (pago único) |
| Plataformas de crowdfunding, redes de business angels, aceleradoras | Capital privado |

## 8. Distribución y exportación

| Fuente | Qué aporta |
|---|---|
| ICEX | Guías país, estudios de mercado, apoyo a la exportación (algunos con registro) |
| Europages, Kompass, Alibaba | Proveedores y fabricantes |
| Packlink y webs de mensajería | Tarifas de envío de referencia |
| Ferias (IFEMA, Fira Barcelona…) y sus catálogos de expositores | Proveedores, distribuidores, competidores |
