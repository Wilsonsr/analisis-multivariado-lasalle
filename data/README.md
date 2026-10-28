# Datos del curso

Los tres archivos son **datos simulados con fines didácticos**. Reproducen relaciones plausibles entre variables, pero no corresponden a mediciones oficiales, encuestas reales ni clientes reales, y no deben citarse como evidencia empírica.

Todos están codificados en UTF-8, con coma como separador y punto decimal.

## `datos_guia1_calidad_aire.csv` (Unidad 1)

30 estaciones de monitoreo × 10 columnas.

| Variable | Descripción | Unidad | Tipo |
|---|---|---|---|
| estacion | Código de la estación (E01 a E30) | — | Identificador |
| zona | Industrial, Residencial o Periurbana | — | Cualitativa nominal |
| PM25 | Material particulado fino (PM2,5) | µg/m³ | Cuantitativa continua |
| PM10 | Material particulado respirable | µg/m³ | Cuantitativa continua |
| NO2 | Dióxido de nitrógeno | µg/m³ | Cuantitativa continua |
| CO | Monóxido de carbono | mg/m³ | Cuantitativa continua |
| O3 | Ozono troposférico | µg/m³ | Cuantitativa continua |
| Temp | Temperatura media | °C | Cuantitativa continua |
| Humedad | Humedad relativa media | % | Cuantitativa continua |
| Viento | Velocidad media del viento | m/s | Cuantitativa continua |

## `datos_guia2_encuesta_salud.csv` (Unidad 2)

600 personas encuestadas × 15 columnas.

| Variable | Categorías o escala | Tipo |
|---|---|---|
| id | 1 a 600 | Identificador |
| zona | Urbana, Rural | Cualitativa nominal |
| nivel_educativo | Primaria, Secundaria, Técnica, Universitaria | Cualitativa ordinal |
| regimen | Contributivo, Subsidiado, Especial, No afiliado | Cualitativa nominal |
| consulta_preventiva | Sí, No (en el último año) | Cualitativa nominal |
| percepcion_calidad | Buena, Regular, Mala | Cualitativa ordinal |
| inst_limpieza, inst_comodidad, inst_equipos | Acuerdo de 1 a 5 | Ítems de escala (infraestructura) |
| trato_amabilidad, trato_escucha, trato_explicacion | Acuerdo de 1 a 5 | Ítems de escala (trato humano) |
| opor_cita, opor_espera, opor_tramites | Acuerdo de 1 a 5 | Ítems de escala (oportunidad) |

## `datos_guia3_clientes.csv` (Unidad 3)

120 clientes de una tienda en línea × 8 columnas.

| Variable | Descripción | Unidad |
|---|---|---|
| cliente | Identificador (C001 a C120) | — |
| recencia_dias | Días desde la última compra | días |
| frecuencia_anual | Compras en el año | compras |
| ticket_promedio | Valor promedio por compra | miles de pesos |
| antiguedad_meses | Tiempo como cliente | meses |
| visitas_mes | Visitas promedio por mes a la tienda en línea | visitas |
| devoluciones_pct | Porcentaje de compras devueltas | % |
| estado_6m | Activo, Inactivo o Retirado, observado seis meses después | — |

`estado_6m` se registró después del periodo de medición del comportamiento y no se construyó a partir de una segmentación; por eso puede usarse como variable de clase en el análisis discriminante.
