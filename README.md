# denisky19.github.io
Root GitHub Pages site and Android app association files.

## Skills para Claude

### `estudio-negocio`: validar y lanzar negocios

Plugin con cuatro skills:
- `validar-negocio`: ¿funciona la idea?
- `oferta-y-web`: packs, precios y web.
- `prospeccion-clientes`: venues y cuentas B2B con contactos y CRM.
- `campanas-marketing`: diseño y ejecución de campañas.

Con `validar-negocio`, antes de investigar, Claude te hace unas preguntas. Después investiga en Internet con fuentes y conectores gratuitos y entrega un estudio por carpetas:
- Mercado y cliente.
- Palabras clave y competencia.
- DAFO/CAME.
- Viabilidad económica.
- Marketing y ventas, producto y distribución.
- Legal.
- Veredicto con experimentos.

Los informes vienen en dos formatos: para personas (Markdown + HTML) y para IAs (JSON + contexto).

Instalación en Claude Code:

```
/plugin marketplace add denisky19/denisky19.github.io
/plugin install estudio-negocio@denisky-skills
```

En claude.ai, sube los zips de `dist/` en *Ajustes → Capacidades → Skills*.

Más detalles: [plugins/estudio-negocio](plugins/estudio-negocio/README.md) · Investigación de skills existentes: [docs/investigacion-skills-negocio.md](docs/investigacion-skills-negocio.md)
