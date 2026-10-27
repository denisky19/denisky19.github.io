# 09 · Producto, operaciones y distribución

**Preguntas que responde:** ¿Cuál es la versión mínima que permite vender y aprender? ¿De dónde salen el producto o el servicio y cuánto cuesta producirlos? ¿Cómo llega al cliente y qué margen se queda cada intermediario? ¿Qué se rompe al crecer?

## 1. Producto mínimo (MVP)

Elige el MVP **más barato que pruebe la hipótesis más arriesgada** (del módulo 07 o el 11):

| Tipo de MVP | Qué prueba | Ideal para |
|---|---|---|
| Landing + anuncios (*smoke test*, puerta falsa) | Interés y conversión a registro o preventa | Cualquiera con demanda online |
| Preventa o reserva con pago | Disposición real a pagar | Producto físico, cursos, eventos |
| Concierge (hacerlo a mano para pocos clientes) | Valor de la solución sin construirla | Servicios, SaaS, marketplaces |
| Mago de Oz (parece automático pero se hace a mano) | Experiencia y demanda | Apps, plataformas |
| Pop-up, mercadillo o feria | Demanda presencial, precio, producto | Alimentación, moda, retail, local |
| Carta de intenciones o piloto pagado | Compromiso B2B | B2B |
| Crowdfunding | Demanda y financiación a la vez | Producto físico con historia |
| Versión mínima en una plataforma existente (Etsy, Amazon, Shopify, Wallapop, Instagram) | Venta real con poca inversión | Ecommerce, artesanía |

**Prioriza funciones** con MoSCoW (imprescindible, importante, deseable, ahora no) o RICE (alcance × impacto × confianza / esfuerzo). Basa cada "imprescindible" en un dolor del módulo 03.

**Señales de encaje producto-mercado** que medir después:
- Test de Sean Ellis: el 40 % o más diría que se sentiría "muy decepcionado" sin el producto.
- Curva de retención que se aplana.
- Recomendaciones espontáneas.
- Ventas que crecen sin subir el gasto en captación.

## 2. Fabricación, aprovisionamiento y operaciones

- **Proveedores**: cómo encontrarlos (Alibaba o 1688 para importación, Europages, Kompass, directorios sectoriales, ferias, asociaciones, mayoristas como Makro) y qué preguntar (pedido mínimo, plazo, precio por volumen, certificaciones, muestras, condiciones de pago). Busca 3 alternativas para no depender de uno.
- **Requisitos del producto**: marcado CE, seguridad de juguetes, registro sanitario, etiquetado, cosmética (CPNP), electrónica (RAEE) y envases (responsabilidad ampliada del productor). Detalle en el módulo 10.
- **Capacidad**: el cuello de botella real (horas del fundador, horno, sillas, aforo, producción) y qué pasa con 10, 100 o 1.000 pedidos al mes.
- **Inventario y circulante**: stock inicial, rotación y días de pago a proveedores frente a días de cobro.
- **Calidad y servicio**: devoluciones, garantías, atención al cliente.
- **Herramientas**: TPV, ecommerce, facturación (normativa de facturación electrónica y sistemas de facturación verificables: comprueba plazos vigentes), CRM y reservas.

## 3. Distribución: cómo llega al cliente

| Canal | Ventajas | Inconvenientes | Margen que se queda el canal (orientativo; verifícalo en el sector) |
|---|---|---|---|
| Venta directa (tienda propia, web, local) | Margen completo, relación con el cliente | Hay que generar todo el tráfico | 0 % (pero tú pagas la captación) |
| Marketplaces (Amazon, Miravia, El Corte Inglés, Etsy, Zalando…) | Tráfico inmediato | Comisiones, dependencia, guerra de precios | Comisión por venta y servicios (consulta las tarifas actuales) |
| Minoristas o tiendas | Visibilidad, volumen | Margen bajo, cobro a plazo, negociación | El minorista suele multiplicar el precio de compra |
| Distribuidor o mayorista | Llega a muchos puntos | Margen intermedio, menos control | Se acumula sobre el del minorista |
| Horeca o canal profesional | Volumen recurrente | Exige servicio y precio | Variable |
| Apps de reparto o reserva | Demanda local | Comisiones altas | Comisión por pedido |
| Franquicia o licencia | Expansión con capital ajeno | Control de marca, obligaciones legales | Canon y royalties |
| Exportación | Mercados mayores | Logística, aduanas, normativa | ICEX ofrece guías y apoyo |

**Cadena de precios**: haz la cuenta desde el PVP hacia atrás (PVP con IVA, menos IVA, menos margen del minorista, menos margen del distribuidor, menos logística = lo que recibes) y compárala con tu coste. Muchos productos son viables en venta directa y **no** a través de distribución.

**Logística**: compara tarifas de mensajería (agregadores como Packlink para tener una referencia), envíos gratis o de pago, devoluciones (muy altas en moda), embalaje, almacén propio o externalizado (logística 3PL o el almacenaje de Amazon) y entregas en el día para negocios locales.

## Recetas de búsqueda

```
fabricante [producto] España / Portugal / Europa
proveedor mayorista [producto]
[producto] MOQ precio fábrica
margen distribuidor [sector] porcentaje
cómo vender en [marketplace] comisiones [año]
tarifas envío paquete [peso] España comparativa
requisitos vender [producto] en España normativa etiquetado
```

## Salidas

- `08-producto-distribucion/informe.md`: MVP recomendado y por qué, funciones priorizadas, proveedores y alternativas, requisitos del producto, capacidad y cuellos de botella, canales de distribución comparados, cadena de márgenes, logística y riesgos operativos.
- `08-producto-distribucion/datos.json` → `metricas`:
```json
{
  "mvp": {"tipo": "", "descripcion": "", "hipotesis_que_prueba": "", "coste": 0, "plazo": ""},
  "funciones_imprescindibles": [],
  "proveedores": [{"nombre": "", "url": "", "producto": "", "moq": "", "precio": "", "fuentes": []}],
  "canales_distribucion": [{"canal": "", "margen_canal_pct": null, "recomendado": true, "motivo": ""}],
  "cuellos_botella": []
}
```
