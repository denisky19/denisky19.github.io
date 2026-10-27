# 02 · Mercado: tamaño, tendencias y momento

**Preguntas que responde:** ¿Cuánto dinero se mueve en esto? ¿Crece o decrece? ¿Qué parte puedo conseguir yo de forma realista? ¿Por qué es (o no) buen momento?

## 1. Define el mercado antes de medirlo

Escribe en una línea **qué se compra, quién lo compra y dónde**. "Café de especialidad para llevar consumido por oficinistas en el centro de Valencia" se puede medir; "el mercado del café" no sirve para decidir nada.

## 2. TAM, SAM y SOM

| Nivel | Significado | Ejemplo (local) |
|---|---|---|
| **TAM** (mercado total) | Gasto total en la categoría en el país o región | Gasto en cafeterías en España |
| **SAM** (mercado alcanzable) | Parte a la que llega tu modelo (zona, segmento, canal) | Gasto en café para llevar en el área de influencia del local |
| **SOM** (mercado obtenible) | Lo que puedes captar en 1–3 años con tus recursos | Ventas realistas del local según capacidad y competidores |

**Haz siempre dos cálculos y compáralos:**

**a) De arriba abajo (top-down).** Parte de cifras publicadas (informes sectoriales, asociaciones, estadísticas oficiales) y filtra por segmento y geografía.
- España: la *Encuesta de Presupuestos Familiares* (INE) da el gasto medio por hogar y por grupo de consumo (COICOP); multiplícalo por el número de hogares del ámbito. El DIRCE (INE) da el número de empresas por actividad (CNAE) y provincia, lo que sirve para mercados B2B. Ver `referencias/fuentes-datos.md`.
- Desconfía de los "informes de mercado" con cifras globales enormes y CAGR redondos de webs que venden informes: son T3 salvo que expliquen su método.

**b) De abajo arriba (bottom-up)**, que es el preferido:
```
Clientes potenciales en el ámbito × % que realmente compra la categoría × frecuencia anual × ticket medio
```
- Clientes potenciales: población o empresas filtradas (padrón por municipio o sección censal, DIRCE por CNAE, censos sectoriales, colegios profesionales).
- % que compra, frecuencia y ticket: encuestas sectoriales, datos de competidores, reseñas, búsquedas y tu propia investigación.

**c) Para negocios locales**, haz además el cálculo por **capacidad**: máximo de clientes/día × ticket × días de apertura. El SOM nunca puede superar la capacidad real.

Muestra las fórmulas con los números sustituidos. Si top-down y bottom-up difieren más de 3 veces, explica por qué y quédate con el más conservador **para decidir**.

## 3. Tendencias y momento ("¿por qué ahora?")

Busca evidencias de dirección, no adjetivos:

- **Interés de búsqueda**: Google Trends a 5 años en el país (web o conector). Wikipedia pageviews como indicador adicional (`scripts/datos_publicos.py wikipedia`).
- **Atención mediática**: volumen de noticias (`scripts/datos_publicos.py gdelt`, que permite filtrar por país e idioma).
- **Dinero**: rondas de inversión en el sector, aperturas y cierres de empresas, fusiones.
- **Datos oficiales**: series de INE/Eurostat (consumo, número de empresas del CNAE, comercio electrónico por sector según la CNMC).
- **Cambios regulatorios y tecnológicos** que abren o cierran el mercado.

**Fase del mercado**: introducción, crecimiento, madurez o declive. Justifícala con datos.

## 4. PESTEL rápido

Solo los factores que **cambian la decisión**, con su fuente: Político, Económico (renta, inflación, tipos de interés, consumo), Social (demografía, hábitos), Tecnológico, Ecológico (normativa ambiental, envases, residuos) y Legal (normativa sectorial). Cada factor se marca como Oportunidad u Amenaza y pasa al DAFO (módulo 06).

## Recetas de búsqueda

```
[sector] mercado España [año] facturación
[sector] informe sectorial [año] pdf
[sector] asociación española estadísticas
gasto medio hogar [categoría] INE
número de empresas [actividad] [provincia] DIRCE
[sector] tendencias [año] consumidor
[sector] market size Europe [year]
[category] market report CAGR methodology
[sector] crecimiento ventas [año] site:.es
[sector] inversión ronda startup [año]
```

Cambia "España" y las fuentes por las del país del usuario (INEGI, DANE, INDEC, INE Chile, IBGE, etc.; ver `referencias/fuentes-datos.md`).

## Salidas

`01-mercado/informe.md` con estas secciones:
1. Definición del mercado.
2. TAM/SAM/SOM con las dos vías y sus fórmulas.
3. Tendencias y fase del mercado.
4. PESTEL.
5. "¿Por qué ahora?"
6. Riesgos.
7. Lo que no se sabe y cómo averiguarlo.

`01-mercado/datos.json` con estas claves en `metricas`:
```json
{
  "tam": {"valor": 0, "unidad": "EUR/año", "ambito": "", "metodo": "", "fuentes": []},
  "sam": {"valor": 0, "unidad": "EUR/año", "metodo": "", "fuentes": []},
  "som": {"valor": 0, "unidad": "EUR/año", "horizonte": "año 3", "metodo": "", "fuentes": []},
  "crecimiento_anual_pct": null,
  "fase_mercado": "introduccion|crecimiento|madurez|declive",
  "tendencia_busquedas": "sube|estable|baja|desconocida",
  "pestel": [{"factor": "E", "descripcion": "", "efecto": "oportunidad|amenaza", "fuentes": []}]
}
```

## Errores típicos

- Confundir el tamaño del sector entero con lo que tú puedes vender.
- Usar cifras globales para un negocio de barrio.
- Inventarse "si consigo el 1 % del mercado…" sin explicar cómo.
- Tomar como dato una cifra de una web que vende informes sin método publicado.
