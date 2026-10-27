# 12 · Informes para humanos y para IAs

El mismo estudio se entrega en tres capas:
1. **Humanos con prisa**: `README.md` e `informe.html`.
2. **Humanos que quieren el detalle**: `informe.md` de cada carpeta.
3. **IAs**: `datos.json` de cada carpeta, `ia/contexto-ia.md`, `ia/estudio.json` y `fuentes/fuentes.json`.

## Capa 1 · README.md (resumen ejecutivo, una o dos pantallas)

Plantilla: `plantillas/README-estudio.md`. Orden obligatorio:
1. **Veredicto** con semáforo, puntuación y confianza, en una frase que se entienda sin leer nada más.
2. La idea en una línea y la decisión que se quería tomar.
3. **Cifras clave**: mercado (SAM/SOM), precio, margen, punto de equilibrio, inversión y necesidad de financiación, con su etiqueta.
4. **3 señales a favor** y **3 riesgos principales**, cada uno con su referencia.
5. **Lo que todavía es hipótesis.**
6. **Próximos pasos**: los 3 primeros experimentos (coste, plazo, umbral).
7. Índice de carpetas con enlaces relativos.

Estilo para humanos:
- Español claro, frases cortas y sin jerga (si usas TAM, CAC o JTBD, explícalo la primera vez).
- Tablas para comparar y viñetas para listas.
- Las cifras, con unidades y fecha: "≈ 1,2 M€/año (2024)".
- Las etiquetas de evidencia (`[DATO F3]`), visibles pero discretas.
- Cada informe termina con **"Qué significa para tu decisión"** y **"Qué falta por saber"**.

## Capa 2 · informe.md de cada módulo

Plantilla: `plantillas/informe-modulo.md`:
- Cabecera (módulo, fecha, modo, confianza global).
- Resumen en 5 líneas.
- Desarrollo.
- Banderas rojas y amarillas.
- Qué significa para la decisión.
- Qué falta por saber.
- Fuentes usadas (IDs).

## Capa 3 · Para IAs

### datos.json de cada módulo
Esquema común en `plantillas/esquema-datos.md`. Son datos estructurados, sin prosa innecesaria, con IDs estables (`M1` mercado, `C1` cliente, `K1` palabras clave, `X1` competencia, `E1` estrategia, `V1` viabilidad, `G1` go-to-market, `P1` producto, `L1` legal, `R1` veredicto) para que otra IA pueda citar y actualizar hallazgos concretos.

### fuentes/fuentes.json
```json
[{"id": "F1", "titulo": "", "url": "", "editor": "", "fecha_publicacion": "AAAA-MM-DD|AAAA|desconocida",
  "fecha_consulta": "AAAA-MM-DD", "nivel": "T1|T2|T3", "ambito": "España|UE|global|ciudad", "notas": ""}]
```

### ia/contexto-ia.md: traspaso compacto
Pensado para pegarlo en otra conversación o para que lo lean otras skills (copywriting, anuncios, plan de empresa, pitch). Máximo de unas 2.000 palabras, denso y sin adornos. Plantilla `plantillas/contexto-ia.md`, con estas secciones:
- **IDENTIDAD**: idea, arquetipo, ámbito, modelo, fase.
- **DECISIÓN**: veredicto, puntuación por dimensión, confianza.
- **CLIENTE**: segmento principal, JTBD, dolores con su frecuencia, lenguaje literal, objeciones.
- **MERCADO**: TAM/SAM/SOM con su método, tendencia, estacionalidad.
- **COMPETENCIA**: tabla compacta, precios, hueco.
- **POSICIONAMIENTO Y MENSAJE**: frase de valor, diferencias, pruebas.
- **NÚMEROS**: supuestos y resultados clave del modelo, variables críticas.
- **CANALES**: priorizados, CAC asumible.
- **RESTRICCIONES**: legales, operativas, de recursos.
- **HIPÓTESIS PENDIENTES** y experimentos.
- **REGLAS PARA LA IA QUE LEA ESTO**: "No presentes como dato lo que aquí es HIPÓTESIS; respeta las etiquetas; las fuentes están en fuentes.json".

### ia/estudio.json
Lo genera `scripts/generar_informe.py` uniendo todos los `datos.json` y `fuentes.json`. No lo escribas a mano.

## informe.html (panel visual)

```bash
python3 <skill>/scripts/generar_informe.py estudios/<idea>
```
Crea un HTML autocontenido (sin dependencias externas, con modo claro y oscuro, que se ve en el móvil) con:
- El veredicto y la barra de puntuación por dimensión.
- Las cifras clave.
- El DAFO en cuadrícula.
- Tablas de competidores, keywords y canales.
- Las personas.
- Los riesgos y experimentos.
- Las fuentes enlazadas.

Si el HTML sale vacío en alguna sección, es que falta esa clave en el `datos.json` correspondiente.

## Exportar (solo con permiso)

- **Google Drive**: si el conector está disponible, ofrece subir `README.md` (o un documento con su contenido) y el `informe.html` a una carpeta "Estudios de negocio".
- **Claude Docs, Notion u otros**: igual. Pregunta antes de crear nada fuera del equipo del usuario.
- **PDF o Word**: si el usuario lo pide, convierte el README y los informes con las skills de documentos disponibles.

## Lista de comprobación final

- [ ] Cada cifra que decide algo tiene etiqueta y fuente (o cálculo visible).
- [ ] No hay citas de clientes, precios ni datos inventados.
- [ ] Se han considerado los competidores indirectos, los sustitutos y la opción de no hacer nada.
- [ ] Están separados el SAM y el SOM, la facturación y el beneficio, y el beneficio y la caja.
- [ ] El veredicto incluye el mejor argumento en contra y qué lo cambiaría.
- [ ] Cada experimento tiene una métrica, un umbral de éxito, un umbral de parada y un presupuesto.
- [ ] `PROGRESO.md` está actualizado.
- [ ] Se ha ejecutado `generar_informe.py` y el HTML abre bien.
