# 10 · Requisitos legales y trámites

**Preguntas que responde:** ¿Hay algo que impida o encarezca mucho el negocio? ¿Qué licencias, registros y obligaciones tiene? ¿Puedo usar el nombre que quiero? ¿Qué forma jurídica conviene para empezar?

> Esto es una **orientación basada en fuentes públicas**, no asesoramiento legal ni fiscal. Cita siempre la fuente oficial (BOE, ayuntamiento, organismo) con su fecha y recomienda confirmarlo con un gestor, un abogado o el ayuntamiento. Las cuotas, los umbrales y los plazos cambian: compruébalos en la fuente oficial vigente.

## 1. Bloqueadores (lo primero)

Busca si la actividad:
- Está **prohibida o con moratoria** en la zona (algunas ciudades limitan licencias de hostelería, ocio nocturno, pisos turísticos o ciertas aperturas en zonas saturadas).
- Exige **titulación o habilitación** (sanidad, educación reglada, seguridad, instalaciones, transporte, finanzas, seguros, inmobiliaria en algunas comunidades).
- Requiere **autorización previa** de un organismo (sanitaria, financiera (Banco de España o CNMV), juego, alcohol o tabaco, residuos, actividades clasificadas).
- Tiene un **régimen de responsabilidad** que haga el seguro obligatorio o muy caro.

Consultas: `requisitos abrir [actividad] [ciudad]`, `licencia [actividad] [comunidad autónoma] normativa`, `[actividad] autorización sanitaria requisitos`, `[actividad] prohibición moratoria [ciudad] [año]`.

## 2. Forma jurídica (España)

Compara **autónomo (persona física)** y **sociedad limitada (SL)** según:
- **Responsabilidad**: personal ilimitada frente a limitada al capital, con matices.
- **Fiscalidad**: IRPF progresivo frente al Impuesto de Sociedades. Indica el punto aproximado en que suele compensar la SL y pide confirmarlo con el gestor.
- **Costes y trámites** de alta y de mantenimiento (gestoría, cuentas anuales).
- **Socios**: con socios, la SL es casi siempre la opción adecuada. Recomienda un pacto de socios.
- **Imagen** ante clientes y bancos.

Recursos oficiales: el Punto de Atención al Emprendedor (PAE) y el sistema CIRCE permiten crear empresas en línea, y el Portal PYME del Ministerio de Industria tiene guías de formas jurídicas y trámites.

## 3. Trámites típicos (España; verifica en la fuente oficial vigente)

- **Hacienda**: declaración censal (modelo 036), epígrafe del IAE, régimen de IVA (general, recargo de equivalencia en comercio minorista, módulos en ciertos casos).
- **Seguridad Social**: alta en el RETA (autónomos) o régimen general. Las cuotas de autónomo dependen del rendimiento neto; hay bonificaciones para nuevas altas: comprueba las vigentes.
- **Ayuntamiento**: licencia de apertura o actividad, o declaración responsable o comunicación previa según la actividad y el municipio. Licencia de obras si hay reforma. Revisa las ordenanzas y el uso urbanístico del local **antes de firmar el alquiler**.
- **Trabajadores**: alta como empresa en la Seguridad Social, contratos, convenio colectivo del sector, prevención de riesgos laborales y registro de jornada.
- **Sectoriales**:
  - Alimentación: registro sanitario (RGSEAA) o autorización autonómica, formación de manipuladores, APPCC, alérgenos.
  - Cosmética: notificación CPNP y persona responsable.
  - Juguetes y electrónica: marcado CE y RAEE.
  - Envases: responsabilidad ampliada del productor y registro de productores. El textil y otras categorías también pueden tener obligaciones.
  - Transporte, turismo (registro autonómico), educación, sanidad (autorización de centro sanitario).

## 4. Venta online y datos

- **LSSI**: aviso legal e identificación del titular.
- **RGPD y LOPDGDD**: política de privacidad, base legal de los tratamientos, registro de actividades, contratos con encargados (hosting, email marketing), cookies (banner conforme a la guía de la AEPD).
- **Consumidores**: condiciones generales, información precontractual, **derecho de desistimiento de 14 días** en venta a distancia (con excepciones), garantías, hoja de reclamaciones (en local físico) y accesibilidad cuando corresponda.
- **Comunicaciones comerciales**: consentimiento para el email y el SMS comercial (LSSI, art. 21).
- **Plataformas**: si se intermedia entre terceros, revisa las obligaciones de los marketplaces (Ley de Servicios Digitales de la UE en la escala que corresponda; obligaciones de información a Hacienda sobre vendedores).

## 5. Nombre, marca y propiedad intelectual

Comprueba la **disponibilidad del nombre antes de enamorarte de él**:
- **Marca**: localizador de la OEPM (España), TMview (EUIPO, marcas de la UE y nacionales) y WIPO Global Brand Database. Busca idéntica y parecida en las mismas clases de Niza.
- **Denominación social**: Registro Mercantil Central (certificación negativa).
- **Dominio** (.es y .com) y nombres de usuario en las redes principales.
- **Patentes o diseños** si el producto es innovador: Google Patents, Espacenet, OEPM. Comprueba también que no infringes los de otros.

Recomienda registrar la marca en las clases relevantes si la investigación sigue adelante.

## 6. Seguros e impuestos

- Seguros: responsabilidad civil (obligatoria en algunas actividades), del local y del contenido, profesional, de producto.
- Impuestos y calendario: IVA trimestral, retenciones e IRPF o Impuesto de Sociedades, y modelos informativos. **Explica el efecto en la caja**: el IVA cobrado no es tuyo.

## Otros países

Busca los equivalentes: SAT (México), DIAN y Cámara de Comercio (Colombia), ARCA/AFIP (Argentina), SII (Chile), SUNAT (Perú), Receita Federal (Brasil), además de los portales de "abre tu empresa" de cada país y la normativa municipal correspondiente.

## Salidas

- `09-legal/informe.md`: bloqueadores (sí o no), forma jurídica recomendada y por qué, lista de trámites con organismo, coste orientativo, plazo y fuente, obligaciones online y de datos, disponibilidad del nombre, seguros, calendario fiscal básico y preguntas para el gestor o abogado.
- `09-legal/datos.json` → `metricas`:
```json
{
  "bloqueo_legal": false,
  "nivel_complejidad": "baja|media|alta",
  "forma_juridica_recomendada": "",
  "tramites": [{"tramite": "", "organismo": "", "coste_orientativo": "", "plazo": "", "critico": true, "fuentes": []}],
  "marca_disponible": "si|no|dudosa|sin_comprobar",
  "preguntas_asesor": []
}
```
