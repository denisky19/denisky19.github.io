# Fuentes y recetas para encontrar cuentas

Cada fuente cubre una parte del universo. Combínalas y anota de cuál viene cada cuenta.

| Fuente | Qué da | Acceso |
|---|---|---|
| **OpenStreetMap** (`scripts/buscar_locales_osm.py`) | Locales etiquetados (`amenity=nightclub`, `bar`, `events_venue`, `restaurant`; `tourism=hotel`…) con web, teléfono e Instagram si constan | Script, sin clave (Nominatim + Overpass) |
| **Búsqueda web** | Listados, prensa, rankings, webs propias | WebSearch |
| **Resident Advisor** (ra.co) | Clubs por ciudad, eventos, promotoras; **quién programa house o techno** | Web o navegador |
| **Agendas de ticketing**: Fourvenues, Xceed, Dice, Shotgun, Fever, Wegow, Entradium | Venues y promotoras activos y su frecuencia | Web o navegador |
| **Google Maps** | Universo más completo de locales, reseñas, horario, teléfono | Navegador (Playwright MCP) o Apify |
| **Instagram** | Bios con email de booking, agenda, DJs y promotoras | Manual o navegador |
| **Bodas.net, Zankyou, Bodas de Cuento, guías de bodas** | Fincas, masías, hoteles y planners por provincia, con número de reseñas | Web o navegador |
| **Datos abiertos municipales** (por ejemplo, el censo de actividades en planta baja de Barcelona, licencias de actividades) | Locales con licencia de ocio nocturno | Portales de datos abiertos |
| **Asociaciones**: patronal de ocio nocturno y restauración musical, gremios de hostelería, asociaciones de wedding planners, federaciones de fincas de bodas | Listados de socios | Web |
| **Ferias**: ferias de bodas, ferias del sector de la hostelería | Expositores (fincas, planners, proveedores) | Web |
| **LinkedIn** | Cargos (events manager, F&B director, booker) | Manual |
| **Aviso legal de la web** | Razón social, CIF, email de contacto | `scripts/extraer_contactos.py` |

## Recetas de búsqueda (sustituye [zona])

**Clubs y salas**
```
discoteca [ciudad] · club techno [ciudad] · club house [ciudad] · sala música electrónica [comarca]
site:ra.co clubs [ciudad] · "[ciudad]" club resident advisor
mejores discotecas [ciudad] [año] · ocio nocturno [comarca] guía
```

**Beach clubs, rooftops, coctelerías**
```
beach club [costa/municipio] · chiringuito dj [municipio] · rooftop [ciudad] dj sunset
terraza hotel [ciudad] dj · cocktail bar [ciudad] dj · bar musical [ciudad] house
tardeo [ciudad] house · "sunset session" [municipio]
```

**Bodas**
```
finca para bodas [comarca] · masía bodas [provincia] · castillo bodas [provincia]
hotel bodas [costa] · "wedding venue" Costa Brava · wedding planner [provincia]
"proveedores recomendados" finca [nombre] · bodas.net fincas [provincia]
destination wedding planner Barcelona/Costa Brava
```

**Programación real (quién contrata DJs)**
```
"[nombre del venue]" fourvenues · "[nombre del venue]" xceed · "[nombre del venue]" resident advisor
"[nombre del venue]" programación · "[nombre del venue]" booking email
```

**Decisor y contacto**
```
"[venue]" booking · "[venue]" "eventos@" · "[venue]" aviso legal · "[venue]" director de eventos linkedin
```

Para Cataluña, busca también en **catalán**: `discoteca`, `sala de concerts`, `masia per a casaments`, `casaments [comarca]`, `festa major [municipi] programació`.
