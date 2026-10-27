# Esquema de `datos.json` (capa para IAs)

Cada carpeta de módulo tiene un `datos.json` con esta estructura común. `metricas` cambia según el módulo: las claves están en el apartado **Salidas** de cada `modulos/NN-*.md`. Escribe JSON válido (UTF-8, sin comentarios). Usa `null` si no se sabe y explica por qué en `pendiente`.

```json
{
  "modulo": "mercado",
  "version_esquema": 1,
  "fecha": "AAAA-MM-DD",
  "modo": "express|estandar|profundo",
  "confianza": "alta|media|baja",
  "resumen": "Máximo 5 frases con la conclusión del módulo.",
  "hallazgos": [
    {"id": "M1", "texto": "El gasto medio por hogar en … es de … €/año (2024)", "etiqueta": "DATO",
     "confianza": "alta", "fuentes": ["F3"]}
  ],
  "metricas": {},
  "banderas_rojas": ["…"],
  "banderas_amarillas": ["…"],
  "pendiente": [{"pregunta": "…", "como_averiguarlo": "…"}],
  "implicacion_decision": "Qué significa esto para lanzar o no."
}
```

## Valores permitidos
- `etiqueta`: `DATO` · `ESTIMACION` · `CALCULO` · `HIPOTESIS` · `FUNDADOR` · `DESCONOCIDO`
- `confianza`: `alta` (≥ 2 fuentes T1/T2 coherentes o un cálculo con entradas sólidas) · `media` · `baja` (1 fuente T3 o una suposición)

## Prefijos de ID por módulo
| Carpeta | `modulo` | Prefijo |
|---|---|---|
| 00-brief | `brief` | B |
| 01-mercado | `mercado` | M |
| 02-cliente | `cliente` | C |
| 03-palabras-clave | `palabras_clave` | K |
| 04-competencia | `competencia` | X |
| 05-estrategia | `estrategia` | E |
| 06-viabilidad | `viabilidad` | V |
| 07-marketing-ventas | `marketing_ventas` | G |
| 08-producto-distribucion | `producto_distribucion` | P |
| 09-legal | `legal` | L |
| 10-veredicto | `veredicto` | R |

## `00-brief/datos.json` → `metricas`
```json
{"idea": "", "arquetipo": "", "ambito": "", "cliente_tipo": "B2C|B2B|B2B2C|B2G", "modelo_ingresos": "",
 "fase": "", "decision": "", "inversion_disponible": "", "ambicion": "", "hipotesis_criticas": []}
```

## `fuentes/fuentes.json`
```json
[{"id": "F1", "titulo": "", "url": "", "editor": "", "fecha_publicacion": "AAAA-MM-DD|AAAA|desconocida",
  "fecha_consulta": "AAAA-MM-DD", "nivel": "T1|T2|T3", "ambito": "", "notas": ""}]
```

## `ia/estudio.json`
Lo genera `scripts/generar_informe.py`: `{"idea", "generado", "modulos": {"mercado": {...}, ...}, "fuentes": [...]}`.
